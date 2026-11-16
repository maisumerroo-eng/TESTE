"""Legendas dinâmicas (ASS/libass) + SRT limpo.

Estilo KAGERIMA:
- palavras aparecem quando são cantadas (pop de escala + fade);
- palavras-chave na cor do personagem, maiores e com brilho;
- linha "pulsa" nos kicks;
- refrão sobe para o centro, maior; verso fica no terço inferior;
- nos drops, uma PALAVRA DE IMPACTO gigante (Anton) aparece por ~0,6 s.
"""
from __future__ import annotations

from .common import Project, brand, hex_to_ass, load_json, log

W, H = 1920, 1080


def _ts(t: float) -> str:
    t = max(0.0, t)
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def _srt_ts(t: float) -> str:
    ms = int(round(max(0.0, t) * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def _esc(s: str) -> str:
    s = s.replace("{", "(").replace("}", ")").replace("\\", "/")
    return s.replace("—", "").replace("–", "").strip("-").strip()


def _section_at(sections, t):
    for s in sections:
        if s["start"] <= t < s["end"]:
            return s["label"]
    return "verse"


def _wrap(words, max_chars=30):
    """Divide em 2 linhas visuais se ficar longa; retorna índice da quebra ou None."""
    total = sum(len(w["w"]) + 1 for w in words)
    if total <= max_chars or len(words) < 4:
        return None
    acc, best, bi = 0, 1e9, None
    for i, w in enumerate(words[:-1]):
        acc += len(w["w"]) + 1
        d = abs(acc - total / 2)
        if d < best:
            best, bi = d, i + 1
    return bi


# cor por palavra (normalizada) — a legenda vira parte do efeito
WORD_COLORS = {
    "azul": "#3FA9FF", "blue": "#3FA9FF", "vermelho": "#FF2A3A", "red": "#FF2A3A", "roxo": "#B05CFF",
    "purple": "#B05CFF", "sangue": "#E0102A", "infinito": "#7DF3FF", "limitless": "#7DF3FF",
    "olhos": "#28E6FF", "eyes": "#28E6FF", "sukuna": "#FF2A3A", "mahoraga": "#F2D27A", "dominio": "#B05CFF",
    "expansao": "#B05CFF", "vazio": "#B05CFF", "forte": "#FFFFFF", "gojo": "#7DF3FF", "satoru": "#7DF3FF",
    "fim": "#FF2A3A", "explodir": "#FF6A2A", "corte": "#FFFFFF", "geto": "#B05CFF", "toji": "#C9C9C9",
}
EXPLODE = {"explodir", "vermelho", "roxo", "azul", "forte", "fim", "sukuna", "dominio", "expansao", "corte",
           "infinito", "limitless", "mahoraga", "sangue"}


def _n(w):
    import re
    import unicodedata
    w = unicodedata.normalize("NFKD", w.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", w)


def build_ass(proj: Project, timed: dict | None = None, analysis: dict | None = None) -> tuple:
    """Legenda cinética:
    - VERSO: linha no terço inferior, palavra entra deslizando de baixo com giro leve, palavra-chave colorida
      e maior com brilho;
    - REFRÃO / energia alta: PALAVRA A PALAVRA gigante no centro (Anton), alternando tamanho e inclinação;
    - PALAVRAS DE PODER (azul, vermelho, roxo, infinito, forte...): explodem na tela com cor própria,
      separação RGB, tremida e estouro (escala + blur) ao sair; 'infinito' espalha as letras;
    - DROP: palavra gigante de impacto (mantido).
    """
    import random
    b = brand()
    c = proj.char
    rng = random.Random(proj.cfg.get("seed", 7))
    timed = timed or load_json(proj.work / "lyrics_timed.json")
    analysis = analysis or load_json(proj.work / "analysis.json")
    upper = proj.cfg.get("subtitles", {}).get("uppercase", True)
    bone = hex_to_ass(b["palette"]["bone"])
    void = hex_to_ass(b["palette"]["void"])
    prim = hex_to_ass(c["primary"])
    font, disp = b["fonts"]["lyrics"], b["fonts"]["display"]
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyric,{font},76,{bone},{bone},{void},&H96000000,-1,0,0,0,100,100,1.5,0,1,6,3,2,120,120,90,1
Style: Glow,{font},76,{prim},{prim},{prim},&H00000000,-1,0,0,0,100,100,1.5,0,1,12,0,2,120,120,90,1
Style: Big,{disp},210,{bone},{bone},{void},&H00000000,0,0,0,0,100,100,3,0,1,9,0,5,60,60,0,1
Style: Power,{disp},300,{bone},{bone},{void},&H00000000,0,0,0,0,100,100,6,0,1,10,0,5,40,40,0,1
Style: Impact,{disp},230,{bone},{bone},{prim},&H00000000,0,0,0,0,100,100,4,0,1,8,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    kicks = [k[0] for k in analysis.get("kick", []) if k[1] > 0.35]
    drops = [d["time"] for d in analysis.get("drops", [])]
    lines = timed["lines"]
    ev, srt = [], []
    U = (lambda x: x.upper()) if upper else (lambda x: x)

    def color_of(w):
        hx = WORD_COLORS.get(_n(w["w"]))
        return hex_to_ass(hx) if hx else (prim if w.get("key") else bone)

    def power_word(w, t0, t1, layer=6):
        """Palavra explodindo: entra gigante girando, treme, separação RGB e estoura ao sair."""
        txt = _esc(U(w["w"]).strip(".,!?;:"))
        if not txt:
            return
        nn = _n(w["w"])
        col = color_of(w)
        dur = max(0.45, min(1.1, t1 - t0 + 0.35))
        a, z = t0 - 0.03, t0 + dur
        ms = int(dur * 1000)
        x, y = 960 + rng.randint(-160, 160), 470 + rng.randint(-90, 60)
        rot = rng.choice([-8, -5, 5, 8])
        spread = "\\t(0,{0},\\fsp40)".format(ms) if nn in ("infinito", "limitless") else ""
        base = (f"\\pos({x},{y})\\frz{rot}\\fscx330\\fscy330\\blur6"
                f"\\t(0,110,\\fscx135\\fscy135\\blur0\\frz{rot // 2})"
                f"\\t(110,170,\\frz{-rot // 2})\\t(170,230,\\frz{rot // 3})"
                f"{spread}\\t({ms - 180},{ms},\\fscx240\\fscy240\\blur16\\alpha&HFF&)")
        # separação RGB (camadas deslocadas)
        ev.append(f"Dialogue: {layer},{_ts(a)},{_ts(z)},Power,,0,0,0,,{{{base}\\1c&HFFFF00&\\3c&HFFFF00&"
                  f"\\alpha&H50&\\pos({x - 16},{y + 4})}}{txt}")
        ev.append(f"Dialogue: {layer},{_ts(a)},{_ts(z)},Power,,0,0,0,,{{{base}\\1c&H3020FF&\\3c&H3020FF&"
                  f"\\alpha&H50&\\pos({x + 16},{y - 4})}}{txt}")
        ev.append(f"Dialogue: {layer + 1},{_ts(a)},{_ts(z)},Power,,0,0,0,,{{{base}\\1c{col}\\3c{void}}}{txt}")

    used_power = set()
    for li, line in enumerate(lines):
        words = line["words"]
        if not words:
            continue
        start = words[0]["start"] - 0.08
        nxt = lines[li + 1]["words"][0]["start"] - 0.05 if li + 1 < len(lines) and lines[li + 1]["words"] else 1e9
        end = max(min(words[-1]["end"] + 0.45, nxt), words[-1]["end"] + 0.05)
        label = _section_at(analysis["sections"], words[0]["start"])
        srt.append((words[0]["start"], min(end, words[-1]["end"] + 0.3), " ".join(w["w"] for w in words)))

        # palavras de poder explodem por cima (uma por linha, sem repetir em sequência)
        pw = [w for w in words if _n(w["w"]) in EXPLODE]
        for w in pw[:1]:
            if all(abs(w["start"] - d) > 0.6 for d in drops) and (li, _n(w["w"])) not in used_power:
                power_word(w, w["start"], w["end"])
                used_power.add((li, _n(w["w"])))

        kinetic = label in ("chorus",) or (label == "pre-chorus" and rng.random() < 0.5)
        if kinetic:
            # palavra a palavra, gigante no centro, alternando tamanho/ângulo/posição
            for i, w in enumerate(words):
                if pw and w is pw[0]:
                    continue
                t0 = w["start"] - 0.03
                t1 = words[i + 1]["start"] if i + 1 < len(words) else min(end, w["end"] + 0.35)
                t1 = max(t1, t0 + 0.12)
                sz = rng.choice([95, 110, 130, 150]) if len(w["w"]) > 3 else rng.choice([80, 95])
                rot = rng.choice([-6, -3, 0, 3, 6])
                y = rng.choice([430, 520, 610])
                kk = [k for k in kicks if t0 < k < t1]
                pulse = "".join(f"\\t({int((k - t0) * 1000)},{int((k - t0) * 1000) + 60},\\fscx{sz + 12}\\fscy{sz + 12})"
                                f"\\t({int((k - t0) * 1000) + 60},{int((k - t0) * 1000) + 200},\\fscx{sz}\\fscy{sz})"
                                for k in kk[:3])
                txt = _esc(U(w["w"]))
                ev.append(f"Dialogue: 2,{_ts(t0)},{_ts(t1)},Big,,0,0,0,,"
                          f"{{\\pos(960,{y})\\frz{rot}\\fscx{int(sz * 1.5)}\\fscy{int(sz * 1.5)}\\blur4"
                          f"\\1c{color_of(w)}\\t(0,90,\\fscx{sz}\\fscy{sz}\\blur0){pulse}}}{txt}")
            continue

        # verso: linha inferior com entrada deslizante por palavra
        brk = _wrap(words, 32)
        parts, glow = [], []
        for i, w in enumerate(words):
            t1 = int(max(0, (w["start"] - start)) * 1000)
            txt = _esc(U(w["w"]))
            key = w.get("key") or _n(w["w"]) in WORD_COLORS
            col = color_of(w)
            sc = 128 if key else 100
            tag = (f"{{\\alpha&HFF&\\1c{col}\\fscx{sc + 30}\\fscy{sc + 30}\\frz{rng.choice([-6, 6])}"
                   f"\\t({t1},{t1 + 50},\\alpha&H00&)\\t({t1},{t1 + 140},\\fscx{sc}\\fscy{sc}\\frz0)}}")
            sep = "\\N" if brk is not None and i == brk else (" " if i else "")
            parts.append(sep + tag + txt)
            gtag = (f"{{\\alpha&HFF&\\t({t1},{t1 + 50},\\alpha&H40&)}}" if key else "{\\alpha&HFF&}")
            glow.append(sep + gtag + txt)
        dur_ms = int((end - start) * 1000)
        fade = f"\\fad(60,{min(160, dur_ms // 4)})"
        move = f"\\move(960,1010,960,990,0,250)"
        ev.append(f"Dialogue: 0,{_ts(start)},{_ts(end)},Glow,,0,0,0,,{{\\blur10{fade}{move}\\an2}}" + "".join(glow))
        ev.append(f"Dialogue: 1,{_ts(start)},{_ts(end)},Lyric,,0,0,0,,{{{fade}{move}\\an2}}" + "".join(parts))

    # impacto nos drops
    impacts = []
    all_words = [w for l in lines for w in l["words"]]
    for d in drops:
        cands = [w for w in all_words if abs(w["start"] - d) < 2.0 and len(_n(w["w"])) > 3]
        word = min(cands, key=lambda w: abs(w["start"] - d))["w"] if cands else proj.cfg.get("hook", c["short"])
        word = _esc(U(word).strip(".,!?"))
        ev.append(f"Dialogue: 8,{_ts(d - 0.02)},{_ts(d + 0.75)},Impact,,0,0,0,,"
                  f"{{\\pos(960,520)\\fscx170\\fscy170\\blur2\\t(0,90,\\fscx100\\fscy100\\blur0)"
                  f"\\t(450,750,\\alpha&HFF&\\fscx130\\fscy130\\blur10)}}{word}")
        impacts.append(dict(time=d, word=word))

    ass_path = proj.path("work", "lyrics.ass")
    ass_path.write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    srt = sorted(srt)
    srt = [(a, min(z, srt[k + 1][0] - 0.02) if k + 1 < len(srt) else z, t) for k, (a, z, t) in enumerate(srt)]
    srt_path = proj.path("output", f"{proj.cfg['slug']}.srt")
    srt_path.write_text("\n".join(f"{i}\n{_srt_ts(a)} --> {_srt_ts(z)}\n{t}\n" for i, (a, z, t) in enumerate(srt, 1)),
                        encoding="utf-8")
    log(f"legendas: {len(srt)} linhas, {len(used_power)} palavras explodindo, {len(impacts)} impactos -> "
        f"{ass_path.name}, {srt_path.name}")
    return ass_path, srt_path, impacts
