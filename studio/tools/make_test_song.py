#!/usr/bin/env python3
"""Gera uma música de TESTE (beat sintético 90 BPM + voz robótica espeak) para validar a pipeline
sem material de terceiros. Uso: python3 tools/make_test_song.py saida_dir/"""
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

SR = 48000
BPM = 90
BEAT = 60 / BPM
BAR = BEAT * 4
LEAD = 1.0  # silêncio inicial proposital (testa remoção de espaço morto)

LYRICS = """[Verso]
Eu perdi meu clã numa noite sem lua
O *Sharingan* desperta e a raiva continua
Meu irmão me deixou com o ódio na mão
Cada passo que eu dou é *vingança* no chão
[Pré-refrão]
Sinto o *Chidori* rasgando o céu
[Refrão]
Eu sou o último *Uchiha*
Olhos de sangue na escuridão
Eu sou o último *Uchiha*
*Raio* na palma da minha mão
[Ponte]
Itachi, por que você mentiu
[Refrão]
Eu sou o último *Uchiha*
Olhos de sangue na escuridão
Eu sou o último *Uchiha*
*Raio* na palma da minha mão
"""

# (seção, compassos)
FORM = [("intro", 4), ("verse", 8), ("pre", 2), ("chorus", 8), ("break", 4), ("chorus", 8), ("outro", 4)]


def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)


def kick():
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.16)


def snare():
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    return (np.random.default_rng(1).normal(0, 0.6, n) * env(n, 0.001, 0.07)
            + np.sin(2 * np.pi * 190 * t) * env(n, 0.001, 0.05) * 0.6)


def hat():
    n = int(0.06 * SR)
    x = np.random.default_rng(2).normal(0, 1, n)
    x = np.diff(np.concatenate([[0], x]))
    return x * env(n, 0.0005, 0.015) * 0.35


def bass(freq, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return np.tanh(2 * np.sin(2 * np.pi * freq * t)) * env(n, 0.005, dur * 0.7) * 0.5


def pad(freqs, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * f * t + i) for i, f in enumerate(freqs)) / len(freqs)
    a = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.6)
    return s * a * 0.22


def lead(freq, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    saw = 2 * ((freq * t) % 1) - 1
    return saw * env(n, 0.01, dur * 0.5) * 0.12


def tts(text, path):
    subprocess.run(["espeak-ng", "-v", "pt-br", "-s", "165", "-p", "35", "-w", str(path), text], check=True)
    y, sr = sf.read(path)
    if sr != SR:
        idx = np.linspace(0, len(y) - 1, int(len(y) * SR / sr))
        y = np.interp(idx, np.arange(len(y)), y)
    return y


def main(out_dir):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    total_bars = sum(b for _, b in FORM)
    n = int((LEAD + total_bars * BAR + 3.0) * SR)
    mix = np.zeros(n)
    voc = np.zeros(n)

    def add(buf, sig, t, g=1.0):
        i = int(t * SR)
        j = min(len(buf), i + len(sig))
        buf[i:j] += sig[: j - i] * g

    K, S, Hh = kick(), snare(), hat()
    roots = [55.0, 55.0, 43.65, 49.0]  # A1 A1 F1 G1
    t = LEAD
    sections = []
    for name, bars in FORM:
        sections.append((name, t, t + bars * BAR))
        for b in range(bars):
            bt = t + b * BAR
            r = roots[b % 4]
            last_pre_beat = name == "pre" and b == bars - 1
            if name in ("intro", "break", "outro"):
                add(mix, pad([r * 4, r * 4 * 1.189, r * 4 * 1.498], BAR), bt)
                for k in range(8):
                    add(mix, Hh, bt + k * BEAT / 2, 0.4)
                if name == "outro" and b < 2:
                    add(mix, K, bt, 0.6)
                continue
            for k in range(4):
                if last_pre_beat and k == 3:
                    continue  # respiro antes do drop
                if k in (0, 2) or (name == "chorus" and k == 3 and b % 2):
                    add(mix, K, bt + k * BEAT, 1.0)
                if k in (1, 3):
                    add(mix, S, bt + k * BEAT, 0.8)
            sub = 4 if name == "chorus" else 2
            for k in range(4 * sub):
                if last_pre_beat and k >= 3 * sub:
                    continue
                add(mix, Hh, bt + k * BEAT / sub, 0.5 if k % 2 == 0 else 0.3)
            add(mix, bass(r, BAR * 0.95 if not last_pre_beat else BEAT * 3), bt, 0.9 if name == "chorus" else 0.7)
            if name == "chorus":
                for k, m in enumerate([4, 4.75, 6, 4.75]):
                    add(mix, lead(r * m, BEAT * 0.9), bt + k * BEAT, 1.0)
            if name == "pre":  # riser
                nn = int(BAR * SR)
                rz = np.random.default_rng(b).normal(0, 1, nn) * np.linspace(0, 1, nn) ** 2 * 0.15
                add(mix, rz, bt)
        t += bars * BAR

    # voz: cada linha começa no compasso (2 compassos por linha)
    lines = [l for l in LYRICS.splitlines() if l.strip() and not l.startswith("[")]
    sec_lines = {"verse": lines[0:4], "pre": lines[4:5], "chorus": lines[5:9], "break": lines[9:10]}
    used_chorus = 0
    with tempfile.TemporaryDirectory() as td:
        for name, a, z in sections:
            if name == "chorus":
                ls = lines[5:9] if used_chorus == 0 else lines[10:14]
                used_chorus += 1
            else:
                ls = sec_lines.get(name, [])
            for k, ln in enumerate(ls):
                y = tts(ln.replace("*", ""), Path(td) / f"l{k}.wav")
                add(voc, y, a + k * 2 * BAR + 0.05, 0.9)
    mix = mix / np.abs(mix).max() * 0.6 + voc / (np.abs(voc).max() + 1e-9) * 0.55
    mix = np.tanh(mix * 1.2) * 0.8
    stereo = np.stack([mix, mix * 0.98], 1)
    sf.write(out / "teste_sasuke.wav", stereo, SR, subtype="PCM_24")
    (out / "teste_sasuke_lyrics.txt").write_text(LYRICS, encoding="utf-8")
    print(f"ok: {out / 'teste_sasuke.wav'} ({len(mix) / SR:.1f}s) seções: " +
          ", ".join(f"{s}@{a:.1f}" for s, a, _ in sections))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "test_media")
