#!/usr/bin/env python3
"""Reel 'precisa de um site?' para a Fator Marketing — mesma estrutura/tempos do reel de referencia (30fps)."""
import subprocess, os, sys, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__)); OUT = f"{D}/out"; os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
REF = f"{D}/dl/reel.mp4"
F800 = f"{D}/fonts/BarlowCondensed-800Italic.ttf"
WHITE, DARK, INK, NAVY = (255, 255, 255), (30, 30, 30), (17, 17, 17), (14, 37, 99)

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    if r.returncode: print(c, "\n", r.stderr[-2000:]); sys.exit(1)

def text_block(lines, size, color, gap=0.95):
    f = ImageFont.truetype(F800, size)
    boxes = [f.getbbox(l) for l in lines]
    lh = round(size * gap); w = max(b[2] - b[0] for b in boxes) + 20
    im = Image.new("RGBA", (w, lh * len(lines) + 20))
    d = ImageDraw.Draw(im)
    for i, (l, b) in enumerate(zip(lines, boxes)):
        d.text(((w - (b[2] - b[0])) // 2 - b[0], 10 + i * lh - b[1] + (lh - (b[3] - b[1])) // 2), l, font=f, fill=color + (255,))
    return im

def grunge(im, seed=3):
    """textura gasta (como o slogan da referencia)"""
    random.seed(seed); m = Image.new("L", im.size, 255); d = ImageDraw.Draw(m)
    for _ in range(int(im.width * im.height / 260)):
        x, y = random.randrange(im.width), random.randrange(im.height); r = random.choice([1, 1, 1, 2, 2, 3])
        d.ellipse((x - r, y - r, x + r, y + r), fill=random.choice([0, 60, 110]))
    m = m.filter(ImageFilter.GaussianBlur(0.6))
    a = Image.composite(im.split()[3], Image.new("L", im.size, 0), m); im.putalpha(a); return im

def card(name, bg, content, y_center=0.5):
    im = Image.new("RGB", (W, H), bg)
    for layer, yc in content:
        im.paste(layer, ((W - layer.width) // 2, round(H * yc - layer.height / 2)), layer)
    p = f"{OUT}/card_{name}.png"; im.save(p); return p

# ---------------- cartelas (alternancia de fundo invertida p/ o logo azul fechar no branco)
logo = Image.open(f"{D}/logo_cut.png").convert("RGBA")
k = 560 / logo.width; logo = logo.resize((round(logo.width * k), round(logo.height * k)), Image.LANCZOS)
slogan = grunge(text_block(["Sites e Sistemas", "Personalizados"], 118, NAVY, gap=1.0))
CARDS = [  # (nome, fundo, conteudo, n_frames)  — mesmos tempos do original
    ("site",     DARK,  [(text_block(["precisa de um site?"], 100, WHITE), 0.5)], 30),
    ("limpo",    WHITE, [(text_block(["limpo."], 100, INK), 0.5)], 31),
    ("moderno",  DARK,  [(text_block(["moderno."], 100, WHITE), 0.5)], 31),
    ("converte", WHITE, [(text_block(["que converte."], 100, INK), 0.5)], 31),
    ("cta",      DARK,  [(text_block(['Chama na DM ou comenta "SITE"', "pra uma demo grátis"], 78, WHITE, gap=1.02), 0.5)], 30),
    ("logo",     WHITE, [(logo, 0.42), (slogan, 0.645)], 31),
]
HOOK_FRAMES = 54   # chute de bola, igual ao gancho do original

parts = []
sh(f'ffmpeg -y -v error -i {REF} -vf "scale={W}:{H}:flags=lanczos,setsar=1,trim=end_frame={HOOK_FRAMES},format=yuv420p" '
   f'-an -r {FPS} -c:v libx264 -crf 14 -preset fast {OUT}/p0.mp4'); parts.append(f"{OUT}/p0.mp4")
for i, (name, bg, content, n) in enumerate(CARDS, 1):
    png = card(name, bg, content)
    f = f"{OUT}/p{i}.mp4"
    sh(f'ffmpeg -y -v error -loop 1 -framerate {FPS} -i {png} -frames:v {n} -vf "format=yuv420p" -c:v libx264 -crf 14 -preset fast -tune stillimage {f}')
    parts.append(f)
# fecha com 3 quadros pretos, como o original
sh(f'ffmpeg -y -v error -f lavfi -i color=c=black:s={W}x{H}:r={FPS} -frames:v 3 -vf format=yuv420p -c:v libx264 -crf 14 {OUT}/p_end.mp4')
parts.append(f"{OUT}/p_end.mp4")
with open(f"{OUT}/list.txt", "w") as fh:
    for p in parts: fh.write(f"file '{p}'\n")
sh(f"ffmpeg -y -v error -f concat -safe 0 -i {OUT}/list.txt -c copy {OUT}/video.mp4")
FINAL = f"{D}/fator_marketing_precisa_de_um_site.mp4"
sh(f"ffmpeg -y -v error -i {OUT}/video.mp4 -i {REF} -map 0:v -map 1:a -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p "
   f"-c:a aac -b:a 192k -shortest -movflags +faststart {FINAL}")
print("ok", FINAL)
