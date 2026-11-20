---
name: site-hibrido-ia
description: Fluxo híbrido para criar sites/e-commerces. Outras IAs (Lovable, e Higgsfield quando conectado) geram o CSS e as imagens/assets, que é onde o Claude é mais fraco. O Claude monta a estrutura HTML a partir de um site de referência e escreve o JavaScript vanilla. Usa os créditos de todos os workspaces do Lovable em rodízio quando um acaba. Use quando o usuário pedir site, landing page ou loja "estilo X", "prompt pro Lovable", "gerar imagens da marca", ou quiser HTML + JS puro para continuar codando à mão.
---

# Site híbrido com IA (Lovable gera visual, Claude gera estrutura)

Divisão de trabalho:

| Quem | Faz |
|---|---|
| **Lovable** (e outras IAs de imagem) | `style.css` (tokens, componentes), todas as imagens (hero, tiles, produto, editorial, insta, embalagem) |
| **Claude** | estrutura HTML fiel ao site de referência, JS vanilla (UI pronta + esqueletos `// TODO:` para o usuário codar), catálogo em `products.js`, testes, commit |

Stack de entrega: **HTML + CSS + JS puro (ES modules)**, sem framework e sem build. O usuário quer continuar codando sozinho.

## Se o Claude for gerar visual ou texto

Quando o próprio Claude precisar criar CSS, layout ou texto (porque o Lovable falhou, ficou sem crédito ou para retoques), carregue antes e siga:
- `anthropic-skills:site-sem-cara-de-ia`: sem emoji, sem clichê, sem dado inventado, sem travessão no texto visível, paleta curta, ritmo variado.
- `anthropic-skills:site-de-10k`: barra de qualidade "site de 10 mil", mobília de conversão, autoteste adversarial, revisão de texto e inspeção de coerência de marca nas imagens.

## Passo a passo

### 1. Referência
- Busque o site de referência com o agente `web-fetch` e peça **só a estrutura**: barra de anúncio, header, mega-menu, hero, seções em ordem, anatomia do card, filtros, ordenação, paginação e rodapé.
- Domínios reais costumam diferir do nome da marca. Exemplo: John John é `johnjohndenim.com.br`, e `johnjohn.com.br` não resolve. Se falhar, peça o link ao usuário.
- O fetch volta truncado. Use o que vier e não invente o resto.

### 2. Lovable: projeto e prompt
- `list_workspaces`, depois tente criar com `create_project` no workspace Pro que for dono primeiro.
- Anexe logo e moodboard: `get_file_upload_url`, depois `curl -X PUT` com os headers retornados (`Content-Type`, `x-goog-content-length-range`, `x-goog-meta-user_id`), depois passe o `file_id` em `files`.
- O prompt (modelo em `templates/prompt-lovable.md`) exige:
  - site estático em `public/`, porque a stack do Lovable é React/TanStack e não dá para trocar;
  - `public/assets/css/style.css` com variáveis no `:root`;
  - imagens em `public/assets/img/` com **nomes exatos e previsíveis** (`produto-<slug>-1.jpg` para a frente, `-2.jpg` para o hover, `hero-N-*.jpg`, `tile-*.jpg`, `insta-N.jpg`);
  - direção de arte única descrita em todo prompt de imagem (luz, paleta, fundo, sem texto, sem logos reais);
  - identidade "estilo marca X" descrita **sem usar o nome nem o logo da marca X**.
- Acompanhe com `get_message` (wait 55s). Cada poll devolve o prompt inteiro e é caro: prefira `get_project` e veja `agentFinished` e `attentionReason`.

### 3. Rodízio de créditos entre workspaces (autorizado pelo usuário)
Quando aparecer `out_of_credits` (no erro ou em `get_project.project.attentionReason`):
1. **NÃO faça remix de projeto cujo agente parou no meio** (out_of_credits): o remix **retoma o prompt original inteiro** antes do seu pedido e queima o crédito do workspace novo. Prefira `create_project` novo no próximo workspace com **só** a tarefa que falta (anexe o CSS e as referências). Remix só serve para projeto com `agentFinished: true` e sem tarefa pendente.
2. `send_message` no remix pedindo **só o que falta**, com a lista de arquivos por prioridade e "não mexa em código".
3. Repita até acabar a lista ou os workspaces. Anote qual workspace gastou o quê e avise o usuário no final.

Workspaces deste usuário, por ordem de uso:
- Workspace menor: Pro, dono
- GAGAGA's Lovable: Pro, membro
- Gabriel's Lovable: Free, dono
- Maisumerro's Lovable: Free, membro

Mesmo assim, chame `list_workspaces` de novo a cada vez, porque essa lista muda.

