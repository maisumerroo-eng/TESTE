#!/usr/bin/env python3
"""@anajcilios — Compro x Nao Compro, IGUAL a referencia do TikTok:
enquadramento parado, cortes secos, foto real do produto recortada acima da cabeca, veredito no peito."""
import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__)); OUT = f"{D}/out2"; os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
SRC = f"{D}/v324.mp4"; SW, SH = 576, 1024
FI = "/usr/share/fonts/opentype/inter/"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
WEB = f"{D}/web"

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    if r.returncode: print(c, "\n", r.stderr[-2500:]); sys.exit(1)
    return r.stdout

def shadowed(im, blur=12, off=(0, 6), alpha=150, pad=40):
    base = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad))
    s = Image.new("RGBA", im.size, (0, 0, 0, 0)); s.putalpha(im.split()[3].point(lambda v: v * alpha // 255))
    base.paste(s, (pad + off[0], pad + off[1]), s); base = base.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(im, (pad, pad)); return base

def emoji_img(ch, size):
    im = Image.new("RGBA", (150, 150)); ImageDraw.Draw(im).text((10, 8), ch, font=ImageFont.truetype(EMOJI, 109), embedded_color=True)
    im = im.crop(im.getbbox()); return im.resize((size, round(size * im.height / im.width)), Image.LANCZOS)

def text_img(txt, font, size, fill=(255, 255, 255, 255)):
    f = ImageFont.truetype(font, size); l, t, r, b = f.getbbox(txt)
    im = Image.new("RGBA", (r - l + 8, b - t + 8)); ImageDraw.Draw(im).text((4 - l, 4 - t), txt, font=f, fill=fill); return im

def verdict(name, ok):
    txt = text_img("Compro" if ok else "Não compro", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontes", "Poppins-SemiBold.ttf") if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fontes")) else f"{D}/fonts2/Poppins-SemiBold.ttf", 66)
    em = emoji_img("✅" if ok else "❌", 58)
    im = Image.new("RGBA", (txt.width + 14 + em.width, max(txt.height, em.height)))
    im.alpha_composite(txt, (0, (im.height - txt.height) // 2)); im.alpha_composite(em, (txt.width + 14, (im.height - em.height) // 2))
    p = f"{OUT}/v_{name}.png"; shadowed(im, blur=8, off=(0, 4), alpha=160).save(p); return p

def product(name, src, box=(470, 430)):
    im = Image.open(f"{WEB}/{src}").convert("RGBA"); im = im.crop(im.getbbox())
    a = im.split()[3].filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2)); im.putalpha(a)
    k = min(box[0] / im.width, box[1] / im.height); im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    p = f"{OUT}/prod_{name}.png"; shadowed(im, blur=18, off=(0, 16), alpha=110).save(p); return p

def mark():
    im = text_img("@anajcilios", FI + "Inter-SemiBold.otf", 34, (255, 255, 255, 210))
    p = f"{OUT}/mark.png"; shadowed(im, blur=4, off=(0, 2), alpha=150, pad=12).save(p); return p

