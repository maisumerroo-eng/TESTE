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
        cv2.circle(tex, (c, c), 330, (230, 245, 255), 3, cv2.LINE_AA)
        tex = _glow(tex, 2, 8)
        cv2.circle(tex, (c, c), 95, (5, 5, 10), -1, cv2.LINE_AA)
        cv2.circle(tex, (c - 120, c - 140), 34, (255, 255, 255), -1, cv2.LINE_AA)
        return tex

    def frame(self, rel: float, dur: float, pulse: float = 0.0) -> np.ndarray:
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
                cv2.rectangle(layer, (int(CX), int(CY - r * 0.8)), (int(x), int(CY + r * 0.8)), purple, -1)
                _sphere(layer, x, CY, r * 1.4, purple)
            for x, y, s in zip(CX + self.r0 * np.cos(self.a0 + rel), CY + self.r0 * 0.5 * np.sin(self.a0 + rel), self.sz):
                cv2.circle(layer, (int(x), int(y)), int(s * 0.6 + 0.5), purple, -1)
        elif k == "void":
            z = (self.stars[:, 2] - rel * 0.55) % 2 - 1 + 1.05
            xs = CX + self.stars[:, 0] / z * w * 0.5
            ys = CY + self.stars[:, 1] / z * h * 0.5
            for x, y, zz in zip(xs, ys, z):
                b = int(min(255, 90 / zz))
                cv2.circle(layer, (int(x), int(y)), 1 if zz > 0.5 else 2, (b, b, min(255, b + 30)), -1)
            rng = np.random.default_rng(int(rel * 12))
            for _ in range(40):
                x, y = int(rng.uniform(0, w)), int(rng.uniform(0, h))
                cv2.putText(layer, "".join(rng.choice(list("ᚠᚢᚦᚨᚱᚲ0123456789#/\\=+<>"), 3)), (x, y),
                            cv2.FONT_HERSHEY_PLAIN, rng.uniform(0.6, 1.4), (200, 220, 255), 1, cv2.LINE_AA)
            g = np.exp(-(((np.arange(w) - CX) / (w * 0.35)) ** 2))[None, :, None] * \
                np.exp(-(((np.arange(h) - CY) / (h * 0.25)) ** 2))[:, None, None]
            layer = cv2.add(layer, (g * np.array(self.sec, np.float32) * 0.5).astype(np.uint8))
        elif k == "iris":
            S = self.iris.shape[0]
            M = cv2.getRotationMatrix2D((S / 2, S / 2), rel * 12, 0.7 + 0.25 * p + 0.04 * pulse)
            M[0, 2] += CX - S / 2
            M[1, 2] += CY - S / 2
            layer = cv2.warpAffine(self.iris, M, (w, h))
        elif k == "barrier":
            R = 70
            t = rel * self.sp
            r = R + (self.r0) * np.exp(-t * 2.2)
            xs, ys = CX + r * np.cos(self.a0), CY + r * np.sin(self.a0)
            for x, y, s in zip(xs, ys, self.sz):
                cv2.circle(layer, (int(x), int(y)), int(s + 0.5), (230, 240, 255), -1)
            cv2.circle(layer, (int(CX), int(CY)), R, self.prim, 1 + int(2 * pulse), cv2.LINE_AA)
        out = cv2.add(self.bg, _glow(layer))
        return cv2.resize(out, (W, H), interpolation=cv2.INTER_LINEAR)
