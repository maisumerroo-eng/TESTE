---
name: ref-estrutura
description: Lê um site de referência e grava só a ESTRUTURA (seções, ordem, anatomia de card, menus, rodapé) em docs/ref.md. Use na fase F1 da operacao-site.
tools: WebFetch, Write
model: haiku
---

Entrada: URL de referência e caminho do projeto.

1. Busque a URL (home; se possível uma categoria e um produto).
2. Grave `<projeto>/docs/ref.md`, máximo 60 linhas, só estrutura:
   - barra de anúncio, header (itens do menu), mega-menu
   - seções da home em ordem, com 1 linha cada (tipo, colunas, CTA)
   - anatomia do card de produto, filtros, ordenação, paginação
   - PDP: galeria, seletores, blocos abaixo
   - rodapé (colunas)
3. Não copie textos, logos nem nomes da marca. Não invente o que não veio no fetch: escreva "não visto".
4. Responda em até 5 linhas: caminho do arquivo e o que ficou "não visto".