# ---------------- falas: corte seco 0,15s antes da 1a palavra e 0,2s depois da ultima (blocos de fala medidos)
PIECES = [  # (ini, fim, produto)
    (5.40, 11.40, 0),
    (56.28, 60.55, 1), (61.00, 64.15, 1),
    (79.58, 85.45, 2),
    (124.80, 128.95, 3),
    (159.81, 165.90, 4),
    (10.75, 16.40, None),   # final: ela falando e saindo (v325)
]
SRCS = {None: f"{D}/v325.mp4"}
PRODUCTS = [  # imagem recortada, compra?, momento da palavra do veredito no bruto
    ("cut2_aurora.png", True, 5.52),
    ("cut2_jade.png", False, 56.43),
    ("cut2_fin.png", True, 79.74),
    ("cut2_pote.png", False, 124.95),
    ("cut2_soft.png", True, 159.96),
]
ZOOM, FOCUS = 1.30, (372, 657)     # enquadramento fixo (sem movimento)
cw, ch = round(SW / ZOOM / 2) * 2, round(SH / ZOOM / 2) * 2
cx = max(0, min(SW - cw, FOCUS[0] - cw // 2)); cy = max(0, min(SH - ch, FOCUS[1] - ch // 2))

parts, starts, t = [], [], 0.0
for k, (a, b, pr) in enumerate(PIECES):
    d = b - a; f = f"{OUT}/p{k}.mkv"
    src = SRCS.get(pr, SRC) if pr is None else SRC
    pre = f"scale={SW}:{SH}:flags=lanczos," if pr is None else ""
    sh(f'ffmpeg -y -v error -ss {a} -t {d + 0.2} -i {src} -filter_complex '
       f'"[0:v]fps={FPS},{pre}crop={cw}:{ch}:{cx}:{cy},scale={W}:{H}:flags=lanczos,eq=contrast=1.04:brightness=0.015,'
       f'unsharp=5:5:0.5,trim=duration={d:.3f},setsar=1,format=yuv420p[v];'
       f'[0:a]aresample=48000,atrim=0:{d:.3f},asetpts=PTS-STARTPTS,afade=in:d=0.008,afade=out:st={d - 0.01:.3f}:d=0.01[a]" '
       f'-map "[v]" -map "[a]" -r {FPS} -c:v libx264 -crf 14 -preset fast -c:a pcm_s16le {f}')
    parts.append(f); starts.append(t); t += d
TOTAL = t
ins = " ".join(f"-i {f}" for f in parts)
cc = "".join(f"[{k}:v][{k}:a]" for k in range(len(parts)))
sh(f'ffmpeg -y -v error {ins} -filter_complex "{cc}concat=n={len(parts)}:v=1:a=1[v][a0];'
   f'[a0]highpass=f=80,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-14:TP=-1:LRA=7[a]" '
   f'-map "[v]" -map "[a]" -r {FPS} -c:v libx264 -crf 15 -preset fast -c:a pcm_s16le {OUT}/base.mkv')

def tl(ts):
    for k, (a, b, _) in enumerate(PIECES):
        if a - 0.2 <= ts <= b: return starts[k] + max(0, ts - a)
    raise ValueError(ts)
win = {}
for k, (a, b, p) in enumerate(PIECES):
    if p is None: continue
    s, e = starts[k], starts[k] + b - a
    win[p] = (min(win.get(p, (s, e))[0], s), max(win.get(p, (s, e))[1], e))

OV = []
for p, (img, ok, tv) in enumerate(PRODUCTS):
    s, e = win[p]
    OV.append((product(f"p{p}", img), s, e, "(W-w)/2", "560-h/2"))
    OV.append((verdict(f"p{p}", ok), max(s, tl(tv)), e, "(W-w)/2", "1345"))
ins = " ".join(f"-loop 1 -t {TOTAL:.3f} -framerate {FPS} -i {o[0]}" for o in OV)
chain, last = [], "[0:v]"
for k, (png, t0, t1, x, y) in enumerate(OV):
    chain.append(f"{last}[{k + 1}:v]overlay=x='{x}':y='{y}':enable='between(t,{t0:.3f},{t1:.3f})'[m{k}]"); last = f"[m{k}]"
FINAL = f"{D}/anajcilios_compro_nao_compro_v2.mp4"
sh(f'ffmpeg -y -v error -i {OUT}/base.mkv {ins} -filter_complex "{";".join(chain)};{last}format=yuv420p[v]" '
   f'-map "[v]" -map 0:a -t {TOTAL:.3f} -r {FPS} -c:v libx264 -crf 16 -preset slow -c:a aac -b:a 192k -movflags +faststart {FINAL}')
print("TOTAL", round(TOTAL, 2), "windows", {k: (round(a, 2), round(b, 2)) for k, (a, b) in win.items()})
