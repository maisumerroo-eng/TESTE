// gera as capas (1080x1920) a partir de cover.html com parametros
const { chromium } = require('playwright'); const path = require('path');
const covers = [
  { out: 'cover_geo.png', kick: 'ChatGPT, Gemini e cia', h1: 'A IA tá indicando<br>o seu <em>concorrente</em>?',
    vis: '<div class="bub">qual a melhor hamburgueria<br>perto de mim? <span class="r">→ não é você</span></div>',
    cta: 'Comenta <b>IA</b> e descubra' },
  { out: 'cover_escolher.png', kick: 'Site feito por IA', h1: 'Ficou lindo…<br>mas <em>ninguém acessa</em>.',
    vis: '<div class="bub">hospedagem ✕ &nbsp;segurança ✕ &nbsp;backup ✕</div>',
    cta: 'Comenta <b>SITE</b>' },
  { out: 'cover_precisa.png', kick: 'Demo grátis', h1: 'Precisa de<br>um <em>site</em>?',
    vis: '<div class="bub">limpo · moderno · que converte</div>',
    cta: 'Comenta <b>SITE</b>' },
];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const c of covers) {
    const q = new URLSearchParams({ kick: c.kick, h1: c.h1, vis: c.vis, cta: c.cta }).toString();
    await p.goto('file://' + path.join(__dirname, 'cover.html') + '?' + q);
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(200);
    await p.screenshot({ path: path.join(__dirname, c.out) });
  }
  await b.close();
})();
