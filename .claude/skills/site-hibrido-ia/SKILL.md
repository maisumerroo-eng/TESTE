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
1. `remix_project` do projeto atual para o próximo workspace (Pro primeiro, depois Free). O remix não gasta crédito.
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
- O Higgsfield, quando autorizado, é a alternativa ao Lovable para imagens e vídeo (ver site-de-10k).
