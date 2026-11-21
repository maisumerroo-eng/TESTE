---
name: site-animado
description: Criar do zero um site profissional animado para cliente (landing page, site institucional, portfólio, agência), pronto para entregar e mostrar em vídeo no Instagram. Fluxo completo com Claude Code: briefing, direção visual, HTML/CSS/JS puro, animações com Anime.js v4, polimento, revisão de acessibilidade, gravação do vídeo vertical do site e deploy na Vercel. Use quando o usuário pedir "site pra cliente", "site animado", "site estilo agência", "site com Anime.js", "site pra postar no reel" ou "site entregue pra @marca".
---

# Site animado para cliente

Stack: **HTML + CSS + JS puro (ES modules) + Anime.js 4.5.0 via CDN**. Sem framework, sem build. Deploy na Vercel.
Saídas: pasta do site, `video/reel.webm` (vertical 1080x1920) e URL publicada.

## 1. Briefing (perguntar só o que faltar)

Nome da marca, o que vende, público, 1 ação principal (WhatsApp, agendar, comprar), logo/cores se existirem, 1 ou 2 sites de referência. Sem resposta: assuma e diga o que assumiu.

## 2. Direção visual

Carregue `frontend-design` e `anthropic-skills:site-sem-cara-de-ia`. Defina e escreva no topo do `style.css`:
- 1 ideia de conceito em uma frase (ex: "editorial escuro, tipografia gigante, cortes secos").
- 2 fontes no máximo (Google Fonts), escala tipográfica, paleta de 3 a 5 tokens em `:root`.
- Grid e espaçamento em tokens (`--space-*`).

Inspiração de componente: Magic MCP (`21st`) e `shadcn` quando houver React; para HTML puro, só como referência visual.

## 3. Estrutura

Seções padrão (ajuste ao negócio, corte o que não serve):
1. Header fixo enxuto + CTA
2. Hero: título curto e forte, subtítulo, CTA, mídia (imagem/vídeo)
3. Prova: logos de clientes ou números reais (nunca inventar número)
4. Serviços/produtos em cards
5. Processo ou diferencial (3 a 4 passos)
6. Galeria/portfólio
7. Depoimentos (só reais, senão cortar)
8. CTA final + rodapé com contato

Arquivos: `index.html`, `style.css`, `main.js`, `assets/`. HTML semântico (`header`, `main`, `section` com `aria-labelledby`, `footer`). Conteúdo visível sem JS.

Imagens: Higgsfield MCP quando autenticado; senão placeholders com proporção certa e `alt` real.

## 4. CSS

Mobile primeiro, `clamp()` para tipografia, `min-height: 100svh` na hero, `:focus-visible` em tudo clicável, `@media (hover: hover)` para hover. Sem `opacity: 0` no CSS esperando JS.

## 5. Animação (Anime.js)

Carregue `animate` e `choreograph` para decidir o quê e quando. Implemente seguindo `references/animejs-v4.md` (API v4, nunca sintaxe v3).

Plano padrão de movimento (uma coreografia por tela, o resto parado):
| Onde | Efeito | Receita |
|---|---|---|
| Hero ao carregar | título sobe palavra por palavra, depois subtítulo e CTA | `createTimeline` + `splitText` (wrap clip) + `stagger` |
| Seções | reveal suave ao entrar na tela, uma vez | `onScroll({ repeat: false })` |
| Imagem grande | parallax leve amarrado ao scroll | `onScroll({ sync: true })` |
| Números | contador ao aparecer | objeto + `utils.round` |
| Detalhe de marca | linha/ícone SVG se desenhando | `svg.createDrawable` |
| CTA principal | hover magnético ou mola | `createAnimatable` / `spring` |

Tudo dentro de `if (!matchMedia('(prefers-reduced-motion: reduce)').matches)`.

## 6. Polimento e revisão

1. `impeccable` (polish) e `emil-design-eng` nos detalhes de interação.
2. `web-design-guidelines`: contraste, foco, alvos de toque, `alt`, ordem de títulos.
3. Abrir no Chrome DevTools MCP (ou Playwright): screenshots 390px e 1440px, console sem erro, Lighthouse.

## 7. Vídeo do site para o reel

Gravar o site rolando em formato vertical com Playwright (Chromium já instalado):

```js
// gravar-reel.js  →  node gravar-reel.js http://localhost:8080
const { chromium } = require('playwright');
(async () => {
  const url = process.argv[2];
  const browser = await chromium.launch();
  const ctx = await browser.newContext({
    viewport: { width: 540, height: 960 }, deviceScaleFactor: 2,
    recordVideo: { dir: 'video', size: { width: 1080, height: 1920 } },
  });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500); // entrada da hero
  const total = await page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
  for (let y = 0; y <= total; y += 6) {           // rolagem lenta e contínua
    await page.evaluate(v => scrollTo(0, v), y);
    await page.waitForTimeout(16);
  }
  await page.waitForTimeout(1500);
  await ctx.close(); await browser.close();      // vídeo salvo em video/
})();
```
Servir local com `npx -y serve . -l 8080`. Se `ffmpeg` existir, converter: `ffmpeg -i video/*.webm -c:v libx264 -pix_fmt yuv420p video/reel.mp4`.

Legenda sugerida para o post: curta, cita a marca, chama para o link da bio. Sem prometer resultado.

## 8. Deploy

Vercel (MCP `Vercel` ou `vercel.json` no repo). Conferir a URL publicada com screenshot antes de entregar. Commit e push no branch de trabalho.

## Checklist de entrega

- [ ] Conteúdo legível sem JS e com reduced motion
- [ ] Sem número, depoimento ou logo inventado
- [ ] 390px e 1440px sem scroll horizontal
- [ ] Console limpo, Lighthouse acessibilidade ≥ 95
- [ ] `video/reel.mp4` (ou `.webm`) gravado
- [ ] URL publicada conferida
