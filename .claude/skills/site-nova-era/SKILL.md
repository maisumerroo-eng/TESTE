---
name: site-nova-era
description: Sistema completo para sites de cliente no "novo design" com megapersonalização. Plano obrigatório antes de criar, objeto-herói por nicho, estratégias de conversão e componentes premium testados, DNA e voz real do comprador, roteiro em 8 atos, momento-assinatura da metáfora do negócio (seção fixada SVG, vídeo no scroll com as 12 leis do vídeo, ou 3D Three.js), anti-vício de IA com gate de texto, variantes por visitante com WhatsApp personalizado. Figma, bancos de imagem, ElevenLabs, muapi/Higgsfield. Qualidade medida (LCP, CLS, contraste, flick, SEO, LGPD); modo econômico; reel vertical e deploy. Também aprimora sites existentes (diagnóstico, preservação de SEO, antes/depois) e converte print/mockup do cliente em HTML com verificação por pixels. HTML/CSS/JS puro. Use para site, landing page, site pra cliente, site premium/animado, vídeo no scroll, site personalizado, melhorar/refazer site existente, transformar imagem em HTML, ou site de referência.
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
| `references/3d.md` | quando houver 3D: meios de gerar/modelar (procedural, 3D Jutsu grátis, Poly Haven, Blender, imagem→3D), pipeline, Three.js |
| `templates/base/tres.js` | bloco 3D com Three.js 0.187.0 (carrega sob demanda, poster de fallback) |
| `templates/otimizar-3d.sh` | GLB para web (meshopt + WebP + simplificação) |
| `references/economia.md` | sempre: tokens, créditos, revisão só no diff, ciclo de otimização |
| `templates/auditar-site.js` | auditoria priorizada (LCP, CLS, peso, imagens, código não usado, SEO, a11y) |
| `templates/otimizar-imagens.sh` | AVIF + WebP responsivos com `<picture>` pronto |
| `templates/analisar-site.js` | quando o usuário mandar um site novo para estudar |
| `references/video-scrub.md` | quando a assinatura for vídeo no scroll: 12 leis do vídeo, prompts, pipeline com gates, encode |
| `templates/scrub/` | motor de vídeo no scroll testado (`scrub.js`, `scrub.css`, `exemplo.html`) |
| `templates/auditar-contraste.js` | contraste do pior pixel de texto sobre imagem/vídeo/gradiente |
| `templates/teste-flick.js` | ritmo de seção fixada/scrub com flicks reais de roda (120/240/360px) |
| `references/aprimorar-existente.md` | **site que já existe**: raio-x só leitura, diagnóstico manter/mudar, caminho (evolução no lugar, refazer com 301, plataforma fechada, só imagem), lotes medidos, prova antes/depois |
| `references/imagem-para-html.md` | print/mockup **do cliente** → HTML fiel: paleta medida, análise em camadas, uma imagem por vez, loop de comparação de pixels |
| `templates/paleta-da-imagem.py` / `templates/comparar-imagem.js` | paleta real de uma imagem / semelhança render × imagem com mapa de diferenças |
| `references/estrategia.md` | **estratégia antes do design**: medos e critérios do cliente, buscas no Google e em IA (GEO), concorrentes e diferencial, posicionamento em 1 frase, mapa do site com palavra-chave por página, texto completo, rascunho de layout no celular |
| `references/plano.md` + `templates/plano.md` | **fase de plano obrigatória**: o site inteiro desenhado antes de qualquer arquivo ou crédito |
| `references/objeto-heroi.md` | o objeto do nicho que representa a promessa (a "mão com a moeda" adaptada), prompt, fusão, ambiente da hero |
| `references/estrategias-de-conversao.md` | catálogo das estratégias de venda extraídas da estrutura real da Vexter → como adaptar → componente |
| `references/icones-isometricos.md` | técnica dos ícones "quase 3D" (3 tons + acento), sprite e metáforas por nicho |
| `templates/componentes/` | biblioteca testada: botão 3D, cartão de prova, faixa de ícones, placas com aba, lista de serviços, número gigante, antes/depois, gráfico interativo, valores escalonados, carrossel, formulário → WhatsApp, rodapé com wordmark, odômetro, ambiente de brises, estudo solar 3D, gerador de ícones isométricos |
| `templates/regua-minima.js` | **gate obrigatório**: piso Vexter em 13 parâmetros + teto de performance (reprova com código 1) |
| `references/inovacao.md` + `references/portfolio.md` | reusar o que funciona e inovar ≥ 3 meios por site; registro para não repetir composições |
| `templates/comparar-densidade.js` | régua de acabamento: mede o nosso site contra a referência (ícones, hovers, animações, gradientes, conteúdo) |
| `templates/gate-texto.py` | gate de texto: travessão, estoque, sinais quietos de IA, emoji |

