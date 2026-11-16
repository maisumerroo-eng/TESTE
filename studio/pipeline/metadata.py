"""Pacote YouTube: título, descrição (com capítulos e créditos), tags e hashtags."""
from __future__ import annotations

from .common import Project, brand, load_json, load_yaml, log

LABELS = {"intro": "Intro", "verse": "Verso", "pre-chorus": "Pré-refrão", "chorus": "Refrão",
          "break": "Ponte", "outro": "Final"}


def _mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def build(proj: Project) -> dict:
    b = brand()
    c = proj.char
    cfg = proj.cfg
    hook = cfg.get("hook") or c["short"]
    title = b["titles"]["pattern"].format(CHAR=c["name"], ANIME=c["anime"], HOOK_UPPER=hook.upper(),
                                          HOOK=hook, CHAR_UPPER=c["short"].upper())
    if len(title) > 100:
        title = f"{c['short']} ({c['anime']}) - {hook.upper()} | {b['channel']['name'].title()}"

    a = load_json(proj.work / "analysis.json")
    chapters, last, n = [], None, {}
    for s in a["sections"]:
        lab = LABELS.get(s["label"], "Verso")
        if lab == last:
            continue
        n[lab] = n.get(lab, 0) + 1
        name = lab if n[lab] == 1 else f"{lab} {n[lab]}"
        chapters.append(f"{_mmss(s['start'] if chapters else 0)} {name}")
        last = lab
    if len(chapters) < 3:
        chapters = []

    lyr = proj.input / "lyrics.txt"
    lyrics = lyr.read_text(encoding="utf-8").replace("*", "").strip() if lyr.exists() else ""

    credits = []
    ay = proj.assets / "assets.yaml"
    if ay.exists():
        seen = set()
        for x in load_yaml(ay).get("assets", []):
            key = x["file"].split("#")[0]
            if key in seen:
                continue
            seen.add(key)
            credits.append(f"- {x.get('credit') or key} ({x.get('source', '?')})")

    anime_tag = c["anime"].lower()
    first_l = c["short"].lower()
    tags = [f"rap do {first_l}", f"{first_l} rap", f"rap {anime_tag}", f"{anime_tag} rap", c["name"].lower(),
            anime_tag, "rap geek", "rap de anime", "anime rap", "amv", "rap nerd", "kagerima", hook.lower(),
            f"{first_l} edit", f"{anime_tag} amv", "rap anime brasileiro"]
    tags += [k for k in c.get("keywords", [])[:8]]
    seen, final_tags, total = set(), [], 0
    for tg in tags:
        if tg not in seen and total + len(tg) + 1 <= 480:
            seen.add(tg)
            final_tags.append(tg)
            total += len(tg) + 1
    hashtags = [f"#{first_l}", f"#{anime_tag.replace(' ', '')}", "#rapgeek"]

    feats = cfg.get("feats", "")
    prod = cfg.get("credits", {})
    desc = f"""{c['name']} ({c['anime']}) - {hook.upper()} | Kagerima{(' ft. ' + feats) if feats else ''}

Se curtiu, deixa o like e comenta qual personagem você quer no próximo rap.
Inscreva-se: {b['channel']['handle']}

{"CAPÍTULOS" + chr(10) + chr(10).join(chapters) + chr(10) if chapters else ""}
FICHA
Voz e letra: Kagerima
Beat: {prod.get('beat', 'Kagerima')}
Mix e master: {prod.get('mix', 'Kagerima')}
Edição: {prod.get('edit', 'Kagerima')}
Arte da thumb: {prod.get('thumb_art', 'Kagerima')}
Voz e instrumental feitos com ferramentas de IA (Google Flow).

{"LETRA" + chr(10) + lyrics + chr(10) if lyrics else ""}
{c['anime']} e seus personagens pertencem aos autores e estúdios originais. Este é um trabalho de fã,
sem vínculo oficial. Detentor de direitos: fale com a gente pelo e-mail do canal para ajuste ou remoção.
{("Fontes das cenas:" + chr(10) + chr(10).join(credits)) if credits else ""}

{' '.join(hashtags)}
"""
    meta = dict(title=title, description=desc.strip() + "\n", tags=final_tags, hashtags=hashtags,
                category="Music", made_for_kids=False, contains_synthetic_media=True,
                notes=["Marque 'conteúdo alterado ou sintético' no YouTube Studio (voz/música de IA).",
                       "Revise licenças em assets/sources.yaml antes de publicar.",
                       "Não há garantia contra reivindicações de Content ID."])
    out = proj.out / f"{proj.cfg['slug']}_youtube.md"
    out.write_text(
        f"# TÍTULO\n{title}\n\n# DESCRIÇÃO\n{meta['description']}\n# TAGS\n{', '.join(final_tags)}\n\n"
        f"# HASHTAGS\n{' '.join(hashtags)}\n\n# CHECKLIST DE PUBLICAÇÃO\n" +
        "\n".join(f"- [ ] {n_}" for n_ in meta["notes"]) + "\n", encoding="utf-8")
    from .common import save_json
    save_json(proj.out / f"{proj.cfg['slug']}_youtube.json", meta)
    log(f"metadados YouTube: {out.name} | título: {title}")
    return meta
