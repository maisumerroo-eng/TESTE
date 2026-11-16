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


def build_ass(proj: Project, timed: dict | None = None, analysis: dict | None = None) -> tuple:
    b = brand()
    c = proj.char
    timed = timed or load_json(proj.work / "lyrics_timed.json")
    analysis = analysis or load_json(proj.work / "analysis.json")
    upper = proj.cfg.get("subtitles", {}).get("uppercase", True)

    bone = hex_to_ass(b["palette"]["bone"])
    void = hex_to_ass(b["palette"]["void"])
    prim = hex_to_ass(c["primary"])
    sec = hex_to_ass(c["secondary"])
    font = b["fonts"]["lyrics"]
    disp = b["fonts"]["display"]

    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Lyric,{font},74,{bone},{bone},{void},&H96000000,-1,0,0,0,100,100,1.5,0,1,5,2,2,120,120,96,1
Style: Glow,{font},74,{prim},{prim},{prim},&H00000000,-1,0,0,0,100,100,1.5,0,1,10,0,2,120,120,96,1
Style: Hook,{font},96,{bone},{bone},{void},&H96000000,-1,0,0,0,100,100,2,0,1,6,3,5,120,120,0,1
Style: HookGlow,{font},96,{prim},{prim},{prim},&H00000000,-1,0,0,0,100,100,2,0,1,12,0,5,120,120,0,1
Style: Impact,{disp},230,{bone},{bone},{prim},&H00000000,0,0,0,0,100,100,4,0,1,8,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    kicks = [k[0] for k in analysis.get("kick", []) if k[1] > 0.35]
    lines = timed["lines"]
    events, srt = [], []
    for li, line in enumerate(lines):
        words = line["words"]
        if not words:
            continue
        start = words[0]["start"] - 0.08
        nxt = lines[li + 1]["words"][0]["start"] - 0.05 if li + 1 < len(lines) and lines[li + 1]["words"] else 1e9
        end = min(words[-1]["end"] + 0.45, nxt)
        end = max(end, words[-1]["end"] + 0.05)
        label = _section_at(analysis["sections"], words[0]["start"])
        hook = label == "chorus"
        brk = _wrap(words, 26 if hook else 32)

        # pulso nos kicks (linha inteira)
        pulse = ""
        for k in kicks:
            if start < k < end:
                t0 = int((k - start) * 1000)
                pulse += f"\\t({t0},{t0 + 50},\\fscx104\\fscy104)\\t({t0 + 50},{t0 + 180},\\fscx100\\fscy100)"
        pulse = pulse[:1800]  # limite de segurança

        def render(glow: bool) -> str:
            parts = []
            for i, w in enumerate(words):
                t1 = int(max(0, (w["start"] - start)) * 1000)
                txt = _esc(w["w"].upper() if upper else w["w"])
                if w.get("key"):
                    col = "" if glow else f"\\c{prim}\\3c{void}"
                    tag = (f"{{\\alpha&HFF&{col}\\fscx135\\fscy135"
                           f"\\t({t1},{t1 + 40},\\alpha&H00&)\\t({t1},{t1 + 160},\\fscx112\\fscy112)}}")
                else:
                    col = "" if glow else f"\\c{bone}"
                    tag = (f"{{\\alpha&HFF&{col}\\fscx118\\fscy118"
                           f"\\t({t1},{t1 + 40},\\alpha&H00&)\\t({t1},{t1 + 120},\\fscx100\\fscy100)}}")
                if glow and not w.get("key"):
                    tag = f"{{\\alpha&HFF&}}"  # brilho só nas palavras-chave
                sep = "\\N" if brk is not None and i == brk else (" " if i else "")
                parts.append(sep + tag + txt)
            return "".join(parts)

        dur_ms = int((end - start) * 1000)
        fade = f"\\fad(60,{min(160, dur_ms // 4)})"
        st, gst = ("Hook", "HookGlow") if hook else ("Lyric", "Glow")
        pos = "\\pos(960,820)" if hook else ""
        events.append(f"Dialogue: 0,{_ts(start)},{_ts(end)},{gst},,0,0,0,,{{\\blur9{fade}{pos}\\1a&HFF&}}" + render(True))
        events.append(f"Dialogue: 1,{_ts(start)},{_ts(end)},{st},,0,0,0,,{{{fade}{pos}{pulse}}}" + render(False))
        srt.append((words[0]["start"], words[-1]["end"] + 0.3 if end > words[-1]["end"] + 0.3 else end,
                    " ".join(w["w"] for w in words)))

    # palavras de impacto nos drops (escolhe a palavra-chave cantada mais perto do drop)
    impacts = []
    all_words = [w for l in lines for w in l["words"]]
    for d in analysis.get("drops", []):
        t = d["time"]
        cands = [w for w in all_words if w.get("key") and abs(w["start"] - t) < 2.5]
        word = (min(cands, key=lambda w: abs(w["start"] - t))["w"] if cands else proj.cfg.get("hook", c["short"]))
        word = _esc(word.upper().strip(".,!?"))
        a, z = t - 0.02, t + 0.7
        events.append(f"Dialogue: 3,{_ts(a)},{_ts(z)},Impact,,0,0,0,,"
                      f"{{\\pos(960,520)\\fscx160\\fscy160\\blur2\\t(0,90,\\fscx100\\fscy100\\blur0)"
                      f"\\t(420,700,\\alpha&HFF&\\fscx112\\fscy112)}}{word}")
        impacts.append(dict(time=t, word=word))

    ass_path = proj.path("work", "lyrics.ass")
    ass_path.write_text(head + "\n".join(events) + "\n", encoding="utf-8")

    srt_lines = []
    for i, (a, z, txt) in enumerate(sorted(srt), 1):
        srt_lines.append(f"{i}\n{_srt_ts(a)} --> {_srt_ts(z)}\n{txt}\n")
    srt_path = proj.path("output", f"{proj.cfg['slug']}.srt")
    srt_path.write_text("\n".join(srt_lines), encoding="utf-8")
    log(f"legendas: {len(srt)} linhas, {len(impacts)} palavras de impacto -> {ass_path.name}, {srt_path.name}")
    return ass_path, srt_path, impacts
