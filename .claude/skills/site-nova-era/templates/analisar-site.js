// analisar-site.js: raio-x de um site de referência para atualizar a skill site-nova-era.
// Uso: node analisar-site.js https://site.com.br <pasta-de-saida>
// Saída: info.json (libs, fontes, cores, keyframes, data-attrs, títulos, seções, metas),
//        reqs.txt (scripts/css/mídia carregados), dom.html, shots/d-*.png (desktop rolando), shots/m-full.png (mobile)
// Depois: baixar o JS/CSS principais listados em reqs.txt e procurar técnicas (ver SKILL.md, "Atualizar com novo site").
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const url = process.argv[2];
  const out = process.argv[3] || 'analise';
  if (!url) { console.error('uso: node analisar-site.js <url> <saida>'); process.exit(1); }
  fs.mkdirSync(out + '/shots', { recursive: true });
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 } });
  const p = await ctx.newPage();
  const reqs = []; const errs = [];
  p.on('request', (r) => reqs.push(r.resourceType() + ' ' + r.url()));
  p.on('pageerror', (e) => errs.push(e.message));
  await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await p.waitForTimeout(3000);
  await p.screenshot({ path: out + '/shots/d-000.png' });
  const H = await p.evaluate(() => document.documentElement.scrollHeight);
  let i = 1;
  for (let y = 600; y < H; y += 700) {
    await p.evaluate((v) => scrollTo(0, v), y);
    await p.waitForTimeout(1200);
    await p.screenshot({ path: out + `/shots/d-${String(i++).padStart(3, '0')}.png` });
  }
  fs.writeFileSync(out + '/dom.html', await p.content());
  const info = await p.evaluate(() => {
    const libs = ['anime', 'gsap', 'ScrollTrigger', 'Lenis', 'lenis', 'THREE', 'Swiper', 'AOS', 'Splitting', 'SplitType', 'barba', 'Webflow', '__NEXT_DATA__', '__NUXT__', 'React', 'Vue', 'LocomotiveScroll', 'Motion', 'lottie', 'bodymovin', 'PIXI', 'Spline', 'Framer', 'dataLayer', 'gtag', 'fbq'];
    const all = [...document.querySelectorAll('*')];
    const kf = []; for (const ss of document.styleSheets) { try { for (const r of ss.cssRules) if (r.type === 7) kf.push(r.name); } catch (e) { /* CSS de outro domínio */ } }
    return {
      title: document.title, lang: document.documentElement.lang,
      generator: document.querySelector('meta[name=generator]')?.content || null,
      libs: libs.filter((k) => k in window),
      fonts: [...new Set(all.slice(0, 3000).map((e) => getComputedStyle(e).fontFamily))].slice(0, 15),
      colors: [...new Set(all.slice(0, 2000).flatMap((e) => { const c = getComputedStyle(e); return [c.color, c.backgroundColor]; }))].filter((c) => c !== 'rgba(0, 0, 0, 0)').slice(0, 30),
      keyframes: kf,
      dataAttrs: [...new Set(all.flatMap((e) => [...e.attributes].map((a) => a.name).filter((n) => n.startsWith('data-'))))].slice(0, 80),
      heads: [...document.querySelectorAll('h1,h2,h3')].map((h) => h.tagName + ': ' + h.innerText.trim().replace(/\s+/g, ' ').slice(0, 140)),
      sections: [...document.querySelectorAll('header, section, footer')].slice(0, 60).map((s) => `${s.tagName}.${String(s.className).slice(0, 80)} #${s.id} h=${s.offsetHeight}`),
      media: { video: document.querySelectorAll('video').length, canvas: document.querySelectorAll('canvas').length, svg: document.querySelectorAll('svg').length, img: document.querySelectorAll('img').length },
      meta: [...document.querySelectorAll('meta')].map((m) => (m.name || m.getAttribute('property') || '') + '=' + (m.content || '').slice(0, 160)).filter((x) => x.length > 2),
      jsonld: [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => s.textContent.slice(0, 400)),
      H: document.documentElement.scrollHeight,
      texto: document.body.innerText.replace(/\n{2,}/g, '\n').slice(0, 9000),
    };
  });
  info.errs = errs;
  fs.writeFileSync(out + '/info.json', JSON.stringify(info, null, 2));
  fs.writeFileSync(out + '/reqs.txt', reqs.join('\n'));
  const m = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const mp = await m.newPage();
  await mp.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await mp.waitForTimeout(3000);
  await mp.screenshot({ path: out + '/shots/m-full.png', fullPage: true });
  await b.close();
  console.log(`ok: altura ${info.H}px, ${i} telas, libs: ${info.libs.join(', ') || 'nenhuma global'}`);
})().catch((e) => { console.error('falhou:', e.message); process.exit(1); });
