# Caso de estudo: vexterintelligence.com.br (analisado em 21/11/2026)

Site de contabilidade/BPO para transportadoras. Serve de régua de qualidade, não de molde: **nunca copiar** código, texto, ícones ou layout. Extrair princípios.

## Stack real (medida no navegador)

| Item | O que usa |
|---|---|
| Base | HTML estático + 1 CSS (~140 KB) + 1 JS (~52 KB), bundle próprio, sem framework |
| Scroll | Lenis (smooth scroll) com `data-lenis-prevent` em áreas com scroll próprio |
| Animação | **CSS keyframes** (~57 nomes) disparados por classes via IntersectionObserver + rAF. Não usa GSAP nem Anime.js (o comentário "Anime.js + codex" do reel não se confirma no site publicado) |
| Canvas | 1 canvas 2D (chuva diagonal dourada atrás da marca), DPR limitado a 2, pausa fora da tela |
| SVG | 55 SVGs inline: ícones isométricos, mapa de rota com `getTotalLength`/`getPointAtLength` |
| Fontes | Poppins 600/700 (títulos) + Inter (texto), woff2 self-hosted, só latin |
| Paleta | preto `#000`, grafite `#1b1b1b`, ouro `#c8a34d`, ouro claro `#ddbe7a`, ouro tinta `#8a6720`, branco, cinza `#f5f5f5` |
| Easings | `cubic-bezier(.22,1,.36,1)` (saída suave), `(.65,0,.35,1)` (in-out), `(.16,1,.3,1)`, `(.18,.89,.32,1.2)` (overshoot leve), `(.7,0,.2,1)` |
| CSS moderno | `mask-image` (42x), `clip-path` (25x), `backdrop-filter`, `:has()`, `@container`, `prefers-reduced-motion` (20x) |

## Estrutura (ordem real)

1. **Preloader** com vídeo curto da marca (teto de 6 s; sai quando o vídeo termina e a página carregou).
2. **Header** que some ao rolar para baixo e volta ao subir; vira sólido depois da hero. CTA dourado fixo.
3. **Hero escura**: pergunta-dor em caixa alta ("pagando mais imposto do que deveria?"), foto de mão com moeda, barras verticais douradas ondulando (keyframe `hero-wave` em ~30 barras), 2 cards de número que contam ("R$ 412 mil por ano / R$ 74 mil por mês").
4. **Faixa de prova**: carrossel infinito de frentes com ícones isométricos, arrastável com inércia, teclado (setas), clone `aria-hidden` + `inert`.
5. **Frentes de atuação**: título à esquerda + explicação à direita; 3 "placas" escuras que **empilham** no scroll (sticky stack com abas), cada uma com texto + foto real + links "ver serviço" e etiqueta Recorrente/Avulso/Projeto.
6. **Resultados "medidos em reais"**: casos sem nome do cliente (sigilo declarado), cidade/estado, número gigante dourado, antes/depois ("Devedor" → crédito), aviso "resultados passados não garantem resultados futuros".
7. **Como funciona (assinatura do site)**: seção fixada (~5400 px de scroll) com estrada em S desenhada em SVG; um marcador percorre a estrada; cada parada (Diagnóstico → Evolução) troca número gigante "01/06", ícone, texto e "Entrega". No passo 6 o fundo vira de escuro para claro (amanhecer = evolução). É a metáfora do nicho (transporte) virando interface.
8. **Método/marca**: o símbolo se forma no centro com chuva dourada em canvas; 7 atributos (Informação → Evolução) entram em sequência.
9. **Conteúdo**: carrossel de artigos do blog com termos do nicho (CIOT, CT-e, MDF-e, split payment 2027).
10. **CTA final** sobre foto escura de escritório: "Descubra o que os seus números dizem antes de decidir." + qualificação ("faturamento acima de R$ 500 mil").
11. **Rodapé** com wordmark gigante vazado "VEXTER", colunas Soluções/Vexter/Contato, slogan em caixa alta com tracking.
12. Extras: botão WhatsApp flutuante que só aparece depois da hero; banner LGPD; transição de página com cortina de 6 faixas ao clicar em link interno.

## Estratégias de conversão

- **Uma oferta só**: "Diagnóstico gratuito", repetida em header, hero, frentes, resultados, rota e CTA final.
- **Nicho declarado** no title, H1 de apoio, meta e copy: transportadoras. Vocabulário técnico real como prova de domínio.
- **Prova em reais** com contexto (UF, segmento) e honestidade (sigilo, disclaimer).
- **Processo com entregáveis**: cada etapa diz o que o cliente recebe ("Entrega: ...").
- **Qualificação no CTA** (faturamento mínimo) filtra lead ruim.
- **Conteúdo SEO de cauda longa** do nicho alimentando autoridade.
- WhatsApp como canal principal (cultura BR), sem formulário longo.

## Por que não tem cara de IA

- Metáfora do negócio vira interação (estrada = processo). Nada de "3 cards com ícone".
- Paleta de 2 cores + neutros, aplicada com disciplina; ouro como luz, não como enfeite.
- Ícones próprios isométricos no mesmo estilo; fotos reais de mão/papel/laptop, não ilustração genérica.
- Copy específica, com números, siglas e lugares (GO, PR, MG, SP, RJ). Zero "transforme seu negócio", zero emoji.
- Ritmo variado: hero cheia, faixa curta, placas longas, número gigante, seção fixada enorme, respiro claro.
- Microdetalhes: kicker com traço dourado, tracking em labels, número "01" com o zero vazado, "/06" pequeno.
- Animações com nome e propósito (develop, ignite, goldsweep), cada uma ligada a um tipo de conteúdo.

## Pontos fracos (fazer melhor)

- Banner de cookies com botões azuis padrão: quebra a marca. Estilizar com os tokens.
- Preloader de até 6 s e cortina de 1,4 s em toda navegação interna: bonito na primeira vez, cansativo depois. Mostrar preloader só na 1ª visita da sessão; transição ≤ 600 ms.
- H1 em caixa alta com pergunta: funciona, mas é fórmula comum. Preferir afirmação específica com número.
- Conteúdo fica invisível até o reveal disparar (screenshot de página inteira sai em branco). Garantir estado final visível para robôs e prints.
- Seção fixada de 5400 px é longa no mobile; oferecer pular ("ver todas as etapas").
- Zero personalização por visitante: todo mundo vê a mesma hero, mesmo vindo de anúncio de "PIS/COFINS" ou de "Reforma Tributária". Aqui está o espaço da megapersonalização.
