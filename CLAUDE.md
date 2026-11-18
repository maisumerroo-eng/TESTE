# Projeto TESTE

## Regra principal
Sempre trabalhar em cima do que já existe neste repo antes de criar algo novo. Ler o estado atual primeiro.

## O que já existe
- `.claude/skills/site-scroll-produto/` — site com animação no scroll (vídeo → frames → canvas + GSAP). Gerador fal.ai em `scripts/gerar.mjs`.
- `.claude/skills/showreel-marca/` — roteiro de showreel de marca com HyperFrames.
- `.claude/skills/hyperframes*`, `media-use`, `reverse-any-video` etc. — skills oficiais HyperFrames (HeyGen, Apache-2.0).
- `marcas/skull/` — logo Skull Lounge em SVG (`gerar-svg.js` gera; texto em contorno, Montserrat).
- `sites/skull/` — site do Skull (`fonte.html` + `build.py` → `index.html`). Publicado: https://claude.ai/artifact/5RTj1gn9HDFJxGdvLJdz3N
- `anuncios/skull/` — anúncio vertical 22 s (`render.js` grava com Playwright, `trilha.sh` gera áudio).

## Geração de imagem/vídeo
- Freefield (github.com/neuregex/freefield) no Modal = API própria grátis (US$ 30/mês). Endpoint `.modal.run`, header `Authorization: Bearer <FREEFIELD_TOKEN>`.
- MuAPI (Open Higgsfield): chave salva no ambiente, saldo zerado em 18/11/2026.
- Próximo passo planejado: site vanitas do Skull no estilo do reel da "Pear" (@w.wearebrand): pinturas clássicas por cena + transições no scroll.
