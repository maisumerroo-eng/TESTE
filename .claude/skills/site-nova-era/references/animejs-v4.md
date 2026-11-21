# Referência: Anime.js v4

Referência de implementação da skill `site-nova-era` (motion system). Decisão de SE e COMO animar vem das skills `animate`/`choreograph`.

Versão fixa: **animejs@4.5.0**. A API v4 é diferente da v3 (`anime({...})` não existe mais). Nunca escreva sintaxe v3.

## Instalar

Sem build (HTML puro, ES module):
```html
<script type="module">
  import { animate, createTimeline, stagger, onScroll, splitText, svg, utils }
    from 'https://cdn.jsdelivr.net/npm/animejs@4.5.0/+esm';
</script>
```
Com bundler: `npm i animejs@4.5.0` e `import { animate } from 'animejs'`.

## Mapa v3 → v4 (erros comuns)

| v3 (errado) | v4 (certo) |
|---|---|
| `anime({ targets: '.a', translateX: 100 })` | `animate('.a', { x: 100 })` |
| `easing: 'easeOutExpo'` | `ease: 'outExpo'` |
| `anime.timeline()` | `createTimeline()` |
| `anime.stagger(100)` | `stagger(100)` |
| `direction: 'alternate'` | `alternate: true` |
| `loop: true` | `loop: true` (igual) |
| `complete: fn` / `update: fn` | `onComplete: fn` / `onUpdate: fn` |
| `anime.set` / `anime.random` | `utils.set` / `utils.random` |
| `value: [0, 1]` (from/to) | `opacity: [0, 1]` ou `{ from: 0, to: 1 }` |

Atalhos de transform: `x`, `y`, `z`, `rotate`, `scale`, `skewX`... Prefira transform e opacity (composite-only). Não anime `top/left/width/height`.

## Receitas

**Entrada da hero (timeline):**
```js
const tl = createTimeline({ defaults: { ease: 'outExpo', duration: 900 } });
tl.add('.hero-kicker', { opacity: [0, 1], y: [16, 0] })
  .add('.hero-title .word', { opacity: [0, 1], y: ['100%', '0%'], delay: stagger(60) }, '-=600')
  .add('.hero-cta', { opacity: [0, 1], scale: [0.96, 1] }, '-=500');
```
Posição: `'-=600'` sobrepõe, `'+=200'` espera, `'<'` junto com o anterior, número = tempo absoluto.

**Texto palavra/letra (splitText):**
```js
const { words, chars } = splitText('.hero-title', { words: { wrap: 'clip' }, chars: true });
animate(chars, { y: ['100%', '0%'], duration: 700, ease: 'outQuart', delay: stagger(18) });
```
`wrap: 'clip'` cria máscara (overflow hidden) para o texto "subir" de dentro da linha. Use em títulos curtos, nunca em parágrafo.

**Reveal no scroll (dispara uma vez):**
```js
utils.$('.reveal').forEach(el => {
  animate(el, {
    opacity: [0, 1], y: [24, 0], duration: 800, ease: 'outCubic',
    autoplay: onScroll({ enter: 'bottom-=10% top', repeat: false }),
  });
});
```

**Scroll amarrado à rolagem (parallax / progresso):**
```js
animate('.parallax-img', {
  y: ['-8%', '8%'], ease: 'linear',
  autoplay: onScroll({ target: '.parallax-wrap', enter: 'bottom top', leave: 'top bottom', sync: true }),
});
```
`sync: true` amarra 1:1; `sync: 0.25` suaviza; `debug: true` mostra os limites na tela.

**Linha SVG se desenhando:**
```js
animate(svg.createDrawable('.line path'), { draw: ['0 0', '0 1'], duration: 1600, ease: 'inOutQuad' });
```

**Morph de forma:** `animate('#a', { d: svg.morphTo('#b'), duration: 800 })`.

**Contador numérico:**
```js
const o = { n: 0 };
animate(o, { n: 1250, duration: 1600, ease: 'outExpo', modifier: utils.round(0),
  onUpdate: () => (el.textContent = o.n) });
```

**Grade em onda (stagger 2D a partir do centro):**
```js
animate('.grid .cell', { scale: [0, 1], delay: stagger(40, { grid: [8, 5], from: 'center' }) });
```

**Mola (spring):** `ease: spring({ bounce: 0.3, duration: 600 })`. Bom para hover, toggle, cartões.

**Texto embaralhado (scramble):** `animate('.tag', { innerHTML: scrambleText() })` só em rótulo curto; confira a assinatura em `node_modules/animejs/dist` antes de usar parâmetros.

**Hover magnético (createAnimatable, sem criar animação a cada mousemove):**
```js
const a = createAnimatable('.magnet', { x: 300, y: 300, ease: 'outQuart' });
btn.addEventListener('mousemove', e => {
  const r = btn.getBoundingClientRect();
  a.x((e.clientX - r.left - r.width / 2) * 0.3);
  a.y((e.clientY - r.top - r.height / 2) * 0.3);
});
btn.addEventListener('mouseleave', () => { a.x(0); a.y(0); });
```

## React / Next

Use `createScope` para limpar tudo ao desmontar:
```js
useEffect(() => {
  const scope = createScope({ root: rootRef }).add(() => {
    animate('.card', { opacity: [0, 1], y: [20, 0], delay: stagger(80) });
  });
  return () => scope.revert();
}, []);
```

## Regras obrigatórias

1. **Reduced motion:** envolva tudo:
   ```js
   if (!matchMedia('(prefers-reduced-motion: reduce)').matches) { /* animações */ }
   ```
   Conteúdo deve estar visível sem JS: não deixe `opacity: 0` no CSS; o `[0, 1]` no `animate` já define o estado inicial.
2. Durações: UI 150–300 ms, entrada de seção 600–900 ms, hero até ~1,4 s no total. Nada que bloqueie clique.
3. Uma coreografia por tela: hero anima na chegada, seções revelam no scroll, o resto fica parado.
4. Sem `onScroll` com `sync` em mobile fraco se houver muitas imagens grandes; teste.
5. Testar com o Chrome DevTools MCP (ou Playwright): screenshot no fim da animação e console sem erros.
