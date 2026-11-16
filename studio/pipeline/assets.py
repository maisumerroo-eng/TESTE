"""Biblioteca de mídia do projeto: ingestão, corte em planos, painéis de mangá, contact sheets e tags.

Coloque os arquivos em:
  assets/clips/   vídeos (cenas, trailers, PVs oficiais/autorizados)
  assets/images/  ilustrações, key visuals, artes promocionais
  assets/manga/   páginas de mangá (o sistema recorta os painéis)
  assets/sources.yaml  (opcional) créditos/licença por arquivo: {arquivo: {source: ..., license: ..., credit: ...}}

Gera assets/assets.yaml. Tags podem ser editadas à mão (ou por mim, olhando os contact sheets).
Tags úteis: closeup, eyes, battle, transformation, emotional, calm, tension, impact, power, rain,
  flashback, villain, duo, crowd, dark, light, fire, lightning, blood, smile, scream, run, fall, sky.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .common import FONTS_DIR, Project, ffprobe, load_yaml, log, save_yaml

VID = {".mp4", ".mkv", ".mov", ".webm", ".avi", ".m4v"}
IMG = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def _stats(frame: np.ndarray) -> dict:
    small = cv2.resize(frame, (64, 36))
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    return dict(brightness=round(float(hsv[..., 2].mean() / 255), 3),
                saturation=round(float(hsv[..., 1].mean() / 255), 3))


def split_shots(path: Path, thresh: float = 0.42, min_len: float = 0.6, max_len: float = 8.0) -> list[dict]:
    """Detecta cortes por diferença de histograma HSV + mede movimento por plano."""
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, int(round(fps / 8)))  # analisa ~8 fps
    prev_h, prev_g = None, None
    cuts, motion, bright = [0.0], [], []
    for i in range(0, n, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, f = cap.read()
        if not ok:
            break
        small = cv2.resize(f, (160, 90))
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
        h = cv2.calcHist([hsv], [0, 1, 2], None, [8, 8, 8], [0, 180, 0, 256, 0, 256])
        h = cv2.normalize(h, h).flatten()
        g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        t = i / fps
        if prev_h is not None:
            d = cv2.compareHist(prev_h, h, cv2.HISTCMP_BHATTACHARYYA)
            if d > thresh and t - cuts[-1] >= min_len:
                cuts.append(t)
            motion.append((t, float(np.abs(g.astype(int) - prev_g.astype(int)).mean() / 255)))
        bright.append((t, float(hsv[..., 2].mean() / 255)))
        prev_h, prev_g = h, g
    dur = n / fps
    cap.release()
    cuts.append(dur)
    shots = []
    for a, b in zip(cuts[:-1], cuts[1:]):
        # planos longos são quebrados em pedaços utilizáveis
        t = a
        while b - t >= min_len:
            e = min(b, t + max_len)
            mv = [m for tt, m in motion if t <= tt < e]
            br = [v for tt, v in bright if t <= tt < e]
            mean_b = float(np.mean(br)) if br else 0.5
            if mean_b > 0.04:  # descarta trechos pretos
                shots.append(dict(start=round(t, 3), end=round(e, 3),
                                  motion=round(float(np.mean(mv)) if mv else 0.0, 4),
                                  brightness=round(mean_b, 3)))
            t = e
    return shots


def extract_panels(page: Path, out_dir: Path, min_area=0.025) -> list[Path]:
    """Recorta painéis de uma página de mangá usando as calhas brancas entre quadros."""
    img = cv2.imread(str(page))
    if img is None:
        return []
    H, W = img.shape[:2]
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, ink = cv2.threshold(g, 235, 255, cv2.THRESH_BINARY_INV)
    ink = cv2.morphologyEx(ink, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    cnts, _ = cv2.findContours(ink, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w * h >= min_area * W * H and w > 80 and h > 80:
            boxes.append((x, y, w, h))
    # ordem de leitura japonesa: cima->baixo, direita->esquerda
    boxes.sort(key=lambda b: (round(b[1] / (H * 0.08)), -b[0]))
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    if not boxes or (len(boxes) == 1 and boxes[0][2] * boxes[0][3] > 0.9 * W * H):
        return [page]  # página sem calhas: usa inteira
    for i, (x, y, w, h) in enumerate(boxes):
        p = out_dir / f"{page.stem}_p{i + 1:02d}.png"
        cv2.imwrite(str(p), img[y:y + h, x:x + w])
        paths.append(p)
    return paths


def ingest(proj: Project) -> list[dict]:
    root = proj.assets
    for sub in ("clips", "images", "manga"):
        (root / sub).mkdir(parents=True, exist_ok=True)
    yml = root / "assets.yaml"
    old = {a["id"]: a for a in (load_yaml(yml).get("assets", []) if yml.exists() else [])}
    sources = load_yaml(root / "sources.yaml") if (root / "sources.yaml").exists() else {}
    items: list[dict] = []

    def meta_for(fname: str) -> dict:
        m = sources.get(fname, {})
        return dict(source=m.get("source", "fornecido pelo usuário"), license=m.get("license", "a confirmar"),
                    credit=m.get("credit", ""))

    for f in sorted((root / "clips").iterdir()):
        if f.suffix.lower() not in VID:
            continue
        info = ffprobe(f)
        vs = next(s for s in info["streams"] if s["codec_type"] == "video")
        num, den = map(int, vs.get("r_frame_rate", "24/1").split("/"))
        for k, s in enumerate(split_shots(f)):
            aid = f"{f.stem}#{k:03d}"
            items.append(dict(id=aid, kind="clip", file=f"clips/{f.name}", start=s["start"], end=s["end"],
                              motion=s["motion"], brightness=s["brightness"],
                              fps=round(num / den, 3), w=vs["width"], h=vs["height"], **meta_for(f.name)))
    for f in sorted((root / "images").iterdir()):
        if f.suffix.lower() not in IMG:
            continue
        im = cv2.imread(str(f))
        if im is None:
            continue
        items.append(dict(id=f.stem, kind="image", file=f"images/{f.name}", w=im.shape[1], h=im.shape[0],
                          **_stats(im), **meta_for(f.name)))
    for f in sorted((root / "manga").iterdir()):
        if f.suffix.lower() not in IMG:
            continue
        for p in extract_panels(f, root / "panels"):
            im = cv2.imread(str(p))
            items.append(dict(id=p.stem, kind="panel", file=str(p.relative_to(root)), page=f.name,
                              w=im.shape[1], h=im.shape[0], **_stats(im), **meta_for(f.name)))
    # preserva tags e anotações manuais
    for it in items:
        o = old.get(it["id"], {})
        it["tags"] = o.get("tags", [])
        it["note"] = o.get("note", "")
        if "use" in o:
            it["use"] = o["use"]
    save_yaml(yml, dict(assets=items))
    log(f"biblioteca: {sum(i['kind'] == 'clip' for i in items)} planos de vídeo, "
        f"{sum(i['kind'] == 'image' for i in items)} imagens, {sum(i['kind'] == 'panel' for i in items)} painéis")
    contact_sheets(proj, items)
    return items


def _thumb(proj: Project, a: dict, w=320, h=180) -> Image.Image:
    p = proj.assets / a["file"]
    if a["kind"] == "clip":
        cap = cv2.VideoCapture(str(p))
        cap.set(cv2.CAP_PROP_POS_MSEC, (a["start"] + a["end"]) / 2 * 1000)
        ok, f = cap.read()
        cap.release()
        im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)) if ok else Image.new("RGB", (w, h))
    else:
        im = Image.open(p).convert("RGB")
    im.thumbnail((w, h))
    canvas = Image.new("RGB", (w, h), (10, 10, 14))
    canvas.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    return canvas


def contact_sheets(proj: Project, items: list[dict], per=24):
    """Folhas de contato numeradas para revisão/etiquetagem visual."""
    font = ImageFont.truetype(str(FONTS_DIR / "ChakraPetch-Bold.ttf"), 16)
    out = proj.work / "contact"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.jpg"):
        old.unlink()
    for s in range(0, len(items), per):
        chunk = items[s:s + per]
        cols = 6
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * 330, rows * 214), (7, 7, 10))
        d = ImageDraw.Draw(sheet)
        for i, a in enumerate(chunk):
            x, y = (i % cols) * 330 + 5, (i // cols) * 214 + 5
            sheet.paste(_thumb(proj, a), (x, y))
            d.text((x + 2, y + 182), a["id"][:34], fill=(198, 255, 61), font=font)
        sheet.save(out / f"contact_{s // per + 1:02d}.jpg", quality=85)
    log(f"contact sheets em {out}")
