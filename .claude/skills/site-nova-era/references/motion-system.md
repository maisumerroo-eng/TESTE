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
| **Vídeo no scroll (scrub)** | vídeo avança/volta com o scroll, faixas de legenda com platô, hero estático em celular/reduced motion; `templates/scrub/`, regras em `video-scrub.md` | alto, é o momento-assinatura |
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

## 6. Coreografia "eco" (seções guiadas por scroll: pin e scrub)

Cada batida ganha a própria entrada, e ela **ecoa o que a cena está fazendo** naquele momento: palavras derivam para baixo enquanto algo cai, uma palavra "soca" quando um impacto pousa, letras se juntam enquanto a tinta se junta. Entrada e cena leem como um evento só. Parte fixa (vale para qualquer entrada inventada): só `transform` e `opacity`, guiadas por uma variável de progresso `--k` (0 a 1) escrita pelo loop só quando muda, **reversíveis** ao rolar para cima (exceção: a 1ª batida abre montada no carregamento), deslocamentos "aleatórios" com **semente fixa** (iguais a cada carregamento).

Cardápio (exemplos, não lista fechada):
| Entrada | Ecoa | Como |
|---|---|---|
| Dispersão | tinta/partículas se juntando | por letra, limiar aleatório `--th`, voo de `--jx/--jy/--jr` até 0 |
| Alinhamento em grade | precisão, montagem | igual à dispersão, limiar em ordem de leitura, só horizontal |
| Desfoque → nítido | névoa clareando, foco | duas cópias: a suave com `blur` **estático**; crossfade só de opacidade (nunca animar `filter`) |
| Soco com overshoot | impacto | escala por palavra passa de 1 e assenta; ênfase com overshoot maior |
| Subida em etapas | chegada ao repouso | título por palavra → subtítulo (`--k` > .66) → CTA (`--k` > .78) |
| Deriva para baixo | queda, despejo | `translateY` negativo até 0 |
| Aproximação | túnel, avanço | `scale(.82 → 1)` com opacidade |
| Metades se abrindo | cortina, dobra | duas metades saem da linha central |

## 7. Armadilhas que matam animação em silêncio

- **Cascata:** estados inicial e final da entrada com o prefixo do contêiner (`.card .part` / `.card.in .part`), senão uma regra posterior cancela. Provar que cada entrada toca.
- **Aposentar o escalonamento:** depois da entrada, o atraso e a transição de reveal não podem continuar valendo (hover de botão ficaria seco ou atrasado). O `motion.js` já troca `data-reveal` por `data-revealed` ao terminar.
- **`animation-fill-mode: forwards` vence para sempre:** entrada no pai, estilo dinâmico no filho.
- **Loops começam no meio do ciclo:** atraso negativo (`-1.2s`). Pausar fora da tela com classe via IntersectionObserver e em aba oculta com `body.paused *, body.paused *::before, body.paused *::after { animation-play-state: paused !important }` (a propriedade não é herdada).
- **Nunca** sobrescrever `el.style.transition` em JS: alternar classe.
- **Texto mascarado** precisa de respiro para descendentes (g, y, p): padding em em com margem negativa igual (já no `.rv-w`).
- **Loop de scroll suavizado:** `shown += (target - shown) * (1 - Math.pow(1 - k, dt / 16.667))` para a mesma sensação em 60 e 120 Hz; o loop descansa ao convergir.
- **DOM só na mudança:** comparar com valor em cache; texto que muda com scroll no máximo ~10 Hz.

## 8. Ambiente (opcional, com crítica)

Uma camada fixa atrás de tudo (grão, deriva lenta ≥ 60 s, brilho suave no mundo da marca) faz rolar parecer atravessar um lugar. Usar só se a marca pedir e se não brigar com a assinatura; pausada fora de foco; desligada em reduced motion. O padrão "site inteiro animado, partículas em todo lugar" **não** entra: conflita com a regra de uma assinatura e loops só no fundo.
