"""Cenas de efeito 100% procedurais (originais, sem personagem desenhado), usadas como 'momentos de animação'
ligados a palavras da letra. Renderizadas em meia resolução e ampliadas (rápido).

  vortex   — esfera que suga partículas em espiral (ex.: "azul")
  burst    — esfera que explode para fora com anel de choque (ex.: "vermelho")
  merge    — duas esferas colidem e viram um feixe que atravessa a tela (ex.: "roxo")
  void     — espaço infinito: estrelas em dobra + glifos passando (ex.: "domínio", "vazio")
  iris     — macro de uma íris brilhante girando (ex.: "olhos")
  barrier  — partículas desaceleram e param antes de tocar o centro (ex.: "infinito", "tocar")
"""
from __future__ import annotations

import math

import cv2
import numpy as np

from .fx import H, W

w, h = W // 2, H // 2
CX, CY = w / 2, h / 2

KEYWORDS = {
    "azul": "vortex", "blue": "vortex", "vermelho": "burst", "red": "burst", "roxo": "merge", "purple": "merge",
    "dominio": "void", "expansao": "void", "vazio": "void", "infinita": "void", "informacao": "void",
    "olhos": "iris", "olho": "iris", "eyes": "iris", "olhar": "iris",
    "infinito": "barrier", "limitless": "barrier", "tocar": "barrier", "atravessar": "barrier",
}


def _glow(layer: np.ndarray, s1=4, s2=14) -> np.ndarray:
    return cv2.add(layer, cv2.add(cv2.GaussianBlur(layer, (0, 0), s1), cv2.GaussianBlur(layer, (0, 0), s2)))


def _sphere(layer, x, y, r, color, core=(255, 255, 255)):
    if r < 1:
        return layer
    cv2.circle(layer, (int(x), int(y)), int(r * 1.6), tuple(int(c * 0.35) for c in color), -1, cv2.LINE_AA)
    cv2.circle(layer, (int(x), int(y)), int(r), color, -1, cv2.LINE_AA)
    cv2.circle(layer, (int(x), int(y)), max(1, int(r * 0.45)), core, -1, cv2.LINE_AA)
    return layer


_NOISE = None


def _noise_tex(S=256):
    global _NOISE
    if _NOISE is None:
        rng = np.random.default_rng(21)
        acc = np.zeros((S, S), np.float32)
        for k, amp in ((4, 1.0), (8, 0.5), (16, 0.25), (32, 0.12)):
            n = rng.random((k, k)).astype(np.float32)
            n = np.tile(n, (2, 2))
            n = cv2.resize(n, (S * 2, S * 2), interpolation=cv2.INTER_CUBIC)[S // 2:S // 2 + S, S // 2:S // 2 + S]
            acc += amp * n
        acc = (acc - acc.min()) / (acc.max() - acc.min())
        _NOISE = acc
    return _NOISE


_POLAR = {}


def _polar(cx, cy):
    key = (int(cx), int(cy))
    if key not in _POLAR:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        _POLAR[key] = (np.arctan2(yy - cy, xx - cx), np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2))
    return _POLAR[key]


