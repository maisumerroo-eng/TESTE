# Qualidade: performance, acessibilidade, SEO, LGPD

## Performance (metas)

- LCP < 2,0 s em 4G, CLS < 0,05, INP < 200 ms. Lighthouse ≥ 90 em todas as categorias.
- Fontes: woff2 self-hosted (variável, subset latin), `preload` das fontes da 1ª dobra. Fonte de **título** com `font-display: optional` (zera o CLS da troca de fonte; testado: CLS 0,27 → 0); texto com `swap` + fallback calibrado (`@font-face` local Arial com `size-adjust` medido **na página servida**, comparando a largura da mesma frase nas duas fontes; medir via `file://` dá valor errado).
- Hero alinhada embaixo (`align-items: end`) amplifica CLS: qualquer crescimento do texto empurra tudo para cima. Testar com `auditar-site.js` (4G + CPU 4x), não só sem throttle.
- Imagens: AVIF/WebP, `width`/`height` sempre, `loading="lazy"` abaixo da dobra, `fetchpriority="high"` na hero.
- JS: 1 arquivo `type="module"` com `defer` implícito; nada bloqueando render. Lenis e Anime.js só se usados.
- Animar só `transform`, `opacity`, `clip-path`, `filter` (com moderação). Ver `animation-performance`.
- Canvas e loops: pausar com IntersectionObserver e `visibilitychange`; DPR ≤ 2; densidade pela área.
- Vídeo de fundo: mudo, `playsinline`, poster, ≤ 2 MB, nunca no mobile em conexão `saveData`.

## Conteúdo sempre visível

- O CSS esconde elementos para reveal **só** sob `html.motion` (classe adicionada pelo JS quando não há reduced motion). Sem JS, robô ou print: tudo visível.
- Clones de marquee: `aria-hidden="true"` + `inert`, e removem `data-reveal`.
- Seção fixada: no reduced motion vira lista vertical comum.

## Acessibilidade

- Contraste AA (4.5:1 texto, 3:1 texto grande). Dourado sobre branco quase nunca passa: usar tom escuro (`--gold-ink`).
- `:focus-visible` com anel na cor de marca; ordem de tab lógica; skip link.
- Um H1; H2 por seção com `aria-labelledby`; números grandes com texto alternativo legível ("88 mil reais").
- Carrosséis: teclado (setas), pausa no hover/foco, `aria-roledescription="carrossel"`.
- Alvos de toque ≥ 44px; WhatsApp flutuante não cobre CTA nem conteúdo no mobile.
- `prefers-reduced-motion`: sem smooth scroll, sem loops, reveals viram estado final.
- Rodar `web-design-guidelines` no final.

## SEO

- `title` = serviço + nicho + marca; `meta description` com oferta de entrada.
- Open Graph 1200x630 com a marca; `theme-color` da marca.
- JSON-LD: `Organization` + `ProfessionalService`/`LocalBusiness` (endereço, área atendida, telefone), `FAQPage` se houver FAQ.
- URLs de serviço próprias (uma página por frente) e blog com termos de cauda longa do nicho.
- `sitemap.xml`, `robots.txt`, `canonical`.

## LGPD

- Banner de consentimento com a cara da marca: Aceitar, Rejeitar, Personalizar com o mesmo peso visual.
- Scripts de análise/pixel só após aceitar. Personalização da Camada 2 com sinais de primeira parte não exige cookie de terceiro.
- Páginas: Política de Privacidade, Termos, canal do encarregado (DPO).
- Formulários: só os campos necessários, finalidade escrita ao lado do botão.

## Legibilidade sobre imagem, vídeo e gradiente (sistema de 4 camadas)

1. **Scrim global** suave sobre a mídia (radial ou linear), sempre ligado.
2. **Scrim local** atrás do bloco de texto (que aprofunda só enquanto o texto está ativo em seções guiadas por scroll); escurecer sem achatar: o gradiente morre antes dos cantos.
3. **Sombra de texto** em 3 camadas (borda justa, brilho médio, queda larga); desligada em botões.
4. **Chip** (pílula com fundo desfocado) para rótulos pequenos sobre mídia.

**Auditoria do pior pixel:** `node templates/auditar-contraste.js <url> 390 "<seletores>"` e de novo em 1440. Esconde só os glifos, fotografa a caixa como o visitante vê e mede contra o pixel mais desfavorável. Metas: 3,5:1 texto grande, 4,5:1 texto normal. Calibrar o scrim contra o pior quadro, nunca o médio. (No caso Meridiano pegou 2 falhas que Lighthouse e a auditoria geral não pegaram: título da hero no celular 2,85:1 e parágrafo do CTA 1,61:1.)

## Piso de qualidade (sempre)