## Como falar com o usuário
- Perguntas com opções clicáveis (AskUserQuestion), uma decisão por vez, a recomendada primeiro com "(Recomendado)". Digitar só quando a resposta é texto livre (descrever a ideia, dar feedback).
- Preço antes de gastar, sempre com número real; o passo barato primeiro.
- Linguagem simples; descrever o trabalho em termos humanos ("deixei a sombra da casa mais longa de manhã"), não em código. Observação casual ("essa parte ficou sem graça") é relatório de bug válido.
- Avisar em uma linha quando algo leva minutos (render, gravação, publicação).
- Projeto já existente: reaproveitar decisões salvas (`dna.md`, skill `anthropic-skills:memoria-projetos`).

## Pronto quando
1. Site no ar, verificado com requisições reais e recibos de velocidade medidos.
2. Assinatura lisa e todo texto legível (contraste do pior pixel aprovado, flick aprovado).
3. Funciona no celular do usuário, na rede dele.
4. O usuário olhou e disse que ficou como imaginou (a palavra dele).
5. Pendências (fotos, dados reais, textos) listadas para o usuário.
Polimento sem fim que ninguém pediu não é o trabalho.

## Modo econômico (vale para todas as fases)
Siga `references/economia.md`: busque e edite trechos (nunca reescreva arquivo inteiro), parta dos templates testados, rascunho barato antes de geração cara, manifesto de assets, revisão e screenshots só do que mudou, auditoria completa só em marcos (1ª versão, pré-deploy, mudança grande) e correção na ordem P1 → P2.

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

## Modos de entrada
- **Site novo:** fases abaixo, desde a 0.
- **Aprimorar site existente:** comece por `references/aprimorar-existente.md` (raio-x e diagnóstico), escolha o caminho com o usuário e então siga as fases a partir da estratégia, preservando URLs, conteúdo que posiciona e a stack do cliente.
- **Imagem do cliente → HTML:** `references/imagem-para-html.md` (fidelidade medida), depois as fases para subir de nível.

## Fases

### 0. Recursos e Figma
Leia `midia-e-ferramentas.md`. Confirme com 1 chamada barata o que está ativo (Figma `whoami`, saldo muapi/Higgsfield, vozes ElevenLabs). Crie o **arquivo Figma do projeto** (hub obrigatório: DNA, tokens, assets, telas, reel). Toda geração paga: estimar e pedir ok antes.

### 1. DNA do cliente (não pule)
Preencha `dna.md` no projeto com o modelo de `megapersonalizacao.md` (Camada 1). Fontes: briefing, site atual, Instagram, Google Business, concorrentes. Lacunas viram `[A CONFIRMAR]`, nunca invenção. Pergunte ao usuário só o que for bloqueante (oferta, nicho, contato). Faça a **pesquisa da voz do comprador** (avaliações e fóruns do nicho, frases exatas de dor, desejo e objeção) e defina a **premissa da marca** (uma palavra/ideia que o site inteiro vende). Negócio real sem fotos: decidir com o usuário se as imagens de IA serão declaradas ou trocadas depois.

### 1a. Estratégia antes do design (obrigatória)
Siga `references/estrategia.md` na ordem: análise do nicho (cliente, critérios, **medos antes de contratar**) → buscas no Google **e em assistentes de IA** + concorrentes do topo → **posicionamento em 1 frase** e **mapa do site com uma palavra-chave por página** → **texto completo da home** (título de 3 s, prova no topo, um botão, sem promessa nem número inventado; gate de texto já aqui) → **rascunho de layout no celular** seção por seção. Resultado vai para a seção 0 do `plano.md`; o texto aprovado embarca ao pé da letra.

### 1b. Plano (obrigatório, antes de criar qualquer arquivo)
Preencha `plano.md` no projeto com `templates/plano.md` seguindo `references/plano.md`: premissa e oferta com selo, **objeto-herói** (`objeto-heroi.md`), tabela referência → adaptação (estratégias de `estrategias-de-conversao.md`), mapa seção a seção (estratégia, componente, ícones, número, interação, efeito de fundo), inventário de componentes, lista de ícones, gráficos com dados e interação, metas de densidade, assets com custo. Mostre o resumo e peça ok (pergunta clicável). Mudança grande depois volta ao plano antes do código.

