"""Diretor de edição: transforma análise musical + letra + biblioteca de mídia numa timeline (EDL).

Decide: onde cortar (no grid de batidas, ritmo por seção), qual cena entra (casando letra/tags/energia,
sem repetir), movimento de câmera, velocidade (speed ramp / slow / reverse), transições, receitas de
drop (variadas), efeitos sincronizados (kick/snare/downbeat), partículas e respiros.

Roteiro manual opcional: assets/scenes.yaml — ver docs/ROTEIRO.md.
"""
from __future__ import annotations

import random
import re
import unicodedata

import numpy as np

from .common import Project, load_json, load_yaml, log, save_json

# ritmo de corte (em batidas) por seção — ciclos variados para não ficar mecânico
PATTERNS = {
    "intro": [8, 4, 4],
    "verse": [4, 2, 2, 4, 2, 2, 3, 1],
    "pre-chorus": [2, 2, 1, 1, 1, 1],
    "chorus": [2, 1, 1, 2, 1, 1, 1, 1, 2, 2],
    "break": [8, 4],
    "outro": [4, 8, 8],
}
MOOD = {
    "intro": {"dark": 2, "eyes": 2, "closeup": 1.5, "calm": 1, "tension": 1},
    "verse": {"closeup": 1, "emotional": 1, "flashback": 1, "tension": 1, "calm": 0.5},
    "pre-chorus": {"tension": 2, "closeup": 1.5, "eyes": 1.5, "power": 1},
    "chorus": {"battle": 2, "impact": 2, "power": 2, "transformation": 1.5, "lightning": 1},
    "break": {"emotional": 2, "calm": 2, "rain": 1, "sky": 1},
    "outro": {"calm": 2, "sky": 1.5, "emotional": 1.5, "dark": 1},
    "drop": {"impact": 3, "battle": 2.5, "power": 2.5, "transformation": 2},
    "suspend": {"closeup": 3, "eyes": 3, "tension": 2},
}
GENERIC_TAGS = {  # palavras comuns em PT -> tags
    "olho": ["eyes", "closeup"], "olhos": ["eyes", "closeup"], "sangue": ["blood"], "chuva": ["rain"],
    "lagrima": ["emotional"], "chorar": ["emotional"], "dor": ["emotional", "dark"], "raio": ["lightning"],
    "fogo": ["fire"], "chama": ["fire"], "luta": ["battle"], "guerra": ["battle"], "golpe": ["impact"],
    "poder": ["power"], "forca": ["power"], "sombra": ["dark"], "escuro": ["dark"], "trevas": ["dark"],
    "ceu": ["sky"], "morte": ["dark", "emotional"], "grito": ["scream"], "sorriso": ["smile"],
    "passado": ["flashback"], "memoria": ["flashback"], "correr": ["run"], "cair": ["fall"],
    "despertar": ["transformation", "eyes"], "transformar": ["transformation"], "irmao": ["emotional"],
}
DROP_RECIPES = ["invert_impact", "freeze_lightning", "blackout_shockwave", "whip_speedlines", "glitch_burst"]
IMG_MOTIONS = ["parallax_push", "parallax_orbit", "push_in", "parallax_rise", "pull_out", "pan_lr", "pan_rl"]
TRANS_BY_SECTION = {"chorus": "glitch", "pre-chorus": "zoom", "verse": "ink", "break": "fade_black",
                    "outro": "fade_black", "intro": "crossfade"}


def _norm(w):
    w = unicodedata.normalize("NFKD", w.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9 ]", "", w)


def _sec_at(sections, t):
    for s in sections:
        if s["start"] <= t < s["end"]:
            return s
    return sections[-1]


def _parse_time(v):
    if isinstance(v, (int, float)):
        return float(v)
    parts = str(v).split(":")
    return sum(float(p) * 60 ** i for i, p in enumerate(reversed(parts)))