- `overflow-x: clip` em `html` **e** `body`, com `hidden` antes como recuo.
- Largura de texto em `ch` **no próprio elemento de texto**, nunca no contêiner (o `ch` usa a fonte herdada).
- Linhas de texto lado a lado alinhadas na linha de base (`align-items: baseline`).
- Alvos de toque ≥ 44px em `(pointer: coarse)` sem mudar o layout (re-declarar alinhamento ao trocar `display`).
- Decorações posicionadas reservam espaço e somem em telas baixas (`@media (max-height: 560px)`).
- `<title>`, meta description, `theme-color` e **favicon SVG inline** da marca.
- `og:image`/`og:url` com URL absoluta: comentário `<!-- DEPLOY STEP -->` e ajuste na publicação.
- Marcos semânticos, skip link, `aria-hidden` em decoração; vídeo decorativo com `aria-hidden`, sem `controls`, fora da ordem de tab.
- Reduced motion no scrub é **ao vivo** (portões com listener de mudança). Nos reveals, a decisão é no carregamento; quem liga reduced motion no meio da sessão vê o resto revelar sem animação (limitação aceita).

## Testes antes de mostrar a alguém

- Larguras: **360, 390, 768, 1280 e 1440** (sem rolagem lateral, sem texto estourando, sem imagem quebrada).
- `auditar-site.js` (performance, peso, SEO, a11y básica) e `auditar-contraste.js` (pior pixel).
- `teste-flick.js` em toda seção fixada/scrub (5+ flicks de 120px por batida, nenhuma pulável em 360px).
- `gate-texto.py` limpo.
- Exercitar cada botão, link e o formulário; links reais (WhatsApp, Instagram, mapa).
- **Passe de olhos frescos, por último:** largar o checklist e olhar como visitante sem contexto. Algo flutua sem explicação? Algum item paralelo desigual? Algum trecho lê como enchimento? Consertar antes do usuário ver. Se houver como, um revisor independente acha o que o checklist não pensou.

## Depois de publicar: verificação no ar e recibos de velocidade

- `curl -sSI "$URL"` (200 por HTTPS), mídia pesada servindo direto, console limpo na URL do ar, scrub/pin funcionando no ar.
- Recibos reais (nunca estimativa): `curl -s -o /dev/null -w "TTFB %{time_starttransfer}s, total %{time_total}s, %{size_download} bytes\n" "$URL"` + `auditar-site.js` na URL do ar. Apresentar ao usuário com o argumento: site estático, sem backend para ser lento, mídia pesada atrás de pôster.
- Domínio novo: DNS pode levar horas e o certificado HTTPS sai depois; avisar em vez de declarar quebrado.
- Pedir ao usuário que teste no celular dele, na rede real.

## Régua de acabamento (nível de referência premium)

Medido com `templates/comparar-densidade.js` em 21/11/2026, Vexter (referência) x Meridiano v1 (nosso, aprovado em todas as auditorias técnicas e ainda assim percebido como "abaixo"):

| Métrica | Vexter | Meridiano v1 |
|---|---|---|
| Regras CSS | 1550 | 221 |
| Keyframes (animações nomeadas) | 57 | 2 |
| Regras de hover | 59 | 3 |
| Gradientes / mask-image | 87 / 21 | 6 / 0 |
| Elementos SVG (ícones, desenhos) | 223 | 24 |
| Imagens | 35 | 6 |
| Títulos h3 / palavras | 64 / 1676 | 7 / 782 |
| Links | 69 | 15 |

Lição: performance, contraste e ausência de vícios **não bastam** para parecer premium. O que separa é **densidade de acabamento**. Antes de entregar, conferir:
- [ ] **Sistema de ícones próprio** (8 a 40) num estilo só, usado em faixa de prova, frentes, etapas e valores.
- [ ] **Estado de hover/foco em tudo que é clicável** (botão com preenchimento/face, link com sublinhado animado, card que responde), 20+ estados.
- [ ] **Material nos números-chave:** gradiente metálico/da marca, varredura de luz uma vez, cartões com borda e brilho.
- [ ] **Bordas que somem** (`mask-image`) em carrosséis e fotos que sangram no fundo.
- [ ] **Assinatura com acabamento fotográfico ou 3D**, não ilustração chapada (blocos de cor lisos leem como placeholder).
- [ ] **Placas empilhadas mostrando o cabeçalho de cada placa** (lê como baralho, não como tela que cobre tela).
- [ ] **Resultados com antes/depois e gráfico que cresce**, não só números em linha.
- [ ] **Profundidade de conteúdo:** seção de autoridade (artigos/guias com imagem), rodapé completo (colunas, contatos, slogan), 1.500+ palavras na home quando o nicho pede confiança.
- [ ] **Peso na rolagem:** smooth scroll (Lenis) quando houver seções fixadas; microdetalhes (traço que se desenha, ícone que respira) em nível de sussurro.
- [ ] Rodar `comparar-densidade.js` contra a referência do cliente/nicho e fechar as lacunas que importam (não perseguir número).

