"""Motor de render KAGERIMA: timeline.json -> vídeo 1920x1080 H.264 + legendas ASS + áudio master.

Render em paralelo (N processos, cada um um trecho), frames gerados em numpy/OpenCV e enviados
por pipe ao FFmpeg. Passo final: concat + legendas (libass) + áudio AAC 48 kHz.
"""
from __future__ import annotations

import math
import os
import subprocess
from multiprocessing import Pool
from pathlib import Path

import cv2
import numpy as np

from . import fx, overlays
from .common import FONTS_DIR, Project, brand, hex_to_rgb, load_json, log, run
from .fx import H, W

TW = 0.18  # duração padrão das transições (s)
TRANS_DUR = {"flash": 0.10, "glitch": 0.16, "whip": 0.22, "zoom": 0.26, "ink": 0.30, "crossfade": 0.5,
             "fade_black": 0.6, "fade_in": 0.8, "cut": 0.0}


def _ramp_cum(ramp, dur, n=200):
    ts = np.linspace(0, 1, n)
    v = np.interp(ts, [r[0] for r in ramp], [r[1] for r in ramp])
    cum = np.concatenate([[0], np.cumsum((v[1:] + v[:-1]) / 2 * np.diff(ts))]) * dur
    return ts, cum


class ClipSource:
    def __init__(self, path: Path, shot: dict, src_fps: float):
        self.shot = shot
        dur = shot["end"] - shot["start"]
        self.ts, self.cum = _ramp_cum(shot["ramp"], dur)
        need = self.cum[-1]
        self.t0 = max(0.0, shot["src_in"] - 0.25)
        t1 = shot["src_in"] + need + 0.25
        cap = cv2.VideoCapture(str(path))
        cap.set(cv2.CAP_PROP_POS_MSEC, self.t0 * 1000)
        self.fps = src_fps
        self.frames = []
        for _ in range(int((t1 - self.t0) * src_fps) + 2):
            ok, f = cap.read()
            if not ok:
                break
            self.frames.append(fx.cover(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)))
        cap.release()
        if not self.frames:
            self.frames = [np.zeros((H, W, 3), np.uint8)]

    def frame(self, rel: float) -> np.ndarray:
        dur = self.shot["end"] - self.shot["start"]
        p = min(1.0, max(0.0, rel / dur))
        off = float(np.interp(p, self.ts, self.cum))
        if self.shot.get("reverse"):
            off = self.cum[-1] - off
        st = self.shot["src_in"] + off
        idx = int(round((st - self.t0) * self.fps))
        return self.frames[min(len(self.frames) - 1, max(0, idx))]


