"""Gráficos de marca renderizados com PIL (RGBA): HUD, cartela de título, end card, logo, barra 'signal'."""
from __future__ import annotations

from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .common import FONTS_DIR, brand, hex_to_rgb

FONT_FILES = {
    "Anton": "Anton-Regular.ttf", "Chakra Petch": "ChakraPetch-Bold.ttf",
    "Chakra Petch Medium": "ChakraPetch-Medium.ttf", "Zen Dots": "ZenDots-Regular.ttf",
    "Noto Sans JP Black": "NotoSansJP-Black.ttf", "Bebas Neue": "BebasNeue-Regular.ttf",
}


@lru_cache(maxsize=64)
def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS_DIR / FONT_FILES.get(name, name)), size)


def _rgba(img: Image.Image) -> np.ndarray:
    return np.array(img.convert("RGBA"))


def text_size(d: ImageDraw.ImageDraw, txt, f):
    b = d.textbbox((0, 0), txt, font=f)
    return b[2] - b[0], b[3] - b[1], b


def glow_text(size, xy, txt, f, fill, glow_rgb, glow_r=14, stroke=0, stroke_fill=(0, 0, 0)):
    """Texto com brilho (camada borrada) sobre RGBA transparente."""
    base = Image.new("RGBA", size, (0, 0, 0, 0))
    g = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(g).text(xy, txt, font=f, fill=glow_rgb + (255,), stroke_width=stroke + 6, stroke_fill=glow_rgb + (255,))
    g = g.filter(ImageFilter.GaussianBlur(glow_r))
    base.alpha_composite(g)
    ImageDraw.Draw(base).text(xy, txt, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return base


def hud(char_name: str, track: str, blink: bool) -> np.ndarray:
    b = brand()
    sig = hex_to_rgb(b["palette"]["signal"])
    bone = hex_to_rgb(b["palette"]["bone"])
    im = Image.new("RGBA", (900, 70), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = font(b["fonts"]["hud"], 26)
    if blink:
        d.rectangle([4, 20, 18, 46], fill=sig + (255,))
    d.text((30, 17), b["channel"]["name"], font=f, fill=sig + (255,))
    w, _, _ = text_size(d, b["channel"]["name"], f)
    d.text((30 + w + 14, 17), f"//  {char_name.upper()}  //  {track}", font=f, fill=bone + (200,))
    return _rgba(im)


def title_card(char: dict, hook: str) -> np.ndarray:
    b = brand()
    W, H = 1920, 1080
    prim = hex_to_rgb(char["primary"])
    bone = hex_to_rgb(b["palette"]["bone"])
    sig = hex_to_rgb(b["palette"]["signal"])
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # faixa escura atrás do texto
    band = Image.new("RGBA", (W, 330), (7, 7, 10, 150))
    im.alpha_composite(band, (0, 640))
    name = char["name"].upper()
    f1 = font(b["fonts"]["display"], 150)
    d = ImageDraw.Draw(im)
    w, h, bb = text_size(d, name, f1)
    im.alpha_composite(glow_text((W, H), (120, 660 - bb[1]), name, f1, bone + (255,), prim, 22))
    f2 = font(b["fonts"]["lyrics"], 46)
    d = ImageDraw.Draw(im)
    d.text((126, 852), f"「{hook.upper()}」", font=font(b["fonts"]["jp"], 46), fill=prim + (255,))
    d.text((126, 912), f"{char['anime'].upper()}  ·  {b['channel']['name']}", font=f2, fill=sig + (255,))
    kanji = char.get("kanji", b["channel"]["kanji"])
    fk = font(b["fonts"]["jp"], 300)
    k = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(k).text((W - 120, 600), kanji[:2], font=fk, fill=prim + (70,), anchor="rs")
    im.alpha_composite(k)
    return _rgba(im)


def end_card(next_hint: str = "") -> np.ndarray:
    b = brand()
    W, H = 1920, 1080
    sig = hex_to_rgb(b["palette"]["signal"])
    bone = hex_to_rgb(b["palette"]["bone"])
    im = Image.new("RGBA", (W, H), (7, 7, 10, 205))
    d = ImageDraw.Draw(im)
    fk = font(b["fonts"]["jp"], 360)
    d.text((W // 2, 470), b["channel"]["kanji"], font=fk, fill=bone + (40,), anchor="mm")
    logo = font(b["fonts"]["logo"], 110)
    w, h, bb = text_size(d, b["channel"]["name"], logo)
    im.alpha_composite(glow_text((W, H), ((W - w) // 2, 400 - bb[1]), b["channel"]["name"], logo, bone + (255,), sig, 18))
    d = ImageDraw.Draw(im)
    if next_hint:
        f2 = font(b["fonts"]["hud"], 40)
        msg = f"PRÓXIMO: {next_hint.upper()}"
        w2, _, _ = text_size(d, msg, f2)
        d.text(((W - w2) // 2, 590), msg, font=f2, fill=sig + (255,))
    d.rectangle([(W - w2) // 2 - 34, 598, (W - w2) // 2 - 16, 632], fill=sig + (255,))
    f3 = font(b["fonts"]["hud"], 30)
    sub = b["channel"]["handle"]
    w3, _, _ = text_size(d, sub, f3)
    d.text(((W - w3) // 2, 660), sub, font=f3, fill=bone + (190,))
    return _rgba(im)


def signal_bar(width=420) -> np.ndarray:
    sig = hex_to_rgb(brand()["palette"]["signal"])
    im = Image.new("RGBA", (width + 40, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([20, 16, 20 + width, 24], fill=sig + (255,))
    g = im.filter(ImageFilter.GaussianBlur(6))
    g.alpha_composite(im)
    return _rgba(g)
