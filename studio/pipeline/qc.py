"""Controle de qualidade antes da entrega. Reprova o vídeo se algo técnico estiver fora do padrão."""
from __future__ import annotations

import re
from collections import Counter

from PIL import Image

from .common import Project, brand, ffprobe, load_json, log, run, save_json


def check(proj: Project, video=None) -> dict:
    b = brand()
    v = video or proj.out / f"{proj.cfg['slug']}.mp4"
    info = ffprobe(v)
    vs = next(s for s in info["streams"] if s["codec_type"] == "video")
    aus = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    num, den = map(int, vs["r_frame_rate"].split("/"))
    fps = num / den
    dur = float(info["format"]["duration"])
    tl = load_json(proj.work / "timeline.json")
    res = []

    def ok(name, cond, detail=""):
        res.append(dict(check=name, ok=bool(cond), detail=detail))

    ok("resolução 1920x1080", (vs["width"], vs["height"]) == (1920, 1080), f"{vs['width']}x{vs['height']}")
    ok("FPS", abs(fps - tl["fps"]) < 0.01, f"{fps:.2f}")
    ok("codec H.264 yuv420p", vs["codec_name"] == "h264" and vs.get("pix_fmt") == "yuv420p",
       f"{vs['codec_name']} {vs.get('pix_fmt')}")
    ok("áudio AAC 48 kHz", aus is not None and aus["codec_name"] == "aac" and aus["sample_rate"] == "48000",
       f"{aus and aus['codec_name']} {aus and aus['sample_rate']}")
    ok("duração = música", abs(dur - tl["duration"]) < 0.25, f"vídeo {dur:.2f}s / música {tl['duration']:.2f}s")

    # telas pretas acidentais (ignora o fade-in inicial, o blackout proposital e o end card)
    r = run(["ffmpeg", "-hide_banner", "-i", str(v), "-vf", "blackdetect=d=0.25:pic_th=0.97:pix_th=0.06",
             "-an", "-f", "null", "-"])
    blacks = [(float(a), float(z)) for a, z in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", r.stderr)]
    bad_black = [x for x in blacks if x[0] > 1.0 and x[1] < dur - 5.5]
    ok("sem tela preta acidental", not bad_black, str(bad_black[:5]))

    # congelamentos longos (fora de pausas intencionais)
    r = run(["ffmpeg", "-hide_banner", "-i", str(v), "-vf", "freezedetect=n=0.002:d=2.5", "-an", "-f", "null", "-"])
    fz = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", r.stderr)]
    ok("sem congelamento > 2,5 s", not fz, str(fz[:5]))

    # loudness final
    r = run(["ffmpeg", "-hide_banner", "-i", str(v), "-af", "ebur128=peak=true", "-vn", "-f", "null", "-"])
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    lufs = float(m[-1]) if m else 0
    peak = float(tp[-1]) if tp else 0
    ok("loudness -14 LUFS (±1,5)", abs(lufs - b["audio"]["target_lufs"]) <= 1.5, f"{lufs} LUFS")
    ok("true peak ≤ -0,5 dBTP", peak <= -0.5, f"{peak} dBTP")

    # edição: repetição, ritmo, estrutura
    shots = tl["shots"]
    cnt = Counter(s.get("asset") for s in shots if s.get("asset"))
    most = cnt.most_common(1)[0] if cnt else ("-", 0)
    ok("sem cena repetida em excesso", (most[1] <= max(3, len(shots) // 12)) or len(cnt) < 6,
       f"mais usada: {most[0]} x{most[1]} | {len(cnt)} cenas distintas / {len(shots)} planos")
    longest = max(s["end"] - s["start"] for s in shots)
    pauses = tl["events"].get("pauses", [])
    ok("sem plano parado longo demais (>8 s)", longest <= 8.0, f"maior plano {longest:.1f}s")
    adj = sum(1 for x, y in zip(shots, shots[1:]) if x.get("asset") and x.get("asset") == y.get("asset"))
    ok("sem mesma cena em planos seguidos", adj == 0, f"{adj} ocorrências")
    labels = [s["section"] for s in shots]
    ok("tem começo/desenvolvimento/fim", len(set(labels)) >= 3, ", ".join(dict.fromkeys(labels)))
    ok("drops com impacto", len(tl["drops"]) >= 1, str([d["recipe"] for d in tl["drops"]]))

    # legendas
    srt = proj.out / f"{proj.cfg['slug']}.srt"
    if srt.exists():
        txt = srt.read_text(encoding="utf-8")
        times = re.findall(r"(\d\d):(\d\d):(\d\d),(\d{3}) --> (\d\d):(\d\d):(\d\d),(\d{3})", txt)
        ts = [(int(a) * 3600 + int(b_) * 60 + int(c) + int(d) / 1000, int(e) * 3600 + int(f) * 60 + int(g) + int(h) / 1000)
              for a, b_, c, d, e, f, g, h in times]
        overl = sum(1 for x, y in zip(ts, ts[1:]) if y[0] < x[1] - 0.05)
        ok("SRT válido e sem sobreposição", ts and overl == 0, f"{len(ts)} linhas, {overl} sobreposições")
        lt = load_json(proj.work / "lyrics_timed.json")
        if lt.get("match_rate") is not None:
            ok("alinhamento letra x voz ≥ 60%", lt["match_rate"] >= 0.6, f"{lt['match_rate']:.0%}")
        else:
            ok("letra oficial fornecida (lyrics.txt)", False, "legendas vieram do Whisper: revisar português")
    else:
        ok("SRT gerado", False, "sem SRT")

    th = proj.out / f"{proj.cfg['slug']}_thumb.jpg"
    if th.exists():
        im = Image.open(th)
        ok("thumbnail 1280x720 < 2 MB", im.size == (1280, 720) and th.stat().st_size < 2 * 1024 * 1024,
           f"{im.size} {th.stat().st_size // 1024} KB")

    passed = all(x["ok"] for x in res)
    rep = dict(video=str(v), passed=passed, checks=res, blacks=blacks)
    save_json(proj.out / f"{proj.cfg['slug']}_qc.json", rep)
    for x in res:
        log(f"  {'OK ' if x['ok'] else 'FALHA'}  {x['check']:<38} {x['detail']}")
    log("QC APROVADO" if passed else "QC COM PENDÊNCIAS — corrigir antes de publicar")
    return rep
