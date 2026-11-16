"""Tratamento de áudio que PRESERVA a voz original.

Regras: nada de pitch shift, troca de voz ou reconstrução. Só correção técnica:
high-pass, limpeza de lama, de-esser, compressão leve, controle de pico e loudness
-14 LUFS / -1 dBTP (padrão YouTube) em 2 passadas, 48 kHz.
"""
from __future__ import annotations

import json
import re

import numpy as np
import soundfile as sf
import pyloudnorm as pyln

from .common import Project, brand, log, run, save_json


def measure(path) -> dict:
    data, sr = sf.read(str(path), always_2d=True)
    meter = pyln.Meter(sr)
    lufs = meter.integrated_loudness(data)
    peak = float(np.max(np.abs(data)))
    clip = int(np.sum(np.abs(data) >= 0.999))
    # piso de ruído: percentil 5 do RMS em janelas de 50 ms
    mono = data.mean(axis=1)
    win = int(sr * 0.05)
    n = len(mono) // win
    rms = np.sqrt((mono[: n * win].reshape(n, win) ** 2).mean(axis=1) + 1e-12)
    floor_db = float(20 * np.log10(np.percentile(rms, 5) + 1e-12))
    return dict(lufs=round(float(lufs), 2), peak_dbfs=round(float(20 * np.log10(peak + 1e-12)), 2),
                clipped_samples=clip, noise_floor_db=round(floor_db, 1), sr=sr, channels=data.shape[1])


def dead_air(src, lead_keep=0.12, tail_keep=1.0):
    """Silêncio desnecessário no começo/fim (não mexe em pausas internas, que são dramáticas)."""
    res = run(["ffmpeg", "-hide_banner", "-i", str(src), "-af", "silencedetect=n=-50dB:d=0.3", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", res.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", res.stderr)]
    from .common import media_duration
    dur = media_duration(src)
    t0, t1 = 0.0, None
    if starts and starts[0] <= 0.01 and ends:
        t0 = max(0.0, ends[0] - lead_keep)
    if starts and (len(ends) < len(starts) or ends[-1] >= dur - 0.05) and starts[-1] > t0 + 5:
        if dur - starts[-1] > tail_keep + 0.3:
            t1 = starts[-1] + tail_keep
    return t0, t1


def _loudnorm_pass1(src, chain, target, tp, lra) -> dict:
    res = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-af",
               f"{chain},loudnorm=I={target}:TP={tp}:LRA={lra}:print_format=json", "-f", "null", "-"])
    txt = res.stderr
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", txt, re.S)
    return json.loads(m.group(0))


def master(proj: Project) -> dict:
    b = brand()["audio"]
    src = proj.song
    before = measure(src)
    log(f"antes: {before}")

    chain = [f"highpass=f={b['highpass_hz']}:poles=2"]
    if before["clipped_samples"] > 50:
        chain.append("adeclip")  # reconstrói picos clipados
    denoise = b.get("denoise", "auto")
    if denoise is True or (denoise == "auto" and before["noise_floor_db"] > -55):
        chain.append("afftdn=nr=8:nf=-50:tn=1")  # leve, só se o piso de ruído for alto
    chain += [
        "equalizer=f=250:t=q:w=1.2:g=-1.5",     # tira lama
        "equalizer=f=3200:t=q:w=1.0:g=1.2",      # presença/clareza vocal
        "equalizer=f=55:t=q:w=0.9:g=1.0",        # corpo do 808 sem embolar
    ]
    if b.get("deesser", True):
        chain.append("deesser=i=0.35:m=0.5:f=0.5:s=o")
    chain.append("acompressor=threshold=-18dB:ratio=2:attack=15:release=180:makeup=1")
    pre = ",".join(chain)

    t, tp, lra = b["target_lufs"], b["true_peak"], b.get("lra_max", 9)
    p1 = _loudnorm_pass1(src, pre, t, tp, lra)
    ln = (f"loudnorm=I={t}:TP={tp}:LRA={lra}:measured_I={p1['input_i']}:measured_TP={p1['input_tp']}"
          f":measured_LRA={p1['input_lra']}:measured_thresh={p1['input_thresh']}:offset={p1['target_offset']}"
          f":linear=true")
    full = f"{pre},{ln},alimiter=limit={10 ** ((tp - 0.2) / 20):.4f}:attack=3:release=50:level=false,aresample=48000"
    out = proj.path("work", "audio_master.wav")
    t0, t1 = dead_air(src)
    trim = []
    if t0 > 0:
        trim += ["-ss", f"{t0:.3f}"]
    if t1:
        trim += ["-to", f"{t1:.3f}"]
        full += f",afade=t=out:st={max(0, t1 - t0 - 0.8):.3f}:d=0.8"
    if t0 or t1:
        log(f"espaço morto removido: início {t0:.2f}s" + (f", fim após {t1:.2f}s" if t1 else ""))
    run(["ffmpeg", "-y", "-hide_banner", *trim, "-i", str(src), "-af", full, "-ar", "48000", "-c:a", "pcm_s24le", str(out)])
    proj.cfg["audio_trim"] = dict(start=round(t0, 3), end=round(t1, 3) if t1 else None)
    proj.save()
    after = measure(out)
    log(f"depois: {after}")
    report = dict(before=before, after=after, chain=full)
    save_json(proj.path("work", "audio_report.json"), report)
    return report


def separate_vocals(proj: Project) -> dict:
    """Demucs (htdemucs) -> vocals.wav e instrumental. Usado p/ transcrição e detecção de voz.
    NÃO entra no master final (a música original é a referência)."""
    out_dir = proj.work / "stems"
    if (out_dir / "vocals.wav").exists():
        return dict(vocals=out_dir / "vocals.wav", no_vocals=out_dir / "no_vocals.wav")
    log("separando voz com Demucs (CPU, pode levar alguns minutos)...")
    tmp = proj.work / "demucs"
    src = proj.work / "audio_master.wav"
    src = src if src.exists() else proj.song
    run(["python3", "-m", "demucs", "--two-stems", "vocals", "-n", "htdemucs", "-o", str(tmp), str(src)])
    found = list(tmp.rglob("vocals.wav"))
    if not found:
        raise RuntimeError("Demucs não gerou vocals.wav")
    out_dir.mkdir(parents=True, exist_ok=True)
    found[0].replace(out_dir / "vocals.wav")
    found[0].with_name("no_vocals.wav").replace(out_dir / "no_vocals.wav")
    return dict(vocals=out_dir / "vocals.wav", no_vocals=out_dir / "no_vocals.wav")
