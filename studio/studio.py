#!/usr/bin/env python3
"""KAGERIMA STUDIO — CLI de produção.

  python3 studio.py new MUSICA.mp3 --char sasuke --hook "Ódio e Sharingan" [--lyrics letra.txt] [--track 01]
  python3 studio.py produce <projeto>            # pipeline completa
  python3 studio.py preview <projeto> --from 40 --to 55
  python3 studio.py <etapa> <projeto>            # master | analyze | lyrics | subs | ingest | plan | sfx | render | thumb | meta | qc
  python3 studio.py brand                        # (re)gera o kit de marca
"""
from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from pipeline.common import PROJECTS, Project, character, log, save_yaml, slugify  # noqa: E402


def cmd_new(a):
    char = character(a.char)
    src = Path(a.audio)
    if not src.exists():
        raise SystemExit(f"arquivo não encontrado: {src}")
    slug = slugify(a.name or f"{a.track}-{a.char}-{a.hook or src.stem}")
    root = PROJECTS / slug
    for d in ("input", "assets/clips", "assets/images", "assets/manga", "work", "output"):
        (root / d).mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, root / "input" / src.name)
    if a.lyrics:
        shutil.copy2(a.lyrics, root / "input" / "lyrics.txt")
    cfg = dict(slug=slug, character=a.char, hook=a.hook or char["short"], track=a.track,
               song_file=src.name, language="pt", fps=a.fps, seed=7, title_at=1.0, next_hint="",
               whisper_model=a.whisper, subtitles=dict(uppercase=True),
               thumbnail=dict(text="", image="", focus_y=0.35), feats="",
               credits=dict(beat="Kagerima", mix="Kagerima", edit="Kagerima", thumb_art="Kagerima"))
    save_yaml(root / "project.yaml", cfg)
    (root / "assets" / "sources.yaml").write_text(
        "# créditos/licença por arquivo de mídia (vai para a descrição do vídeo)\n"
        "# exemplo.mp4: {source: 'PV oficial - canal X', license: 'uso autorizado', credit: 'Studio Y'}\n",
        encoding="utf-8")
    (root / "assets" / "scenes.yaml").write_text(
        "# roteiro do diretor (opcional). Ver docs/ROTEIRO.md\nscenes: []\n", encoding="utf-8")
    log(f"projeto criado: {root}")
    log("próximos passos: colocar mídia em assets/ (clips, images, manga) e rodar: "
        f"python3 studio.py produce {slug}")


def step(name, fn, *args, **kw):
    t = time.time()
    log(f"── {name} ──")
    r = fn(*args, **kw)
    log(f"   ({time.time() - t:.1f}s)")
    return r


def run_steps(p: Project, steps: list[str], a):
    from pipeline import (assets, audio_analysis, lyrics_sync, mastering, metadata, planner, qc, renderer,
                          sfx, subtitles, thumbnail)
    for s in steps:
        if s == "master":
            step("tratamento de áudio", mastering.master, p)
        elif s == "analyze":
            step("análise musical", audio_analysis.analyze, p)
        elif s == "lyrics":
            step("letra sincronizada", lyrics_sync.build, p, p.cfg.get("whisper_model", "small"))
        elif s == "subs":
            step("legendas dinâmicas", subtitles.build_ass, p)
        elif s == "ingest":
            step("biblioteca de mídia", assets.ingest, p)
        elif s == "plan":
            step("plano de edição", planner.plan, p)
        elif s == "sfx":
            step("camada de SFX", sfx.build, p)
        elif s == "render":
            step("render", renderer.render, p, a.workers, a.t_from or 0.0, a.t_to)
        elif s == "thumb":
            step("thumbnail", thumbnail.build, p)
        elif s == "meta":
            step("metadados YouTube", metadata.build, p)
        elif s == "qc":
            step("controle de qualidade", qc.check, p)


FULL = ["master", "analyze", "lyrics", "subs", "ingest", "plan", "sfx", "render", "thumb", "meta", "qc"]


def main():
    ap = argparse.ArgumentParser(description="KAGERIMA STUDIO")
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new")
    n.add_argument("audio")
    n.add_argument("--char", required=True)
    n.add_argument("--hook", default="")
    n.add_argument("--lyrics")
    n.add_argument("--track", default="01")
    n.add_argument("--name")
    n.add_argument("--fps", type=int, default=30)
    n.add_argument("--whisper", default="small")
    for name in FULL + ["produce", "preview"]:
        s = sub.add_parser(name)
        s.add_argument("project")
        s.add_argument("--workers", type=int)
        s.add_argument("--from", dest="t_from", type=float)
        s.add_argument("--to", dest="t_to", type=float)
    sub.add_parser("brand")
    a = ap.parse_args()

    if a.cmd == "new":
        return cmd_new(a)
    if a.cmd == "brand":
        from pipeline import brand_kit
        return brand_kit.build_all()
    p = Project.open(a.project)
    if a.cmd == "produce":
        return run_steps(p, FULL, a)
    if a.cmd == "preview":
        from pipeline import renderer
        a.t_from = a.t_from or 0.0
        return step("preview", renderer.render, p, a.workers, a.t_from, a.t_to or a.t_from + 15,
                    f"{p.cfg['slug']}_preview_{int(a.t_from)}.mp4")
    run_steps(p, [a.cmd], a)


if __name__ == "__main__":
    main()
