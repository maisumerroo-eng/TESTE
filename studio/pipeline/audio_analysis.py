"""Análise musical: BPM, batidas, compassos, kick/snare/hats, energia, seções, drops e silêncios.

Saída: work/analysis.json — é o "mapa" que o planner usa para sincronizar cortes e efeitos.
"""
from __future__ import annotations

import numpy as np
import librosa
import scipy.signal as sps

from .common import Project, log, save_json

SR = 22050
HOP = 512


def _band_onsets(S: np.ndarray, freqs: np.ndarray, lo: float, hi: float, sr: int, delta: float):
    band = S[(freqs >= lo) & (freqs < hi)]
    env = librosa.onset.onset_strength(S=librosa.amplitude_to_db(band, ref=np.max), sr=sr, hop_length=HOP)
    env = env / (env.max() + 1e-9)
    frames = librosa.onset.onset_detect(onset_envelope=env, sr=sr, hop_length=HOP, delta=delta, backtrack=False)
    times = librosa.frames_to_time(frames, sr=sr, hop_length=HOP)
    strength = env[frames]
    return env, [(round(float(t), 3), round(float(s), 3)) for t, s in zip(times, strength)]


def _smooth(x: np.ndarray, n: int) -> np.ndarray:
    if n <= 1:
        return x
    k = np.hanning(n)
    k /= k.sum()
    return np.convolve(x, k, mode="same")


def _bar_features(y, sr, bars, duration):
    """Vetor por compasso: energia total/grave/médio/agudo, densidade de ataques e harmonia."""
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=HOP))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
    t = librosa.frames_to_time(np.arange(S.shape[1]), sr=sr, hop_length=HOP)
    bands = [(20, 150), (150, 2000), (2000, 6000), (6000, 11000)]
    bandE = [np.log1p(S[(freqs >= lo) & (freqs < hi)].sum(0)) for lo, hi in bands]
    onset = librosa.onset.onset_strength(S=librosa.amplitude_to_db(S), sr=sr, hop_length=HOP)
    chroma = librosa.feature.chroma_stft(S=S ** 2, sr=sr, hop_length=HOP)
    edges = list(bars) + [duration]
    F = []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (t >= a) & (t < b)
        if not m.any():
            m = np.zeros_like(t, bool); m[np.argmin(np.abs(t - a))] = True
        F.append([be[m].mean() for be in bandE] + [onset[m].mean()] + list(chroma[:, m].mean(1) * 0.6))
    F = np.array(F)
    Z = (F - F.mean(0)) / (F.std(0) + 1e-6)
    return Z, F


def _repetition_bounds(Z, idx, n):
    """Acha repetições do trecho mais intenso (refrão) via matriz de auto-similaridade por compasso
    e adiciona as fronteiras dessas repetições."""
    inten = Z[:, :5].mean(1)
    segs = list(zip(idx[:-1], idx[1:]))
    a, b = max(segs, key=lambda ab: inten[ab[0]:ab[1]].mean() if ab[1] - ab[0] >= 4 else -9)
    L = b - a
    if L < 4 or L > n // 2:
        return idx
    Zn = Z / (np.linalg.norm(Z, axis=1, keepdims=True) + 1e-9)
    ssm = Zn @ Zn.T
    score = np.full(n, -1.0)
    for j in range(0, n - L + 1):
        if abs(j - a) < L:
            continue
        score[j] = float(np.mean([ssm[a + k, j + k] for k in range(L)]))
    new = set(idx)
    for j in np.argsort(-score):
        if score[j] < 0.55:
            break
        if all(abs(j - x) >= 2 or x in (0, n) for x in new if x not in idx) and not any(
                j < x < j + L for x in new if x not in idx):
            new.update([int(j), int(min(n, j + L))])
    # remove fronteiras originais que caem dentro de um refrão detectado (exceto bordas)
    return sorted(new)


