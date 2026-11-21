// regua-minima.js: GATE obrigatório. O site precisa igualar ou superar o nível medido da Vexter
// (referência premium da skill) em TODOS os parâmetros de acabamento, sem estourar o orçamento de performance.
// Uso: node regua-minima.js <url-do-nosso-site>      → sai com código 1 se reprovar.
// Os mínimos são da medição de 21/11/2026 (references/qualidade.md, "Régua mínima"). Não inflar número com
// regra duplicada, SVG vazio ou texto de enchimento: cada item precisa vir de componente, conteúdo ou estado real.
const { chromium } = require('playwright');

const MINIMO = {           // Vexter (home), 21/11/2026
  regrasCSS: 1550, keyframes: 57, regrasHover: 59, transicoes: 91, gradientes: 87, maskImage: 21, clipPath: 7,
  svgElementos: 223, imagens: 35, h3: 64, palavras: 1676, links: 69, variaveisCSS: 89,
};
const TETO = { lcpMs: 2500, cls: 0.1, pesoInicialKB: 1500, cssKB: 220, bloqueioInicialMs: 600 };   // performance não pode piorar

const url = process.argv[2];
if (!url) { console.error('uso: node regua-minima.js <url>'); process.exit(1); }

(async () => {
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await ctx.newPage();
  let cssBytes = 0, pesoInicial = 0, carregou = false;
  p.on('response', async (r) => { try { const len = (await r.body()).length; if (!carregou) pesoInicial += len; if (r.request().resourceType() === 'stylesheet') cssBytes += len; } catch { /* sem corpo */ } });
  await p.addInitScript(() => {
    window.__r = { lcp: 0, cls: 0, lt: 0 };
    new PerformanceObserver((l) => l.getEntries().forEach((e) => (window.__r.lcp = e.startTime))).observe({ type: 'largest-contentful-paint', buffered: true });
    new PerformanceObserver((l) => l.getEntries().forEach((e) => { if (!e.hadRecentInput) window.__r.cls += e.value; })).observe({ type: 'layout-shift', buffered: true });
    new PerformanceObserver((l) => l.getEntries().forEach((e) => (window.__r.lt += Math.max(0, e.duration - 50)))).observe({ type: 'longtask', buffered: true });
  });
  await p.goto(url, { waitUntil: 'networkidle', timeout: 90000 });
  await p.waitForTimeout(2500);
  carregou = true;
  const ini = await p.evaluate(() => ({ lcp: window.__r.lcp, lt: window.__r.lt }));
  await p.evaluate(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += 600) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 90)); } });
  await p.waitForTimeout(1200);
  const m = await p.evaluate(() => {
    let regrasCSS = 0, keyframes = 0, regrasHover = 0, transicoes = 0, gradientes = 0, maskImage = 0, clipPath = 0; const vars = new Set();
    const walk = (rs) => { for (const r of rs) { regrasCSS++; if (r.type === 7) { keyframes++; continue; } if (r.cssRules) { walk(r.cssRules); if (r.type === 4 || r.type === 12) continue; }
      const t = r.cssText || ''; if (t.includes(':hover')) regrasHover++; if (/transition\s*:/.test(t)) transicoes++; if (/gradient\(/.test(t)) gradientes++; if (/mask-image/.test(t)) maskImage++; if (/clip-path/.test(t)) clipPath++;
      (t.match(/--[\w-]+(?=\s*:)/g) || []).forEach((v) => vars.add(v)); } };
    for (const ss of document.styleSheets) { try { walk(ss.cssRules); } catch { /* CSS de outro domínio */ } }
    const q = (s) => document.querySelectorAll(s).length;
    // SVG: conta elementos desenhados, incluindo os de sprites referenciados por <use> (contados uma vez por uso)
    let svgElementos = q('svg path, svg polygon, svg rect, svg circle, svg ellipse, svg line, svg polyline');
    return { regrasCSS, keyframes, regrasHover, transicoes, gradientes, maskImage, clipPath, svgElementos, usosSprite: q('svg use'),
      imagens: q('img'), h3: q('h3'), palavras: document.body.innerText.split(/\s+/).filter(Boolean).length, links: q('a[href]'), variaveisCSS: vars.size };
  });
  const fim = await p.evaluate(() => window.__r);
  await b.close();

  // ícones em sprite externo (<use href="arquivo.svg#id">) contam como os elementos do símbolo: estimar 8 por uso
  m.svgElementos += m.usosSprite * 8;
  let reprovado = 0;
  console.log('PISO (Vexter)            nosso   mínimo');
  for (const [k, min] of Object.entries(MINIMO)) {
    const ok = m[k] >= min; if (!ok) reprovado++;
    console.log(`${ok ? 'ok   ' : 'FALTA'} ${k.padEnd(18)} ${String(m[k]).padStart(6)}   ${min}${ok ? '' : `  (faltam ${min - m[k]})`}`);
  }
  const perf = { lcpMs: Math.round(ini.lcp), cls: +fim.cls.toFixed(3), pesoInicialKB: Math.round(pesoInicial / 1024), cssKB: Math.round(cssBytes / 1024), bloqueioInicialMs: Math.round(ini.lt) };
  console.log('\nTETO (performance)       nosso   máximo');
  for (const [k, max] of Object.entries(TETO)) {
    const ok = perf[k] <= max; if (!ok) reprovado++;
    console.log(`${ok ? 'ok   ' : 'ESTOURO'} ${k.padEnd(18)} ${String(perf[k]).padStart(6)}   ${max}`);
  }
  console.log(reprovado ? `\nREPROVADO: ${reprovado} parâmetro(s). Subir com componentes, conteúdo e estados reais (nunca enchimento) e medir de novo.` : '\nAPROVADO: nível mínimo Vexter atingido sem perder performance.');
  process.exit(reprovado ? 1 : 0);
})().catch((e) => { console.error('falhou:', e.message); process.exit(1); });
