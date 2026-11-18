#!/usr/bin/env python3
"""@anajcilios — Compro x Nao Compro (formato da referencia do TikTok).
Cortes sem pausa (melhores takes), aproximacao suave, card do produto acima da cabeca, veredito no peito."""
import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
D = os.path.dirname(os.path.abspath(__file__)); OUT = f"{D}/out"; os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
SRC = f"{D}/v324.mp4"; SW, SH = 576, 1024
FI = "/usr/share/fonts/opentype/inter/"
EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
SERIF_I = "/usr/share/fonts/truetype/crosextra/Caladea-BoldItalic.ttf"

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    if r.returncode: print(c, "\n", r.stderr[-2500:]); sys.exit(1)
    return r.stdout

# ---------------- graficos (PIL, com emoji colorido)
def emoji_img(ch, size):
    f = ImageFont.truetype(EMOJI, 109)
    im = Image.new("RGBA", (150, 150)); ImageDraw.Draw(im).text((10, 8), ch, font=f, embedded_color=True)
    im = im.crop(im.getbbox())
    return im.resize((size, round(size * im.height / im.width)), Image.LANCZOS)

def shadowed(im, blur=14, off=(0, 8), alpha=150, pad=40):
    base = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad))
    a = im.split()[3].point(lambda v: v * alpha // 255)
    sh_ = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh_.putalpha(a)
    base.paste(sh_, (pad + off[0], pad + off[1]), sh_)
    base = base.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(im, (pad, pad))
    return base

def text_img(txt, font, size, fill=(255, 255, 255, 255)):
    f = ImageFont.truetype(font, size)
    l, t, r, b = f.getbbox(txt)
    im = Image.new("RGBA", (r - l + 8, b - t + 8)); ImageDraw.Draw(im).text((4 - l, 4 - t), txt, font=f, fill=fill)
    return im

def verdict(name, ok):
    txt = text_img("COMPRO" if ok else "NÃO COMPRO", FI + "Inter-ExtraBold.otf", 92)
    em = emoji_img("✅" if ok else "❌", 86)
    im = Image.new("RGBA", (txt.width + 22 + em.width, max(txt.height, em.height)))
    im.alpha_composite(txt, (0, (im.height - txt.height) // 2))
    im.alpha_composite(em, (txt.width + 22, (im.height - em.height) // 2))
    p = f"{OUT}/v_{name}.png"; shadowed(im, blur=10, off=(0, 5), alpha=170).save(p); return p

def card(name, title, brand, icon):
    """card branco do produto (no lugar da foto do produto da referencia)"""
    em = emoji_img(icon, 130)
    t = text_img(title, FI + "Inter-Bold.otf", 64, (40, 26, 32, 255))
    b = text_img(brand.upper(), FI + "Inter-SemiBold.otf", 34, (176, 96, 120, 255)) if brand else None
    w = max(t.width, b.width if b else 0, em.width) + 110
    h = 50 + em.height + 26 + t.height + ((14 + b.height) if b else 0) + 50
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=56, fill=(255, 255, 255, 245))
    y = 50; im.alpha_composite(em, ((w - em.width) // 2, y)); y += em.height + 26
    im.alpha_composite(t, ((w - t.width) // 2, y)); y += t.height + 14
    if b: im.alpha_composite(b, ((w - b.width) // 2, y))
    p = f"{OUT}/c_{name}.png"; shadowed(im, blur=22, off=(0, 14), alpha=120).save(p); return p

def serif(name, txt, size):
    p = f"{OUT}/s_{name}.png"; shadowed(text_img(txt, SERIF_I, size), blur=10, off=(0, 5), alpha=170).save(p); return p

# ---------------- pecas (melhores takes, sem pausas)  (ini, fim, produto)
PIECES = [(5.40, 11.86, 0), (55.70, 60.70, 1), (61.00, 64.10, 1), (79.45, 85.95, 2), (124.50, 128.95, 3), (159.65, 166.10, 4)]
PRODUCTS = [  # titulo, marca, icone, compra?, momento do veredito (s do bruto)
    ("Cola Aurora", "Cherry", "💧", True, 6.28),
    ("Pedra de Jade", "", "💚", False, 56.02),
    ("Finalizador", "", "✨", True, 79.74),
    ("Pote Térmico", "", "🫙", False, 124.60),
    ("Shampoo Soft Snow", "Cherry", "🧴", True, 159.75),
]
XF_PROD, XF_IN = 0.25, 0.12      # dissolve entre produtos / dentro do mesmo produto
FOCUS = (372, 657)               # Ana no quadro (fonte 576x1024)

def piece(k, a, b, z0, z1):
    dur = b - a; N = round(dur * FPS); S = 2
    p = f"min(on/{N - 1},1)"; e = f"(3*{p}*{p}-2*{p}*{p}*{p})"
    z = f"({z0}+({z1}-{z0})*{e})"
    cx, cy = FOCUS[0] * S * W / SW, FOCUS[1] * S * H / SH
    x = f"max(0,min(iw-iw/zoom,{cx}-iw/zoom/2))"; y = f"max(0,min(ih-ih/zoom,{cy}-ih/zoom/2))"
    f = f"{OUT}/p{k}.mp4"
    sh(f'ffmpeg -y -v error -ss {a} -t {dur + 0.2} -i {SRC} -filter_complex '
       f'"[0:v]fps={FPS},scale={S * W}:{S * H}:flags=lanczos,zoompan=z=\'{z}\':x=\'{x}\':y=\'{y}\':d=1:s={W}x{H}:fps={FPS},'
       f'eq=contrast=1.04:brightness=0.015,unsharp=5:5:0.5,trim=duration={dur:.3f},setsar=1,format=yuv420p[v];'
       f'[0:a]atrim=0:{dur:.3f},asetpts=PTS-STARTPTS,aresample=48000,afade=in:d=0.04,afade=out:st={dur - 0.05:.3f}:d=0.05[a]" '
       f'-map "[v]" -map "[a]" -r {FPS} -c:v libx264 -crf 14 -preset fast -c:a pcm_s16le {f}.mkv')
    return f + ".mkv", dur

files, starts, t = [], [], 0.0
for k, (a, b, prod) in enumerate(PIECES):
    zin = 1.30 + 0.04 * (k % 2)                       # cada peca aproxima devagar, ritmo leve
    f, d = piece(k, a, b, zin, zin + 0.10)
    if k:
        t -= XF_IN if PIECES[k - 1][2] == prod else XF_PROD
    starts.append(t); files.append((f, d)); t += d
TOTAL = t

# ---------------- junta com dissolve (video) + crossfade (audio)
ins = " ".join(f"-i {f}" for f, _ in files)
fc, lv, la = [], "[0:v]", "[0:a]"
for k in range(1, len(files)):
    xd = XF_IN if PIECES[k - 1][2] == PIECES[k][2] else XF_PROD
    fc.append(f"{lv}[{k}:v]xfade=transition=fade:duration={xd}:offset={starts[k]:.3f}[v{k}]")
    fc.append(f"{la}[{k}:a]acrossfade=d={xd}:c1=tri:c2=tri[a{k}]")
    lv, la = f"[v{k}]", f"[a{k}]"
fc.append(f"{lv}fade=out:st={TOTAL - 0.4:.3f}:d=0.4,format=yuv420p[vo]")
fc.append(f"{la}highpass=f=80,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,"
          f"afade=out:st={TOTAL - 0.4:.3f}:d=0.4,loudnorm=I=-14:TP=-1:LRA=7[ao]")
sh(f'ffmpeg -y -v error {ins} -filter_complex "{";".join(fc)}" -map "[vo]" -map "[ao]" -r {FPS} '
   f'-c:v libx264 -crf 15 -preset fast -c:a pcm_s16le {OUT}/base.mkv')

# ---------------- overlays: gancho, card do produto (flutuando), veredito, @
def src2tl(ts):            # tempo do bruto -> tempo da timeline
    for k, (a, b, _) in enumerate(PIECES):
        if a <= ts <= b: return starts[k] + ts - a
    raise ValueError(ts)

prod_start, prod_end = {}, {}
for k, (a, b, p) in enumerate(PIECES):
    s, e = starts[k], starts[k] + (b - a)
    prod_start.setdefault(p, s); prod_end[p] = e
OV = []   # (png, t0, t1, x, y, kind)
OV.append((serif("hook", "compro ou não compro?", 84), 0.15, 3.0, "(W-w)/2", "120", "fade"))
for p, (title, brand, icon, ok, tv) in enumerate(PRODUCTS):
    s = prod_start[p] + (0.05 if p == 0 else 0.0)
    e = prod_end[p] - (XF_PROD / 2 if p < len(PRODUCTS) - 1 else 0.3)
    OV.append((card(f"p{p}", title, brand, icon), s + 0.05, e, "(W-w)/2", "330", "card"))
    OV.append((verdict(f"p{p}", ok), max(s + 0.25, src2tl(tv) + 0.15), e, "(W-w)/2", "1330", "pop"))
OV.append((serif("arroba", "@anajcilios", 96), TOTAL - 2.6, TOTAL, "(W-w)/2", "H-330", "fade"))

ins = " ".join(f"-loop 1 -t {TOTAL:.3f} -framerate {FPS} -i {o[0]}" for o in OV)
chain, last = [], "[0:v]"
for k, (png, t0, t1, x, y, kind) in enumerate(OV):
    fi, fo = 0.25, 0.2
    sc = ""
    if kind in ("card", "pop"):   # entra crescendo suave (ease-out), sem tranco
        sc = (f",scale=w='trunc(iw*(0.86+0.14*(1-pow(1-min(max((t-{t0})/0.32,0),1),3)))/2)*2':h=-2:eval=frame")
    yy = y if kind != "card" else f"{y}+10*sin(2*PI*(t-{t0})/2.4)-h/2+250"   # card flutua de leve
    xx = x if kind == "fade" else "(W-w)/2"
    chain.append(f"[{k + 1}:v]format=rgba{sc},fade=in:st={t0}:d={fi}:alpha=1,fade=out:st={t1 - fo:.3f}:d={fo}:alpha=1[o{k}]")
    chain.append(f"{last}[o{k}]overlay=x='{xx}':y='{yy}':enable='between(t,{t0},{t1})':eval=frame[m{k}]")
    last = f"[m{k}]"
FINAL = f"{D}/anajcilios_compro_nao_compro.mp4"
sh(f'ffmpeg -y -v error -i {OUT}/base.mkv {ins} -filter_complex "{";".join(chain)};{last}format=yuv420p[v]" '
   f'-map "[v]" -map 0:a -t {TOTAL:.3f} -r {FPS} -c:v libx264 -crf 18 -preset slow -c:a aac -b:a 192k -movflags +faststart {FINAL}')
print("TOTAL", round(TOTAL, 2), "starts", [round(s, 2) for s in starts])
for p in range(len(PRODUCTS)): print(PRODUCTS[p][0], round(prod_start[p], 2), round(prod_end[p], 2))