def _sections(y, sr, bars, duration, energy_t, energy):
    if len(bars) < 8:
        return [dict(start=0.0, end=round(duration, 3), label="verse", energy=1.0)]
    Z, F = _bar_features(y, sr, bars, duration)
    n = len(bars)
    wdw = 4 if n >= 24 else 2  # frases de 4 compassos
    nov = np.zeros(n)
    for i in range(2, n - 1):
        a0 = max(0, i - wdw)
        nov[i] = np.linalg.norm(Z[i:i + wdw].mean(0) - Z[a0:i].mean(0)) * min(1.0, (i - a0) / wdw) ** 0.5
    thr = nov[nov > 0].mean() + 0.35 * nov[nov > 0].std()
    cands = [i for i in range(2, n - 1) if nov[i] >= thr and nov[i] == nov[max(0, i - 2):i + 3].max()]
    # separação mínima de 2 compassos; prioriza novidade alta
    chosen = []
    for i in sorted(cands, key=lambda i: -nov[i]):
        if all(abs(i - j) >= 2 for j in chosen):
            chosen.append(i)
    idx = [0] + sorted(chosen) + [n]
    idx = _repetition_bounds(Z, idx, n)
    secs = []
    inten = Z[:, :5].mean(1)  # intensidade = camadas/densidade (grave, médio, agudo, ataques)
    for a, b in zip(idx[:-1], idx[1:]):
        st = 0.0 if a == 0 else bars[a]
        en = duration if b == n else bars[b]
        m = (energy_t >= st) & (energy_t < en)
        secs.append(dict(start=round(float(st), 3), end=round(float(en), 3), bars=b - a,
                         energy=round(float(energy[m].mean()) if m.any() else 0.0, 3),
                         intensity=float(inten[a:b].mean())))
    iv = np.array([s["intensity"] for s in secs])
    lo, hi = iv.min(), iv.max() + 1e-6
    for k, s in enumerate(secs):
        rel = (s.pop("intensity") - lo) / (hi - lo)
        s["intensity"] = round(float(rel), 3)
        s["label"] = "chorus" if rel >= 0.78 else ("break" if rel < 0.3 else "verse")
    if secs[0]["intensity"] < 0.5:
        secs[0]["label"] = "intro"
    if len(secs) > 2 and secs[-1]["intensity"] < 0.5:
        secs[-1]["label"] = "outro"
    for k in range(len(secs) - 1):
        if secs[k + 1]["label"] == "chorus" and secs[k]["label"] in ("verse", "chorus") and secs[k]["bars"] <= 4 \
                and secs[k + 1]["bars"] >= 4 and k > 0:
            secs[k]["label"] = "pre-chorus"
    # funde vizinhos com mesmo rótulo
    merged = [secs[0]]
    for s in secs[1:]:
        if s["label"] == merged[-1]["label"]:
            m = merged[-1]
            for key in ("energy", "intensity"):
                m[key] = round((m[key] * m["bars"] + s[key] * s["bars"]) / (m["bars"] + s["bars"]), 3)
            m["end"], m["bars"] = s["end"], m["bars"] + s["bars"]
        else:
            merged.append(s)
    return merged


def _drops(energy_t, energy, bars, kick, sections):
    """Drop = entrada de refrão (ou salto grande de energia) num downbeat, travado no kick mais próximo."""
    def e_at(a, b):
        m = (energy_t >= a) & (energy_t < b)
        return float(energy[m].mean()) if m.any() else 0.0
    kick_t = np.array([k[0] for k in kick]) if kick else np.array([])
    bar = float(np.median(np.diff(bars))) if len(bars) > 1 else 2.0
    drops = []
    for k, s in enumerate(sections[1:], 1):
        t = s["start"]
        before, after = e_at(t - bar, t - 0.03), e_at(t, t + bar)
        dip = e_at(t - bar / 4, t - 0.02)
        jump = after - before
        if s["label"] == "chorus" or jump > 0.22:
            near = kick_t[np.abs(kick_t - t) < 0.15] if len(kick_t) else []
            hit = float(near[np.argmin(np.abs(near - t))]) if len(near) else t
            drops.append(dict(time=round(hit, 3), strength=round(max(jump, after - dip), 3),
                              pre_gap=bool(dip < before * 0.8), section=s["label"]))
    return drops


def _silences(rms_db, t, thresh_db=-38.0, min_len=0.35):
    quiet = rms_db < thresh_db
    out, start = [], None
    for i, q in enumerate(quiet):
        if q and start is None:
            start = t[i]
        elif not q and start is not None:
            if t[i] - start >= min_len:
                out.append(dict(start=round(float(start), 3), end=round(float(t[i]), 3)))
            start = None
    if start is not None and t[-1] - start >= min_len:
        out.append(dict(start=round(float(start), 3), end=round(float(t[-1]), 3)))
    return out