class Planner:
    def __init__(self, proj: Project, seed: int | None = None):
        self.p = proj
        self.a = load_json(proj.work / "analysis.json")
        lt = proj.work / "lyrics_timed.json"
        self.lines = load_json(lt)["lines"] if lt.exists() else []
        ay = proj.assets / "assets.yaml"
        self.assets = [x for x in (load_yaml(ay).get("assets", []) if ay.exists() else []) if x.get("use") != "never"]
        sy = proj.assets / "scenes.yaml"
        self.script = load_yaml(sy).get("scenes", []) if sy.exists() else []
        self.char = proj.char
        self.rng = random.Random(seed if seed is not None else proj.cfg.get("seed", 7))
        tm = {_norm(k): v for k, v in GENERIC_TAGS.items()}
        tm.update({_norm(k): v for k, v in self.char.get("tag_map", {}).items()})
        self.tag_map = tm
        self.uses: dict[str, int] = {}
        self.assigned: dict[int, str] = {}

    # ---------- grade de cortes ----------
    def cut_points(self) -> list[float]:
        beats = np.array(self.a["beats"])
        dur = self.a["duration"]
        if len(beats) < 4:
            return list(np.arange(0, dur, 2.0)) + [dur]
        cuts = [0.0]
        drops = [d["time"] for d in self.a["drops"]]
        bp = self.a["beat_period"]
        # cada seção é cortada a partir do SEU primeiro tempo, com o padrão rítmico dela
        for si, sec in enumerate(self.a["sections"]):
            i = int(np.argmin(np.abs(beats - sec["start"])))
            if si > 0 and beats[i] - cuts[-1] > bp * 0.6:
                cuts.append(float(beats[i]))
            pat = PATTERNS.get(sec["label"], PATTERNS["verse"])
            mult = 2 if self.a["bpm"] >= 120 else 1  # trap a 140–160 BPM é sentido em meio-tempo
            k = 0
            while True:
                step = pat[k % len(pat)] * mult
                e = self._energy(beats[i])
                if sec["label"] == "verse" and e > 0.75 and step >= 2:  # verso intenso acelera
                    step = max(1, step // 2)
                k += 1
                i += step
                if i >= len(beats) or beats[i] >= sec["end"] - bp * 0.5:
                    break
                cuts.append(float(beats[i]))
        protected = set(cuts[:1])
        for sec in self.a["sections"][1:]:
            protected.add(float(beats[int(np.argmin(np.abs(beats - sec["start"])))]))
        # cortes obrigatórios: drops e 1 batida antes (suspensão)
        for d in drops:
            cuts = [c for c in cuts if abs(c - d) > bp * 0.6 and abs(c - (d - bp)) > bp * 0.45]
            cuts += [d, max(0.0, d - bp)]
            protected.update([d, max(0.0, d - bp)])
        # início de cada linha da letra puxa o corte mais próximo (narrativa)
        for ln in self.lines:
            s = ln["start"]
            j = int(np.argmin([abs(c - s) for c in cuts]))
            if 0.12 < abs(cuts[j] - s) < bp * 0.9 and cuts[j] not in protected and j > 0:
                b = beats[np.argmin(np.abs(beats - s))]
                if all(abs(b - d) > bp * 0.5 for d in drops):
                    cuts[j] = float(b)
        # pausas dramáticas: não cortar dentro do silêncio
        for s in self.a["silences"]:
            if s["start"] > 1 and s["end"] < dur - 1:
                cuts = [c for c in cuts if not (s["start"] + 0.05 < c < s["end"] - 0.05)]
        cuts = sorted(set(round(c, 3) for c in cuts if 0 <= c < dur - 0.3))
        clean = [cuts[0]]
        for c in cuts[1:]:
            if c - clean[-1] >= min(0.28, bp * 0.6):
                clean.append(c)
        return clean + [dur]

    def _energy(self, t):
        v = self.a["energy"]["values"]
        return v[min(len(v) - 1, int(t / self.a["energy"]["step"]))]

    # ---------- escolha de cena ----------
    def _words_in(self, a, b):
        out = []
        for ln in self.lines:
            for w in ln["words"]:
                if a - 0.4 <= w["start"] < b + 0.2:
                    out.append(w)
        return out

    def _wanted_tags(self, a, b, role, mood=True):
        tags: dict[str, float] = {}
        for w in self._words_in(a, b):
            n = _norm(w["w"])
            for key, tl in self.tag_map.items():
                if key and (n == key or (len(key) > 4 and (key in n or (len(n) > 5 and n[:6] == key[:6])))):
                    for tg in tl:
                        tags[tg] = tags.get(tg, 0) + (4.0 if w.get("key") else 2.0)
            if mood:
                tags[n] = tags.get(n, 0) + 0.5
        for tg, wv in (MOOD.get(role, {}).items() if mood else []):
            tags[tg] = tags.get(tg, 0) + wv
        return tags

    def _script_for(self, a, b):
        for sc in self.script:
            if "line" in sc and self.lines:
                needle = _norm(sc["line"])
                hit = next((ln for ln in self.lines if needle in _norm(" ".join(w["w"] for w in ln["words"]))), None)
                if hit and hit["start"] - 0.3 <= a < hit["end"] + 0.3:
                    return sc
            if "at" in sc:
                s0 = _parse_time(sc["at"])
                s1 = _parse_time(sc.get("until", s0 + 4))
                if s0 <= a < s1:
                    return sc
        return None

    def pick(self, i, a, b, role, energy):
        if not self.assets:
            return None
        sc = self._script_for(a, b)
        pool = self.assets
        tags = self._wanted_tags(a, b, role)
        if sc:
            if sc.get("assets"):
                ids = set(sc["assets"])
                pool = [x for x in self.assets if x["id"] in ids or x["id"].split("#")[0] in ids] or pool
            for tg in sc.get("tags", []):
                tags[tg] = tags.get(tg, 0) + 4
        best, best_s = None, -1e9
        max_motion = max([x.get("motion", 0) for x in self.assets] + [1e-6])
        for x in pool:
            s = sum(tags.get(tg, 0) for tg in x.get("tags", []))
            s += 0.8 * sum(1 for tg in tags if tg and tg in _norm(x.get("note", "") + " " + x["id"]))
            if x["kind"] == "clip":
                m = x.get("motion", 0) / max_motion
                s -= 1.5 * abs(m - energy)
                if role in ("drop", "chorus"):
                    s += 1.0 * m
            else:
                s += 0.3 if role in ("verse", "intro", "break", "suspend") else -0.2
            s -= 2.2 * self.uses.get(x["id"], 0)
            for j, aid in self.assigned.items():  # vizinhos dos dois lados (atribuição fora de ordem)
                d = abs(i - j)
                if aid == x["id"]:
                    s -= 8 if d <= 3 else (3 if d <= 8 else 0)
                elif d <= 1 and self._file(aid) == x["file"]:
                    s -= 2.5
            s += self.rng.uniform(0, 0.9)
            if s > best_s:
                best, best_s = x, s
        self.uses[best["id"]] = self.uses.get(best["id"], 0) + 1
        self.assigned[i] = best["id"]
        return best

    def _file(self, aid):
        return next((x["file"] for x in self.assets if x["id"] == aid), None)

    # ---------- montagem ----------
    def build(self) -> dict:
        cuts = self.cut_points()
        a = self.a
        cover = self.p.cfg.get("cover")
        cover_out = None
        if cover:
            intro = next((sec for sec in a["sections"] if sec["label"] == "intro"), None)
            if intro:
                cuts = [c for c in cuts if not (0 < c < intro["end"] - 0.05)]
                if all(abs(c - intro["end"]) > 0.05 for c in cuts):
                    cuts = sorted(cuts + [intro["end"]])
            cover_out = round(a["duration"] - 5.0, 3)
            cuts = sorted([c for c in cuts if c < cover_out - 0.3] + [cover_out, a["duration"]])
            cuts = sorted(set(cuts))
        bp = a["beat_period"]
        drops = a["drops"]
        drop_t = [d["time"] for d in drops]
        recipes = {}
        pool = DROP_RECIPES[1:]
        self.rng.shuffle(pool)
        for i, d in enumerate(drops):
            recipes[d["time"]] = "invert_impact" if i == 0 else pool[(i - 1) % len(pool)]

        skel = []
        for i, (s, e) in enumerate(zip(cuts[:-1], cuts[1:])):
            label = _sec_at(a["sections"], s + 0.06)["label"]
            role = label
            if any(abs(s - d) < 0.05 for d in drop_t):
                role = "drop"
            elif any(abs(e - d) < 0.05 for d in drop_t):
                role = "suspend"
            energy = self._energy((s + e) / 2)
            strength = sum(self._wanted_tags(s, e, role, mood=False).values())
            skel.append((i, s, e, label, role, energy, strength))
        # 1º passe: planos em que a letra cita algo concreto escolhem primeiro (sincronia narrativa)
        is_cover = lambda k: cover and (k[3] == "intro" or (cover_out is not None and k[1] >= cover_out - 0.01))
        order = sorted([k for k in skel if k[6] >= 4], key=lambda k: -k[6]) + [k for k in skel if k[6] < 4]
        picked = {}
        for i, s, e, label, role, energy, _ in order:
            picked[i] = None if is_cover(skel[i]) else self.pick(i, s, e, role, energy)

        shots = []
        prev_label = None
        img_k = 0
        for i, s, e, label, role, energy, strength in skel:
            x = picked[i]
            shot = dict(i=i, start=round(s, 3), end=round(e, 3), section=label, role=role,
                        energy=round(energy, 3), lyric_match=round(strength, 1))
            if is_cover(skel[i]):
                shot.update(kind="cover", motion="cover_intro" if label == "intro" else "cover_outro")
            elif x is None:
                shot.update(self._generated(i, s, e, label, role))
            else:
                shot.update(asset=x["id"], kind=x["kind"], file=x["file"])
                if x["kind"] == "clip":
                    shot.update(self._clip_timing(x, e - s, role, energy))
                    shot["motion"] = "clip"
                else:
                    aspect = x["w"] / max(1, x["h"])
                    if aspect < 1.2:
                        shot["motion"] = self.rng.choice(["panel_tilt", "panel_push"])
                    else:
                        shot["motion"] = IMG_MOTIONS[img_k % len(IMG_MOTIONS)] if role != "suspend" else "push_in_slow"
                        img_k += 1 + (self.rng.random() < 0.3)
                    if role == "drop":
                        shot["motion"] = "parallax_push" if aspect >= 1.2 else "panel_push"
            # transição de entrada
            tr = "cut"
            if i == 0:
                tr = "fade_in"
            elif role == "drop":
                tr = {"whip_speedlines": "whip", "glitch_burst": "glitch"}.get(recipes.get(s), "cut")
            elif label != prev_label:
                tr = TRANS_BY_SECTION.get(label, "flash")
            elif label == "chorus" and self.rng.random() < 0.18:
                tr = "flash"
            elif label == "verse" and self.rng.random() < 0.12:
                tr = self.rng.choice(["whip", "zoom", "glitch"])
            shot["trans_in"] = tr
            # momento 3D "do nada": raro (~1 a cada 25 s), num plano de 1–3 s fora de drop/suspensão
            if (shot.get("kind") not in ("cover", None) and role not in ("drop", "suspend") and
                    0.9 <= e - s <= 3.2 and s - getattr(self, "_last3d", -99) > 22 and self.rng.random() < 0.35):
                shot["fx3d"] = "spin" if self.rng.random() < 0.5 else "tilt"
                self._last3d = s
            prev_label = label
            shots.append(shot)

        events = self._events(shots, recipes)
        tl = dict(duration=a["duration"], fps=self.p.cfg.get("fps", 30), bpm=a["bpm"], shots=shots,
                  events=events, drops=[dict(time=t, recipe=r) for t, r in recipes.items()])
        save_json(self.p.path("work", "timeline.json"), tl)
        n_assets = len({s.get("asset") for s in shots if s.get("asset")})
        log(f"timeline: {len(shots)} planos, {n_assets} cenas distintas, "
            f"média {a['duration'] / max(1, len(shots)):.2f}s/plano, drops: {list(recipes.values())}")
        return tl

    def _generated(self, i, s, e, label, role):
        """Sem mídia para o plano: efeito ligado à palavra cantada, ou a capa em 3D, ou efeito do clima."""
        from .vfx import KEYWORDS
        for w in self._words_in(s, e):
            kind = KEYWORDS.get(_norm(w["w"]).replace(" ", ""))
            if kind:
                return dict(kind="vfx", motion=kind, lyric_vfx=w["w"])
        if not hasattr(self, "_gen_k"):
            self._gen_k = 0
        self._gen_k += 1
        if self.p.cfg.get("cover") and (role in ("verse", "break", "intro", "outro") and self._gen_k % 2 == 0):
            return dict(kind="cover", motion="cover_card", variant=self._gen_k % 6)
        mood = {"chorus": ["burst", "vortex", "merge", "void"], "drop": ["burst", "merge"],
                "pre-chorus": ["barrier", "iris"], "suspend": ["iris"], "break": ["void", "iris"],
                "verse": ["void", "iris", "vortex", "barrier", "merge"], "outro": ["void"]}
        opts = mood.get(role, mood.get(label, ["void"]))
        kind = opts[self._gen_k % len(opts)]
        if kind == getattr(self, "_last_gen", None):
            kind = opts[(self._gen_k + 1) % len(opts)]
        self._last_gen = kind
        return dict(kind="vfx", motion=kind)

    def _clip_timing(self, x, dur, role, energy):
        avail = x["end"] - x["start"]
        if role == "drop":
            ramp = [[0, 0.3], [0.22, 0.3], [0.38, 1.7], [0.6, 1.0], [1, 1.0]]
        elif role == "suspend":
            ramp = [[0, 0.5], [1, 0.25]]
        elif x.get("motion", 0) < 0.02 and role in ("verse", "break", "outro") and self.rng.random() < 0.12:
            ramp = [[0, 1.0], [1, 1.0]]
            return dict(src_in=x["start"], ramp=ramp, reverse=True, src_need=dur)
        elif role in ("break", "outro", "intro"):
            ramp = [[0, 0.65], [1, 0.65]]
        elif role == "chorus" and self.rng.random() < 0.25:
            ramp = [[0, 1.0], [0.5, 1.35], [1, 0.9]]
        else:
            ramp = [[0, 1.0], [1, 1.0]]
        need = _ramp_len(ramp, dur)
        if need > avail:  # desacelera para caber
            k = avail / need * 0.98
            ramp = [[t, v * k] for t, v in ramp]
            need = avail * 0.98
        uses = self.uses.get(x["id"], 1)
        slack = max(0.0, avail - need)
        off = (slack * ((uses * 0.37) % 1.0)) if uses > 1 else slack * 0.1
        return dict(src_in=round(x["start"] + off, 3), ramp=ramp, reverse=False, src_need=round(need, 3))

    def _events(self, shots, recipes):
        a = self.a
        secs = a["sections"]
        lab = lambda t: _sec_at(secs, t)["label"]
        strong_k = [k[0] for k in a["kick"] if k[1] > 0.45]
        events = dict(
            shake=[t for t in strong_k if lab(t) in ("chorus",)] + [d for d in recipes],
            punch=[t for t in a["bars"] if lab(t) in ("chorus", "pre-chorus")],
            rgb=[s[0] for s in a["snare"] if s[1] > 0.5 and lab(s[0]) == "chorus"],
            flash=[t for i, t in enumerate(a["bars"]) if lab(t) == "chorus" and i % 2 == 0],
            signal=[t for t in a["bars"] if lab(t) == "chorus"],
            embers=[[s["start"], s["end"], 1.0 if s["label"] == "chorus" else 0.35]
                    for s in secs if s["label"] in ("chorus", "pre-chorus", "outro")],
            leak=[[s["start"], s["end"], 0.28] for s in secs if s["label"] in ("verse", "intro", "break")],
            pauses=[[s["start"], s["end"]] for s in a["silences"] if 1 < s["start"] and s["end"] < a["duration"] - 1],
            glitch=[sh["start"] for sh in shots if sh["trans_in"] == "glitch"],
        )
        return events


def _ramp_len(ramp, dur):
    """Integral da velocidade (tempo de fonte consumido)."""
    ts = np.linspace(0, 1, 50)
    v = np.interp(ts, [r[0] for r in ramp], [r[1] for r in ramp])
    return float(np.trapezoid(v, ts) * dur)


def plan(proj: Project, seed=None) -> dict:
    return Planner(proj, seed).build()
