"""Primitivas de efeito visual (numpy/OpenCV), todas em frames uint8 RGB 1920x1080.

Câmera: cover-fit, zoom/pan/rotação, shake, parallax 2.5D por mapa de profundidade.
Efeitos: RGB split, aberração cromática, glitch, flash, inversão, motion blur, speed lines,
partículas (brasas), raios, light leak, grão, vinheta, scanlines, color grade por personagem.
"""
from __future__ import annotations

import math
from functools import lru_cache

import cv2
import numpy as np

W, H = 1920, 1080


# ---------- utilidades ----------
def cover(img: np.ndarray, w=W, h=H, margin=1.0) -> np.ndarray:
    """Redimensiona preenchendo w x h (corta sobras). margin>1 deixa folga para movimento."""
    ih, iw = img.shape[:2]
    s = max(w * margin / iw, h * margin / ih)
    nw, nh = int(math.ceil(iw * s)), int(math.ceil(ih * s))
    interp = cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC
    r = cv2.resize(img, (nw, nh), interpolation=interp)
    x, y = (nw - int(w * margin)) // 2, (nh - int(h * margin)) // 2
    return r[y:y + int(h * margin), x:x + int(w * margin)]


def ease(p: float, kind="inout") -> float:
    p = min(1.0, max(0.0, p))
    if kind == "in":
        return p * p * p
    if kind == "out":
        return 1 - (1 - p) ** 3
    if kind == "expo_out":
        return 1 - 2 ** (-10 * p) if p < 1 else 1.0
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2


def camera(img: np.ndarray, zoom=1.0, dx=0.0, dy=0.0, rot=0.0) -> np.ndarray:
    """img já em resolução >= tela. zoom relativo à tela, dx/dy em px de tela, rot em graus."""
    ih, iw = img.shape[:2]
    cx, cy = iw / 2, ih / 2
    s = zoom * max(W / iw, H / ih)
    M = cv2.getRotationMatrix2D((cx, cy), rot, s)
    M[0, 2] += W / 2 - cx + dx
    M[1, 2] += H / 2 - cy + dy
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT101)


def parallax(img: np.ndarray, depth: np.ndarray, zoom=1.0, dx=0.0, dy=0.0, depth_zoom=0.0, strength=1.0):
    """2.5D: pixels próximos (depth~1) andam mais que o fundo. img/depth já em W x H (com folga)."""
    grid = _grid(img.shape[1], img.shape[0])
    gx, gy = grid
    ih, iw = img.shape[:2]
    cx, cy = iw / 2, ih / 2
    d = depth * strength
    z = zoom * (1 + depth_zoom * d)
    mx = (cx + (gx - cx) / z - dx * d).astype(np.float32)
    my = (cy + (gy - cy) / z - dy * d).astype(np.float32)
    out = cv2.remap(img, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT101)
    if out.shape[1] != W or out.shape[0] != H:
        out = cover(out)
    return out


@lru_cache(maxsize=4)
def _grid(w, h):
    return np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))


def shake_offset(t: float, hits: list[float], amp=28.0, decay=9.0, seed=0) -> tuple[float, float, float]:
    """Tremida que explode em cada hit e decai (ruído suave)."""
    e = 0.0
    for h in hits:
        if 0 <= t - h < 0.6:
            e = max(e, math.exp(-(t - h) * decay))
    if e < 0.01:
        return 0.0, 0.0, 0.0
    n = t * 37 + seed
    return (amp * e * math.sin(n * 2.1) * math.cos(n * 0.7),
            amp * e * math.sin(n * 1.7 + 1.3),
            amp * 0.04 * e * math.sin(n * 2.9))


# ---------- efeitos de cor/canal ----------
def rgb_split(f: np.ndarray, px: int) -> np.ndarray:
    if px == 0:
        return f
    out = f.copy()
    out[..., 0] = np.roll(f[..., 0], px, axis=1)
    out[..., 2] = np.roll(f[..., 2], -px, axis=1)
    return out


