// Grava anuncio.html quadro a quadro (30 fps) e monta MP4 com trilha sintetizada.
const { chromium } = require('playwright'); const fs = require('fs'); const { execSync } = require('child_process');
const dir = process.argv[2] || 'frames', FPS = 30;
(async () => {
  fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + __dirname + '/anuncio.html', { waitUntil: "domcontentloaded" }); await p.evaluate(async () => { await document.fonts.ready; }); await p.waitForTimeout(800);
  const dur = await p.evaluate(() => window.__dur); const N = Math.ceil(dur * FPS);
  for (let i = 0; i < N; i++) {
    await p.evaluate(t => { window.__tl.seek(t, false); }, i / FPS);
    await p.screenshot({ path: `${dir}/${String(i).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 92 });
  }
  await b.close(); console.log(N, 'quadros,', dur.toFixed(2), 's');
})();
