"""Comprime JPG/PNG de uma pasta no lugar.
Uso: python3 comprimir.py <pasta> [--max-hero 2000] [--max 1200]
hero-*, editorial-* e shop-the-look usam --max-hero; o resto usa --max.
JPEG q78 progressivo. PNG sem transparência vira JPG só se o nome terminar em .jpg.
Imprime 1 linha: total antes -> depois.
"""
import argparse
import os
import sys

from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("pasta")
ap.add_argument("--max-hero", type=int, default=2000)
ap.add_argument("--max", type=int, default=1200)
a = ap.parse_args()

antes = depois = 0
for nome in sorted(os.listdir(a.pasta)):
    caminho = os.path.join(a.pasta, nome)
    ext = nome.lower().rsplit(".", 1)[-1]
    if ext not in ("jpg", "jpeg", "png"):
        continue
    antes += os.path.getsize(caminho)
    limite = a.max_hero if nome.startswith(("hero", "editorial", "shop-the-look")) else a.max
    im = Image.open(caminho)
    if max(im.size) > limite:
        im.thumbnail((limite, limite), Image.LANCZOS)
    if ext in ("jpg", "jpeg"):
        im.convert("RGB").save(caminho, "JPEG", quality=78, progressive=True, optimize=True)
    else:
        im.save(caminho, "PNG", optimize=True)
    depois += os.path.getsize(caminho)

if not antes:
    sys.exit("nenhuma imagem")
print(f"{antes/1e6:.1f} MB -> {depois/1e6:.1f} MB")
