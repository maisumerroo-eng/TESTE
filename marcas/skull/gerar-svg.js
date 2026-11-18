const opentype = require('opentype.js'), fs = require('fs');
const out = process.argv[2];
const f5 = opentype.loadSync('mont-500.ttf'), f4 = opentype.loadSync('mont-400.ttf');
// texto centralizado com tracking (em unidades do size)
function textPath(font, str, size, cx, y, track) {
  const glyphs = font.stringToGlyphs(str), sc = size / font.unitsPerEm;
  const adv = glyphs.map(g => g.advanceWidth * sc);
  const total = adv.reduce((a, b) => a + b, 0) + track * (glyphs.length - 1);
  let x = cx - total / 2, d = '';
  glyphs.forEach((g, i) => { d += g.getPath(x, y, size).toPathData(2); x += adv[i] + track; });
  return d;
}
// coords no espaço ampliado 3x (grade da referência); transform volta para 640
const L = [
  'M360 52 L360 486',                                   // sutura central
  'M95 196 L163 352 L122 462',                         // têmpora
  'M142 424 L262 380 L328 424 L314 486 L262 520 L186 540 L144 500 Z', // olho
  'M122 462 L76 546 L132 610 L232 598 L258 638 L262 690 L318 714 L360 718', // maçã + maxilar
  'M360 486 L318 556 L306 600 L334 630 L360 606',       // nariz
  'M360 630 L360 718',                                  // septo/dentes
  'M156 646 L162 762 L292 882 L360 882',                // mandíbula externa
  'M186 640 L272 836 L292 882',                          // ramo interno
  'M236 734 Q300 770 360 772',                           // sorriso
];
const cranium = 'M122 470 A300 270 0 1 1 598 470';
const skull = `<g id="simbolo" transform="translate(200 95) scale(0.3333)" fill="none" stroke="url(#ouro)" stroke-width="20" stroke-linejoin="round" stroke-linecap="round">
  <path id="cranio" d="${cranium}"/>
  <g id="esq">${L.map(d=>`<path d="${d}"/>`).join('')}</g>
  <g id="dir" transform="translate(720 0) scale(-1 1)">${L.map(d=>`<path d="${d}"/>`).join('')}</g>
</g>`;
const word = textPath(f5, 'SKULL', 92, 320, 498, 14);
const sub = textPath(f4, 'LOUNGE & NIGHTCLUB', 22, 320, 538, 3.2);
const defs = `<defs><linearGradient id="ouro" gradientUnits="userSpaceOnUse" x1="0" y1="90" x2="0" y2="560">
  <stop offset="0" stop-color="#F1D9A0"/><stop offset=".45" stop-color="#C9A45C"/><stop offset="1" stop-color="#9A7535"/></linearGradient></defs>`;
const svg = (bg) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="80 70 480 500" width="960" height="1000">
<title>Skull Lounge &amp; Nightclub</title>${defs}${bg ? '<rect x="0" y="0" width="640" height="640" fill="#0e0e10"/>' : ''}
${skull}
<path id="nome" d="${word}" fill="url(#ouro)"/>
<path id="subtitulo" d="${sub}" fill="url(#ouro)"/>
</svg>`;
fs.writeFileSync(out + '/skull-logo.svg', svg(false));
fs.writeFileSync(out + '/skull-logo-fundo.svg', svg(true));
