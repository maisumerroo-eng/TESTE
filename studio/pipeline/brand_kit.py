"""Kit de identidade KAGE.EXE: logo, avatar, banner do YouTube, vinheta (vídeo+som), template de thumbnail
e prancha de estilo. Saída em brand/."""
from __future__ import annotations

import subprocess

import cv2
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter

from . import overlays, sfx
from .common import BRAND_DIR, CONFIGS, brand, hex_to_rgb, load_yaml, log

B = brand()
P = {k: hex_to_rgb(v) for k, v in B["palette"].items()}
F = B["fonts"]


def _grain(im: Image.Image, amount=8, scan=True) -> Image.Image:
    a = np.array(im.convert("RGB")).astype(np.float32)
    a += np.random.default_rng(3).normal(0, amount, a.shape[:2])[..., None]
    if scan:
        a[::3] *= 0.93
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def _glitch_text(size, xy, txt, f, fill, shift=6, anchor=None):
    """Texto com separação RGB (glitch) — assinatura do canal."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    kw = dict(font=f, anchor=anchor) if anchor else dict(font=f)
    d.text((xy[0] - shift, xy[1]), txt, fill=P["glitch"] + (170,), **kw)
    d.text((xy[0] + shift, xy[1]), txt, fill=(60, 220, 255, 150), **kw)
    d.text(xy, txt, fill=fill, **kw)
    return layer


def logo(scale=1.0, bg=None) -> Image.Image:
    W, H = int(1600 * scale), int(420 * scale)
    im = Image.new("RGBA", (W, H), bg or (0, 0, 0, 0))
    s = int(300 * scale)
    x0, y0 = int(40 * scale), (H - s) // 2
    # bloco "signal" com o kanji (como um cursor de terminal)
    ImageDraw.Draw(im).rectangle([x0, y0, x0 + s, y0 + s], fill=P["signal"] + (255,))
    ImageDraw.Draw(im).text((x0 + s // 2, y0 + s // 2 + int(8 * scale)), B["channel"]["kanji"],
                            font=overlays.font(F["jp"], int(230 * scale)), fill=P["void"] + (255,), anchor="mm")
    f = overlays.font(F["logo"], int(170 * scale))
    tx = x0 + s + int(60 * scale)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).text((tx, H // 2), B["channel"]["name"], font=f, fill=P["signal"] + (120,), anchor="lm")
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(18 * scale)))
    im.alpha_composite(_glitch_text((W, H), (tx, H // 2), B["channel"]["name"], f, P["bone"] + (255,),
                                    int(5 * scale), anchor="lm"))
    # cortes de glitch horizontais
    a = np.array(im)
    rng = np.random.default_rng(11)
    for _ in range(5):
        y = int(rng.integers(int(H * 0.25), int(H * 0.75)))
        h = int(rng.integers(3, int(10 * scale) + 4))
        a[y:y + h] = np.roll(a[y:y + h], int(rng.integers(-30, 30) * scale), axis=1)
    return Image.fromarray(a)


def avatar() -> Image.Image:
    S = 800
    im = Image.new("RGB", (S, S), P["void"])
    d = ImageDraw.Draw(im)
    y, x = np.mgrid[0:S, 0:S]
    g = np.exp(-(((x - S / 2) ** 2 + (y - S / 2) ** 2) / (2 * (S * 0.32) ** 2)))
    arr = np.array(im).astype(np.float32) + g[..., None] * np.array(P["graphite"]) * 1.6
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    im.alpha_composite(_glitch_text((S, S), (S // 2, S // 2 + 20), B["channel"]["kanji"],
                                    overlays.font(F["jp"], 520), P["bone"] + (255,), 10, anchor="mm"))
    d = ImageDraw.Draw(im)
    d.rectangle([S // 2 + 170, S // 2 + 190, S // 2 + 230, S // 2 + 290], fill=P["signal"] + (255,))
    d.ellipse([24, 24, S - 24, S - 24], outline=P["signal"] + (200,), width=4)
    a = np.array(im)
    rng = np.random.default_rng(4)
    for _ in range(7):
        yy = int(rng.integers(200, 600))
        hh = int(rng.integers(4, 14))
        a[yy:yy + hh] = np.roll(a[yy:yy + hh], int(rng.integers(-40, 40)), axis=1)
    return _grain(Image.fromarray(a), 6)


def banner() -> Image.Image:
    W, H = 2560, 1440
    im = Image.new("RGB", (W, H), P["void"])
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    g = np.exp(-(((x - W / 2) / (W * 0.35)) ** 2 + ((y - H / 2) / (H * 0.18)) ** 2))
    arr = np.array(im).astype(np.float32) + g[..., None] * np.array(P["graphite"]) * 2.2
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(im)
    # kanjis dos personagens como "canais" de transmissão (cores próprias)
    chars = [load_yaml(p) for p in sorted((CONFIGS / "characters").glob("*.yaml"))]
    fk = overlays.font(F["jp"], 120)
    for i, c in enumerate(chars):
        cx = int(W / 2 + (i - (len(chars) - 1) / 2) * 330)
        d.text((cx, 360), c["kanji"][0], font=fk, fill=hex_to_rgb(c["primary"]) + (90,), anchor="mm")
        d.text((cx, 1080), c["kanji"][-1], font=fk, fill=hex_to_rgb(c["primary"]) + (60,), anchor="mm")
    lg = logo(0.8)
    im.alpha_composite(lg, ((W - lg.width) // 2, H // 2 - lg.height // 2 - 40))
    f2 = overlays.font(F["hud"], 44)
    tag = "RAP GEEK DIRETO DA SOMBRA  //  NOVA TRANSMISSÃO TODA SEMANA"
    d = ImageDraw.Draw(im)
    d.text((W // 2, H // 2 + 175), tag, font=f2, fill=P["ash"] + (255,), anchor="mm")
    # guia da área segura (1546x423) só no arquivo _guia
    out = _grain(im, 5)
    guide = out.copy()
    ImageDraw.Draw(guide).rectangle([(W - 1546) // 2, (H - 423) // 2, (W + 1546) // 2, (H + 423) // 2],
                                    outline=(255, 0, 0), width=3)
    guide.save(BRAND_DIR / "banner_guia_area_segura.png")
    return out


def vinheta(seconds=3.0, fps=30):
    """Vinheta curta de abertura/fechamento: kanji em glitch -> logo digitando -> barra signal."""
    W, H = 1920, 1080
    n = int(seconds * fps)
    lg = np.array(logo(1.0))
    kan = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(kan).text((W // 2, H // 2), B["channel"]["kanji"], font=overlays.font(F["jp"], 700),
                             fill=P["bone"] + (255,), anchor="mm")
    kan = np.array(kan)
    out = BRAND_DIR / "vinheta_kage.mp4"
    wav = BRAND_DIR / "vinheta_kage.wav"
    # som: whoosh reverso -> boom + zaps
    sr = sfx.SR
    audio = np.zeros(int(seconds * sr))
    w = sfx.whoosh_rev(1.0) * 0.5
    audio[: len(w)] += w
    b = sfx.boom(1.6)
    i = int(1.0 * sr)
    audio[i:i + len(b)] += b[: len(audio) - i]
    for t in (0.35, 0.6, 1.9):
        z = sfx.zap()
        j = int(t * sr)
        audio[j:j + len(z)] += z * 0.6
    audio = audio / np.abs(audio).max() * 0.85
    sf.write(str(wav), np.stack([audio, audio], 1), sr)
    from . import fx
    pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(fps), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", str(out)], stdin=subprocess.PIPE)
    void = np.zeros((H, W, 3), np.uint8)
    void[:] = P["void"]
    for k in range(n):
        t = k / fps
        f = void.copy()
        if t < 1.0:  # kanji piscando em glitch
            if int(t * 14) % 3 != 0:
                f = fx.alpha_over(f, kan, 0, 0, min(1, t * 1.5))
                f = fx.glitch(f, 1 - t, k)
        else:
            r = t - 1.0
            if r < 0.1:
                f = fx.flash(f, 1 - r / 0.1)
            # logo revelado da esquerda para a direita (digitando)
            reveal = int(min(1, r / 0.6) * lg.shape[1])
            part = lg.copy()
            part[:, reveal:, 3] = 0
            f = fx.alpha_over(f, part, (W - lg.shape[1]) // 2, (H - lg.shape[0]) // 2)
            if r < 0.5:
                f = fx.glitch(f, 0.6 * (1 - r / 0.5), k)
            bw = int(min(1, max(0, (r - 0.4) / 0.5)) * 900)
            if bw:
                cv2.rectangle(f, ((W - 900) // 2, H // 2 + 200), ((W - 900) // 2 + bw, H // 2 + 208), P["signal"], -1)
            if t > seconds - 0.25:
                f = fx.blackout(f, (t - (seconds - 0.25)) / 0.25)
        f = fx.finish(f, k)
        pr.stdin.write(f.tobytes())
    pr.stdin.close()
    pr.wait()
    return out


def style_board():
    """Prancha de estilo: paleta da marca + paletas de personagens + tipografia + legenda exemplo."""
    W, H = 1920, 1080
    im = Image.new("RGB", (W, H), P["void"]).convert("RGBA")
    d = ImageDraw.Draw(im)
    lg = logo(0.45)
    im.alpha_composite(lg, (60, 40))
    d = ImageDraw.Draw(im)
    fh = overlays.font(F["hud"], 26)
    d.text((70, 250), "PALETA DA MARCA", font=fh, fill=P["ash"])
    for i, (k, v) in enumerate(B["palette"].items()):
        x = 70 + i * 290
        d.rectangle([x, 290, x + 260, 400], fill=hex_to_rgb(v), outline=P["graphite"], width=2)
        d.text((x, 410), f"{k.upper()}  {v}", font=fh, fill=P["bone"])
    d.text((70, 480), "PERSONAGENS (cor própria + elementos fixos da marca)", font=fh, fill=P["ash"])
    chars = [load_yaml(p) for p in sorted((CONFIGS / "characters").glob("*.yaml"))]
    for i, c in enumerate(chars):
        x = 70 + i * 300
        for j, key in enumerate(("primary", "secondary", "dark", "accent")):
            d.rectangle([x + j * 65, 520, x + j * 65 + 60, 580], fill=hex_to_rgb(c[key]))
        d.text((x, 590), c['slug'].upper(), font=fh, fill=P["bone"])
        d.text((x, 625), f"{c['element']}", font=fh, fill=hex_to_rgb(c["primary"]))
    d.text((70, 700), "TIPOGRAFIA", font=fh, fill=P["ash"])
    d.text((70, 740), "IMPACTO — ANTON", font=overlays.font(F["display"], 90), fill=P["bone"])
    d.text((70, 860), "LEGENDAS — CHAKRA PETCH BOLD", font=overlays.font(F["lyrics"], 54), fill=P["bone"])
    d.text((70, 940), "HUD // CHAKRA PETCH MEDIUM", font=overlays.font(F["hud"], 40), fill=P["signal"])
    d.text((1150, 740), "影 写輪眼 無量空処", font=overlays.font(F["jp"], 80), fill=P["bone"])
    # exemplo de legenda
    fl = overlays.font(F["lyrics"], 64)
    d.text((1150, 900), "O ", font=fl, fill=P["bone"], stroke_width=4, stroke_fill=P["void"])
    d.text((1150 + d.textlength("O ", font=fl), 900), "SHARINGAN", font=fl, fill=hex_to_rgb("#E01E37"),
           stroke_width=4, stroke_fill=P["void"])
    d.text((1150 + d.textlength("O SHARINGAN ", font=fl), 900), "DESPERTA", font=fl, fill=P["bone"],
           stroke_width=4, stroke_fill=P["void"])
    return _grain(im, 4)


def build_all():
    BRAND_DIR.mkdir(exist_ok=True)
    lg = logo(1.0)
    lg.save(BRAND_DIR / "logo_kage_transparente.png")
    bg = Image.new("RGBA", lg.size, P["void"] + (255,))
    bg.alpha_composite(lg)
    bg.convert("RGB").save(BRAND_DIR / "logo_kage_fundo_escuro.png")
    avatar().save(BRAND_DIR / "avatar_800.png")
    banner().save(BRAND_DIR / "banner_2560x1440.png")
    style_board().save(BRAND_DIR / "prancha_estilo.png")
    log("vinheta...")
    vinheta()
    log(f"kit de marca gerado em {BRAND_DIR}")
