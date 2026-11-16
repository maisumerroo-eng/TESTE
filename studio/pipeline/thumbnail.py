"""Thumbnail 1280x720 no padrão da cena de rap geek BR (AniRap, M4rkim, 7 Minutoz, Henrique Mendonça):
ARTE EM TELA CHEIA, cores saturadas, brilho forte (bloom) na cor do personagem, contraste alto,
selo do canal no canto e quase nenhum texto (texto só se project.yaml -> thumbnail.text).

Melhor resultado: uma arte/ilustração do personagem em assets/images/ marcada com a tag `thumb`.
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
    pref = [a for a in items if "thumb" in a.get("tags", [])] or \
           [a for a in items if a["kind"] == "image" and {"closeup", "eyes", "power"} & set(a.get("tags", []))] or \
           [a for a in items if a["kind"] != "clip"]
    if pref and pref[0]["kind"] != "clip":
        return proj.assets / pref[0]["file"]
    clips = pref or [a for a in items if a["kind"] == "clip"]
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


def _bloom(arr: np.ndarray, tint, strength=0.55) -> np.ndarray:
    """Brilho estilo pintura digital: realces vazam luz na cor do personagem."""
    f = arr.astype(np.float32) / 255
    lum = f.mean(2, keepdims=True)
    hi = np.clip((lum - 0.55) / 0.45, 0, 1) * f
    glow = cv2.GaussianBlur(hi, (0, 0), 18) + cv2.GaussianBlur(hi, (0, 0), 45) * 0.8
    glow = glow * 0.6 + glow.mean(2, keepdims=True) * np.array(tint, np.float32) / 255 * 0.8
    out = 1 - (1 - f) * (1 - np.clip(glow * strength * 1.6, 0, 1))  # screen
    return np.clip(out * 255, 0, 255).astype(np.uint8)


def _mark(canvas: Image.Image):
    """Selo do canal no canto inferior esquerdo: bloco signal com 影 + KAGERIMA."""
    b = brand()
    sig = hex_to_rgb(b["palette"]["signal"])
    void = hex_to_rgb(b["palette"]["void"])
    d = ImageDraw.Draw(canvas)
    x, y, s = 34, TH - 34 - 70, 70
    d.rectangle([x, y, x + s, y + s], fill=sig + (255,))
    d.text((x + s // 2, y + s // 2 + 3), b["channel"]["kanji"], font=overlays.font(b["fonts"]["jp"], 54),
           fill=void + (255,), anchor="mm")
    f = overlays.font(b["fonts"]["logo"], 32)
    d.text((x + s + 14, y + s // 2), b["channel"]["name"], font=f, fill=(255, 255, 255), anchor="lm",
           stroke_width=3, stroke_fill=(0, 0, 0))


def build(proj: Project) -> Path:
    b = brand()
    c = proj.char
    prim, dark = hex_to_rgb(c["primary"]), hex_to_rgb(c["dark"])
    cfg = proj.cfg.get("thumbnail", {})

    src = _pick_image(proj)
    if src and src.exists():
        img = Image.open(src).convert("RGB")
        s = max(TW / img.width, TH / img.height)
        img = img.resize((int(img.width * s + 0.5), int(img.height * s + 0.5)), Image.LANCZOS)
        fy = float(cfg.get("focus_y", 0.35))  # rosto costuma ficar no terço de cima
        l, t = (img.width - TW) // 2, int((img.height - TH) * fy)
        img = img.crop((l, t, l + TW, t + TH))
    else:
        y, x = np.mgrid[0:TH, 0:TW].astype(np.float32)
        g = np.exp(-(((x - TW / 2) / (TW * 0.4)) ** 2 + ((y - TH / 2) / (TH * 0.5)) ** 2))
        bg = np.array(dark, np.float32) * (1 - g[..., None]) + np.array(prim, np.float32) * g[..., None]
        img = Image.fromarray(bg.astype(np.uint8))

    img = ImageEnhance.Contrast(img).enhance(1.22)
    img = ImageEnhance.Color(img).enhance(1.35)
    arr = _bloom(np.array(img), prim, 0.6)
    # sombras puxadas para a cor escura do personagem + vinheta (foco no centro)
    yy, xx = np.ogrid[:TH, :TW]
    dist = np.sqrt(((xx - TW / 2) / (TW / 2)) ** 2 + ((yy - TH * 0.45) / (TH / 2)) ** 2)
    v = (1 - 0.55 * np.clip(dist - 0.55, 0, 1))[..., None]
    f = arr.astype(np.float32)
    lum = f.mean(2, keepdims=True) / 255
    f = f * (1 - 0.35 * (1 - lum)) + np.array(dark, np.float32) * 0.35 * (1 - lum)
    canvas = Image.fromarray(np.clip(f * v, 0, 255).astype(np.uint8)).convert("RGBA")

    text = (cfg.get("text") or "").upper()
    if text:  # opcional: a cena usa pouco ou nenhum texto
        size = 150 if len(text) <= 10 else 110
        fnt = overlays.font(b["fonts"]["display"], size)
        canvas.alpha_composite(overlays.glow_text((TW, TH), (50, TH - 150 - size), text, fnt,
                                                  (255, 255, 255, 255), prim, 16, stroke=6, stroke_fill=dark))
    _mark(canvas)
    out = canvas.convert("RGB").filter(ImageFilter.UnsharpMask(2, 90, 2))
    path = proj.out / f"{proj.cfg['slug']}_thumb.jpg"
    path.parent.mkdir(parents=True, exist_ok=True)
    out.save(path, quality=92, optimize=True)
    out.resize((1920, 1080), Image.LANCZOS).save(proj.out / f"{proj.cfg['slug']}_thumb_1080.png")
    log(f"thumbnail: {path} ({path.stat().st_size // 1024} KB)")
    return path
