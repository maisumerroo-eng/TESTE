#!/usr/bin/env python3
# Template: coloque os videos (b.mp4 antes/depois, a.mp4 extra, c.mp4 timelapse) na mesma pasta e ajuste tempos, focos e textos.
"""v7: closes por aproximacao suave (zoompan com easing, sub-pixel via 2x), transicoes por dissolve."""
import subprocess, os, sys
D = os.path.dirname(os.path.abspath(__file__)); OUT = f"{D}/out4"; os.makedirs(OUT, exist_ok=True)
W, H, FPS = 1080, 1920, 30
INTER_SB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
INTER_M = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
SERIF_I = "/usr/share/fonts/truetype/crosextra/Caladea-BoldItalic.ttf"
SW, SH = 464, 832                       # resolucao das fontes
NEUTRO = "eq=contrast=1.03:brightness=0.01"
WARM = "eq=brightness=0.02:contrast=1.05:saturation=1.05,colorbalance=rs=0.03:bs=-0.03"

def sh(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    if r.returncode: print(c, "\n", r.stderr[-2500:]); sys.exit(1)
    return r.stdout

def dur_of(f): return float(sh(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {f}"))

def png_text(name, text, font, size, fill="#FFFFFF", kerning=6):
    p = f"{OUT}/t_{name}.png"
    sh(f"convert -background none -font '{font}' -pointsize {size} -kerning {kerning} -fill '{fill}' "
       f"label:'{text}' -trim +repage -bordercolor none -border 30 {p}")
    sh(f"convert {p} \\( +clone -background '#00000099' -shadow 70x10+0+6 \\) +swap -background none -layers merge +repage {p}")
    return p

def sparkle_png():
    p = f"{OUT}/sparkle.png"
    sh(f"convert -size 160x160 xc:none -fill white -draw 'polygon 80,0 90,70 160,80 90,90 80,160 70,90 0,80 70,70' "
       f"\\( +clone -blur 0x8 \\) -compose screen -composite {p}")
    return p

def shot(name, src, ss, dur_src, speed=1.0, z1=1.0, focus=None, grade=NEUTRO, hold=0.0, ovs=()):
    """Plano com aproximacao suave: zoom 1.0 -> z1 com easing (smoothstep), centro deslizando ate 'focus'.
    Escala 2x antes do zoompan p/ movimento sub-pixel (sem tremido); lanczos + nitidez leve p/ segurar qualidade."""
    dur = dur_src / speed
    N = max(2, round(dur * FPS))
    S = 2  # superamostragem
    p = f"min(on/{N - 1},1)"
    e = f"(3*{p}*{p}-2*{p}*{p}*{p})"                 # smoothstep
    z = f"(1+({z1}-1)*{e})"
    fx, fy = focus if focus else (SW / 2, SH / 2)
    cx = f"({SW / 2}+({fx}-{SW / 2})*{e})*{S * W / SW}"     # centro em px da imagem escalada
    cy = f"({SH / 2}+({fy}-{SH / 2})*{e})*{S * H / SH}"
    x = f"max(0,min(iw-iw/zoom,{cx}-iw/zoom/2))"
    y = f"max(0,min(ih-ih/zoom,{cy}-ih/zoom/2))"
    vf = (f"setpts=(PTS-STARTPTS)/{speed},fps={FPS},"
          f"scale={S * W}:{S * H}:flags=lanczos,"
          f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s={W}x{H}:fps={FPS},"
          f"{grade},unsharp=5:5:0.5:3:3:0.0")
    if hold: vf += f",tpad=stop_mode=clone:stop_duration={hold}"
    vf += f",trim=duration={dur + hold:.3f},setsar=1,format=yuv420p"
    f = f"{OUT}/{name}.mp4"
    sh(f'ffmpeg -y -v error -ss {ss} -t {dur_src + 0.3} -i {D}/{src} -vf "{vf}" -an -r {FPS} '
       f'-c:v libx264 -crf 14 -preset fast {f}')
    if ovs: overlay(f, dur + hold, ovs)
    return f, dur + hold

def overlay(f, dur, ovs):
    ins = " ".join(f"-loop 1 -t {dur} -framerate {FPS} -i {o[0]}" for o in ovs)
    chain, last = [], "[0:v]"
    for k, (png, t0, t1, x, y, fin, fout, pop) in enumerate(ovs):
        t1 = min(t1, dur)
        sc = f",scale=w='trunc(iw*(0.85+0.15*min((t-{t0})/0.3,1))/2)*2':h=-2:eval=frame" if pop else ""
        fo = f",fade=out:st={t1 - fout}:d={fout}:alpha=1" if fout and t1 < dur - 0.01 else ""
        fi = f",fade=in:st={t0}:d={fin}:alpha=1" if fin else ""
        chain.append(f"[{k + 1}:v]format=rgba{sc}{fi}{fo}[o{k}]")
        chain.append(f"{last}[o{k}]overlay=x='{x}':y='{y}':enable='between(t,{t0},{t1})':eval=frame[m{k}]")
        last = f"[m{k}]"
    tmp = f + ".ov.mp4"
    sh(f'ffmpeg -y -v error -i {f} {ins} -filter_complex "{";".join(chain)};{last}format=yuv420p[v]" '
       f'-map "[v]" -t {dur} -r {FPS} -c:v libx264 -crf 14 -preset fast {tmp}')
    os.replace(tmp, f)

T_TREINO = png_text("treinando", "treinando antes", SERIF_I, 120, kerning=1)
T_RES = png_text("resultado", "o resultado", SERIF_I, 150, kerning=1)
T_ARROBA = png_text("arroba", "@anajcilios", INTER_SB, 92, kerning=3)
T_CTA = png_text("cta", "AGENDE SEU HORÁRIO", INTER_M, 44, kerning=12)
SPK = sparkle_png()

# ---------------- planos
TL = shot("tl", "c.mp4", 0.0, 43.4, speed=43.4 / 6.4, z1=1.28, focus=(290, 450), grade=WARM,
          ovs=[(T_TREINO, 0.1, 3.4, "(W-w)/2", "210", 0.45, 0.5, False)])
ANTES = shot("antes", "b.mp4", 0.0, 2.3, speed=0.7, z1=1.45, focus=(212, 284))
R1 = shot("res1", "b.mp4", 7.5, 2.85, speed=0.6, z1=1.45, focus=(245, 300),
          ovs=[(T_RES, 0.3, 3.4, "(W-w)/2", "230", 0.35, 0.45, True)] +
              [(SPK, t, t + 0.9, str(x), str(y), 0.15, 0.45, True)
               for (x, y, t) in [(330, 700, 0.35), (700, 660, 0.5), (780, 930, 0.7), (290, 1000, 0.85)]])
R2 = shot("res2", "a.mp4", 4.9, 3.2, speed=0.65, z1=1.4, focus=(228, 318), hold=0.8,
          ovs=[(T_ARROBA, 2.6, 99, "(W-w)/2", "H-560", 0.45, 0, True),
               (T_CTA, 2.95, 99, "(W-w)/2", "H-400", 0.45, 0, False)])

# ---------------- costura com dissolves (sem cortes secos)
seq = [TL, ANTES, R1, R2]
trans = [("fade", 0.5), ("fadewhite", 0.4), ("fade", 0.55)]
ins = " ".join(f"-i {f}" for f, _ in seq)
fc, last, t = [], "[0:v]", seq[0][1]
starts = [0.0]
for k, ((kind, xd), (f, d)) in enumerate(zip(trans, seq[1:]), start=1):
    off = t - xd
    starts.append(off)
    fc.append(f"{last}[{k}:v]xfade=transition={kind}:duration={xd}:offset={off:.3f}[x{k}]")
    last = f"[x{k}]"; t = off + d
TOTAL = t
fc.append(f"{last}fade=out:st={TOTAL - 0.45}:d=0.45,format=yuv420p[v]")
sh(f'ffmpeg -y -v error {ins} -filter_complex "{";".join(fc)}" -map "[v]" -r {FPS} '
   f'-c:v libx264 -crf 16 -preset medium {OUT}/video.mp4')
REVEAL = starts[2] + trans[1][1] / 2          # pico do branco = drop

# ---------------- audio: mesmo esquema da v4 (abafado continuo -> filtro abre -> drop limpo)
DROP, GEND, OPEN = 5.13, 14.49, 0.9
S0 = GEND - REVEAL
af = (f"[0:a]aresample=44100,atrim={S0}:{GEND},asetpts=PTS-STARTPTS,lowpass=f=700,lowpass=f=700,"
      f"afade=in:d=0.6,afade=out:st={REVEAL - OPEN}:d={OPEN}[A];"
      f"[1:a]aresample=44100,atrim={S0}:{GEND},asetpts=PTS-STARTPTS,volume=-4dB,"
      f"afade=in:st={REVEAL - OPEN}:d={OPEN},atrim=0:{REVEAL}[B];"
      f"[2:a]aresample=44100,atrim={DROP}:15.02,asetpts=PTS-STARTPTS,"
      f"adelay={int(REVEAL * 1000)}|{int(REVEAL * 1000)}[C];"
      f"[A][B][C]amix=inputs=3:normalize=0,atrim=0:{TOTAL},afade=out:st={TOTAL - 0.8}:d=0.8,"
      f"aformat=channel_layouts=stereo,loudnorm=I=-14:TP=-1:LRA=9[a]")
sh(f'ffmpeg -y -v error -i {D}/b.mp4 -i {D}/b.mp4 -i {D}/b.mp4 -filter_complex "{af}" -map "[a]" -ar 48000 {OUT}/audio.wav')
FINAL = f"{D}/lash_antes_depois_v7.mp4"
sh(f"ffmpeg -y -v error -i {OUT}/video.mp4 -i {OUT}/audio.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k "
   f"-movflags +faststart -shortest {FINAL}")
print("TOTAL", round(TOTAL, 2), "starts", [round(s, 2) for s in starts], "REVEAL", round(REVEAL, 2), "S0", round(S0, 2))
