"""Utilidades compartilhadas da pipeline KAGERIMA."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import unicodedata
from pathlib import Path

import yaml

STUDIO = Path(__file__).resolve().parents[1]
CONFIGS = STUDIO / "configs"
BRAND_DIR = STUDIO / "brand"
FONTS_DIR = BRAND_DIR / "fonts"
PROJECTS = STUDIO / "projects"


def log(msg: str) -> None:
    print(f"[kagerima] {msg}", flush=True)


def load_yaml(p: Path) -> dict:
    return yaml.safe_load(Path(p).read_text(encoding="utf-8")) or {}


def save_yaml(p: Path, data: dict) -> None:
    Path(p).write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def load_json(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def save_json(p: Path, data) -> None:
    Path(p).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def brand() -> dict:
    return load_yaml(CONFIGS / "brand.yaml")


def character(slug: str) -> dict:
    p = CONFIGS / "characters" / f"{slug}.yaml"
    if not p.exists():
        raise SystemExit(f"Personagem '{slug}' sem config. Crie {p} (copie um existente).")
    return load_yaml(p)


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hex_to_ass(h: str, alpha: int = 0) -> str:
    """#RRGGBB -> &HAABBGGRR (formato ASS)."""
    r, g, b = hex_to_rgb(h)
    return f"&H{alpha:02X}{b:02X}{g:02X}{r:02X}"


def run(cmd: list[str], quiet: bool = True) -> subprocess.CompletedProcess:
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Falhou: {' '.join(map(str, cmd))[:400]}\n{res.stderr[-2000:]}")
    if not quiet:
        print(res.stdout)
    return res


def ffprobe(path: Path) -> dict:
    res = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)])
    return json.loads(res.stdout)


def media_duration(path: Path) -> float:
    return float(ffprobe(path)["format"]["duration"])


class Project:
    """Pasta de uma produção: projects/<slug>/"""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.cfg_path = self.root / "project.yaml"
        self.cfg = load_yaml(self.cfg_path) if self.cfg_path.exists() else {}

    # caminhos padrão
    @property
    def input(self): return self.root / "input"
    @property
    def assets(self): return self.root / "assets"
    @property
    def work(self): return self.root / "work"
    @property
    def out(self): return self.root / "output"

    def path(self, *parts) -> Path:
        p = self.root.joinpath(*parts)
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    @property
    def song(self) -> Path:
        return self.input / self.cfg["song_file"]

    @property
    def char(self) -> dict:
        return character(self.cfg["character"])

    def save(self):
        save_yaml(self.cfg_path, self.cfg)

    @classmethod
    def open(cls, name_or_path: str) -> "Project":
        p = Path(name_or_path)
        if not p.exists():
            p = PROJECTS / name_or_path
        if not (p / "project.yaml").exists():
            raise SystemExit(f"Projeto não encontrado: {name_or_path}")
        return cls(p)


def require(binary: str) -> None:
    if shutil.which(binary) is None:
        raise SystemExit(f"Ferramenta ausente: {binary}")
