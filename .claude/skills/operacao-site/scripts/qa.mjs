// QA de site estático. Uso:
//   node qa.mjs <baseURL> <pagina1.html> [pagina2.html ...]
// Escreve docs/qa.md (só falhas) e docs/shots/*.png na pasta atual.
// Saída no terminal: 1 linha por falha, ou "OK".
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';
// require acha o Playwright global; import ESM não.
const { chromium } = createRequire(process.cwd() + '/')('playwright');

const [base, ...pages] = process.argv.slice(2);
if (!base || !pages.length) {
  console.error('uso: node qa.mjs <baseURL> <pagina.html> [...]');
  process.exit(2);
}

const VIEWPORTS = [{ w: 1440, h: 900 }, { w: 390, h: 844 }];
// Lista mínima de clichês (ver site-sem-cara-de-ia). Ajuste em Aprendizados.
const CLICHES = ['eleve', 'desbloqueie', 'revolucion', 'experiência única', 'no próximo nível', 'mergulhe', 'jornada', 'sem igual', 'incomparável'];
const EMOJI = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u;

mkdirSync('docs/shots', { recursive: true });
const falhas = [];
const browser = await chromium.launch();

for (const vp of VIEWPORTS) {
  const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, deviceScaleFactor: 1 });
  for (const p of pages) {
    const page = await ctx.newPage();
    const erros = [];
    page.on('pageerror', (e) => erros.push(e.message));
    page.on('console', (m) => m.type() === 'error' && erros.push(m.text()));
    const tag = `${p}@${vp.w}`;
    try {
      await page.goto(`${base.replace(/\/$/, '')}/${p}`, { waitUntil: 'networkidle', timeout: 30000 });
    } catch (e) {
      falhas.push(`${tag}: não carregou (${e.message.split('\n')[0]})`);
      await page.close();
      continue;
    }
    // rola até o fim para disparar lazy-load
    await page.evaluate(async () => {
      for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); }
      window.scrollTo(0, 0);
    });
    await page.waitForTimeout(400);

    const r = await page.evaluate(() => {
      const overflow = document.documentElement.scrollWidth - window.innerWidth;
      const largos = overflow > 0
        ? [...document.querySelectorAll('body *')].filter((el) => el.getBoundingClientRect().right > window.innerWidth + 1)
            .slice(0, 3).map((el) => el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/)[0] : ''))
        : [];
      const quebradas = [...document.images].filter((i) => i.complete && i.naturalWidth === 0 && !i.src.endsWith('.svg')).map((i) => i.getAttribute('src')).slice(0, 5);
      const semAlt = [...document.images].filter((i) => !i.hasAttribute('alt')).length;
      return { overflow, largos, quebradas, semAlt, texto: document.body.innerText };
    });

    if (r.overflow > 0) falhas.push(`${tag}: overflow horizontal ${r.overflow}px em ${r.largos.join(', ')}`);
    if (r.quebradas.length) falhas.push(`${tag}: imagens quebradas ${r.quebradas.join(', ')}`);
    if (r.semAlt) falhas.push(`${tag}: ${r.semAlt} <img> sem alt`);
    for (const e of [...new Set(erros)].slice(0, 3)) falhas.push(`${tag}: erro JS ${e.slice(0, 160)}`);
    if (vp.w === VIEWPORTS[0].w) {
      if (EMOJI.test(r.texto)) falhas.push(`${p}: emoji no texto visível`);
      // traço sozinho na linha = placeholder de dado vazio (ok); no meio de frase = travessão proibido
      if (r.texto.split('\n').some((l) => l.includes('—') && l.trim() !== '—')) falhas.push(`${p}: travessão (—) no texto visível`);
      const low = r.texto.toLowerCase();
      const achou = CLICHES.filter((c) => low.includes(c));
      if (achou.length) falhas.push(`${p}: clichê: ${achou.join(', ')}`);
    }
    await page.screenshot({ path: `docs/shots/${p.replace(/\W+/g, '-')}-${vp.w}.png`, fullPage: false });
    await page.close();
  }
  await ctx.close();
}
await browser.close();

const out = falhas.length ? falhas.map((f) => `- ${f}`).join('\n') : 'OK';
writeFileSync('docs/qa.md', `# QA ${new Date().toISOString().slice(0, 16)}\n\n${out}\n`);
console.log(falhas.length ? out : 'OK');
process.exit(falhas.length ? 1 : 0);
