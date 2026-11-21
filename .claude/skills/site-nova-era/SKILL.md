---
name: site-nova-era
description: Sistema completo para criar sites de cliente no "novo design" e com megapersonalização. Figma como hub (imagens e ícones por IA, telas, reel), fotos de bancos públicos com licença, vídeo e voz (ElevenLabs, muapi, Higgsfield). Roteiro em 8 atos, momento-assinatura nascido da metáfora do negócio, motion system com vocabulário próprio (reveal por data-attributes, seção fixada com rota SVG, pilha de placas, marquee com inércia, contadores), anti-vício de IA, DNA do cliente, variantes por visitante (UTM, origem, escolha, horário, retorno) com WhatsApp personalizado, performance, acessibilidade, SEO, LGPD, vídeo vertical do site para o reel e deploy. HTML/CSS/JS puro com templates testados. Use quando o usuário pedir site, landing page, site institucional, site pra cliente, site premium/animado/"estilo agência", site personalizado por público/anúncio, ou citar sites como referência de nível (ex. vexterintelligence.com.br).
---

# Site nova era

Meta: o site parece **feito à mão para aquele cliente** e **escrito para cada visitante**. Nada de template, nada de cara de IA.

Stack: HTML + CSS + JS puro (ES modules), sem build. Lenis e Anime.js opcionais. Deploy na Vercel.
Régua de qualidade: os casos em `references/casos/` (sites analisados; aprender princípios, nunca copiar).

## Casos estudados

| Caso | Nicho | Lição principal |
|---|---|---|
| `casos/vexter.md` | contabilidade/BPO para transportadoras | metáfora do negócio (estrada) vira a seção fixada; uma oferta só; prova em reais |

Antes de começar um site, leia os casos do mesmo nicho ou com a mesma lição que o projeto precisa.

## Mapa de arquivos

| Arquivo | Quando ler |
|---|---|
| `references/casos/*.md` | antes de começar: nível esperado, estratégias, estrutura, pontos fracos a superar |
| `references/megapersonalizacao.md` | fase 1 (DNA) e fase 6 (variantes por visitante) |
| `references/narrativa-estrutura.md` | fase 2: roteiro, momento-assinatura por nicho, fórmulas de copy |
| `references/motion-system.md` | fase 4: tokens, vocabulário de reveal, biblioteca de interações |
| `references/animejs-v4.md` | só se precisar de timeline complexa com Anime.js |
| `references/anti-vicio-ia.md` | fase 3 e antes de entregar |
| `references/qualidade.md` | fase 7: performance, a11y, SEO, LGPD |
| `templates/base/` | copiar para o projeto: `index.html`, `style.css`, `motion.css`, `motion.js`, `personaliza.js` (testados juntos) |
| `references/midia-e-ferramentas.md` | fase 0 e sempre que precisar de imagem, ícone, vídeo, voz ou Figma |
| `templates/buscar-imagens.js` | fotos de bancos públicos sem chave (Openverse + Wikimedia), com créditos |
| `templates/gravar-reel.js` | fase 8: vídeo vertical do site |
| `templates/montar-reel.sh` | fase 8: junta vídeo + narração ElevenLabs + trilha em MP4 1080x1920 |
| `templates/analisar-site.js` | quando o usuário mandar um site novo para estudar |

## Atualizar com novo site (quando o usuário mandar uma URL de referência)

1. **Raio-x:** `node templates/analisar-site.js <url> <scratchpad>/<nome>`. Montar folhas de contato das telas (PIL) e olhar todas.
2. **Código:** baixar o JS e o CSS principais de `reqs.txt` e procurar: libs (gsap, anime, lenis, three, swiper, framer), `IntersectionObserver`, `requestAnimationFrame`, `cubic-bezier`, keyframes, `clip-path`, `mask-image`, `@property`, `animation-timeline`, `:has(`, `@container`, `startViewTransition`, `getContext`, `matchMedia`. Separar o bundle por módulos e resumir o que cada um faz.
3. **Caso:** criar `references/casos/<nome>.md` no mesmo formato de `vexter.md`: stack real, estrutura em ordem, estratégias de conversão, por que não tem cara de IA, pontos fracos, e o que existe de personalização. Afirmar só o que foi medido; o que for suposição, marcar como suposição.
4. **Comparar com a skill e incorporar só o que for novo:**
   - estrutura/copy/assinatura nova → `narrativa-estrutura.md` (tabela de metáforas, fórmulas)
   - efeito ou interação nova → `motion-system.md` (vocabulário ou biblioteca) e, se for reutilizável e testável, `templates/base/`
   - vício evitado de um jeito novo → `anti-vicio-ia.md`
   - personalização nova → `megapersonalizacao.md`
   - técnica de performance/a11y/SEO → `qualidade.md`
   Se contradizer uma regra existente, manter a regra mais forte e registrar a divergência no caso.
5. **Tabela "Casos estudados"** acima: adicionar a linha com nicho e lição principal.
6. **Testar** qualquer mudança em `templates/base/` no Chromium (console limpo, reduced motion, 390px e 1440px).
7. Nunca copiar texto, código, ícones ou imagens do site analisado. Escrever implementação própria.
8. Commit e push; responder ao usuário com o resumo do raio-x e a lista do que mudou na skill.

## Fases

### 0. Recursos e Figma
Leia `midia-e-ferramentas.md`. Confirme com 1 chamada barata o que está ativo (Figma `whoami`, saldo muapi/Higgsfield, vozes ElevenLabs). Crie o **arquivo Figma do projeto** (hub obrigatório: DNA, tokens, assets, telas, reel). Toda geração paga: estimar e pedir ok antes.

