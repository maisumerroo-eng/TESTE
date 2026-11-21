// auditar-site.js: auditoria automática e PRIORIZADA de um site (local ou publicado).
// Mede no Chromium com celular simulado (4G lento + CPU 4x): LCP, CLS, peso por tipo, maiores arquivos,
// JS/CSS não usado, imagens grandes demais, sem width/height, sem alt, fontes, terceiros, SEO, a11y básica.
// Uso: node auditar-site.js <url> [saida=auditoria]   → auditoria.md (ler isto) + auditoria.json
// Economia: corrija só os itens P1/P2 do relatório; não revise o site inteiro.
const { chromium } = require('playwright');
const fs = require('fs');

const url = process.argv[2];
const saida = process.argv[3] || 'auditoria';
if (!url) { console.error('uso: node auditar-site.js <url> [saida]'); process.exit(1); }
const KB = (b) => Math.round(b / 1024);

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  const cdp = await ctx.newCDPSession(page);
  await cdp.send('Network.enable');
  await cdp.send('Network.emulateNetworkConditions', { offline: false, latency: 150, downloadThroughput: 1.6 * 1024 * 1024 / 8, uploadThroughput: 750 * 1024 / 8 });
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
  const erros = [];
  page.on('pageerror', (e) => erros.push(e.message));
  page.on('console', (m) => { if (m.type() === 'error') erros.push(m.text()); });
  await page.addInitScript(() => {
    window.__m = { lcp: 0, lcpEl: '', cls: 0, longTasks: 0 };
    new PerformanceObserver((l) => l.getEntries().forEach((e) => { window.__m.lcp = e.startTime; window.__m.lcpEl = e.element ? (e.element.tagName + '.' + String(e.element.className).slice(0, 40)) : e.url || ''; })).observe({ type: 'largest-contentful-paint', buffered: true });
    new PerformanceObserver((l) => l.getEntries().forEach((e) => { if (!e.hadRecentInput) window.__m.cls += e.value; })).observe({ type: 'layout-shift', buffered: true });
    new PerformanceObserver((l) => l.getEntries().forEach((e) => { window.__m.longTasks += Math.max(0, e.duration - 50); })).observe({ type: 'longtask', buffered: true });
  });
  await Promise.all([page.coverage.startJSCoverage(), page.coverage.startCSSCoverage()]);
  const t0 = Date.now();
  await page.goto(url, { waitUntil: 'load', timeout: 120000 });
  const loadMs = Date.now() - t0;
  await page.waitForTimeout(2500);
  // congela o LCP antes de rolar (rolar por script não encerra a medição como um toque real faria)
  await page.evaluate(() => { window.__lcp0 = { lcp: window.__m.lcp, el: window.__m.lcpEl }; });
  // rola até o fim para disparar lazy-load, reveals e medir CLS real
  await page.evaluate(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += 500) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 120)); } scrollTo(0, 0); });
  await page.waitForTimeout(1000);
  const [js, css] = await Promise.all([page.coverage.stopJSCoverage(), page.coverage.stopCSSCoverage()]);
  const naoUsado = (arr) => arr.filter((e) => e.text).map((e) => {
    const total = e.text.length;
    let usado = 0;
    if (e.functions) { // JS: soma ranges de nível de bloco com count > 0 (aproximação)
      const r = e.functions.flatMap((f) => f.ranges).filter((x) => x.count > 0).sort((a, b) => a.startOffset - b.startOffset);
      let fim = 0; r.forEach((x) => { if (x.endOffset > fim) { usado += x.endOffset - Math.max(x.startOffset, fim); fim = x.endOffset; } });
    } else (e.ranges || []).forEach((x) => (usado += x.end - x.start));
    return { url: e.url, total, pct: Math.round(100 - Math.min(100, (usado / total) * 100)) };
  }).filter((x) => x.total > 20000);
  const sobra = [...naoUsado(js), ...naoUsado(css)];

  const dados = await page.evaluate(() => {
    const res = performance.getEntriesByType('resource').map((r) => ({ url: r.name, tipo: r.initiatorType, bytes: r.transferSize || r.encodedBodySize || 0 }));
    const nav = performance.getEntriesByType('navigation')[0];
    const host = location.hostname;
    const dpr = devicePixelRatio;
    const imgs = [...document.images].map((i) => {
      const r = i.getBoundingClientRect();
      return {
        src: (i.currentSrc || i.src).slice(0, 120), nat: i.naturalWidth, mostrado: Math.round(r.width * dpr),
        semDim: !i.getAttribute('width') || !i.getAttribute('height'), semAlt: !i.hasAttribute('alt'),
        abaixoDobra: r.top + scrollY > innerHeight * 1.2, lazy: i.loading === 'lazy',
        formatoAntigo: /\.(jpe?g|png)(\?|$)/i.test(i.currentSrc || i.src),
      };
    });
    const semNome = [...document.querySelectorAll('a[href], button')].filter((e) => !(e.innerText.trim() || e.getAttribute('aria-label') || e.getAttribute('title') || e.querySelector('img[alt]:not([alt=""]), svg title'))).length;
    const fontes = [...document.fonts].filter((f) => f.status === 'loaded').map((f) => `${f.family} ${f.weight} ${f.style}`);
    const meta = (n) => document.querySelector(`meta[name="${n}"], meta[property="${n}"]`)?.content || '';
    return {
      m: { ...window.__m, lcp: window.__lcp0.lcp, lcpEl: window.__lcp0.el }, html: nav ? nav.transferSize : 0, res, imgs, semNome, fontes: [...new Set(fontes)],
      terceiros: [...new Set(res.map((r) => { try { return new URL(r.url).hostname; } catch { return ''; } }).filter((h) => h && h !== host && !h.endsWith('.' + host)))],
      seo: { title: document.title, desc: meta('description'), canonical: !!document.querySelector('link[rel=canonical]'), og: !!meta('og:image'), lang: document.documentElement.lang, h1: document.querySelectorAll('h1').length, jsonld: document.querySelectorAll('script[type="application/ld+json"]').length, viewport: !!meta('viewport') },
      largura: document.documentElement.scrollWidth > innerWidth + 1,
    };
  });
  await browser.close();

  // ---------- análise ----------
  const porTipo = {};
  dados.res.forEach((r) => { porTipo[r.tipo] = (porTipo[r.tipo] || 0) + r.bytes; });
  const total = dados.res.reduce((s, r) => s + r.bytes, 0) + (dados.html || 0);
  const maiores = [...dados.res].sort((a, b) => b.bytes - a.bytes).slice(0, 8);
  const achados = [];
  const add = (p, area, txt, como) => achados.push({ p, area, txt, como });
  const lcp = Math.round(dados.m.lcp), cls = +dados.m.cls.toFixed(3);
  if (lcp > 4000) add(1, 'Performance', `LCP ${lcp} ms (meta < 2500) no elemento ${dados.m.lcpEl}`, 'pré-carregar a imagem/fonte do LCP (fetchpriority="high"), reduzir peso, tirar preloader/JS do caminho crítico');
  else if (lcp > 2500) add(2, 'Performance', `LCP ${lcp} ms (meta < 2500) em ${dados.m.lcpEl}`, 'otimizar o recurso do LCP');
  if (cls > 0.1) add(1, 'Performance', `CLS ${cls} (meta < 0,1)`, 'width/height em mídias, reservar espaço de fontes e banners');
  else if (cls > 0.05) add(3, 'Performance', `CLS ${cls}`, 'revisar elementos que mudam de tamanho');
  if (dados.m.longTasks > 600) add(2, 'Performance', `${Math.round(dados.m.longTasks)} ms de bloqueio do main thread (CPU 4x)`, 'adiar JS não crítico, dividir tarefas, import dinâmico');
  if (total > 3 * 1024 * 1024) add(1, 'Peso', `página com ${KB(total)} KB`, 'meta < 1,5 MB na carga inicial');
  else if (total > 1.5 * 1024 * 1024) add(2, 'Peso', `página com ${KB(total)} KB`, 'meta < 1,5 MB');
  const grandes = dados.imgs.filter((i) => i.nat && i.mostrado && i.nat > i.mostrado * 1.6);
  if (grandes.length) add(2, 'Imagens', `${grandes.length} imagem(ns) maiores que o exibido (ex.: ${grandes[0].src} ${grandes[0].nat}px p/ ${grandes[0].mostrado}px)`, 'gerar tamanhos com otimizar-imagens.sh + srcset/sizes');
  const antigas = dados.imgs.filter((i) => i.formatoAntigo);
  if (antigas.length) add(2, 'Imagens', `${antigas.length} imagem(ns) JPG/PNG`, 'converter para AVIF/WebP com <picture>');
  const semDim = dados.imgs.filter((i) => i.semDim);
  if (semDim.length) add(2, 'Imagens', `${semDim.length} imagem(ns) sem width/height`, 'declarar dimensões para evitar CLS');
  const semLazy = dados.imgs.filter((i) => i.abaixoDobra && !i.lazy);
  if (semLazy.length) add(3, 'Imagens', `${semLazy.length} imagem(ns) abaixo da dobra sem loading="lazy"`, 'adicionar loading="lazy" decoding="async"');
  const semAlt = dados.imgs.filter((i) => i.semAlt);
  if (semAlt.length) add(1, 'Acessibilidade', `${semAlt.length} imagem(ns) sem atributo alt`, 'alt descritivo ou alt="" se decorativa');
  if (dados.semNome) add(1, 'Acessibilidade', `${dados.semNome} link(s)/botão(ões) sem nome acessível`, 'texto visível ou aria-label');
  sobra.filter((x) => x.pct > 60).forEach((x) => add(x.total > 100000 ? 2 : 3, 'Código', `${x.url.split('/').pop() || x.url} com ${x.pct}% não usado (${KB(x.total)} KB de texto)`, 'remover código morto, dividir por página, carregar sob demanda'));
  if (dados.fontes.length > 4) add(3, 'Fontes', `${dados.fontes.length} variações de fonte carregadas`, 'meta ≤ 4: cortar pesos, usar fonte variável, subset latin');
  if (dados.terceiros.length > 4) add(3, 'Terceiros', `${dados.terceiros.length} domínios de terceiros: ${dados.terceiros.slice(0, 6).join(', ')}`, 'carregar análise só após consentimento, self-host do que der');
  if (erros.length) add(1, 'Erros', `${erros.length} erro(s) no console: ${erros[0].slice(0, 120)}`, 'corrigir antes de qualquer otimização');
  if (dados.largura) add(1, 'Layout', 'rolagem horizontal no mobile (390px)', 'achar o elemento que vaza (overflow) e corrigir');
  const s = dados.seo;
  if (!s.title || s.title.length > 65) add(2, 'SEO', `title ${s.title ? 'com ' + s.title.length + ' caracteres' : 'ausente'}`, 'serviço + nicho + marca, até ~60 caracteres');
  if (!s.desc) add(2, 'SEO', 'sem meta description', 'oferta de entrada em ~150 caracteres');
  if (s.h1 !== 1) add(2, 'SEO', `${s.h1} H1 na página`, 'exatamente 1 H1');
  if (!s.og) add(3, 'SEO', 'sem og:image', 'imagem 1200x630 da marca');
  if (!s.canonical) add(3, 'SEO', 'sem canonical', '<link rel="canonical">');
  if (!s.jsonld) add(3, 'SEO', 'sem JSON-LD', 'Organization + ProfessionalService/LocalBusiness');
  if (!s.lang) add(2, 'Acessibilidade', 'html sem lang', 'lang="pt-BR"');
  achados.sort((a, b) => a.p - b.p);

  const md = [
    `# Auditoria: ${url}`, '', `Mobile 390px, 4G lento, CPU 4x. Load ${loadMs} ms.`, '',
    '| Métrica | Valor | Meta |', '|---|---|---|',
    `| LCP | ${lcp} ms | < 2500 |`, `| CLS | ${cls} | < 0,1 |`, `| Bloqueio (long tasks) | ${Math.round(dados.m.longTasks)} ms | < 600 |`,
    `| Peso total | ${KB(total)} KB | < 1500 |`, `| Requisições | ${dados.res.length + 1} | < 60 |`, '',
    `Peso por tipo: ${Object.entries(porTipo).sort((a, b) => b[1] - a[1]).map(([t, b]) => `${t} ${KB(b)} KB`).join(' · ')}`, '',
    '## O que corrigir (em ordem)', '',
    achados.length ? achados.map((a) => `- **P${a.p} ${a.area}:** ${a.txt}. Como: ${a.como}.`).join('\n') : '- Nada acima das metas.', '',
    '## Maiores arquivos', '', ...maiores.map((r) => `- ${KB(r.bytes)} KB ${r.tipo} ${r.url.slice(0, 110)}`), '',
    `Fontes: ${dados.fontes.join(', ') || 'nenhuma'}`, `Terceiros: ${dados.terceiros.join(', ') || 'nenhum'}`,
  ].join('\n');
  fs.writeFileSync(saida + '.md', md + '\n');
  fs.writeFileSync(saida + '.json', JSON.stringify({ url, lcp, cls, total, achados, maiores, naoUsado: sobra, erros, dados }, null, 2));
  console.log(md.split('## Maiores')[0]);
})().catch((e) => { console.error('falhou:', e.message); process.exit(1); });