def chroma_aberration(f: np.ndarray, amount=0.004) -> np.ndarray:
    if amount <= 0:
        return f
    r = cv2.warpAffine(f[..., 0], cv2.getRotationMatrix2D((W / 2, H / 2), 0, 1 + amount), (W, H),
                       borderMode=cv2.BORDER_REFLECT101)
    b = cv2.warpAffine(f[..., 2], cv2.getRotationMatrix2D((W / 2, H / 2), 0, 1 - amount), (W, H),
                       borderMode=cv2.BORDER_REFLECT101)
    return np.dstack([r, f[..., 1], b])


def flash(f: np.ndarray, a: float, color=(255, 255, 255)) -> np.ndarray:
    if a <= 0:
        return f
    c = np.empty_like(f)
    c[:] = color
    return cv2.addWeighted(f, 1 - a, c, a, 0)


def invert(f: np.ndarray) -> np.ndarray:
    return 255 - f


def impact_frame(f: np.ndarray, color) -> np.ndarray:
    """Quadro de impacto estilo anime: alto contraste P&B invertido + cor do personagem."""
    g = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY)
    g = cv2.equalizeHist(g)
    _, m = cv2.threshold(g, 110, 255, cv2.THRESH_BINARY)
    out = np.zeros_like(f)
    out[m == 0] = color
    out[m > 0] = (8, 8, 10)
    return out


def glitch(f: np.ndarray, amount: float, seed: int) -> np.ndarray:
    if amount <= 0:
        return f
    rng = np.random.default_rng(seed)
    out = f.copy()
    for _ in range(int(4 + 14 * amount)):
        y = int(rng.integers(0, H - 10))
        h = int(rng.integers(6, int(20 + 90 * amount)))
        s = int(rng.integers(-1, 2) * rng.integers(20, int(40 + 220 * amount)))
        out[y:y + h] = np.roll(out[y:y + h], s, axis=1)
        if rng.random() < 0.35:
            ch = int(rng.integers(0, 3))
            out[y:y + h, :, ch] = 255 - out[y:y + h, :, ch]
    return rgb_split(out, int(12 * amount))


def motion_blur(cur: np.ndarray, prev: np.ndarray | None, a=0.45) -> np.ndarray:
    if prev is None or a <= 0:
        return cur
    return cv2.addWeighted(cur, 1 - a, prev, a, 0)


