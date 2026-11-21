// teste-flick.js: valida o ritmo de seções guiadas por scroll (pin com [data-step], scrub com [data-band]).
// Visitante real dá "flick" na roda do mouse, não arrasta devagar. Critério:
//   - passos de 120px: cada item fica totalmente visível por pelo menos 5 passos seguidos (dá para ler);
//   - passos de 360px: nenhum item é pulado (chega a ficar visível pelo menos uma vez).
// Uso: node teste-flick.js <url> "<seção>" "<itens>"   ex.: node teste-flick.js http://localhost:8080 "#um-dia" "[data-step]"
const { chromium } = require('playwright');

const [url, secSel = '[data-pin]', itemSel = '[data-step]'] = process.argv.slice(2);
if (!url) { console.error('uso: node teste-flick.js <url> "<seção>" "<itens>"'); process.exit(1); }

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(url, { waitUntil: 'networkidle' });
  const visiveis = () => p.evaluate((sel) => [...document.querySelectorAll(sel)].map((el) => {
    const cs = getComputedStyle(el);
    return cs.visibility !== 'hidden' && cs.display !== 'none' && +cs.opacity >= 0.9;
  }), itemSel);
  let falhou = false;
  for (const passo of [120, 240, 360]) {
    await p.evaluate((s) => { const e = document.querySelector(s); const y = e.offsetTop - innerHeight * 0.1; if (window.__lenis) window.__lenis.scrollTo(y, { immediate: true, force: true }); else scrollTo(0, y); }, secSel);   // com Lenis, posicionar pelo Lenis
    await p.waitForTimeout(600);
    await p.mouse.move(700, 450);
    const fim = await p.evaluate((s) => { const e = document.querySelector(s); return e.offsetTop + e.offsetHeight; }, secSel);
    const hist = [];
    for (let i = 0; i < 400; i++) {
      await p.mouse.wheel(0, passo);
      await p.waitForTimeout(400);
      hist.push(await visiveis());
      if (await p.evaluate(() => scrollY + innerHeight) > fim + 200) break;
    }
    const n = hist[0]?.length || 0;
    const res = [];
    for (let k = 0; k < n; k++) {
      let max = 0, cur = 0, vezes = 0;
      hist.forEach((h) => { if (h[k]) { cur++; vezes++; max = Math.max(max, cur); } else cur = 0; });
      res.push({ item: k + 1, maiorSequencia: max, vezes });
    }
    const ruim = passo === 120 ? res.filter((r) => r.maiorSequencia < 5) : passo === 360 ? res.filter((r) => r.vezes === 0) : [];
    if (ruim.length) falhou = true;
    console.log(`passo ${passo}px (${hist.length} flicks): ` + res.map((r) => `#${r.item}=${r.maiorSequencia}`).join(' ') + (ruim.length ? `  FALHA: ${ruim.map((r) => '#' + r.item).join(', ')}` : '  ok'));
  }
  console.log(falhou ? 'RESULTADO: ajustar (fundir batida com a vizinha ou aumentar a altura da seção; nunca encurtar as rampas)' : 'RESULTADO: ritmo aprovado');
  await b.close();
})().catch((e) => { console.error('falhou:', e.message); process.exit(1); });