### 1. DNA do cliente (não pule)
Preencha `dna.md` no projeto com o modelo de `megapersonalizacao.md` (Camada 1). Fontes: briefing, site atual, Instagram, Google Business, concorrentes. Lacunas viram `[A CONFIRMAR]`, nunca invenção. Pergunte ao usuário só o que for bloqueante (oferta, nicho, contato).

### 2. Roteiro
Monte os 8 atos de `narrativa-estrutura.md`, cortando o que o cliente não sustenta com verdade. Escolha **um** momento-assinatura a partir da metáfora do negócio (tabela por nicho) e descreva em 3 linhas: o que o visitante vê, o que o scroll controla, como fica sem animação.

### 3. Direção visual
Carregue `frontend-design` e `anthropic-skills:site-sem-cara-de-ia`. Defina em `:root`: 1 cor de marca + neutros (claro e escuro), 1 fonte display + 1 de texto, escala tipográfica com contraste forte, linhas finas. Defina 1 detalhe tipográfico de assinatura. Ícones: SVG próprios num estilo só, gerados no Figma (`generate_vector_illustration`, `kind: "icon"`). Imagens: do cliente; senão geradas com o prompt-mestre de `midia-e-ferramentas.md` (Figma `generate_image` primeiro, depois muapi/Higgsfield/Lovable); bancos públicos via `templates/buscar-imagens.js` para textura, fundo e placeholder, com créditos. Tudo vai para a página `02 Assets` do Figma. Logos de parceiros: `21st` `search_logo`. Inspiração de componentes: Magic MCP (`21st`), `shadcn` se for React.

### 4. Construção
1. Copie `templates/base/` para o projeto e troque os placeholders `[...]` pelo DNA.
2. HTML semântico completo primeiro (conteúdo final visível sem JS).
3. CSS mobile primeiro; fundos escuro/claro marcando capítulos.
4. Motion: siga `motion-system.md`. Use os `data-reveal` com propósito (máx. 4 tipos por página), um `data-pin` para o momento-assinatura, contadores com valor real. Carregue `animate` e `choreograph` para decisões de curva e ordem.

### 5. Prova de autoria
Rode o detector e a lista "Prova de autoria" de `anti-vicio-ia.md`. Mínimo 5 de 8 itens. Reescreva o que falhar.

### 6. Megapersonalização por visitante
Quando houver anúncios, públicos ou regiões diferentes: siga `megapersonalizacao.md` (Camada 2). Variantes em `<template data-p-variant>`, ordem por segmento com `data-p-order`, WhatsApp com mensagem do segmento via `data-wa`, seletor de perfil com `data-p-choose`, link "ver versão padrão". Liste cada variante e sua fonte no `dna.md`. Teste com `?seg=<segmento>`.

### 7. Qualidade
`qualidade.md` inteiro. Depois: `impeccable` (polish), `emil-design-eng` (interações), `web-design-guidelines` (a11y/UX). Abra com Chrome DevTools MCP ou Playwright: 390px e 1440px, console limpo, reduced motion ligado e desligado, Lighthouse.

### 8. Entrega
- Vídeo: `templates/gravar-reel.js` (1080x1920). Narração com ElevenLabs (voz pt-BR escolhida pelo tom da marca, roteiro de 15 a 30 s) e montagem com `templates/montar-reel.sh` (trilha opcional abaixa sob a voz; legenda via transcrição). Subir os quadros na página `04 Reel` do Figma. Legenda do post curta citando a marca, sem prometer resultado.
- Telas finais (390 e 1440) na página `03 Telas` do Figma para o cliente comentar.
- Deploy na Vercel; conferir a URL publicada com screenshot.
- Commit e push no branch de trabalho.

## Regras inegociáveis

1. Nenhum número, depoimento, logo ou caso inventado.
2. Nicho, região e oferta claros nos primeiros 3 segundos.
3. Uma oferta principal repetida em todos os CTAs.
4. Conteúdo visível sem JS, com reduced motion e em print de página inteira (reveal só sob `html.motion`).
5. Um momento-assinatura por página; loops só no fundo e pausados fora da tela.
6. Preloader só na 1ª visita da sessão, ≤ 2,5 s; transição de página ≤ 600 ms.
7. Banner LGPD com a cara da marca; análise só após consentimento.
8. Personalização sem dado pessoal e sempre reversível.
9. Figma é o hub de todo projeto. Geração paga só com estimativa e ok do usuário; nunca repetir chamada de geração.
10. Imagem de banco público só com licença comercial/editável e crédito quando exigido; nunca imagem do site analisado.

## Checklist final

- [ ] `dna.md` preenchido, sem `[A CONFIRMAR]` no texto visível
- [ ] 8 atos revisados; momento-assinatura funcionando e com versão estática
- [ ] Detector anti-vício limpo; prova de autoria ≥ 5/8
- [ ] Variantes testadas com `?seg=` e com escolha manual (se houver Camada 2)
- [ ] 390px e 1440px sem scroll horizontal; console limpo
- [ ] Lighthouse ≥ 90; contraste AA; foco visível; reduced motion ok
- [ ] JSON-LD, OG 1200x630, sitemap, robots
- [ ] Arquivo Figma com DNA, tokens, assets, telas e reel
- [ ] `creditos.md` revisado e créditos CC BY visíveis no site (se houver)
- [ ] Vídeo do reel com narração montado; URL publicada conferida
