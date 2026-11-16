#!/usr/bin/env python3
"""Mídia de TESTE 100% procedural (sem material de terceiros): clipes, artes e páginas de 'mangá'.
Uso: python3 tools/make_test_assets.py <projeto>/assets"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

W, H = 1600, 900


def sky(top, bottom):
    y = np.linspace(0, 1, H)[:, None, None]
    arr = np.array(top, float) * (1 - y) + np.array(bottom, float) * y
    return Image.fromarray(np.repeat(arr, W, 1).astype(np.uint8))


def silhouette(d, x, base, s, color=(5, 5, 8)):
    d.ellipse([x - 40 * s, base - 330 * s, x + 40 * s, base - 250 * s], fill=color)  # cabeça
    d.polygon([(x - 70 * s, base - 250 * s), (x + 70 * s, base - 250 * s), (x + 95 * s, base), (x - 95 * s, base)], fill=color)
    d.polygon([(x + 60 * s, base - 240 * s), (x + 230 * s, base - 300 * s), (x + 240 * s, base - 285 * s), (x + 70 * s, base - 215 * s)], fill=color)


def art(out: Path):
    rng = np.random.default_rng(4)
    # 1 lua vermelha + silhueta
    im = sky((20, 4, 10), (120, 20, 30))
    d = ImageDraw.Draw(im)
    d.ellipse([1050, 120, 1350, 420], fill=(230, 40, 50))
    for i in range(14):
        x = rng.integers(0, W)
        d.rectangle([x, 600 - rng.integers(50, 260), x + rng.integers(40, 120), H], fill=(10, 4, 8))
    silhouette(d, 520, 860, 1.6)
    im.filter(ImageFilter.GaussianBlur(0.6)).save(out / "lua_vermelha.png")
    # 2 tempestade de raios
    im = sky((8, 8, 25), (40, 30, 80))
    d = ImageDraw.Draw(im)
    for b in range(3):
        x, y = rng.integers(300, 1300), 0
        pts = [(x, y)]
        while y < 700:
            x += rng.normal(0, 40)
            y += rng.uniform(30, 70)
            pts.append((x, y))
        d.line(pts, fill=(190, 170, 255), width=9)
        d.line(pts, fill=(255, 255, 255), width=3)
    silhouette(d, 800, 900, 1.9)
    im.save(out / "tempestade_raio.png")
    # 3 olho abstrato (close)
    im = Image.new("RGB", (W, H), (12, 6, 8))
    d = ImageDraw.Draw(im)
    d.ellipse([300, 250, 1300, 650], fill=(235, 225, 220))
    d.ellipse([650, 300, 950, 600], fill=(200, 20, 35))
    d.ellipse([755, 405, 845, 495], fill=(10, 0, 0))
    for a in range(0, 360, 120):
        r = np.radians(a)
        cx, cy = 800 + 95 * np.cos(r), 450 + 95 * np.sin(r)
        d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(10, 0, 0))
    d.rectangle([0, 0, W, 300], fill=(12, 6, 8))
    im.filter(ImageFilter.GaussianBlur(1.2)).save(out / "olho_close.png")
    # 4 chuva / emocional
    im = sky((30, 35, 50), (70, 80, 100))
    d = ImageDraw.Draw(im)
    for _ in range(500):
        x, y = rng.integers(0, W), rng.integers(0, H)
        d.line([(x, y), (x - 8, y + 40)], fill=(180, 190, 210), width=1)
    silhouette(d, 900, 900, 1.5, (20, 22, 30))
    silhouette(d, 600, 900, 1.2, (20, 22, 30))
    im.save(out / "chuva_irmaos.png")


def manga(out: Path):
    rng = np.random.default_rng(9)
    for pg in range(2):
        im = Image.new("RGB", (1200, 1800), (255, 255, 255))
        d = ImageDraw.Draw(im)
        boxes = [(40, 40, 1160, 620), (40, 660, 590, 1220), (630, 660, 1160, 1220), (40, 1260, 1160, 1760)]
        for k, (a, b, c, e) in enumerate(boxes):
            pw, ph = c - a, e - b
            pan = Image.new("RGB", (pw, ph), (250, 250, 250))
            pd = ImageDraw.Draw(pan)
            cx, cy = pw // 2, ph // 2
            for _ in range(60):  # linhas de ação
                ang = rng.uniform(0, 2 * np.pi)
                r0 = rng.uniform(80, 160)
                pd.line([(cx + r0 * np.cos(ang), cy + r0 * np.sin(ang)), (cx + 900 * np.cos(ang), cy + 900 * np.sin(ang))],
                        fill=(0, 0, 0), width=2)
            silhouette(pd, cx, ph - 10, ph / 520, (0, 0, 0))
            pd.rectangle([0, 0, pw - 1, ph - 1], outline=(0, 0, 0), width=6)
            im.paste(pan, (a, b))
        # mantém as calhas brancas limpas
        im.save(out / f"pagina_{pg + 1}.png")


def clips(out: Path):
    srcs = ["mandelbrot=s=1280x720:rate=24", "life=s=1280x720:mold=10:r=24:ratio=0.1:death_color=#C00000:life_color=#200008",
            "cellauto=s=1280x720:rule=110:rate=24", "gradients=s=1280x720:r=24:speed=0.03",
            "mandelbrot=s=1280x720:rate=24:start_scale=0.3:end_scale=0.01:outer=normalized_iteration_count"]
    parts = []
    for i, s in enumerate(srcs):
        p = out / f"_p{i}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", s, "-t", "4",
                        "-vf", "eq=saturation=1.4,hue=h=-20", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(p)], check=True)
        parts.append(p)
    lst = out / "_l.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(out / "cenas_teste.mp4")], check=True)
    for p in parts + [lst]:
        p.unlink()


if __name__ == "__main__":
    root = Path(sys.argv[1])
    for sub in ("images", "manga", "clips"):
        (root / sub).mkdir(parents=True, exist_ok=True)
    art(root / "images")
    manga(root / "manga")
    clips(root / "clips")
    print("ok")
