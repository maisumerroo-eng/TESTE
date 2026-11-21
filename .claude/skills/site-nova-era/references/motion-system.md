# Motion system

Movimento é **linguagem da marca**, com vocabulário fechado. Antes de animar, carregue `animate` (decidir se e como) e `choreograph` (ordem e sobreposição).

## 1. Tokens (sempre em `:root`)

```css
--ease-out:   cubic-bezier(.22, 1, .36, 1);   /* entradas: chega rápido, assenta devagar */
--ease-io:    cubic-bezier(.65, 0, .35, 1);   /* trocas de estado, cortinas */
--ease-snap:  cubic-bezier(.7, 0, .2, 1);     /* abrir menu, wipe */
--ease-pop:   cubic-bezier(.18, .89, .32, 1.2); /* overshoot leve: badge, ícone */
--dur-ui: 220ms;  --dur-in: 800ms;  --dur-hero: 1200ms;
--stagger: 90ms;
```

## 2. Vocabulário de reveal (data-reveal)

Cada tipo tem **um uso**. Não misture mais de 4 tipos por página.

| `data-reveal` | Efeito | Usar em |
|---|---|---|
| `rise` | sobe 24px + fade | blocos de texto, cards (padrão) |
| `fade` | só opacidade | fundos, imagens secundárias |
| `words` | palavras sobem de dentro de máscara, leve rotação | títulos H1/H2 curtos |
| `wipe` | revela por `clip-path` da esquerda | linhas, faixas, imagens horizontais |
| `blur` | sai de desfoque + escala .94 | ícone/arte principal |
| `develop` | foto "revela" de cinza desfocado para cor | fotografias reais |
| `flip` | gira em X a partir da base | números, cards de etapa |
| `ignite` | texto acende (brilho na cor de destaque) e esfria | palavra-chave, número de resultado |
| `sweep` | brilho diagonal passa uma vez | botões principais, cards premium |
| `track` | itens de grupo entram em sequência | listas, logos, links de rodapé |

Grupo com sequência: `data-reveal-group data-stagger="90"` no pai; filhos com `data-reveal`.
Contador: `data-count="88" data-count-prefix="R$ " data-count-suffix=" mil"`.

Implementação pronta: `templates/motion.css` + `templates/motion.js` (sem dependência). Anime.js é opcional para timelines complexas: `references/animejs-v4.md`.

## 3. Biblioteca de interações (escolher, não empilhar)

| Interação | Como | Custo |
|---|---|---|
| **Header esperto** | some ao descer, volta ao subir, sólido após a hero | baixo |
| **Smooth scroll** | Lenis (`lenis@1.3.x` via CDN). Desligar com reduced motion. `data-lenis-prevent` em áreas roláveis | baixo |
| **Marquee arrastável** | loop infinito + arrasto com inércia + setas do teclado; clone com `aria-hidden` e `inert`; pausa fora da tela | médio |
| **Pilha de placas (sticky stack)** | cards `position: sticky` com `top` crescente; o de baixo escurece/encolhe ao ser coberto | médio |
| **Seção fixada com progresso** | container alto (300–500 svh) + palco `sticky`; progresso 0→1 do scroll controla passos, caminho SVG (`stroke-dashoffset`), marcador (`getPointAtLength`) | alto, é o momento-assinatura |
| **Troca de clima** | fundo muda de escuro para claro no último passo (amanhecer = resultado) | baixo |
| **Número que conta** | ease-out, 1,2–1,8 s, sempre até o mesmo valor, `tabular-nums` | baixo |
| **Ambiente em canvas** | partículas/chuva/grão; DPR ≤ 2, pausa com IntersectionObserver e `document.hidden`, densidade pela área | médio |
| **Botão com face 3D** | duas faces (frente e topo) giram em X no hover; frame dourado | baixo |
| **Wordmark gigante no rodapé** | texto vazado (`-webkit-text-stroke`) que preenche no scroll | baixo |
| **Preloader de marca** | só 1ª visita da sessão (`sessionStorage`), teto 2,5 s, pula se já carregou | médio |
| **Transição de página** | View Transitions API (`@view-transition { navigation: auto; }`) com cortina ≤ 600 ms; nada de `setTimeout` segurando o clique | baixo |
| **Cursor/hover magnético** | só `(hover: hover) and (pointer: fine)`; máx. 30% do deslocamento | baixo |

## 4. Coreografia por página

1. Hero ao carregar: kicker → título por palavras (stagger 60–90 ms) → subtítulo → CTA → mídia/números. Total ≤ 1,4 s.
2. Cada seção revela ao entrar 15% na tela, uma vez.
3. Uma seção fixada (assinatura) por página, no máximo.
4. Loops contínuos (ondas, chuva) só no fundo e pausados fora da tela.
5. Nada anima em resposta a teclado/ação repetitiva (ver `remove-animations`).

## 5. CSS moderno que diferencia

- `mask-image: linear-gradient(...)` para bordas que somem (fotos sangrando no fundo).
- `clip-path: inset()` para wipes e revelações sem layout shift.
- `animation-timeline: view()` para parallax barato (com `@supports` e fallback parado).
- `@property` para animar variáveis (ângulo de gradiente, porcentagem de brilho).
- `:has()` para estado de seção (`.sec:has(.is-active)`), `@container` para cards que se adaptam ao espaço.
- `text-wrap: balance` em títulos, `font-variant-numeric: tabular-nums` em números.
