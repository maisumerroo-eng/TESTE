"""Transcrição + alinhamento palavra a palavra.

- Whisper (faster-whisper) com timestamps por palavra, rodando na voz isolada (Demucs).
- Se existir input/lyrics.txt (letra oficial), o TEXTO vem da letra e o TEMPO vem do Whisper
  (alinhamento por sequência). Isso garante legendas sem erro de português.
- Marque palavras de destaque na letra com *asteriscos*: *Sharingan*.
"""
from __future__ import annotations

import difflib
import re
import unicodedata

from .common import Project, log, save_json, load_json


def _norm(w: str) -> str:
    w = unicodedata.normalize("NFKD", w.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", w)


def transcribe(proj: Project, audio_path, model_size: str = "small") -> list[dict]:
    from faster_whisper import WhisperModel

    char = proj.char
    extra = proj.cfg.get("whisper_prompt", "")
    prompt = (f"Rap em português sobre {char['name']} de {char['anime']}. " +
              ", ".join(char.get("keywords", [])[:12]) + (". " + extra if extra else ""))
    log(f"whisper '{model_size}' transcrevendo (CPU int8)...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    import librosa
    audio, _ = librosa.load(str(audio_path), sr=16000, mono=True)  # evita dependência do PyAV
    segs, info = model.transcribe(audio, language=proj.cfg.get("language", "pt"), word_timestamps=True,
                                  vad_filter=True, initial_prompt=prompt, beam_size=5,
                                  condition_on_previous_text=False)
    words = []
    for s in segs:
        for w in s.words or []:
            t = w.word.strip()
            if t:
                words.append(dict(w=t, start=round(w.start, 3), end=round(w.end, 3), p=round(w.probability, 3)))
    save_json(proj.path("work", "whisper_words.json"), words)
    log(f"whisper: {len(words)} palavras")
    return words


def fix_starts(words):
    """Whisper costuma 'esticar' a 1ª palavra após uma pausa (início cedo demais).
    O fim da palavra é confiável: reconstrói o início pelo tamanho da palavra."""
    out = []
    for w in words:
        w = dict(w)
        dur = w["end"] - w["start"]
        est = 0.12 + 0.065 * len(_norm(w["w"]))
        if dur > max(0.9, est * 2.5):
            w["start"] = round(w["end"] - min(est * 1.4, 0.7), 3)
        out.append(w)
    return out


def _parse_lyrics(text: str):
    lines = []
    for raw in text.splitlines():
        raw = raw.strip()
        if not raw or (raw.startswith("[") and raw.endswith("]")):  # ignora [Refrão] etc.
            continue
        toks = []
        for tok in raw.split():
            key = tok.startswith("*") and tok.rstrip(".,!?;:").endswith("*")
            clean = tok.replace("*", "")
            toks.append(dict(w=clean, key=key))
        lines.append(toks)
    return lines


def align(lyric_lines, words):
    """Alinhamento global (Needleman-Wunsch) tolerante a erros de grafia do Whisper
    ('chabingan' ~ 'Sharingan'); só palavras com similaridade alta herdam o tempo."""
    flat = [t for line in lyric_lines for t in line]
    a = [_norm(t["w"]) for t in flat]
    b = [_norm(w["w"]) for w in words]
    n, m = len(a), len(b)
    sim = lambda x, y: difflib.SequenceMatcher(None, x, y).ratio() if x and y else 0.0
    G = -0.55
    S = [[0.0] * (m + 1) for _ in range(n + 1)]
    P = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        S[i][0], P[i][0] = G * i, 1
    for j in range(1, m + 1):
        S[0][j], P[0][j] = G * j, 2
    for i in range(1, n + 1):
        ai = a[i - 1]
        for j in range(1, m + 1):
            r = sim(ai, b[j - 1])
            d = S[i - 1][j - 1] + (2 * r if r >= 0.5 else -1.0)
            u = S[i - 1][j] + G
            l = S[i][j - 1] + G
            if d >= u and d >= l:
                S[i][j], P[i][j] = d, 0
            elif u >= l:
                S[i][j], P[i][j] = u, 1
            else:
                S[i][j], P[i][j] = l, 2
    times = [None] * n
    i, j = n, m
    while i > 0 and j > 0:
        if P[i][j] == 0:
            if sim(a[i - 1], b[j - 1]) >= 0.5:
                times[i - 1] = (words[j - 1]["start"], words[j - 1]["end"])
            i, j = i - 1, j - 1
        elif P[i][j] == 1:
            i -= 1
        else:
            j -= 1
    # interpola buracos
    known = [i for i, t in enumerate(times) if t]
    matched = sum(1 for t in times if t)
    if not known:
        raise RuntimeError("Não foi possível alinhar a letra com o áudio.")
    line_of = [li for li, line in enumerate(lyric_lines) for _ in line]
    for i in range(len(times)):
        if times[i]:
            continue
        prev = max([k for k in known if k < i], default=None)
        nxt = min([k for k in known if k > i], default=None)
        same_prev = prev is not None and line_of[prev] == line_of[i]
        same_next = nxt is not None and line_of[nxt] == line_of[i]
        if same_next and not same_prev or prev is None:
            # cola antes da próxima palavra conhecida (mesma linha)
            k = nxt - i
            e = times[nxt][0] - 0.28 * (k - 1)
            times[i] = (e - 0.28, e - 0.02)
        elif same_prev and not same_next or nxt is None:
            k = i - prev
            st = times[prev][1] + 0.28 * (k - 1)
            times[i] = (st + 0.02, st + 0.28)
        else:
            t0, t1 = times[prev][1], times[nxt][0]
            span = nxt - prev
            times[i] = (t0 + (t1 - t0) * (i - prev - 1) / span, t0 + (t1 - t0) * (i - prev) / span)
    for t, tm in zip(flat, times):
        t["start"], t["end"] = round(tm[0], 3), round(max(tm[1], tm[0] + 0.08), 3)
    return lyric_lines, matched / max(1, len(flat))


def _repair(lines):
    """Linhas 'espremidas' (voz baixa que o Whisper perdeu) são redistribuídas no vão entre as linhas boas,
    e nenhuma linha começa antes da anterior terminar."""
    def dur(l):
        return l[-1]["end"] - l[0]["start"]
    bad = [len(l) > 0 and dur(l) < 0.12 * len(l) for l in lines]
    i = 0
    while i < len(lines):
        if not bad[i]:
            i += 1
            continue
        j = i
        while j < len(lines) and bad[j]:
            j += 1
        prev_end = lines[i - 1][-1]["end"] + 0.1 if i > 0 else max(0.0, lines[i][0]["start"] - 2)
        next_start = lines[j][0]["start"] - 0.1 if j < len(lines) else prev_end + 2.0 * (j - i)
        if next_start - prev_end < 0.4 * (j - i):  # sem vão: divide o espaço da próxima linha boa
            next_start = prev_end + 0.9 * (j - i)
        total = sum(len(lines[k]) for k in range(i, j))
        t = prev_end
        span = next_start - prev_end
        for k in range(i, j):
            seg = span * len(lines[k]) / total
            n = len(lines[k])
            for m, w in enumerate(lines[k]):
                w["start"] = round(t + seg * m / n, 3)
                w["end"] = round(t + seg * (m + 0.9) / n, 3)
            t += seg
        i = j
    for k in range(1, len(lines)):
        a, b = lines[k - 1], lines[k]
        if b[0]["start"] < a[-1]["end"] - 0.02:
            lim = b[0]["start"] - 0.02
            s0 = a[0]["start"]
            if lim - s0 > 0.2 * len(a):
                f = (lim - s0) / max(0.01, a[-1]["end"] - s0)
                for w in a:
                    w["start"] = round(s0 + (w["start"] - s0) * f, 3)
                    w["end"] = round(s0 + (w["end"] - s0) * f, 3)
            else:
                sh = a[-1]["end"] + 0.02 - b[0]["start"]
                for w in b:
                    w["start"] = round(w["start"] + sh, 3)
                    w["end"] = round(w["end"] + sh, 3)
    return lines


def _tighten(lines, max_gap=1.0):
    """Palavras de uma mesma linha são cantadas em sequência: se a 1ª ficou isolada longe da 2ª,
    ela é puxada para perto da 2ª (erro típico de timestamp após pausa)."""
    for line in lines:
        if len(line) < 2:
            continue
        a, b = line[0], line[1]
        if b["start"] - a["end"] > max_gap:
            est = 0.12 + 0.065 * len(_norm(a["w"]))
            a["end"] = round(b["start"] - 0.02, 3)
            a["start"] = round(a["end"] - est, 3)
    return lines


def _lines_from_whisper(words, max_words=6, gap=0.6):
    lines, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or w["start"] - cur[-1]["end"] > gap or cur[-1]["w"][-1:] in ".!?"):
            lines.append(cur)
            cur = []
        cur.append(dict(w=w["w"], start=w["start"], end=w["end"], key=False))
    if cur:
        lines.append(cur)
    return lines


def _auto_keys(lines, keywords):
    kw = {_norm(k) for k in keywords for k in k.split()}
    for line in lines:
        for t in line:
            n = _norm(t["w"])
            if n in kw or (t["w"].isupper() and len(t["w"]) > 2):
                t["key"] = True
        # garante pelo menos um destaque por linha longa: a palavra mais longa
        if len(line) >= 4 and not any(t["key"] for t in line):
            max(line, key=lambda t: len(_norm(t["w"])))["key"] = True
    return lines


def build(proj: Project, model_size: str = "small", use_stems: bool = True) -> dict:
    audio = proj.song
    if use_stems:
        try:
            from .mastering import separate_vocals
            audio = separate_vocals(proj)["vocals"]
        except Exception as e:  # segue com a mix completa
            log(f"aviso: separação de voz falhou ({e}); usando mix completa")
    wpath = proj.work / "whisper_words.json"
    words = fix_starts(load_json(wpath) if wpath.exists() else transcribe(proj, audio, model_size))

    lyr = proj.input / "lyrics.txt"
    if lyr.exists():
        lines, rate = align(_parse_lyrics(lyr.read_text(encoding="utf-8")), words)
        log(f"letra oficial alinhada: {rate:.0%} das palavras casaram com o Whisper")
        source = "lyrics.txt"
    else:
        lines = _lines_from_whisper(words)
        rate = None
        source = "whisper"
        log("sem lyrics.txt: legendas a partir do Whisper — REVISE work/lyrics_draft.txt")
        (proj.work / "lyrics_draft.txt").write_text("\n".join(" ".join(t["w"] for t in l) for l in lines), encoding="utf-8")
    lines = _repair(_tighten(lines))
    # ajuste fino do diretor: project.yaml -> lyric_timing: {"começo da linha": [inicio, fim]}
    for prefix, (a, z) in (proj.cfg.get("lyric_timing") or {}).items():
        npre = _norm(prefix)
        for line in sorted(lines, key=lambda l: abs(l[0]["start"] - a)):  # ocorrência mais perto do tempo dado
            if "".join(_norm(t["w"]) for t in line).startswith(npre.replace(" ", "")):
                n = len(line)
                for m, t in enumerate(line):
                    t["start"] = round(a + (z - a) * m / n, 3)
                    t["end"] = round(a + (z - a) * (m + 0.9) / n, 3)
                break
    lines = _auto_keys(lines, proj.char.get("keywords", []))
    out = dict(source=source, match_rate=rate,
               lines=[dict(start=l[0]["start"], end=l[-1]["end"], words=l) for l in lines if l])
    save_json(proj.path("work", "lyrics_timed.json"), out)
    return out
