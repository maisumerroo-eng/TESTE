// gravar-reel.js: grava o site rolando em vídeo vertical para Reels/TikTok.
// Uso: npx -y serve . -l 8080   (em outro terminal)
//      node gravar-reel.js http://localhost:8080 [velocidade_px_por_frame=6]
// Saída: video/*.webm (1080x1920). Converter: ffmpeg -i video/X.webm -c:v libx264 -pix_fmt yuv420p video/reel.mp4
const { chromium } = require('playwright');

(async () => {
  const url = process.argv[2] || 'http://localhost:8080';
  const step = Number(process.argv[3] || 6);
  const browser = await chromium.launch();
  const ctx = await browser.newContext({
    viewport: { width: 540, height: 960 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true,
    recordVideo: { dir: 'video', size: { width: 1080, height: 1920 } },
  });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  // fecha banner de cookies, se houver, para não aparecer no vídeo
  await page.locator('[data-cookie-action="accept"], .cookie-accept').first().click({ timeout: 1500 }).catch(() => {});
  await page.waitForTimeout(2500); // entrada da hero
  const total = await page.evaluate(() => document.documentElement.scrollHeight - innerHeight);
  for (let y = 0; y <= total; y += step) {
    await page.evaluate((v) => (window.__lenis ? window.__lenis.scrollTo(v, { immediate: true }) : scrollTo(0, v)), y);
    await page.waitForTimeout(16);
  }
  await page.waitForTimeout(1500);
  await ctx.close();
  await browser.close();
  console.log('vídeo salvo em ./video');
})();
