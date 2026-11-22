// comparar-imagem.js: loop de fidelidade imagem → HTML. Renderiza a página no mesmo tamanho da imagem de referência,
// mede a semelhança (% de pixels quase iguais + diferença média) e gera um mapa de diferenças para corrigir.
// Uso: node comparar-imagem.js <url-ou-arquivo-html> <imagem-referencia.png> [saida=diff] [--alvo=0.9] [--largura=1440]
// Repetir corrigir → comparar até atingir o alvo. Só para designs do próprio cliente (mockup, Figma, site antigo dele).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const flags = Object.fromEntries(args.filter((a) => a.startsWith('--')).map((a) => a.slice(2).split('=')));
const [alvoUrl, refImg, saida = 'diff'] = args.filter((a) => !a.startsWith('--'));
if (!alvoUrl || !refImg) { console.error('uso: node comparar-imagem.js <url|arquivo.html> <referencia.png> [saida] [--alvo=0.9] [--largura=1440]'); process.exit(1); }
const meta = parseFloat(flags.alvo || 0.9);

(async () => {
  const b = await chromium.launch();
  const p0 = await b.newPage();
  const refB64 = fs.readFileSync(refImg).toString('base64');
  const ext = path.extname(refImg).slice(1).replace('jpg', 'jpeg') || 'png';
  // descobre o tamanho da referência
  const dim = await p0.evaluate(async ([d, e]) => { const i = new Image(); i.src = `data:image/${e};base64,${d}`; await i.decode(); return [i.width, i.height]; }, [refB64, ext]);
  const largura = Number(flags.largura || dim[0]);
  const escala = largura / dim[0];
  const altura = Math.round(dim[1] * escala);
  await p0.close();
  const p = await b.newPage({ viewport: { width: largura, height: altura }, deviceScaleFactor: 1 });
  const url = /^https?:/.test(alvoUrl) ? alvoUrl : 'file://' + path.resolve(alvoUrl);
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: '*,*::before,*::after{animation:none!important;transition:none!important} html{scroll-behavior:auto!important}' });
  await p.waitForTimeout(800);
  const shot = (await p.screenshot({ fullPage: false })).toString('base64');
  const r = await p.evaluate(async ([a, bb, e, w, h]) => {
    const load = async (src) => { const i = new Image(); i.src = src; await i.decode(); return i; };
    const A = await load('data:image/png;base64,' + a), B = await load(`data:image/${e};base64,${bb}`);
    const ca = new OffscreenCanvas(w, h).getContext('2d'); ca.drawImage(A, 0, 0, w, h);
    const cb = new OffscreenCanvas(w, h).getContext('2d'); cb.drawImage(B, 0, 0, w, h);
    const da = ca.getImageData(0, 0, w, h).data, db = cb.getImageData(0, 0, w, h).data;
    const out = new OffscreenCanvas(w, h); const co = out.getContext('2d'); const img = co.createImageData(w, h);
    let iguais = 0, soma = 0; const n = w * h; const faixas = new Array(10).fill(0);
    for (let k = 0; k < da.length; k += 4) {
      const d = (Math.abs(da[k] - db[k]) + Math.abs(da[k + 1] - db[k + 1]) + Math.abs(da[k + 2] - db[k + 2])) / 3;
      soma += d; if (d < 16) iguais++;
      const y = Math.floor((k / 4) / w); if (d >= 16) faixas[Math.min(9, Math.floor(y / h * 10))]++;
      const g = (da[k] + da[k + 1] + da[k + 2]) / 3 * 0.35;
      img.data[k] = d >= 16 ? 255 : g; img.data[k + 1] = d >= 16 ? 40 : g; img.data[k + 2] = d >= 16 ? 60 : g; img.data[k + 3] = 255;
    }
    co.putImageData(img, 0, 0);
    const blob = await out.convertToBlob({ type: 'image/png' });
    const buf = new Uint8Array(await blob.arrayBuffer()); let bin = ''; for (const x of buf) bin += String.fromCharCode(x);
    return { semelhanca: iguais / n, difMedia: soma / n, faixas: faixas.map((f) => +(f / (n / 10) * 100).toFixed(1)), diff: btoa(bin) };
  }, [shot, refB64, ext, largura, altura]);
  fs.writeFileSync(saida + '-render.png', Buffer.from(shot, 'base64'));
  fs.writeFileSync(saida + '-mapa.png', Buffer.from(r.diff, 'base64'));
  await b.close();
  console.log(`semelhança ${(r.semelhanca * 100).toFixed(1)}% (meta ${(meta * 100).toFixed(0)}%) · diferença média ${r.difMedia.toFixed(1)}/255`);
  console.log('onde está a diferença (% de pixels diferentes por faixa de altura, topo → base): ' + r.faixas.join(' | '));
  console.log(`arquivos: ${saida}-render.png (como ficou) e ${saida}-mapa.png (vermelho = diferente). ${r.semelhanca >= meta ? 'ATINGIU a meta.' : 'Corrigir as faixas com mais vermelho e comparar de novo.'}`);
  process.exit(r.semelhanca >= meta ? 0 : 2);
})().catch((e) => { console.error('falhou:', e.message); process.exit(1); });
