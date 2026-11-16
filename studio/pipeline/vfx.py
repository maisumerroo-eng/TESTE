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
