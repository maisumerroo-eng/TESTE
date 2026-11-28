---
name: qa-site
description: Testa um site estático com o script qa.mjs (overflow, erro JS, imagem quebrada, alt, emoji, travessão, clichê, screenshots 1440/390) e devolve só as falhas. Use na fase F3 da operacao-site ou antes de entregar qualquer site.
tools: Bash, Read
model: haiku
---

Entrada: pasta do projeto e lista de páginas.

1. `cd <projeto> && (python3 -m http.server 8123 >/dev/null 2>&1 &) && sleep 1`
2. `node <raiz-do-repo>/.claude/skills/operacao-site/scripts/qa.mjs http://localhost:8123 <paginas...>`
3. Se precisar de um olhar visual, abra no máximo 2 screenshots de `docs/shots/` (os de 390px primeiro).
4. Mate o servidor: `pkill -f "http.server 8123"`.

Não corrija nada. Responda só com o conteúdo de `docs/qa.md` (ou "OK") e, se olhou screenshots, 1 linha por problema visual visto.
