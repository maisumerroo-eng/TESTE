// auditar-contraste.js: contraste do PIOR pixel de texto sobre imagem/vídeo/gradiente (o quadro médio mente).
// Esconde só os glifos (cor transparente, sem sombra), fotografa a caixa do texto como o visitante vê
// (com scrims, gradientes e imagem) e compara a cor do texto com o pixel de fundo mais desfavorável.
// Metas: texto grande (≥ 24px ou ≥ 18,7px negrito) 3,5:1 · texto normal 4,5:1.
// Uso: node auditar-contraste.js <url> [largura=390] ["seletores"]   (padrão: "h1, .hero p, [data-contrast]")
const { chromium } = require('playwright');

const [url, largura = '390', sels = 'h1, .hero p, [data-contrast]'] = process.argv.slice(2);
if (!url) { console.error('uso: node auditar-contraste.js <url> [largura] ["seletores"]'); process.exit(1); }

(async () => {
  const b = await chromium.launch();
  const w = Number(largura);
  const p = await b.newPage({ viewport: { width: w, height: w < 700 ? 844 : 900 }, deviceScaleFactor: 1 });
  await p.goto(url, { waitUntil: 'networkidle' });
  const n = await p.evaluate((s) => document.querySelectorAll(s).length, sels);
  let falhas = 0;
  for (let i = 0; i < Math.min(n, 20); i++) {
    const info = await p.evaluate(([s, i]) => {
      const el = document.querySelectorAll(s)[i];
      el.scrollIntoView({ block: 'center' });
      const cs = getComputedStyle(el);
      return { txt: el.textContent.trim().replace(/\s+/g, ' ').slice(0, 50), cor: cs.color, size: parseFloat(cs.fontSize), peso: +cs.fontWeight };
    }, [sels, i]);
    await p.waitForTimeout(1300);   // reveals e imagens assentam
    const box = await p.evaluate(([s, i]) => {
      const el = document.querySelectorAll(s)[i];
      el.dataset.ctxOld = el.getAttribute('style') || '';
      el.style.setProperty('color', 'transparent', 'important');
      el.style.setProperty('text-shadow', 'none', 'important');
      el.querySelectorAll('*').forEach((c) => { c.style.setProperty('color', 'transparent', 'important'); c.style.setProperty('text-shadow', 'none', 'important'); });
      const r = el.getBoundingClientRect();
      return { x: Math.max(0, r.x), y: Math.max(0, r.y), width: Math.min(r.width, innerWidth - Math.max(0, r.x)), height: Math.min(r.height, innerHeight - Math.max(0, r.y)) };
    }, [sels, i]);
    if (box.width < 2 || box.height < 2) continue;
    const png = (await p.screenshot({ clip: box })).toString('base64');
    const res = await p.evaluate(async ([png, cor]) => {
      const img = new Image(); img.src = 'data:image/png;base64,' + png; await img.decode();
      const c = new OffscreenCanvas(img.width, img.height).getContext('2d'); c.drawImage(img, 0, 0);
      const d = c.getImageData(0, 0, img.width, img.height).data;
      const lin = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
      const lum = (r, g, b) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
      const [tr, tg, tb] = cor.match(/[\d.]+/g).map(Number);
      const lt = lum(tr, tg, tb);
      const claro = lt > 0.4;
      let pior = claro ? 0 : 1;
      for (let k = 0; k < d.length; k += 4) { const L = lum(d[k], d[k + 1], d[k + 2]); pior = claro ? Math.max(pior, L) : Math.min(pior, L); }
      const hi = Math.max(lt, pior), lo = Math.min(lt, pior);
      return (hi + 0.05) / (lo + 0.05);
    }, [png, info.cor]);
    await p.evaluate(([s, i]) => {
      const el = document.querySelectorAll(s)[i];
      el.setAttribute('style', el.dataset.ctxOld); delete el.dataset.ctxOld;
      el.querySelectorAll('*').forEach((c) => { c.style.removeProperty('color'); c.style.removeProperty('text-shadow'); });
    }, [sels, i]);
    const grande = info.size >= 24 || (info.size >= 18.7 && info.peso >= 700);
    const meta = grande ? 3.5 : 4.5;
    const ok = res >= meta;
    if (!ok) falhas++;
    console.log(`${ok ? 'ok   ' : 'FALHA'} ${res.toFixed(2)}:1 (meta ${meta}) ${grande ? 'grande' : 'normal'} "${info.txt}"`);
  }
  console.log(falhas ? `${falhas} falha(s): aprofundar o scrim/gradiente atrás desse texto ou mover o texto para a área mais calma da imagem` : 'contraste aprovado no pior pixel');
  await b.close();
})().catch((e) => { console.error('falhou:', e.message); process.exit(1); });
