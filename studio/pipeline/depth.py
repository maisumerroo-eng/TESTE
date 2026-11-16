"""Mapa de profundidade (Depth Anything V2 Small, CPU) para parallax 2.5D de painéis e ilustrações.
Fallback sem modelo: profundidade sintética (centro/baixo mais perto)."""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from .common import log

_PIPE = None


def _model():
    global _PIPE
    if _PIPE is None:
        from transformers import pipeline
        _PIPE = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device="cpu")
    return _PIPE


def synthetic(h, w):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    d = 1 - np.sqrt(((x - w / 2) / (w / 2)) ** 2 * 0.6 + ((y - h * 0.6) / h) ** 2)
    return np.clip(d, 0, 1)


def depth_map(img_path: Path, cache: Path) -> np.ndarray:
    """Retorna profundidade 0..1 (1 = perto) na resolução da imagem, com cache .npy."""
    cache.parent.mkdir(parents=True, exist_ok=True)
    if cache.exists():
        return np.load(cache)
    img = cv2.imread(str(img_path))
    h, w = img.shape[:2]
    try:
        from PIL import Image
        pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        pil.thumbnail((768, 768))
        d = np.array(_model()(pil)["predicted_depth"], dtype=np.float32)
        d = (d - d.min()) / (d.max() - d.min() + 1e-6)
        d = cv2.resize(d, (w, h), interpolation=cv2.INTER_CUBIC)
    except Exception as e:  # sem modelo: usa sintético
        log(f"aviso: depth model indisponível ({e}); usando profundidade sintética")
        d = synthetic(h, w)
    d = cv2.GaussianBlur(d, (0, 0), max(2, w / 300))  # suaviza bordas -> menos rasgos no parallax
    np.save(cache, d.astype(np.float16))
    return d