def cursed_aura(t, cx, cy, R, thick, colors, speed=1.0, inward=False, lobes=7.0, rise=0.9):
    """Energia amaldiçoada em cel-shading: línguas de chama subindo em volta de um núcleo,
    3 tons chapados + contorno de tinta grosso. Retorna (rgb, alfa)."""
    N = _noise_tex()
    S = N.shape[0]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    # chamas sobem: o campo é esticado para cima e rola com o tempo
    dy = (yy - cy)
    up = np.clip(-dy / max(1, thick * 2.2), 0, 1)  # acima do centro = mais alcance
    rad = np.sqrt((xx - cx) ** 2 + (dy * (1 - 0.45 * rise * (dy < 0))) ** 2)
    sgn = -1 if inward else 1
    u = (np.abs(xx - cx) * 0.6 + 7) % S  # espelhado: aura simétrica
    v = (yy * 0.32 + sgn * t * speed * 95) % S
    n1 = cv2.remap(N, u, v, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
    n2 = cv2.remap(N, (xx * 1.1 + 91) % S, (yy * 0.7 + sgn * t * speed * 150) % S, cv2.INTER_LINEAR,
                   borderMode=cv2.BORDER_WRAP)
    n = 0.6 * n1 + 0.4 * n2
    d = (rad - R) / np.maximum(1.0, thick * (1 + 0.8 * up))
    fall = np.clip(1 - d, 0, 1) ** 1.2
    val = n * fall * 1.7 + 0.25 * np.clip(1 - rad / max(1, R), 0, 1)
    c_dark, c_mid, c_hi = colors
    out = np.zeros((h, w, 3), np.uint8)
    m1, m2, m3 = val > 0.46, val > 0.70, val > 0.92
    out[m1] = c_dark
    out[m2] = c_mid
    out[m3] = c_hi
    alpha = m1.astype(np.uint8) * 255
    edge = cv2.morphologyEx(alpha, cv2.MORPH_GRADIENT, np.ones((5, 5), np.uint8))
    inner = cv2.morphologyEx((m2 * 255).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
    out[inner > 0] = c_dark
    out[edge > 0] = (8, 6, 14)  # tinta
    return out, alpha


_LINES = {}


def speed_bg(color, seed=0):
    """Fundo de mangá: linhas de velocidade radiais finas + retícula."""
    if (color, seed) not in _LINES:
        img = np.zeros((h, w, 3), np.uint8)
        rng = np.random.default_rng(seed)
        for _ in range(160):
            a = rng.uniform(0, 2 * np.pi)
            r0 = rng.uniform(150, 260)
            cv2.line(img, (int(CX + r0 * math.cos(a)), int(CY + r0 * math.sin(a))),
                     (int(CX + 900 * math.cos(a)), int(CY + 900 * math.sin(a))),
                     tuple(int(c * 0.22) for c in color), int(rng.integers(1, 3)), cv2.LINE_AA)
        _LINES[(color, seed)] = img
    return _LINES[(color, seed)]


def screentone(img, color, spacing=7, amount=0.18):
    yy, xx = np.mgrid[0:img.shape[0], 0:img.shape[1]]
    dots = ((xx % spacing - spacing / 2) ** 2 + (yy % spacing - spacing / 2) ** 2) < (spacing * 0.28) ** 2
    out = img.copy()
    out[dots] = (out[dots] * (1 - amount) + np.array(color) * amount).astype(np.uint8)
    return out


def black_sparks(layer, t, cx, cy, seed, color=(230, 20, 40), n=6, reach=300):
    """Faíscas pretas grossas com borda vermelha brilhante (raio de impacto)."""
    rng = np.random.default_rng(seed + int(t * 20))
    glow = np.zeros_like(layer)
    for _ in range(n):
        a = rng.uniform(0, 2 * np.pi)
        x, y = cx, cy
        pts = [(x, y)]
        for _ in range(5):
            a += rng.choice([-1, 1]) * rng.uniform(0.5, 1.2)
            step = rng.uniform(reach / 7, reach / 3.5)
            x, y = x + step * math.cos(a), y + step * math.sin(a)
            pts.append((x, y))
        p = np.array(pts, np.int32)
        cv2.polylines(glow, [p], False, color, 16, cv2.LINE_AA)
        cv2.polylines(layer, [p], False, color, 11, cv2.LINE_AA)
        cv2.polylines(layer, [p], False, (6, 0, 6), 6, cv2.LINE_AA)
    return cv2.add(cv2.GaussianBlur(glow, (0, 0), 6), layer)


def _comp(base, rgb, alpha):
    m = cv2.merge([alpha, alpha, alpha])
    return cv2.add(cv2.multiply(base, 255 - m, scale=1 / 255), cv2.multiply(rgb, m, scale=1 / 255))


class VFX:
    def __init__(self, kind: str, seed: int, prim, sec, dark):
        self.kind = kind
        self.rng = np.random.default_rng(seed)
        self.prim, self.sec, self.dark = tuple(map(int, prim)), tuple(map(int, sec)), tuple(map(int, dark))
        n = 900
        self.a0 = self.rng.uniform(0, 2 * np.pi, n)
        self.r0 = self.rng.uniform(60, 520, n)
        self.sp = self.rng.uniform(0.6, 1.6, n)
        self.sz = self.rng.uniform(0.6, 2.2, n)
        if kind == "iris":
            self.iris = self._iris_tex()
        if kind == "void":
            self.stars = self.rng.uniform(-1, 1, (1400, 3))
            self.glyphs = [chr(c) for c in list(range(0x16A0, 0x16F0))]  # runas (combina com a capa)
        y = np.linspace(0, 1, h)[:, None, None]
        self.bg = np.repeat((np.array(self.dark, np.float32) * (0.6 + 0.4 * y)).astype(np.uint8), w, 1)

    def _iris_tex(self):
        S = 700
        tex = np.zeros((S, S, 3), np.uint8)
        c = S // 2
        for _ in range(2600):
            a = self.rng.uniform(0, 2 * np.pi)
            r0, r1 = self.rng.uniform(70, 130), self.rng.uniform(220, 330)
            col = tuple(int(v) for v in (np.array(self.prim) * self.rng.uniform(0.5, 1.3)).clip(0, 255))
            cv2.line(tex, (int(c + r0 * math.cos(a)), int(c + r0 * math.sin(a))),
                     (int(c + r1 * math.cos(a)), int(c + r1 * math.sin(a))), col, 1, cv2.LINE_AA)
        cv2.circle(tex, (c, c), 332, tuple(int(v * 0.5) for v in self.prim), 6, cv2.LINE_AA)
        tex = cv2.addWeighted(tex, 1.0, cv2.GaussianBlur(tex, (0, 0), 6), 0.6, 0)
        cv2.circle(tex, (c, c), 95, (5, 5, 10), -1, cv2.LINE_AA)
        cv2.circle(tex, (c - 120, c - 140), 34, (255, 255, 255), -1, cv2.LINE_AA)
        return tex

    def frame(self, rel: float, dur: float, pulse: float = 0.0) -> np.ndarray:
        rel = max(0.0, rel)
        p = min(1.0, rel / max(0.01, dur))
        layer = np.zeros((h, w, 3), np.uint8)
        k = self.kind
        if k == "vortex":
            ang = self.a0 + rel * 3.0 * self.sp + 6 / (0.3 + rel)
            r = self.r0 * np.exp(-rel * 1.4 * self.sp)
            xs, ys = CX + r * np.cos(ang), CY + r * np.sin(ang) * 0.85
            for x, y, s in zip(xs, ys, self.sz):
                cv2.circle(layer, (int(x), int(y)), int(s), self.prim, -1)
            _sphere(layer, CX, CY, 34 + 10 * pulse + 6 * math.sin(rel * 9), self.prim)
        elif k == "burst":
            r = (self.r0 * 0.15) + (rel * 420 * self.sp)
            xs, ys = CX + r * np.cos(self.a0), CY + r * np.sin(self.a0)
            for x, y, s in zip(xs, ys, self.sz):
                cv2.circle(layer, (int(x), int(y)), int(s + 0.5), self.prim, -1)
            ring = int(30 + p * 700)
            cv2.circle(layer, (int(CX), int(CY)), ring, self.prim, max(1, int(10 * (1 - p))), cv2.LINE_AA)
            _sphere(layer, CX, CY, 40 * (1 + 0.6 * pulse) * (1 - 0.5 * p), self.prim)
        elif k == "merge":
            blue, red = (90, 170, 255), (255, 50, 60)
            purple = (170, 80, 255)
            if p < 0.45:
                q = p / 0.45
                d = 300 * (1 - q ** 1.5)
                _sphere(layer, CX - d, CY, 30, blue)
                _sphere(layer, CX + d, CY, 30, red)
            else:
                q = (p - 0.45) / 0.55
                r = 40 + 30 * math.sin(q * 3.14)
                x = CX + q ** 2 * (w * 0.9)
                poly = np.array([(CX - 20, CY), (x - r, CY - r * 0.9), (x, CY - r * 1.1), (x, CY + r * 1.1),
                                 (x - r, CY + r * 0.9)], np.int32)
                cv2.fillPoly(layer, [poly], tuple(int(c * 0.6) for c in purple), cv2.LINE_AA)
                _sphere(layer, x, CY, r * 1.4, purple)
            for x, y, s in zip(CX + self.r0 * np.cos(self.a0 + rel), CY + self.r0 * 0.5 * np.sin(self.a0 + rel), self.sz):
                cv2.circle(layer, (int(x), int(y)), int(s * 0.6 + 0.5), purple, -1)
        elif k == "void":
            z = (self.stars[:, 2] - rel * 0.55) % 2 - 1 + 1.05
            xs = CX + self.stars[:, 0] / z * w * 0.5
            ys = CY + self.stars[:, 1] / z * h * 0.5
            x2 = CX + self.stars[:, 0] / (z + 0.08) * w * 0.5
            y2 = CY + self.stars[:, 1] / (z + 0.08) * h * 0.5
            for xa, ya, xb, yb, zz in zip(xs, ys, x2, y2, z):
                b = int(min(255, 120 / zz))
                cv2.line(layer, (int(xa), int(ya)), (int(xb), int(yb)), (b, b, min(255, b + 40)), 1, cv2.LINE_AA)
        elif k == "iris":
            S = self.iris.shape[0]
            M = cv2.getRotationMatrix2D((S / 2, S / 2), rel * 12, 0.7 + 0.25 * p + 0.04 * pulse)
            M[0, 2] += CX - S / 2
            M[1, 2] += CY - S / 2
            layer = cv2.warpAffine(self.iris, M, (w, h))
            S2 = self.iris.shape[0]
            if not hasattr(self, "_imask"):
                self._imask = np.zeros((S2, S2), np.uint8)
                cv2.circle(self._imask, (S2 // 2, S2 // 2), 336, 255, -1, cv2.LINE_AA)
            self._iris_alpha = cv2.warpAffine(self._imask, M, (w, h))
        elif k == "barrier":
            R = 70
            t = rel * self.sp
            r = R + (self.r0) * np.exp(-t * 2.2)
            xs, ys = CX + r * np.cos(self.a0), CY + r * np.sin(self.a0)
            for x, y, s in zip(xs, ys, self.sz):
                cv2.circle(layer, (int(x), int(y)), int(s + 0.5), (230, 240, 255), -1)
            cv2.circle(layer, (int(CX), int(CY)), R, self.prim, 1 + int(2 * pulse), cv2.LINE_AA)
        return self._stylize(layer, rel, p, pulse)

    def _stylize(self, layer, rel, p, pulse):
        """Pós de anime: fundo com retícula, aura amaldiçoada em cel-shading, partículas com brilho,
        posterização e contorno."""
        k = self.kind
        prim = np.array(self.prim)
        hi = tuple(int(v) for v in np.clip(prim * 0.4 + 255 * 0.6, 0, 255))
        dark = tuple(int(v) for v in np.clip(np.array(self.sec) * 0.8, 0, 255))
        base = screentone(cv2.add(self.bg, speed_bg(self.sec, 3)), self.sec, 8, 0.22)
        R, thick, inward, col = 60, 150, False, (dark, self.prim, hi)
        if k == "vortex":
            R, thick, inward = 45 + 10 * pulse, 190, True
        elif k == "burst":
            red = (230, 40, 50)
            col = ((90, 10, 20), red, (255, 200, 190))
            R, thick = 40 + p * 160, 170 + 80 * pulse
        elif k == "merge":
            col = ((60, 20, 110), (170, 80, 255), (240, 210, 255))
            R, thick = 50 + 40 * p, 210
        elif k == "barrier":
            R, thick = 68, 45 + 25 * pulse
        elif k == "iris":
            R, thick = 700 * 0.47 * (0.7 + 0.25 * p), 70
        elif k == "void":
            R, thick = 30, 140
        aura, a = cursed_aura(rel, CX, CY, R, thick, col, speed=1.3 if k != "void" else 0.4, inward=inward)
        if k == "iris":  # chama atrás do olho, olho por cima
            out = _comp(base, aura, a)
            out = _comp(out, layer, self._iris_alpha)
        else:
            out = cv2.add(base, _glow(layer, 3, 10)) if k == "void" else base
            out = _comp(out, aura, a)
            if k != "void":
                out = cv2.add(out, _glow(layer, 3, 10))
        if k in ("burst", "merge") and p < 0.35:
            out = cv2.add(out, black_sparks(np.zeros_like(out), rel, CX, CY, 3, (230, 30, 40), 5, 380))
        # posterização (tons chapados de anime)
        out = (out // 32) * 32 + 16
        out = cv2.resize(out, (W, H), interpolation=cv2.INTER_LINEAR)
        return out


# ================= cenas abstratas filosóficas (originais) =================
CYAN = (40, 230, 255)


def _base(sec, seed=3):
    bg = np.zeros((h, w, 3), np.uint8)
    bg[:] = (6, 7, 14)
    return screentone(cv2.add(bg, speed_bg(sec, seed)), sec, 8, 0.16)


def draw_eye(canvas, openness, look=(0.0, 0.0), scale=1.0, glow=1.0, iris_rot=0.0):
    """Olho estilo anime (original): pálpebra superior grossa com cílios, íris ciano em 3 tons chapados,
    dois brilhos. openness 0..1."""
    L, A, B = 300 * scale, 120 * scale, 70 * scale
    xs = np.linspace(-L, L, 120)
    o = max(0.02, openness)
    up = [(CX + x, CY - A * o * (1 - (x / L) ** 2) ** 0.8 + 18 * scale * (x / L)) for x in xs]
    lo = [(CX + x, CY + B * o * (1 - (x / L) ** 2) ** 1.2 + 8 * scale * (x / L)) for x in xs]
    poly = np.array(up + lo[::-1], np.int32)
    mask = np.zeros((h, w), np.uint8)
    cv2.fillPoly(mask, [poly], 255, cv2.LINE_AA)
    eye = np.zeros((h, w, 3), np.uint8)
    eye[:] = (215, 230, 245)
    ix, iy = CX + look[0] * 80 * scale, CY + look[1] * 30 * scale
    r = 105 * scale
    cv2.circle(eye, (int(ix), int(iy)), int(r), (10, 70, 140), -1, cv2.LINE_AA)
    cv2.circle(eye, (int(ix), int(iy)), int(r * 0.86), (20, 150, 230), -1, cv2.LINE_AA)
    cv2.ellipse(eye, (int(ix), int(iy + r * 0.25)), (int(r * 0.7), int(r * 0.45)), 0, 0, 360, CYAN, -1, cv2.LINE_AA)
    for k in range(24):  # estrias da íris
        a = iris_rot + k * 2 * math.pi / 24
        cv2.line(eye, (int(ix + r * 0.35 * math.cos(a)), int(iy + r * 0.35 * math.sin(a))),
                 (int(ix + r * 0.8 * math.cos(a)), int(iy + r * 0.8 * math.sin(a))), (150, 250, 255), 1, cv2.LINE_AA)
    cv2.circle(eye, (int(ix), int(iy)), int(r * 0.3), (4, 10, 30), -1, cv2.LINE_AA)
    cv2.circle(eye, (int(ix), int(iy)), int(r), (5, 20, 50), 4, cv2.LINE_AA)
    cv2.ellipse(eye, (int(ix - r * 0.38), int(iy - r * 0.4)), (int(r * 0.2), int(r * 0.13)), -30, 0, 360,
                (255, 255, 255), -1, cv2.LINE_AA)
    cv2.circle(eye, (int(ix + r * 0.35), int(iy + r * 0.38)), int(r * 0.07), (255, 255, 255), -1, cv2.LINE_AA)
    # sombra da pálpebra no topo do olho
    shade = np.zeros((h, w), np.uint8)
    cv2.polylines(shade, [np.array(up, np.int32)], False, 255, int(30 * scale))
    eye[shade > 0] = (eye[shade > 0] * 0.55).astype(np.uint8)
    g = cv2.GaussianBlur((mask > 0).astype(np.uint8) * 255, (0, 0), 1)
    canvas = _comp(canvas, eye, g)
    # brilho ciano saindo do olho (energia)
    if glow > 0:
        gl = np.zeros_like(canvas)
        cv2.circle(gl, (int(ix), int(iy)), int(r * 1.4), CYAN, -1)
        gl = cv2.GaussianBlur(gl, (0, 0), 40 * scale)
        gl = cv2.multiply(gl, cv2.merge([mask // 2 + 40] * 3), scale=1 / 255)
        canvas = cv2.add(canvas, (gl * glow).astype(np.uint8))
    # pálpebra superior + cílios (tinta)
    cv2.polylines(canvas, [np.array(up, np.int32)], False, (8, 8, 16), int(14 * scale), cv2.LINE_AA)
    for k in range(9):
        x, y = up[60 + k * 6]
        ang = -0.4 - 0.12 * k
        cv2.line(canvas, (int(x), int(y)), (int(x + 55 * scale * math.cos(ang)), int(y - 30 * scale - 6 * k * scale)),
                 (8, 8, 16), int(6 * scale), cv2.LINE_AA)
    cv2.polylines(canvas, [np.array(lo, np.int32)], False, (30, 30, 50), int(3 * scale), cv2.LINE_AA)
    return canvas


def _blink(rel, dur, mode, pulse):
    if mode == "open":
        return fx_ease_out(min(1, rel / max(0.3, dur * 0.6)))
    if mode == "close":
        return 1 - fx_ease_out(min(1, rel / max(0.3, dur * 0.8)))
    # piscada no meio do plano
    c = dur * 0.55
    d = abs(rel - c)
    return 1.0 if d > 0.12 else d / 0.12


def fx_ease_out(p):
    return 1 - (1 - p) ** 3


def _sky(rel, p):
    """Câmera subindo pelo céu: nuvens chapadas descendo, céu escurece até virar espaço."""
    y = np.linspace(0, 1, h)[:, None, None]
    q = min(1.0, max(0.0, (p - 0.45) / 0.55))
    top = np.array((40, 80, 170), np.float32) * (1 - q) + np.array((4, 4, 12), np.float32) * q
    bot = np.array((150, 205, 255), np.float32) * (1 - q) + np.array((25, 20, 70), np.float32) * q
    img = np.repeat((top * (1 - y) + bot * y).astype(np.uint8), w, 1)
    rng = np.random.default_rng(5)
    for _ in range(int(320 * q)):
        cv2.circle(img, (int(rng.uniform(0, w)), int(rng.uniform(0, h))), 1, (230, 240, 255), -1)
    N = _noise_tex()
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    n = cv2.remap(N, (xx * 0.35) % 256, (yy * 0.45 - rel * 220) % 256, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
    fade = 1 - q
    if fade > 0.05:
        cl1, cl2 = n > 0.64, (n > 0.56) & (n <= 0.64)
        img[cl1] = (np.array((245, 248, 255)) * fade + img[cl1] * (1 - fade)).astype(np.uint8)
        img[cl2] = (np.array((170, 200, 240)) * fade + img[cl2] * (1 - fade)).astype(np.uint8)
        edge = cv2.morphologyEx(cl1.astype(np.uint8) * 255, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8))
        img[edge > 0] = (90, 120, 170)
    return img


class Abstract:
    """Cenas conceituais. Cada uma é um 'plano' de 0,5–3 s ligado à letra."""

    def __init__(self, kind, seed, prim, sec, dark):
        self.kind, self.seed = kind, seed
        self.prim, self.sec = tuple(map(int, prim)), tuple(map(int, sec))
        self.rng = np.random.default_rng(seed)
        self.parts = self.rng.uniform(-1, 1, (500, 3))
        self.vfx = VFX("iris", seed, prim, sec, dark) if kind == "six" else None

    def frame(self, rel, dur, pulse=0.0):
        rel = max(0.0, rel)
        p = min(1.0, rel / max(0.01, dur))
        k = self.kind
        c = _base(self.sec, self.seed % 5)
        if k in ("eye", "eye_open", "eye_close"):
            mode = {"eye": "blink", "eye_open": "open", "eye_close": "close"}[k]
            op = _blink(rel, dur, mode, pulse)
            sc = 1.0 + 0.12 * p + 0.03 * pulse
            look = (0.25 * math.sin(rel * 1.3 + self.seed), 0.0) if k == "eye" else (0, 0)
            aura, a = cursed_aura(rel, CX, CY + 20, 255 * sc, 55 + 20 * pulse,
                                  ((10, 40, 90), (30, 150, 230), (150, 240, 255)), 0.8, rise=0.3)
            c = _comp(c, aura, a)
            c = draw_eye(c, op, look, sc, 0.6 + pulse, rel * 0.4)
        elif k == "six":  # mergulho na íris -> galáxia dentro da pupila
            f = self.vfx.frame(rel, dur, pulse)
            f = cv2.resize(f, (w, h))
            z = 0.85 + 2.6 * p ** 2.2
            M = cv2.getRotationMatrix2D((CX, CY), rel * 25, z)
            c = cv2.warpAffine(f, M, (w, h))
            if p > 0.55:
                st = np.zeros_like(c)
                for x, y, zz in self.parts:
                    zz2 = (zz - rel * 0.7) % 2 - 1 + 1.05
                    cv2.circle(st, (int(CX + x / zz2 * w * 0.5), int(CY + y / zz2 * h * 0.5)), 1, (220, 240, 255), -1)
                q = (p - 0.55) / 0.45
                c = cv2.addWeighted(c, 1 - q, cv2.add(st, _base(self.sec)), q, 0)
        elif k == "infinity":  # ∞ de luz percorrido sem fim
            pts = []
            for i in range(240):
                tt = i / 240 * 2 * math.pi
                s = 1 + math.sin(tt) ** 2
                pts.append((CX + 300 * math.cos(tt) / s, CY + 150 * math.sin(tt) * math.cos(tt) / s))
            pts = np.array(pts, np.int32)
            lay = np.zeros_like(c)
            cv2.polylines(lay, [pts], True, (20, 90, 160), 10, cv2.LINE_AA)
            cv2.polylines(lay, [pts], True, CYAN, 3, cv2.LINE_AA)
            head = int((rel * 90) % 240)
            for j in range(40):
                x, y = pts[(head - j) % 240]
                cv2.circle(lay, (int(x), int(y)), max(1, 9 - j // 5), (230, 255, 255), -1, cv2.LINE_AA)
            for i in range(6):  # anéis que se aproximam e nunca chegam
                r = 40 + 400 * (0.5 ** (rel * 1.5 + i * 0.6))
                cv2.circle(lay, (int(CX), int(CY)), int(r), (40, 120, 200), 1, cv2.LINE_AA)
            c = cv2.add(c, _glow(lay, 3, 12))
        elif k == "sky":
            c = _sky(rel, fx_ease_out(p))
        elif k == "blood":
            c[:] = (238, 236, 232)
            c = screentone(c, (180, 170, 170), 7, 0.25)
            for i in range(7):
                rr = np.random.default_rng(self.seed + i)
                x = rr.uniform(0.2, 0.8) * w
                t0 = rr.uniform(0, 0.5) * dur
                y = (rel - t0) * 900 - 40
                if y < 0:
                    continue
                if y < h * 0.62:
                    cv2.ellipse(c, (int(x), int(y)), (10, 16), 0, 0, 360, (150, 0, 15), -1, cv2.LINE_AA)
                else:
                    sp = min(1, (y - h * 0.62) / 200)
                    cv2.ellipse(c, (int(x), int(h * 0.65)), (int(20 + 70 * sp), int(8 + 18 * sp)), 0, 0, 360,
                                (120, 0, 12), -1, cv2.LINE_AA)
                    for a in range(6):
                        an = a / 6 * math.pi + math.pi
                        cv2.circle(c, (int(x + 90 * sp * math.cos(an)), int(h * 0.65 + 40 * sp * math.sin(an))),
                                   4, (150, 0, 15), -1, cv2.LINE_AA)
        elif k == "rewind":  # estilhaços voltando (reversão)
            q = 1 - fx_ease_out(p)
            lay = np.zeros_like(c)
            for x, y, z in self.parts[:220]:
                px, py = CX + x * 60 + x * 520 * q, CY + y * 60 + y * 300 * q
                poly = np.array([(px, py), (px + 14 * z, py + 6), (px + 4, py + 16 * abs(z) + 3)], np.int32)
                cv2.fillPoly(lay, [poly], CYAN if z > 0 else (200, 220, 255), cv2.LINE_AA)
            for i in range(12):  # ponteiros girando para trás
                a = -rel * 3 + i * math.pi / 6
                cv2.line(lay, (int(CX + 200 * math.cos(a)), int(CY + 200 * math.sin(a))),
                         (int(CX + 230 * math.cos(a)), int(CY + 230 * math.sin(a))), (120, 200, 255), 2, cv2.LINE_AA)
            c = cv2.add(c, _glow(lay, 2, 8))
        elif k == "bond":  # duas luzes que orbitam e se separam
            lay = np.zeros_like(c)
            sep = max(0, (p - 0.55) / 0.45)
            a = rel * 2.4
            d = 90 + 520 * sep ** 1.5
            x1, y1 = CX + d * math.cos(a), CY + d * 0.4 * math.sin(a)
            x2, y2 = CX - d * math.cos(a), CY - d * 0.4 * math.sin(a)
            _sphere(lay, x1, y1, 26, CYAN)
            _sphere(lay, x2, y2, 26 * (1 - 0.6 * sep), tuple(int(v * (1 - 0.7 * sep)) for v in (150, 70, 230)))
            if sep == 0:
                cv2.line(lay, (int(x1), int(y1)), (int(x2), int(y2)), (90, 110, 200), 1, cv2.LINE_AA)
            c = cv2.add(c, _glow(lay, 4, 18))
        elif k == "alone":
            c[:] = (3, 4, 9)
            lay = np.zeros_like(c)
            _sphere(lay, CX, CY + 60, 7 + 2 * pulse, CYAN)
            for x, y, z in self.parts[:160]:
                yy = (y * h + rel * 30 * (1 + z)) % h
                cv2.circle(lay, (int(CX + x * w / 2), int(yy)), 1, (90, 110, 150), -1)
            c = cv2.add(c, _glow(lay, 3, 16))
        elif k == "cube":  # cubo de luz fechando (selamento)
            lay = np.zeros_like(c)
            s = 380 * (1 - 0.65 * fx_ease_out(p))
            ay, ax = rel * 1.3, 0.5 + rel * 0.4
            V = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
            P = []
            for x, y, z in V:
                X = x * math.cos(ay) + z * math.sin(ay)
                Z = -x * math.sin(ay) + z * math.cos(ay)
                Y = y * math.cos(ax) - Z * math.sin(ax)
                Z = y * math.sin(ax) + Z * math.cos(ax)
                f = 3.5 / (3.5 + Z)
                P.append((int(CX + X * s * f), int(CY + Y * s * f)))
            for i in range(8):
                for j in range(i + 1, 8):
                    if sum(a != b for a, b in zip(V[i], V[j])) == 1:
                        cv2.line(lay, P[i], P[j], CYAN, 3, cv2.LINE_AA)
            c = cv2.add(c, _glow(lay, 3, 12))
        elif k == "slash":  # corte que separa o espaço
            st = _base(self.sec, 7)
            for x, y, z in self.parts:
                cv2.circle(st, (int(CX + x * w / 2), int(CY + y * h / 2)), 1, (210, 220, 255), -1)
            q = fx_ease_out(min(1, max(0, (p - 0.25) / 0.6)))
            yy, xx = np.mgrid[0:h, 0:w]
            side = (yy - CY) * 1.0 - (xx - CX) * 0.45 > 0
            M1 = np.float32([[1, 0, -40 * q], [0, 1, -60 * q]])
            M2 = np.float32([[1, 0, 40 * q], [0, 1, 60 * q]])
            a1, a2 = cv2.warpAffine(st, M1, (w, h)), cv2.warpAffine(st, M2, (w, h))
            c = np.where(side[..., None], a2, a1).astype(np.uint8)
            if p > 0.15:
                lay = np.zeros_like(c)
                x0, x1 = -50, w + 50
                cv2.line(lay, (x0, int(CY + (x0 - CX) * 0.45)), (x1, int(CY + (x1 - CX) * 0.45)), (255, 255, 255),
                         max(1, int(6 * (1 - q) + 1)), cv2.LINE_AA)
                c = cv2.add(c, _glow(lay, 3, 10))
        elif k == "wheel":  # roda de oito raios que gira e "trava" no tempo
            lay = np.zeros_like(c)
            steps = int(rel / 0.4)
            a0 = steps * math.pi / 8 + min(1, (rel % 0.4) / 0.12) * math.pi / 8
            cv2.circle(lay, (int(CX), int(CY)), 170, (200, 180, 120), 6, cv2.LINE_AA)
            cv2.circle(lay, (int(CX), int(CY)), 30, (200, 180, 120), -1, cv2.LINE_AA)
            for i in range(8):
                a = a0 + i * math.pi / 4
                cv2.line(lay, (int(CX), int(CY)), (int(CX + 210 * math.cos(a)), int(CY + 210 * math.sin(a))),
                         (200, 180, 120), 7, cv2.LINE_AA)
                cv2.circle(lay, (int(CX + 210 * math.cos(a)), int(CY + 210 * math.sin(a))), 12, (230, 210, 150), -1)
            c = cv2.add(c, _glow(lay, 2, 10))
        elif k == "crack":  # o mundo racha a partir do centro
            lay = np.zeros_like(c)
            rng = np.random.default_rng(self.seed)
            q = fx_ease_out(p)
            for _ in range(14):
                a = rng.uniform(0, 2 * math.pi)
                x, y = CX, CY
                pts = [(x, y)]
                for _ in range(8):
                    a += rng.normal(0, 0.35)
                    st = rng.uniform(30, 70) * q
                    x, y = x + st * math.cos(a), y + st * math.sin(a)
                    pts.append((x, y))
                cv2.polylines(lay, [np.array(pts, np.int32)], False, (220, 240, 255), 2, cv2.LINE_AA)
            c = cv2.add(c, _glow(lay, 2, 9))
            c = cv2.warpAffine(c, np.float32([[1, 0, 6 * pulse * math.sin(rel * 50)], [0, 1, 0]]), (w, h))
        c = (c // 32) * 32 + 16  # tons chapados
        return cv2.resize(c, (W, H), interpolation=cv2.INTER_LINEAR)


ABSTRACT_KINDS = {"eye", "eye_open", "eye_close", "six", "infinity", "sky", "blood", "rewind", "bond", "alone",
                  "cube", "slash", "wheel", "crack"}

KEYWORDS.update({
    "ceu": "sky", "limite": "sky", "alem": "sky", "acima": "sky",
    "olhos": "eye", "olho": "eye", "olhar": "eye_open", "eyes": "six", "six": "six", "seis": "six",
    "enxergando": "six", "realidade": "six", "visao": "six",
    "nasce": "eye_open", "nascimento": "eye_open", "diferente": "eye_open", "percebeu": "eye",
    "equilibrio": "crack", "tremeu": "crack", "sociedade": "crack", "mudou": "crack",
    "sangue": "blood", "raro": "blood", "corpo": "blood",
    "infinito": "infinity", "limitless": "infinity", "infinir": "infinity",
    "reverter": "rewind", "sofri": "rewind", "aprendi": "rewind", "voltar": "rewind",
    "parceiro": "bond", "jovens": "bond", "dois": "bond", "caminho": "bond", "acompanhei": "bond",
    "escolheu": "bond", "perdeu": "bond", "perdi": "bond",
    "sozinho": "alone", "liberdade": "alone", "verdade": "alone", "salvar": "alone", "escolher": "alone",
    "prisao": "cube", "plano": "cube", "amigo": "cube", "selado": "cube",
    "adapta": "wheel", "mahoraga": "wheel", "mauraga": "wheel",
    "corte": "slash", "espaco": "slash", "atravessa": "slash",
    "fracasso": "eye_close", "fim": "eye_close", "desabe": "eye_close",
    "sorriso": "eye", "aula": "eye", "monstros": "eye", "forte": "eye_open",
    "controlo": "vortex", "poder": "vortex", "absurdo": "vortex",
})