class ImageSource:
    def __init__(self, path: Path, depth_path: Path | None, shot: dict, char: dict):
        self.shot = shot
        img = cv2.cvtColor(cv2.imread(str(path)), cv2.COLOR_BGR2RGB)
        self.motion = shot["motion"]
        self.panel = self.motion.startswith("panel")
        if self.panel:
            self._build_panel(img, char)
        else:
            self.img = fx.cover(img)
            self.depth = None
            if depth_path is not None and depth_path.exists():
                d = np.load(depth_path).astype(np.float32)
                self.depth = fx.cover(d[..., None].repeat(3, 2))[..., 0] if d.ndim == 2 else fx.cover(d)

    def _build_panel(self, img, char):
        dark = np.array(hex_to_rgb(char["dark"]), np.float32)
        bg = fx.cover(img)
        bg = cv2.GaussianBlur(bg, (0, 0), 28).astype(np.float32) * 0.35 + dark * 0.65
        # retícula (halftone) sutil
        yy, xx = np.mgrid[0:H, 0:W]
        dots = ((np.sin(xx * 0.35) * np.sin(yy * 0.35)) > 0.6).astype(np.float32)[..., None] * 18
        self.bg = np.clip(bg + dots, 0, 255).astype(np.uint8)
        ih, iw = img.shape[:2]
        if self.motion == "panel_tilt":
            s = (W * 0.5) / iw
            if ih * s < H * 1.15:
                s = H * 1.15 / ih
        else:
            s = min(H * 0.86 / ih, W * 0.8 / iw)
        pw, ph = int(iw * s), int(ih * s)
        p = cv2.resize(img, (pw, ph), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
        border = 8
        card = np.full((ph + 2 * border, pw + 2 * border, 4), 255, np.uint8)
        card[border:-border, border:-border, :3] = p
        self.card = card

    def frame(self, rel: float, energy: float) -> np.ndarray:
        dur = self.shot["end"] - self.shot["start"]
        p = fx.ease(rel / dur, "inout")
        m = self.motion
        k = 1.0 + 0.6 * energy  # mais energia = movimento maior
        if self.panel:
            out = fx.camera(self.bg, 1.06 + 0.04 * p, -30 * p * k, 0)
            ch, cw = self.card.shape[:2]
            if m == "panel_tilt" and ch > H:
                y = int(-(ch - H + 60) * p) + 30
                z = 1.0
            else:
                z = 1.0 + 0.08 * p * k
                y = None
            card = self.card if z == 1.0 else cv2.resize(self.card, (int(cw * z), int(ch * z)))
            ch, cw = card.shape[:2]
            x = (W - cw) // 2 + int(20 * p * k)
            if y is None:
                y = (H - ch) // 2
            # sombra
            sh = out[max(0, y + 18):y + 18 + ch, max(0, x + 18):x + 18 + cw]
            sh[:] = (sh.astype(np.uint16) * 115 // 255).astype(np.uint8)
            if z == 1.0:
                if not hasattr(self, "_card_ov"):
                    self._card_ov = fx.Overlay(card)
                return fx.alpha_over(out, self._card_ov, x, y)
            return fx.alpha_over(out, card, x, y)
        if m.startswith("parallax") and self.depth is not None:
            if m == "parallax_push":
                return fx.parallax(self.img, self.depth, 1.06 + 0.08 * p * k, 0, 0, depth_zoom=0.10 * p * k)
            if m == "parallax_orbit":
                return fx.parallax(self.img, self.depth, 1.10, (-1 + 2 * p) * 55 * k, 0, depth_zoom=0.02)
            if m == "parallax_rise":
                return fx.parallax(self.img, self.depth, 1.09 + 0.03 * p, 0, (1 - 2 * p) * 40 * k, depth_zoom=0.03)
        if m in ("push_in", "parallax_push", "push_in_slow"):
            z0, z1 = (1.04, 1.10) if m == "push_in_slow" else (1.04, 1.04 + 0.13 * k)
            return fx.camera(self.img, z0 + (z1 - z0) * p)
        if m == "pull_out":
            return fx.camera(self.img, 1.22 - 0.16 * p)
        if m in ("pan_lr", "pan_rl", "parallax_orbit", "parallax_rise"):
            d = 1 if m != "pan_rl" else -1
            return fx.camera(self.img, 1.18, d * (-1 + 2 * p) * 110)
        return fx.camera(self.img, 1.05 + 0.08 * p)


class BrandBG:
    """Fundo procedural quando não há mídia: gradiente da cor do personagem + kanji gigante."""

    def __init__(self, shot, char):
        from PIL import Image, ImageDraw
        prim = hex_to_rgb(char["primary"])
        dark = hex_to_rgb(char["dark"])
        y = np.linspace(0, 1, H)[:, None, None]
        x = np.linspace(-1, 1, W)[None, :, None]
        g = np.exp(-(x ** 2) * 1.5 - ((y - 0.55) ** 2) * 4)
        img = (np.array(dark, np.float32) * (1 - g * 0.7) + np.array(prim, np.float32) * g * 0.45)
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(im)
        kan = char.get("kanji", "影")
        k = kan[(shot["i"] // 3) % len(kan)]
        d.text((W // 2, H // 2), k, font=overlays.font("Noto Sans JP Black", 780), fill=tuple(int(c * 0.55) for c in prim), anchor="mm")
        self.img = np.array(im)
        self.shot = shot

    def frame(self, rel, energy):
        dur = self.shot["end"] - self.shot["start"]
        return fx.camera(self.img, 1.02 + 0.1 * fx.ease(rel / dur), 0, 0, (rel / dur - 0.5) * 2)


class Renderer:
    def __init__(self, proj: Project):
        self.p = proj
        self.tl = load_json(proj.work / "timeline.json")
        self.shots = self.tl["shots"]
        self.ev = self.tl["events"]
        self.drops = {d["time"]: d["recipe"] for d in self.tl["drops"]}
        self.fps = self.tl["fps"]
        self.char = proj.char
        self.prim = hex_to_rgb(self.char["primary"])
        self.accent = hex_to_rgb(self.char.get("accent", self.char["primary"]))
        self.lut = fx.make_grade_lut(hex_to_rgb(self.char["dark"]), self.prim, 0.32)
        self.embers = fx.Embers(150, self.accent)
        b = brand()
        ay = proj.assets / "assets.yaml"
        from .common import load_yaml
        self.assets = {a["id"]: a for a in (load_yaml(ay).get("assets", []) if ay.exists() else [])}
        self.cache: dict[int, object] = {}
        self.prev = None
        self.hud_on = overlays.hud(self.char["short"], f"TRACK {proj.cfg.get('track', '01')}", True)
        self.hud_off = overlays.hud(self.char["short"], f"TRACK {proj.cfg.get('track', '01')}", False)
        self.hud_on, self.hud_off = fx.Overlay(self.hud_on), fx.Overlay(self.hud_off)
        self.title = fx.Overlay(overlays.title_card(self.char, proj.cfg.get("hook", "")))
        self.endc = fx.Overlay(overlays.end_card(proj.cfg.get("next_hint", "")))
        self.sigbar = fx.Overlay(overlays.signal_bar())
        self.title_at = float(proj.cfg.get("title_at", 1.0))
        self.beats = np.array(load_json(proj.work / "analysis.json")["beats"])
        self.starts = np.array([s["start"] for s in self.shots])

    # ----- fontes -----
    def source(self, i):
        if i in self.cache:
            return self.cache[i]
        s = self.shots[i]
        if s["kind"] == "clip":
            a = self.assets[s["asset"]]
            src = ClipSource(self.p.assets / s["file"], s, a.get("fps", 24))
        elif s["kind"] in ("image", "panel"):
            dp = self.p.work / "depth" / f"{s['asset'].replace('#', '_')}.npy"
            src = ImageSource(self.p.assets / s["file"], dp, s, self.char)
        else:
            src = BrandBG(s, self.char)
        self.cache[i] = src
        for k in [k for k in self.cache if k < i - 2]:
            del self.cache[k]
        return src

    def shot_frame(self, i, t, energy):
        s = self.shots[i]
        src = self.source(i)
        rel = t - s["start"]
        # congelamento (receita freeze no drop)
        if self.drops.get(s["start"]) == "freeze_lightning" and 0 <= rel < 0.28:
            rel = 0.0
        base = src.frame(rel) if isinstance(src, ClipSource) else src.frame(rel, energy)
        # câmera global: shake + zoom punch
        dx, dy, rot = fx.shake_offset(t, self._near(self.ev["shake"], t), amp=22 + 26 * energy, seed=i)
        punch = self._decay(self.ev["punch"], t, 0.045, 9)
        if s["role"] == "drop":
            punch += 0.10 * math.exp(-max(0, rel) * 6)
        if dx or dy or rot or punch:
            base = fx.camera(base, 1.0 + punch + (0.04 if dx or dy else 0), dx, dy, rot)
        return base

    @staticmethod
    def _near(lst, t, win=0.7):
        return [h for h in lst if -0.05 < t - h < win]

    @staticmethod
    def _decay(lst, t, amp, k):
        best = 0.0
        for h in lst:
            d = t - h
            if 0 <= d < 0.6:
                best = max(best, amp * math.exp(-d * k))
        return best

    def energy(self, t):
        v = load_energy(self.p)
        return v[min(len(v) - 1, int(t * 10))]

    # ----- composição de um frame -----
    def frame(self, n: int) -> np.ndarray:
        t = n / self.fps
        i = int(np.searchsorted(self.starts, t, side="right") - 1)
        i = max(0, min(i, len(self.shots) - 1))
        s = self.shots[i]
        e = self.energy(t)
        f = self.shot_frame(i, t, e)

        # transição de entrada (centrada no corte) e saída para o próximo plano
        f = self._transition(f, i, t, e)

        # receitas de drop
        f = self._drop_fx(f, t, s)

        # suspensão pré-drop: dessatura + escurece
        if s["role"] == "suspend":
            p = (t - s["start"]) / max(0.01, s["end"] - s["start"])
            f = fx.desaturate(f, 0.35 + 0.5 * p)
            f = fx.blackout(f, 0.25 * p)
        for a, b in self.ev["pauses"]:
            if a <= t < b:
                f = fx.desaturate(f, 0.4)

        # eventos rítmicos
        rgb = self._decay(self.ev["rgb"], t, 14, 22)
        if rgb > 1:
            f = fx.rgb_split(f, int(rgb))
        fl = self._decay(self.ev["flash"], t, 0.30, 26)
        if fl > 0.02:
            f = fx.flash(f, fl)
        gl = self._decay(self.ev["glitch"], t + 0.06, 0.8, 14)
        if gl > 0.05:
            f = fx.glitch(f, gl, n)

        # partículas e luz
        emb = max([v for a, b, v in self.ev["embers"] if a <= t < b] or [0])
        if emb:
            f = self.embers.draw(f, t, emb * (0.5 + 0.5 * e))
        lk = max([v for a, b, v in self.ev["leak"] if a <= t < b] or [0])
        if lk:
            f = fx.light_leak(f, t, self.accent, lk, seed=1.7)

        # look do canal
        f = fx.grade(f, self.lut)
        ca = 0.0015 + self._decay(list(self.drops), t, 0.01, 6)
        f = fx.chroma_aberration(f, ca)
        f = fx.motion_blur(f, self.prev, 0.25 if e > 0.7 and s["kind"] == "clip" else 0.0)
        self.prev = f
        f = fx.finish(f, n)
        return self._overlays(f, t)

    def _transition(self, f, i, t, e):
        s = self.shots[i]
        tr = s.get("trans_in", "cut")
        d = TRANS_DUR.get(tr, TW)
        rel = t - s["start"]
        # metade final do plano anterior também participa (transição centrada no corte)
        if i + 1 < len(self.shots):
            nxt = self.shots[i + 1]
            ntr = nxt.get("trans_in", "cut")
            nd = TRANS_DUR.get(ntr, TW)
            if ntr in ("whip", "zoom", "crossfade", "fade_black", "ink") and nxt["start"] - t < nd / 2:
                return self._mix(f, self.shot_frame(i + 1, t, e), ntr, 0.5 - (nxt["start"] - t) / nd, t)
        if tr == "fade_in" and rel < d:
            return fx.blackout(f, 1 - fx.ease(rel / d, "out"))
        if tr in ("whip", "zoom", "crossfade", "fade_black", "ink") and rel < d / 2 and i > 0:
            return self._mix(self.shot_frame(i - 1, t, e), f, tr, 0.5 + rel / d, t)
        if tr == "flash" and rel < d:
            return fx.flash(f, 1 - rel / d)
        if tr == "glitch" and rel < d:
            return fx.glitch(f, 1 - rel / d, int(t * 100))
        return f

    def _mix(self, a, b, tr, p, t):
        p = min(1.0, max(0.0, p))
        if tr == "crossfade":
            return cv2.addWeighted(a, 1 - p, b, p, 0)
        if tr == "fade_black":
            return fx.blackout(a, min(1, p * 2)) if p < 0.5 else fx.blackout(b, min(1, (1 - p) * 2))
        if tr == "whip":
            off = int(fx.ease(p) * W)
            out = np.empty_like(a)
            out[:, : W - off] = a[:, off:]
            out[:, W - off:] = b[:, : off]
            return fx.directional_blur(out, int(90 * math.sin(math.pi * p)) + 1)
        if tr == "zoom":
            if p < 0.5:
                z = fx.camera(a, 1 + p * 0.8)
                return fx.radial_zoom_blur(z, 0.12 * p * 2, 5)
            z = fx.camera(b, 1.4 - (p - 0.5) * 0.8)
            return fx.radial_zoom_blur(z, 0.12 * (1 - p) * 2, 5)
        if tr == "ink":
            m = _ink_mask(p)
            return (a.astype(np.float32) * (1 - m) + b.astype(np.float32) * m).astype(np.uint8)
        return b if p >= 0.5 else a

    def _drop_fx(self, f, t, s):
        for d, recipe in self.drops.items():
            r = t - d
            if recipe == "blackout_shockwave" and -3 / self.fps <= r < 0:
                return fx.blackout(f, 1.0)
            if not 0 <= r < 0.9:
                continue
            fr = int(round(r * self.fps))
            if recipe == "invert_impact":
                if fr <= 1:
                    f = fx.impact_frame(f, self.prim)
                elif fr <= 3:
                    f = fx.invert(f)
                f = fx.flash(f, max(0, 0.6 - r * 4))
                if r < 0.45:
                    f = fx.speed_lines(f, t, 1 - r / 0.45, (255, 255, 255))
            elif recipe == "freeze_lightning":
                if r < 0.4:
                    f = fx.lightning(f, t, self.prim, seed=7, bolts=3)
                f = fx.flash(f, max(0, 0.5 - r * 5))
            elif recipe == "blackout_shockwave":
                f = fx.shockwave(f, r / 0.55, self.prim)
                f = fx.flash(f, max(0, 0.7 - r * 6))
            elif recipe == "whip_speedlines":
                if r < 0.6:
                    f = fx.speed_lines(f, t, 1 - r / 0.6, self.prim)
            elif recipe == "glitch_burst":
                f = fx.glitch(f, max(0, 1 - r / 0.4), int(t * 97))
                f = fx.flash(f, max(0, 0.4 - r * 4), self.prim)
            # assinatura elemental do personagem em todo drop
            el = self.char.get("element")
            if el == "lightning" and 0.08 < r < 0.5 and recipe != "freeze_lightning":
                f = fx.lightning(f, t, self.prim, seed=11, bolts=1)
            elif el == "void" and r < 0.6:
                f = fx.shockwave(f, r / 0.6, self.prim)
            elif el == "slash" and r < 0.25:
                f = _slash(f, r / 0.25)
            elif el == "ki" and r < 0.8:
                f = fx.light_leak(f, t, self.accent, 0.9 * (1 - r / 0.8), seed=0.3)
            elif el == "fire" and r < 0.9:
                f = self.embers.draw(f, t, 1.0)
        return f

    def _overlays(self, f, t):
        dur = self.tl["duration"]
        # HUD (depois de 1,2 s; pisca no tempo)
        if 1.2 < t < dur - 5.2:
            bi = int(np.searchsorted(self.beats, t))
            hud = self.hud_on if bi % 2 == 0 else self.hud_off
            op = min(1.0, (t - 1.2) / 0.3)
            if t - 1.2 < 0.25:
                f = fx.alpha_over(f, hud, 40 + int(np.random.default_rng(int(t * 99)).integers(-20, 20)), 34, op)
            else:
                f = fx.alpha_over(f, hud, 40, 34, op * 0.92)
        # cartela de título
        r = t - self.title_at
        if 0 <= r < 3.4:
            op = min(1.0, r / 0.25) * min(1.0, (3.4 - r) / 0.4)
            slide = int((1 - fx.ease(min(1, r / 0.5), "out")) * -80)
            f = fx.alpha_over(f, self.title, slide, 0, op)
        # barra signal nos downbeats do refrão
        if self._decay(self.ev["signal"], t, 1.0, 10) > 0.3:
            f = fx.alpha_over(f, self.sigbar, 40, 92, 0.95)
        # end card
        if t > dur - 5.0:
            op = min(1.0, (t - (dur - 5.0)) / 0.6)
            f = fx.alpha_over(f, self.endc, 0, 0, op)
        return f


_ENERGY = {}


def load_energy(proj):
    k = str(proj.root)
    if k not in _ENERGY:
        _ENERGY[k] = load_json(proj.work / "analysis.json")["energy"]["values"]
    return _ENERGY[k]


def _ink_mask(p):
    """Máscara de 'tinta' que se espalha a partir de borrões (transição mangá)."""
    small = _INK_NOISE
    thr = 1 - p
    m = np.clip((small - thr) * 8, 0, 1)
    return cv2.resize(m, (W, H))[..., None]


_rng = np.random.default_rng(5)
_INK_NOISE = cv2.GaussianBlur(_rng.random((H // 8, W // 8)).astype(np.float32), (0, 0), 6)
_INK_NOISE = (_INK_NOISE - _INK_NOISE.min()) / (_INK_NOISE.max() - _INK_NOISE.min())


def _slash(f, p):
    out = f.copy()
    for k, off in enumerate((-200, 0, 220)):
        x0, y0 = int(-100 + off), int(H * 0.15 + off * 0.3)
        x1 = int(x0 + (W + 400) * min(1, p * 1.8))
        y1 = int(y0 + (H * 0.7) * min(1, p * 1.8))
        cv2.line(out, (x0, y0), (x1, y1), (255, 255, 255), 9 - 2 * k, cv2.LINE_AA)
    glow = cv2.GaussianBlur(out, (0, 0), 3)
    return cv2.addWeighted(out, 0.7, glow, 0.3, 0)


# ---------------- execução ----------------
def _render_chunk(args):
    root, a, b, out, crf = args
    proj = Project(Path(root))
    r = Renderer(proj)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(r.fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf),
           "-pix_fmt", "yuv420p", str(out)]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(a, b):
        pr.stdin.write(r.frame(n).tobytes())
    pr.stdin.close()
    pr.wait()
    return out


def prepare_depth(proj: Project, tl: dict):
    from .depth import depth_map
    ids = {s["asset"]: s["file"] for s in tl["shots"]
           if s.get("kind") in ("image", "panel") and s.get("motion", "").startswith("parallax")}
    for aid, f in ids.items():
        depth_map(proj.assets / f, proj.work / "depth" / f"{aid.replace('#', '_')}.npy")
    if ids:
        log(f"profundidade 2.5D pronta para {len(ids)} imagens")


def render(proj: Project, workers: int | None = None, t_from=0.0, t_to=None, out_name=None, audio=None) -> Path:
    tl = load_json(proj.work / "timeline.json")
    prepare_depth(proj, tl)
    fps = tl["fps"]
    dur = tl["duration"]
    t_to = dur if t_to is None else min(t_to, dur)
    n0, n1 = int(t_from * fps), int(t_to * fps)
    workers = workers or max(1, min(os.cpu_count() or 2, 6))
    chunks = []
    step = math.ceil((n1 - n0) / workers)
    cdir = proj.work / "chunks"
    cdir.mkdir(parents=True, exist_ok=True)
    for k in range(workers):
        a, b = n0 + k * step, min(n1, n0 + (k + 1) * step)
        if a < b:
            chunks.append((str(proj.root), a, b, str(cdir / f"c{k:02d}.mp4"), 13))
    log(f"render {n1 - n0} frames ({(n1 - n0) / fps:.1f}s @ {fps}fps) em {len(chunks)} processos...")
    with Pool(len(chunks)) as pool:
        outs = pool.map(_render_chunk, chunks)
    lst = cdir / "list.txt"
    lst.write_text("".join(f"file '{Path(o).name}'\n" for o in outs))
    b = brand()["video"]
    audio = audio or (proj.work / "audio_final.wav" if (proj.work / "audio_final.wav").exists()
                      else proj.work / "audio_master.wav")
    out = proj.out / (out_name or f"{proj.cfg['slug']}.mp4")
    out.parent.mkdir(parents=True, exist_ok=True)
    ass = proj.work / "lyrics.ass"
    vf = []
    if ass.exists():
        vf.append(f"ass={ass}:fontsdir={FONTS_DIR}")
    if t_from > 0:
        vf.insert(0, f"setpts=PTS+{t_from}/TB")
        vf.append("setpts=PTS-STARTPTS")
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
           "-ss", str(t_from), "-t", str(t_to - t_from), "-i", str(audio)]
    if vf:
        cmd += ["-vf", ",".join(vf)]
    cmd += ["-c:v", b["vcodec"], "-preset", b["preset"], "-crf", str(b["crf"]), "-pix_fmt", b["pix_fmt"],
            "-profile:v", "high", "-maxrate", "24M", "-bufsize", "48M", "-r", str(fps), "-g", str(fps * 2), "-bf", "2", "-movflags", "+faststart",
            "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
            "-c:a", b["acodec"], "-b:a", b["abitrate"], "-ar", str(b["sample_rate"]), "-shortest", str(out)]
    run(cmd)
    log(f"vídeo: {out}")
    return out