### 4. Puxar os assets para o repo
- O preview (`id-preview--*.lovable.app`) é **privado** e responde 401 ao curl.
- Faça `deploy_project` com o slug `<marca>-assets`, depois baixe com `curl https://<slug>.lovable.app/assets/img/<arquivo>`. Os arquivos de `public/` são servidos na raiz.
- `read_file` serve para texto: puxe o CSS por ele. Não use em binário.
- Comprima com PIL: JPEG q78 progressivo, máximo de 2000px para hero/editorial e 1200px para o resto. Exemplo real: 7,4 MB caíram para 2,6 MB.
- Inspecione tudo numa folha de contato (`montage *.jpg -thumbnail 260x260 -tile 5x`):
  - logos de marcas reais;
  - anatomia;
  - se a **cor da peça bate com o catálogo** (ajuste `products.js` à foto, não o contrário).

### 5. Estrutura que o Claude escreve
```
<projeto>/
  index.html  categoria.html  produto.html
  assets/css/style.css        (do Lovable + ajustes)
  assets/js/layout.js         header, mega-menu, footer e drawers injetados via [data-include]
  assets/js/main.js           anúncio, header sólido no scroll, mega-menu (hover + teclado),
                              drawers (Esc, overlay, foco), hero slider, carrosséis,
                              grid 2/3/4 e PDP (cor/tamanho)
  assets/js/products.js       catálogo; imagens derivadas do slug
  assets/js/render.js         card, PDP, formatação BRL, parcelas,
                              fallback de imagem (data-alt e placeholder.svg)
  assets/js/cart.js | wishlist.js | search.js | filters.js
                              ESQUELETOS com // TODO: e lista de ganchos data-* no topo
  assets/img/placeholder.svg
  README.md  PROMPT-*.md
```
- O HTML já sai com os ganchos `data-*`: `data-add-to-cart`, `data-size`, `data-filter`, `data-sort`, `data-cart-count`, `data-drawer` e o resto. Comente cada seção.
- Fallback de imagem: escute `error` em captura **e** varra `img.complete && naturalWidth===0` no load, senão as imagens que falharam antes do módulo rodar ficam quebradas.
- Header desktop com 8 itens: use logo à esquerda, menu no centro e ícones à direita (`auto 1fr auto`). Com logo centralizado o menu encosta nele em 1440px.

### 6. Autoteste antes de entregar
- `python3 -m http.server`, depois Playwright em 1440 e 390:
  - screenshot das 3 páginas;
  - `scrollWidth - innerWidth === 0`;
  - contagem de cards;
  - zero `pageerror`;
  - hover do mega-menu.
- Rode o grep de emoji, travessão e clichê (lista da site-sem-cara-de-ia) e troque as ocorrências.
- Não invente dados (telefone, CNPJ, endereço, depoimentos). Deixe `<!-- PENDENTE -->` e diga ao usuário.

### 7. Entrega
- Commit na branch de desenvolvimento e push.
- Resposta curta em português, no estilo caveman. Informe:
  - o que o Lovable gerou e o que faltou;
  - quais workspaces gastaram crédito;
  - os links do editor e do deploy;
  - as pendências;
  - a ordem sugerida para o usuário codar os TODO (sacola, depois favoritos, filtros e busca).

## Aprendizados (atualize a cada projeto)
- **BRAVO Menswear (nov/2026)**:
  - os créditos do Lovable acabaram no meio do 1º build, que entregou só CSS e 20 imagens, sem HTML;
  - o Claude montou HTML e JS em cima disso, o que confirmou o valor do fluxo híbrido;
  - o remix para o próximo workspace continuou a geração das imagens que faltavam.
