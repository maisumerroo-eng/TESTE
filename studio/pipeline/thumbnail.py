"""Thumbnail 16:9 (1280x720) de alto impacto no padrão KAGE.EXE.

- Personagem recortado por profundidade (Depth Anything) com contorno brilhante na cor dele;
- Texto curto GIGANTE atrás/ao lado do personagem (Anton), alto contraste;
- Kanji e selo KAGE.EXE (verde 'signal') — assinatura constante do canal.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

from . import overlays
from .common import Project, brand, hex_to_rgb, load_yaml, log

TW, TH = 1280, 720


def _pick_image(proj: Project) -> Path | None:
    t = proj.cfg.get("thumbnail", {})
    if t.get("image"):
        return proj.root / t["image"]
    ay = proj.assets / "assets.yaml"
    if not ay.exists():
        return None
    items = load_yaml(ay).get("assets", [])
    pref = [a for a in items if a["kind"] != "clip" and {"closeup", "eyes", "thumb"} & set(a.get("tags", []))]
    pref = pref or [a for a in items if a["kind"] != "clip"]
    if pref:
        return proj.assets / pref[0]["file"]
    clips = [a for a in items if a["kind"] == "clip" and "closeup" in a.get("tags", [])] or \
            [a for a in items if a["kind"] == "clip"]
    if clips:
        a = clips[0]
        cap = cv2.VideoCapture(str(proj.assets / a["file"]))
        cap.set(cv2.CAP_PROP_POS_MSEC, (a["start"] + a["end"]) / 2 * 1000)
        ok, f = cap.read()
        if ok:
            p = proj.path("work", "thumb_src.png")
            cv2.imwrite(str(p), f)
            return p
    return None


def build(proj: Project) -> Path:
    b = brand()
    c = proj.char
    prim, dark = hex_to_rgb(c["primary"]), hex_to_rgb(c["dark"])
    sig, bone = hex_to_rgb(b["palette"]["signal"]), hex_to_rgb(b["palette"]["bone"])
    cfg = proj.cfg.get("thumbnail", {})
    text = (cfg.get("text") or proj.cfg.get("hook") or c["short"]).upper()

    # fundo: escuro + brilho radial na cor do personagem
    y, x = np.mgrid[0:TH, 0:TW].astype(np.float32)
    g = np.exp(-(((x - TW * 0.68) / (TW * 0.38)) ** 2 + ((y - TH * 0.5) / (TH * 0.6)) ** 2))
    bg = np.array(dark, np.float32) * (1 - g[..., None]) + np.array(prim, np.float32) * g[..., None] * 0.75
    canvas = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert("RGBA")

    src = _pick_image(proj)
    subject = None
    if src and src.exists():
        img = Image.open(src).convert("RGB")
        img = ImageEnhance.Contrast(img).enhance(1.15)
        img = ImageEnhance.Color(img).enhance(1.15)
        # encaixa o personagem no lado direito (cover em 820x720)
        sw, sh = 820, TH
        s = max(sw / img.width, sh / img.height)
        img = img.resize((int(img.width * s), int(img.height * s)), Image.LANCZOS)
        l, t = (img.width - sw) // 2, (img.height - sh) // 3
        img = img.crop((l, t, l + sw, t + sh))
        try:
            from .depth import depth_map
            dp = depth_map(src, proj.work / "depth" / "thumb_src.npy").astype(np.float32)
            d = cv2.resize(dp, (int(dp.shape[1] * s), int(dp.shape[0] * s)))[t:t + sh, l:l + sw]
            thr = np.quantile(d, 0.55)
            mask = np.clip((d - thr) / 0.12, 0, 1)
            mask = cv2.GaussianBlur(mask, (0, 0), 2)
        except Exception:
            mask = np.ones((sh, sw), np.float32)
        # funde as bordas da imagem para não ficar "colada"
        fade = np.ones((sh, sw), np.float32)
        ramp = np.linspace(0, 1, 160)
        fade[:, :160] *= ramp
        full = np.clip(0.55 * fade + 0.45 * mask * fade, 0, 1)
        img_rgba = img.convert("RGBA")
        img_rgba.putalpha(Image.fromarray((full * 255).astype(np.uint8)))
        subject = img.convert("RGBA")
        subject.putalpha(Image.fromarray((mask * 255).astype(np.uint8)))
        canvas.alpha_composite(img_rgba, (TW - sw, 0))

    # texto atrás do personagem
    d = ImageDraw.Draw(canvas)
    size = 210 if len(text) <= 8 else (160 if len(text) <= 13 else 120)
    f = overlays.font(b["fonts"]["display"], size)
    words = text.split()
    lines = [" ".join(words[: (len(words) + 1) // 2]), " ".join(words[(len(words) + 1) // 2:])] if len(text) > 10 and len(words) > 1 else [text]
    y0 = 360 - (len(lines) * size * 0.95) / 2
    for k, ln in enumerate(lines):
        layer = overlays.glow_text((TW, TH), (58, int(y0 + k * size * 0.95) - int(size * 0.18)), ln, f,
                                   bone + (255,), prim, 18, stroke=7, stroke_fill=dark)
        canvas.alpha_composite(layer)

    # personagem por cima do texto + contorno brilhante (rim light)
    if subject is not None:
        a = np.array(subject.split()[-1]).astype(np.float32) / 255
        edge = cv2.dilate((a > 0.5).astype(np.uint8), np.ones((7, 7), np.uint8)) - (a > 0.5).astype(np.uint8)
        rim = np.zeros((TH, subject.width, 4), np.uint8)
        rim[..., :3] = prim
        rim[..., 3] = cv2.GaussianBlur(edge.astype(np.float32) * 255, (0, 0), 4).clip(0, 255).astype(np.uint8)
        canvas.alpha_composite(Image.fromarray(rim), (TW - subject.width, 0))
        sub_only = subject.copy()
        sub_only.putalpha(Image.fromarray((np.clip(a * 1.3 - 0.2, 0, 1) * 255).astype(np.uint8)))
        canvas.alpha_composite(sub_only, (TW - subject.width, 0))

    # assinatura do canal
    d = ImageDraw.Draw(canvas)
    hud = overlays.font(b["fonts"]["hud"], 34)
    d.rectangle([40, 640, 56, 672], fill=sig + (255,))
    d.text((68, 634), b["channel"]["name"], font=hud, fill=sig + (255,))
    kan = overlays.font(b["fonts"]["jp"], 64)
    d.text((TW - 40, 30), c.get("kanji", "影")[:3], font=kan, fill=bone + (230,), anchor="ra")
    # moldura fina + vinheta
    vign = np.ones((TH, TW), np.float32)
    vy, vx = np.ogrid[:TH, :TW]
    dist = np.sqrt(((vx - TW / 2) / (TW / 2)) ** 2 + ((vy - TH / 2) / (TH / 2)) ** 2)
    vign = 1 - 0.45 * np.clip(dist - 0.7, 0, 1)
    arr = np.array(canvas.convert("RGB")).astype(np.float32) * vign[..., None]
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(ImageFilter.UnsharpMask(2, 80, 2))
    path = proj.out / f"{proj.cfg['slug']}_thumb.jpg"
    path.parent.mkdir(parents=True, exist_ok=True)
    out.save(path, quality=92, optimize=True)
    out.resize((1920, 1080), Image.LANCZOS).save(proj.out / f"{proj.cfg['slug']}_thumb_1080.png")
    log(f"thumbnail: {path} ({path.stat().st_size // 1024} KB)")
    return path
