---
name: regras-sites
description: Regras de economia e qualidade para criar ou editar sites, lojas, landing pages, UI e CSS. Carregar junto com operacao-site em qualquer trabalho de frontend.
---

# Regras: sites

## Fluxo
1. Site novo: seguir a skill `operacao-site` (briefing, paralelo, montagem, QA, entrega). Visual por IA: `site-hibrido-ia`.
2. Site existente: rodar `qa.mjs` antes de mexer, para saber o estado. Corrigir, rodar de novo.
3. Briefing em `docs/briefing.md`; referência em `docs/ref.md`; textos em `docs/copy.md`. Ler esses arquivos, não refazer a pesquisa.

## Stack
4. Padrão: HTML + CSS + JS puro (ES modules), sem build. O usuário continua codando à mão.
5. React só se o projeto já for React ou o usuário pedir; aí sim shadcn e 21st.dev.
6. CSS com tokens no `:root` (cores, fontes, espaços, raios, durações). Nada de cor solta no meio do arquivo.
7. HTML semântico com ganchos `data-*` para o JS; seções comentadas.
8. JS que o usuário vai implementar: esqueleto com `// TODO:` explicando o quê.

## Design
9. Carregar `frontend-design` para direção visual e `site-sem-cara-de-ia` para texto e visual.
10. Paleta curta (2 neutros + 1 acento). No máximo 2 famílias de fonte.
11. Sem emoji, sem travessão em frase, sem clichê ("eleve", "jornada", "experiência única").
12. Imagem com pessoa: `object-position` por imagem para o celular não cortar o rosto.
13. Mobile primeiro na conferência: 390px. Desktop: 1440px.
14. Animação só com propósito; respeitar `prefers-reduced-motion`. Polimento: skills do Emil.
15. Acessibilidade: alt em toda imagem, foco visível, contraste AA, botões com nome, Esc fecha drawer.

## Conteúdo
16. Nunca inventar preço, telefone, CNPJ, endereço, depoimento, número de clientes. `PENDENTE` e avisar.
17. Sem preço: "Consulte no WhatsApp". WhatsApp vira CTA principal quando existir.
18. Nome e logo de marca de referência nunca aparecem no site nem nas imagens.

## Imagens
19. Nomes previsíveis (`produto-<slug>-1.jpg`), comprimir com `comprimir.py` antes do commit.
20. Inspecionar em folha de contato antes de usar (logo de terceiros, anatomia, cor da peça).
21. `loading="lazy"` abaixo da dobra; `width`/`height` ou `aspect-ratio` para não pular layout.

## Teste e entrega
22. `qa.mjs` zerado antes de entregar (overflow, erro JS, imagem quebrada, alt, emoji, travessão, clichê).
23. Olhar no máximo 2 screenshots (390 primeiro). Screenshots ficam fora do git.
24. Deploy: Vercel (`outputDirectory` = pasta do site) ou Lovable `deploy_project`. Abrir a URL depois.
25. Aprendizado do projeto: 1 a 3 linhas em `site-hibrido-ia` › Aprendizados.