### 2. Roteiro
Monte os 8 atos de `narrativa-estrutura.md`, cortando o que o cliente não sustenta com verdade. Escolha **um** momento-assinatura a partir da metáfora do negócio (tabela por nicho) e do tipo certo: seção fixada SVG/CSS (padrão, leve e grátis), **vídeo no scroll** (`video-scrub.md`, quando a jornada de câmera é a metáfora e há verba) ou 3D. Descreva em 3 linhas: o que o visitante vê, o que o scroll controla, como fica sem animação. Teste de remoção: sem ela, a página mudaria de verdade? Opcional: um momento interativo que encena a ideia da marca. Seção que não serve a premissa sai.

### 3. Direção visual
Carregue `frontend-design` e `anthropic-skills:site-sem-cara-de-ia`. Defina em `:root`: 1 cor de marca + neutros (claro e escuro), 1 fonte display + 1 de texto, escala tipográfica com contraste forte, linhas finas. Defina 1 detalhe tipográfico de assinatura. Barras de direção: **uma** direção tirada do mundo do cliente comandando paleta, tipo, movimento e imagem juntos; acento em doses raras; fundo nunca `#000`/`#fff` puro; hero assimétrica; seções vizinhas nunca com o mesmo esqueleto; nenhum "look reflexo de IA" (lista em `anti-vicio-ia.md`) a não ser que seja o mundo material do cliente, declarado. Ícones: SVG próprios num estilo só, gerados no Figma (`generate_vector_illustration`, `kind: "icon"`). Imagens: do cliente; senão geradas com o prompt-mestre de `midia-e-ferramentas.md` (Figma `generate_image` primeiro, depois muapi/Higgsfield/Lovable); bancos públicos via `templates/buscar-imagens.js` para textura, fundo e placeholder, com créditos. Tudo vai para a página `02 Assets` do Figma. Logos de parceiros: `21st` `search_logo`. Inspiração de componentes: Magic MCP (`21st`), `shadcn` se for React.

### 4. Construção
1. Copie `templates/base/` e os componentes do plano de `templates/componentes/` (`componentes.css`, `componentes.js`, e `estudo-solar-3d.js`/ícones quando usados) para o projeto e troque os placeholders `[...]` pelo DNA.
   Ícones: `python3 templates/componentes/gerar-icones-iso.py` com a paleta e as metáforas do cliente (grátis, ver `icones-isometricos.md`).
2. HTML semântico completo primeiro (conteúdo final visível sem JS).
3. CSS mobile primeiro; fundos escuro/claro marcando capítulos.
4. Motion: siga `motion-system.md`. Use os `data-reveal` com propósito (máx. 4 tipos por página), um `data-pin` para o momento-assinatura, contadores com valor real. Carregue `animate` e `choreograph` para decisões de curva e ordem.
5. Vídeo no scroll (se for a assinatura): storyboard aprovado → quadro → vídeo com gate do usuário → encode `-g 8` → `templates/scrub/` (ver `video-scrub.md`).
6. 3D (só se for assinatura ou mostrar o produto melhor que foto): siga `3d.md`. Modelo do meio mais barato que entrega a qualidade, `otimizar-3d.sh`, bloco `tres.js` com poster.
7. Imagens finais por `otimizar-imagens.sh` (AVIF/WebP, srcset, width/height); a do LCP com `fetchpriority="high"`.

### 5. Prova de autoria
Rode `python3 templates/gate-texto.py <projeto>` até sair limpo e a lista "Prova de autoria" de `anti-vicio-ia.md` (mínimo 5 de 8). Reescreva o que falhar como afirmação direta; dispositivo de marca deliberado do `dna.md` fica.

### 6. Megapersonalização por visitante
Quando houver anúncios, públicos ou regiões diferentes: siga `megapersonalizacao.md` (Camada 2). Variantes em `<template data-p-variant>`, ordem por segmento com `data-p-order`, WhatsApp com mensagem do segmento via `data-wa`, seletor de perfil com `data-p-choose`, link "ver versão padrão". Liste cada variante e sua fonte no `dna.md`. Teste com `?seg=<segmento>`.

### 7. Qualidade
0. **Gate da régua mínima:** `node templates/regua-minima.js <url>` precisa aprovar (piso Vexter + teto de performance). Reprovou: subir com conteúdo e estados reais, nunca enchimento.
1. `node templates/auditar-site.js <url> auditoria` e corrigir P1 e P2 na ordem (ciclo de `economia.md`: medir → corrigir o maior gargalo → medir de novo → parar na meta).
2. `qualidade.md` como checklist. Depois: `impeccable` (polish), `emil-design-eng` (interações), `web-design-guidelines` (a11y/UX), cada um só nas seções que mudaram desde a última revisão.
3. `auditar-contraste.js` em 390 e 1440 (pior pixel ≥ 3,5:1 grande, 4,5:1 normal) e `teste-flick.js` em cada seção fixada/scrub.
4. Chrome DevTools MCP ou Playwright: 360, 390, 768, 1280 e 1440, console limpo, reduced motion ligado e desligado, cada botão/link/formulário exercitado.
5. Passe de olhos frescos por último (ver `qualidade.md`).

