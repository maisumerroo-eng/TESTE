"""Camada de efeitos sonoros sintetizados (100% próprios, sem licença de terceiros).

Impacto (sub boom + transiente), whoosh reverso antes dos drops, zap de glitch nas transições glitch.
Mixados BAIXO, por baixo da música, sem atrapalhar a voz; limiter final -1 dBTP.
"""
from __future__ import annotations

import numpy as np
import soundfile as sf

from .common import Project, load_json, log, run

SR = 48000


def _env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)


def boom(dur=1.4):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = 38 + 70 * np.exp(-t * 18)  # pitch drop
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.45)
    click = np.random.default_rng(1).normal(0, 1, n) * _env(n, 0.0005, 0.012)
    s = np.tanh(1.6 * sub) * 0.9 + click * 0.35
    return s


def whoosh_rev(dur=1.2):
    n = int(SR * dur)
    noise = np.random.default_rng(2).normal(0, 1, n)
    # filtro passa-banda que sobe (aprox. com média móvel variável)
    out = np.zeros(n)
    acc = 0.0
    for i in range(n):
        k = 0.02 + 0.5 * (i / n) ** 2
        acc += k * (noise[i] - acc)
        out[i] = acc
    out *= np.linspace(0, 1, n) ** 2.5
    return out / (np.abs(out).max() + 1e-9)


def zap(dur=0.18):
    n = int(SR * dur)
    t = np.arange(n) / SR
    sq = np.sign(np.sin(2 * np.pi * (900 - 3000 * t) * t))
    return sq * _env(n, 0.001, 0.05) * 0.5


def build(proj: Project, level_db=-11.0) -> "Path":
    tl = load_json(proj.work / "timeline.json")
    master = proj.work / "audio_master.wav"
    dur = tl["duration"]
    n = int(dur * SR) + SR
    lay = np.zeros(n)

    def add(sig, t, g=1.0):
        i = int(t * SR)
        if i < 0:
            sig, i = sig[-i:], 0
        j = min(n, i + len(sig))
        lay[i:j] += sig[: j - i] * g

    b, w, z = boom(), whoosh_rev(), zap()
    for d in tl["drops"]:
        add(w, d["time"] - len(w) / SR, 0.55)
        add(b, d["time"], 1.0)
    for t in tl["events"].get("glitch", [])[:40]:
        add(z, t, 0.4)
    lay = lay / (np.abs(lay).max() + 1e-9) * 10 ** (level_db / 20)
    sfx_path = proj.path("work", "sfx_layer.wav")
    sf.write(str(sfx_path), np.stack([lay, lay], 1).astype(np.float32), SR, subtype="FLOAT")
    out = proj.path("work", "audio_final.wav")
    run(["ffmpeg", "-y", "-hide_banner", "-i", str(master), "-i", str(sfx_path), "-filter_complex",
         "[0:a][1:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.87:attack=3:release=60:level=false",
         "-ar", "48000", "-c:a", "pcm_s24le", str(out)])
    log(f"sfx: {len(tl['drops'])} impactos + {min(40, len(tl['events'].get('glitch', [])))} zaps -> {out.name}")
    return out
