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