### 8. Entrega
- Vídeo: `templates/gravar-reel.js` (1080x1920). Narração com ElevenLabs (voz pt-BR escolhida pelo tom da marca, roteiro de 15 a 30 s) e montagem com `templates/montar-reel.sh` (trilha opcional abaixa sob a voz; legenda via transcrição). Subir os quadros na página `04 Reel` do Figma. Legenda do post curta citando a marca, sem prometer resultado.
- Telas finais (390 e 1440) na página `03 Telas` do Figma para o cliente comentar.
- Deploy na Vercel (com ok do usuário); verificar no ar (`curl -sSI`, console, assinatura funcionando) e apresentar **recibos de velocidade medidos** (ver `qualidade.md`). Pedir teste no celular dele.
- Listar pendências para o usuário (dados reais, fotos, textos a confirmar).
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
11. 3D nunca na frente do conteúdo: carrega sob demanda, tem poster e não piora o LCP.
12. Economia sem perder qualidade: rascunho barato → aprovação → final caro uma vez; revisão e testes só no que mudou.
13. Texto sobre mídia só com contraste medido no pior pixel; seções guiadas por scroll só com teste de flick aprovado.
14. Vídeo no scroll: nada é montado em volta de vídeo que o usuário não aprovou; celular e reduced motion recebem hero estático desenhado; página completa sem o vídeo.
15. Uma premissa de marca: seção que não serve a ela sai.
16. Nada é criado sem `plano.md` aprovado. Toda hero tem objeto-herói planejado (ou justificativa escrita para não ter).
18. **Régua mínima:** nenhum site é entregue abaixo do nível Vexter (`regua-minima.js` aprovado) nem acima do teto de performance.
21. **Site existente:** diagnóstico antes de mexer; nada que posiciona é removido sem 301 ou substituto; a stack do cliente só muda se ele pedir; ganho provado com tabela antes/depois.
22. **Imagem → HTML** só de design do próprio cliente; fidelidade verificada com `comparar-imagem.js`, nunca no olho.
20. **Estratégia antes do design:** nenhum visual antes de posicionamento, mapa do site com palavra-chave por página, texto completo e rascunho de layout no celular aprovados.
19. **Reusar e inovar:** reusar componentes, estratégias e a mão (presença humana aproxima) sempre que servirem, e inovar em pelo menos 3 meios de cumprir a skill por site; inovação testada volta para a biblioteca e para o `portfolio.md`.
17. Toda seção cumpre pelo menos uma estratégia de `estrategias-de-conversao.md`; número de prova aparece grande e colorido; gráfico prova a mudança e é interativo e acessível.

## Checklist final

- [ ] `regua-minima.js` APROVADO (piso Vexter + teto de performance)
- [ ] 3+ inovações entregues e devolvidas à skill; linha no `portfolio.md`
- [ ] Estratégia aprovada (medos respondidos, buscas Google/IA, diferencial, posicionamento, mapa com palavra-chave, texto ao pé da letra, rascunho no celular)
- [ ] `plano.md` aprovado e seguido (objeto-herói, mapa de seções, componentes, ícones, gráficos, metas)
- [ ] `dna.md` preenchido, sem `[A CONFIRMAR]` no texto visível
- [ ] 8 atos revisados; momento-assinatura funcionando e com versão estática
- [ ] Régua de acabamento de `qualidade.md` conferida (`comparar-densidade.js` contra a referência)
- [ ] `gate-texto.py` limpo; prova de autoria ≥ 5/8; teste de remoção da assinatura
- [ ] Contraste do pior pixel aprovado; teste de flick aprovado em seções fixadas/scrub
- [ ] Premissa da marca e frases reais dos compradores no `dna.md`
- [ ] Variantes testadas com `?seg=` e com escolha manual (se houver Camada 2)
- [ ] 390px e 1440px sem scroll horizontal; console limpo
- [ ] `auditoria.md` sem P1/P2; LCP < 2,5 s e CLS < 0,1 no mobile; contraste AA; foco visível; reduced motion ok
- [ ] 3D (se houver) otimizado, com poster e sem piorar o LCP
- [ ] `assets/manifesto.json` com tudo que foi gerado (ferramenta, modelo, prompt, custo)
- [ ] JSON-LD, OG 1200x630, sitemap, robots
- [ ] Arquivo Figma com DNA, tokens, assets, telas e reel
- [ ] `creditos.md` revisado e créditos CC BY visíveis no site (se houver)
- [ ] Vídeo do reel com narração montado; URL publicada conferida