def analyze(proj: Project, audio_path=None) -> dict:
    m = proj.work / "audio_master.wav"
    path = audio_path or (m if m.exists() else proj.song)
    log(f"analisando áudio: {path.name}")
    y, sr = librosa.load(str(path), sr=SR, mono=True)
    duration = len(y) / sr

    y_h, y_p = librosa.effects.hpss(y)
    tempo, beats_f = librosa.beat.beat_track(y=y_p, sr=sr, hop_length=HOP, trim=False)
    bpm = float(np.atleast_1d(tempo)[0])
    # corrige BPM de rap (geralmente 70-100 ou 140-180 metade/dobro)
    beats_t = librosa.frames_to_time(beats_f, sr=sr, hop_length=HOP)

    S = np.abs(librosa.stft(y_p, n_fft=2048, hop_length=HOP))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)
    kick_env, kick = _band_onsets(S, freqs, 25, 160, sr, 0.12)
    _, snare = _band_onsets(S, freqs, 180, 4000, sr, 0.15)
    _, hats = _band_onsets(S, freqs, 6000, 11000, sr, 0.10)

    # compasso: fase do downbeat = a que concentra mais energia de kick
    kick_at_beats = kick_env[np.clip(beats_f, 0, len(kick_env) - 1)] if len(beats_f) else np.array([])
    phase = 0
    if len(kick_at_beats) >= 8:
        # kick costuma cair no 1 e no 3 (ambíguo); a novidade (mudança de seção) desempata, pois
        # seções começam no tempo 1 do compasso
        kscore = np.array([kick_at_beats[p::4].mean() for p in range(4)])
        mf = librosa.util.sync(librosa.feature.mfcc(y=y, sr=sr, hop_length=HOP, n_mfcc=13), beats_f, pad=False)
        mf = (mf - mf.mean(1, keepdims=True)) / (mf.std(1, keepdims=True) + 1e-6)
        nb = mf.shape[1]
        nov = np.zeros(nb)
        for i in range(4, nb - 4):
            nov[i] = np.linalg.norm(mf[:, i:i + 4].mean(1) - mf[:, i - 4:i].mean(1))
        top = nov >= np.quantile(nov, 0.9)
        nscore = np.array([(nov[p::4] * top[p::4]).sum() for p in range(4)])
        score = kscore / (kscore.max() + 1e-9) + 1.5 * nscore / (nscore.max() + 1e-9)
        phase = int(np.argmax(score))
    bars = [round(float(t), 3) for t in beats_t[phase::4]]

    # energia (RMS) suavizada e normalizada 0..1, 10 Hz
    rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=HOP)[0]
    rms_t = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=HOP)
    rms_db = librosa.amplitude_to_db(rms, ref=np.max)
    env = _smooth(rms, int(sr / HOP * 0.5))
    lo, hi = np.percentile(env, 3), np.percentile(env, 98)
    env = np.clip((env - lo) / (hi - lo + 1e-9), 0, 1)
    grid = np.arange(0, duration, 0.1)
    energy = np.interp(grid, rms_t, env)

    sections = _sections(y, sr, bars, duration, grid, energy)
    drops = _drops(grid, energy, bars, kick, sections)
    silences = _silences(rms_db, rms_t)

    # brilho espectral (bom p/ variar intensidade de efeitos)
    cent = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=HOP)[0]
    cent = np.interp(grid, rms_t, _smooth(cent, 20)) / (sr / 2)

    data = dict(
        file=str(path.name), duration=round(duration, 3), bpm=round(bpm, 2),
        beat_period=round(60.0 / bpm, 4) if bpm else 0.5,
        beats=[round(float(t), 3) for t in beats_t], downbeat_phase=phase, bars=bars,
        kick=kick, snare=snare, hats=hats,
        energy=dict(step=0.1, values=[round(float(v), 3) for v in energy]),
        brightness=[round(float(v), 3) for v in cent],
        sections=sections, drops=drops, silences=silences,
    )
    save_json(proj.path("work", "analysis.json"), data)
    log(f"BPM {bpm:.1f} | {len(beats_t)} batidas | {len(bars)} compassos | kicks {len(kick)} | "
        f"snares {len(snare)} | {len(sections)} seções | {len(drops)} drops | {len(silences)} silêncios")
    for s in sections:
        log(f"  {s['start']:7.2f}-{s['end']:7.2f}  {s['label']:<10} energia {s['energy']:.2f}")
    for d in drops:
        log(f"  DROP @ {d['time']:.2f}s força {d['strength']:.2f} {'(com respiro antes)' if d['pre_gap'] else ''}")
    return data