def directional_blur(f: np.ndarray, k: int, horizontal=True) -> np.ndarray:
    if k < 3:
        return f
    k = k | 1
    kern = np.zeros((k, k), np.float32)
    if horizontal:
        kern[k // 2, :] = 1.0 / k
    else:
        kern[:, k // 2] = 1.0 / k
    return cv2.filter2D(f, -1, kern)


def radial_zoom_blur(f: np.ndarray, strength=0.06, steps=5) -> np.ndarray:
    acc = f.astype(np.float32)
    for i in range(1, steps):
        s = 1 + strength * i / steps
        M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, s)
        acc += cv2.warpAffine(f, M, (W, H), borderMode=cv2.BORDER_REFLECT101)
    return (acc / steps).astype(np.uint8)


def desaturate(f: np.ndarray, a: float) -> np.ndarray:
    if a <= 0:
        return f
    g = cv2.cvtColor(cv2.cvtColor(f, cv2.COLOR_RGB2GRAY), cv2.COLOR_GRAY2RGB)
    return cv2.addWeighted(f, 1 - a, g, a, 0)


def make_grade_lut(dark_rgb, primary_rgb, strength=0.35):
    """LUT por canal: sombras puxadas para a cor 'dark' do personagem, médios levemente para 'primary',
    contraste em S. Mantém pele/rosto legíveis (força moderada)."""
    x = np.arange(256, dtype=np.float32) / 255
    s_curve = x + 0.18 * np.sin((x - 0.5) * 2 * np.pi) * -0.5 * 0.9  # leve S
    s_curve = np.clip(0.5 + (s_curve - 0.5) * 1.12, 0, 1)
    luts = []
    for c in range(3):
        sh = (1 - x) ** 2.2
        mid = np.exp(-((x - 0.5) ** 2) / 0.05)
        v = s_curve * (1 - strength * sh) + strength * sh * (dark_rgb[c] / 255) * 1.6
        v = v + strength * 0.12 * mid * (primary_rgb[c] / 255 - 0.5)
        luts.append(np.clip(v * 255, 0, 255).astype(np.uint8))
    return np.stack(luts, axis=-1).reshape(256, 1, 3)


def grade(f: np.ndarray, lut) -> np.ndarray:
    return cv2.LUT(f, lut)


# ---------- texturas globais (pré-calculadas, tudo uint8 p/ SIMD do OpenCV) ----------
@lru_cache(maxsize=1)
def _finish_mask(vig=0.55, scan=0.06):
    y, x = np.ogrid[:H, :W]
    d = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    m = 1 - vig * np.clip((d - 0.55) / 0.85, 0, 1) ** 1.6
    m = np.repeat(m[..., None], 3, 2) * np.ones((H, 1, 1))
    m[::3] *= 1 - scan
    return np.clip(m * 255, 0, 255).astype(np.uint8)


@lru_cache(maxsize=1)
def _grain_bank(n=8, amount=6):
    rng = np.random.default_rng(7)
    bank = []
    for _ in range(n):
        g = rng.normal(0, amount, (H // 2, W // 2)).astype(np.float32)
        g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)
        g3 = np.repeat(g[..., None], 3, 2)
        bank.append((np.clip(g3, 0, 255).astype(np.uint8), np.clip(-g3, 0, 255).astype(np.uint8)))
    return bank


def finish(f: np.ndarray, idx: int) -> np.ndarray:
    """Vinheta + scanlines + grão de filme em uma passada uint8."""
    out = cv2.multiply(f, _finish_mask(), scale=1 / 255)
    pos, neg = _grain_bank()[idx % 8]
    return cv2.subtract(cv2.add(out, pos), neg)


def vignette(f, strength=0.55):
    return finish(f, 0)


# ---------- overlays procedurais ----------
def speed_lines(f: np.ndarray, t: float, intensity=1.0, color=(255, 255, 255), seed=0) -> np.ndarray:
    """Linhas de velocidade radiais (mangá) convergindo para o centro."""
    if intensity <= 0:
        return f
    layer = f.copy()
    rng = np.random.default_rng(seed + int(t * 24))
    cx, cy = W / 2, H / 2
    col = tuple(int(c) for c in color)
    for _ in range(int(70 * min(1.0, intensity) + 10)):
        ang = rng.uniform(0, 2 * np.pi)
        r0 = rng.uniform(330, 520)
        p0 = (int(cx + r0 * np.cos(ang)), int(cy + r0 * np.sin(ang)))
        p1 = (int(cx + 1300 * np.cos(ang)), int(cy + 1300 * np.sin(ang)))
        cv2.line(layer, p0, p1, col, int(rng.integers(2, 7)), cv2.LINE_AA)
    a = 0.85 * min(1.0, intensity)
    return cv2.addWeighted(f, 1 - a, layer, a, 0)


def lightning(f: np.ndarray, t: float, color, seed=0, bolts=2) -> np.ndarray:
    rng = np.random.default_rng(seed + int(t * 30))
    layer = np.zeros((H, W, 3), np.uint8)
    for _ in range(bolts):
        x, y = rng.uniform(0.1, 0.9) * W, -20.0
        pts = [(x, y)]
        while y < H * rng.uniform(0.55, 1.0):
            x += rng.normal(0, 38)
            y += rng.uniform(25, 70)
            pts.append((x, y))
        p = np.array(pts, np.int32)
        cv2.polylines(layer, [p], False, tuple(int(c) for c in color), 10, cv2.LINE_AA)
        cv2.polylines(layer, [p], False, (255, 255, 255), 3, cv2.LINE_AA)
    small = cv2.resize(layer, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    glow = cv2.resize(cv2.GaussianBlur(small, (0, 0), 3.5), (W, H))
    out = cv2.add(f, glow)
    return cv2.add(out, layer)


class Embers:
    """Partículas (brasas/faíscas) com cor do personagem, aditivas, determinísticas."""

    def __init__(self, n=140, color=(255, 120, 60), seed=3):
        rng = np.random.default_rng(seed)
        self.x0 = rng.uniform(0, W, n)
        self.y0 = rng.uniform(0, H, n)
        self.v = rng.uniform(40, 160, n)
        self.sway = rng.uniform(10, 40, n)
        self.ph = rng.uniform(0, 6.28, n)
        self.r = rng.uniform(1.5, 4.5, n)
        self.color = color

    def draw(self, f: np.ndarray, t: float, intensity=1.0) -> np.ndarray:
        if intensity <= 0:
            return f
        layer = np.zeros((H // 2, W // 2, 3), np.uint8)
        ys = (self.y0 - self.v * t) % (H + 40) - 20
        xs = self.x0 + self.sway * np.sin(t * 1.3 + self.ph)
        n = int(len(xs) * min(1.0, intensity))
        for x, y, r in zip(xs[:n], ys[:n], self.r[:n]):
            cv2.circle(layer, (int(x / 2), int(y / 2)), max(1, int(r / 2)), self.color, -1, cv2.LINE_AA)
        glow = cv2.GaussianBlur(layer, (0, 0), 3)
        return cv2.add(f, cv2.resize(cv2.add(layer, glow), (W, H)))


def light_leak(f: np.ndarray, t: float, color, intensity=0.5, seed=0) -> np.ndarray:
    if intensity <= 0:
        return f
    small = np.zeros((H // 8, W // 8, 3), np.float32)
    cx = (0.5 + 0.45 * math.sin(t * 0.35 + seed)) * W / 8
    cy = (0.3 + 0.3 * math.cos(t * 0.27 + seed)) * H / 8
    cv2.circle(small, (int(cx), int(cy)), int(W / 8 * 0.35), tuple(float(c) for c in color), -1)
    small = cv2.GaussianBlur(small, (0, 0), 18)
    leak = np.clip(cv2.resize(small, (W, H)) * intensity, 0, 255).astype(np.uint8)
    return 255 - cv2.multiply(255 - f, 255 - leak, scale=1 / 255)  # screen


def shockwave(f: np.ndarray, p: float, color) -> np.ndarray:
    """Anel de choque expandindo do centro (p: 0..1)."""
    if not 0 <= p <= 1:
        return f
    layer = np.zeros_like(f)
    r = int(60 + p * 1250)
    cv2.circle(layer, (W // 2, H // 2), r, tuple(int(c) for c in color), int(40 * (1 - p) + 4), cv2.LINE_AA)
    small = cv2.GaussianBlur(cv2.resize(layer, (W // 4, H // 4)), (0, 0), 2)
    return cv2.addWeighted(f, 1, cv2.resize(small, (W, H)), 1 - p, 0)


def blackout(f: np.ndarray, a: float) -> np.ndarray:
    return (f.astype(np.float32) * (1 - a)).astype(np.uint8) if a > 0 else f


class Overlay:
    """RGBA pré-multiplicado em uint8 para composição rápida."""

    def __init__(self, rgba: np.ndarray):
        a = rgba[..., 3:4].astype(np.float32) / 255
        self.prem = (rgba[..., :3].astype(np.float32) * a).astype(np.uint8)
        self.alpha = np.repeat(rgba[..., 3:4], 3, 2)
        self.h, self.w = rgba.shape[:2]


def alpha_over(f: np.ndarray, rgba, x=0, y=0, opacity=1.0) -> np.ndarray:
    ov = rgba if isinstance(rgba, Overlay) else Overlay(rgba)
    x2, y2 = min(W, x + ov.w), min(H, y + ov.h)
    if x2 <= x or y2 <= y or opacity <= 0:
        return f
    sx, sy = max(0, -x), max(0, -y)
    x, y = max(0, x), max(0, y)
    if x2 <= x or y2 <= y:
        return f
    prem = ov.prem[sy:sy + y2 - y, sx:sx + x2 - x]
    al = ov.alpha[sy:sy + y2 - y, sx:sx + x2 - x]
    if opacity < 1:
        prem = cv2.multiply(prem, np.full_like(prem, int(opacity * 255)), scale=1 / 255)
        al = cv2.multiply(al, np.full_like(al, int(opacity * 255)), scale=1 / 255)
    f = f.copy()
    roi = f[y:y2, x:x2]
    f[y:y2, x:x2] = cv2.add(cv2.multiply(roi, 255 - al, scale=1 / 255), prem)
    return f