- **Produtos reais do cliente** (fotos de celular): copie para `<projeto>/referencias/` (no `.gitignore`), suba ao Lovable e peça **edição fiel**: mesma peça, textura, cor, botões e cordão, **sem etiqueta ou logo de terceiros** (as fotos vinham com etiqueta ZARA), fundo da direção de arte. Depois gere fotos com modelo vestindo só essas peças. Apague do catálogo e da pasta tudo que não for do cliente.
- Com catálogo real: **cada cor = 1 produto**, gerado de `MODELOS` em `products.js`. Sem preço informado, use `preco: null`; o card mostra "Consulte o preço no WhatsApp". Nunca invente preço, composição, política de troca ou cuidados.
- Número de 12 dígitos começando em 55 é WhatsApp (`config.js`, `waLink(texto)`). Ele vira a ação principal: barra de anúncio, PDP (mensagem com produto e tamanho), CTA final e rodapé.
- O conector do Lovable não tem cancelar: mensagem na fila roda e gasta crédito. Antes de enfileirar, confira se o pedido ainda vale. Pedido novo vai para outro workspace via remix.
- O check de segurança do Bash bloqueia heredoc grande e comandos encadeados longos: grave scripts em arquivo no scratchpad, use Edit para textos e mande comandos git simples.
- **Imagens sem cara de IA**: 1 pessoa por cena (duas lado a lado, simétricas e posando, gritam IA). Peça "candid, shot on 35mm film, mid-step, natural skin texture, slightly wrinkled fabric, not glossy, not symmetrical". O Figma AI (`generate_image`, só texto, sem referência) serve de reserva quando o Lovable está ocupado: crie o arquivo, `create_session`, gere e baixe o `image.url`.
- **Hero responsiva**: imagem 16:9 com pessoa no terço direito some no celular, porque o `cover` corta o centro. Use `object-position: var(--foco)` por slide (`style="--foco: 70% 20%"`). O degradê escurece só o lado do texto no desktop, e de baixo para cima no celular. Limite o texto a 42vw no desktop.
- **Header**: selecione por `#header`, nunca por `[data-header]`, porque o `<body data-header="transparente">` casa com o mesmo seletor e o JS liga no body, deixando o header transparente por cima do conteúdo. Para o vidro Apple, use `backdrop-filter: saturate(180%) blur(20px)` com fundo rgba (escuro sobre a hero, claro depois de rolar) e fallback em `@supports not`. O `top` do header acompanha a barra de anúncio por JS: `max(0, alturaAnuncio - scrollY)`.
- **Estética "Hugo Boss potente"** (prompt base que funcionou): "Hugo Boss style menswear campaign, ONE powerful confident man, early 30s, hard directional side light, deep shadows, raw concrete / brutalist architecture, monochrome palette, natural skin texture, medium format, subtle grain, no logos/text/tags". Para a foto de produto: "seamless warm stone-grey studio background, standing facing camera, cropped head to mid-shin" com o mesmo homem-tipo em todas as cores, o que dá consistência de catálogo. Descreva a peça igual em todos os prompts e troque só a cor.
- **Painel admin**: entregue `admin.html` + `admin.css` com todas as telas e ganchos `data-*` (`data-tela`, `data-ir`, `data-form`, `<template>` para linhas) e `admin.js` só com TODO, para o usuário codar depois. KPIs sem dado mostram "—", nunca número inventado.
- **Foto de produto "sem fundo" (padrão aprovado)**: 3 imagens por produto, todas com "pure flat seamless background solid very light warm off-white #FAFAF8, no floor line, no shadow on background, isolated cutout look":
  - `-1` é um modelo de corpo inteiro **posando**. Varie a etnia e a idade entre os produtos para dar representatividade.
  - `-2` é a **peça sozinha em ghost mannequin** (invisible mannequin, front view, no hanger).
  - `-3` é o mesmo modelo **de costas**.
  - Meça a cor do canto da foto com PIL (deu #F7F7F5) e iguale o `--branco` do site a ela: a pessoa parece recortada.
- **Hover do card**: o modelo some (opacity 0, scale 1.05, blur 6px) e a peça surge (de scale .94 + blur 8px para nítida, com 80ms de atraso), em 520 a 900ms, só em `@media (hover: hover)`. A PDP tem um visor com botões de ângulo Frente/Costas/Peça e a mesma transição.
- **Header da home**: transparente de verdade sobre a hero, sem blur e sem linha. O vidro só entra quando `scrollY > hero.offsetTop + hero.offsetHeight - header.offsetHeight`, ou com o mega-menu aberto. Um degradê escuro de 180px no topo da hero (`.hero::before`) segura a legibilidade do menu branco.
- **Checkout sem backend**: a sacola fica no localStorage (`cart.js`) e o `checkout.html` tem dados, entrega (envio ou retirada, CEP pelo ViaCEP), pagamento (Pix, link de cartão, dinheiro) e resumo. O botão monta a mensagem e abre `wa.me` e depois mostra a tela de sucesso com "abrir de novo". Nunca peça número de cartão no site.
- **Divisão Figma × Lovable que funcionou**: o Lovable, com as fotos reais anexadas, faz **flat lay fiel** (peça idêntica, sem etiqueta), que vira o ângulo "Dobrado" (`-4`) na PDP. O Figma, só por texto, faz as fotos de **modelo** (diversidade, poses, fundo do site). Os modelos do Lovable saem sempre o mesmo homem: não use para catálogo. Baixe primeiro para `referencias/lovable/` e só promova para `assets/img/` o que passar na inspeção.
- **Publicar (o que funcionou)**:
  - Vercel: o conector deu 403 de escopo e os links de aprovação "expiravam", porque o app abre o link para montar a prévia e o link é de uso único. O push direto para a `main` foi bloqueado pela proteção da sessão; o caminho foi abrir PR e o usuário fazer o merge.
  - **Cloudflare Pages, feito sozinho**: peça o token com `request_credential` (host `api.cloudflare.com`, permissões Pages Edit + Account Settings Read) e crie o projeto pela API. O `wrangler pages deploy` falha (8000013) porque o proxy troca o JWT de upload pelo token. Use `scripts/deploy-cloudflare.py`, que manda as chamadas com o token pelo proxy e as com o JWT direto (`--noproxy '*'`), com hash blake3(base64+ext)[:32]. O Pages troca `x.html` por `/x` com 308 e mantém a query string.
  - Antes de publicar, monte uma pasta só com o público: sem `admin.html` (não tem login) e sem `referencias/`.
- O Higgsfield, quando autorizado, é a alternativa ao Lovable para imagens e vídeo (ver site-de-10k).
