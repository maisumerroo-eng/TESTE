// scrub.js: hero de vídeo controlado pelo scroll (skill site-nova-era, references/video-scrub.md).
// Padrão: vídeo baixado como Blob (funciona sem HTTP Range), transmitido atrás de um anel com watchdog,
// tempo interpolado num loop rAF que descansa (normalizado por dt), seeks travados à prova de deadlock,
// escritas no DOM só quando mudam, faixas de legenda ritmadas em distância de scroll, 5 portões do hero
// estático decididos AO VIVO (iguais ao CSS) e página completa mesmo se o vídeo nunca chegar.
//
// <section class="scrub" data-scrub data-src="assets/hero-scrub.mp4" data-poster="assets/hero-poster.jpg"
//          data-bytes="6000000" style="--scrub-h: 400vh; --scrub-static: url(assets/hero-final.jpg)">
//   <div class="scrub__stage">
//     <div class="scrub__static" aria-hidden="true"></div><div class="scrub__poster" aria-hidden="true"></div>
//     <video class="scrub__video" muted playsinline preload="none" aria-hidden="true" tabindex="-1"></video>
//     <div class="scrub__scrim" aria-hidden="true"></div>
//     <div class="scrub__band" data-band="0,0.32" data-static><h1 data-split>...</h1>...</div>
//     <div class="scrub__band" data-band="0.36,0.66">...</div>
//     <svg class="scrub__ring" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="20" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="126"/></svg>
//   </div>
// </section>

const GATES = [
  '(max-width: 720px)',
  '(orientation: portrait) and (max-width: 1024px)',
  '(orientation: portrait) and (pointer: coarse)',
  '(orientation: landscape) and (pointer: coarse) and (max-height: 560px)',
  '(prefers-reduced-motion: reduce)',
];

const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
const smooth = (p, e0, e1) => { const t = clamp((p - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t); };
function rng(seed) { let s = seed >>> 0; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }

function splitWords(el, seed) {
  if (el.dataset.splitDone) return;
  el.dataset.splitDone = '1';
  const text = el.textContent.replace(/\s+/g, ' ').trim();
  el.setAttribute('aria-label', text);
  const r = rng(seed);
  const words = text.split(' ');
  el.textContent = '';
  words.forEach((w, i) => {
    const s = document.createElement('span');
    s.className = 'rv-wi'; s.setAttribute('aria-hidden', 'true');
    s.style.setProperty('--th', (i / words.length * 0.45 + r() * 0.05).toFixed(3)); // ordem de leitura + leve variação com semente
    s.textContent = w;
    el.append(s, ' ');
  });
}

function montar(sec) {
  const video = sec.querySelector('.scrub__video');
  const poster = sec.querySelector('.scrub__poster');
  const ring = sec.querySelector('.scrub__ring');
  const bands = [...sec.querySelectorAll('[data-band]')].map((el, i, all) => {
    const [a, b] = el.dataset.band.split(',').map(Number);
    el.querySelectorAll('[data-split]').forEach((t, j) => splitWords(t, 7 + i * 31 + j));
    return { el, a, b, first: i === 0, last: i === all.length - 1, ramp: el.dataset.ramp ? +el.dataset.ramp : null, op: -1, k: -1 };
  });

  let ligado = false, iniciado = false, naTela = false, rafId = null, lastTick = 0;
  let target = 0, shown = 0, seekBusy = false, pending = null, loadK = 0, loadT0 = 0;

  const progresso = () => {
    const r = sec.getBoundingClientRect();
    return clamp(-r.top / Math.max(1, sec.offsetHeight - innerHeight), 0, 1);
  };

  // ---------- seeks travados ----------
  function requestSeek(t) {
    if (!video.duration || sec.classList.contains('is-failed')) return;
    if (seekBusy) { pending = t; return; }
    seekBusy = true;
    video.currentTime = t;
  }
  video.addEventListener('seeked', () => {
    seekBusy = false;
    if (pending !== null) { const t = pending; pending = null; requestSeek(t); }
  });
  video.addEventListener('error', () => { seekBusy = false; pending = null; falhar(); });

  // ---------- faixas: opacidade com platô e --k, escritas só na mudança ----------
  function legendas(p, now) {
    if (!loadT0) loadT0 = now || performance.now();
    loadK = clamp(((now || performance.now()) - loadT0) / 900, 0, 1); // faixa 1 abre montada no carregamento
    for (const bd of bands) {
      const f = Math.min(0.02, (bd.b - bd.a) / 3);
      const entra = bd.first ? (p <= bd.b ? 1 : 0) : smooth(p, bd.a, bd.a + f);
      const sai = bd.last ? 1 : 1 - smooth(p, bd.b - f, bd.b);
      const op = +(entra * sai).toFixed(3);
      let k = clamp((p - bd.a) / (bd.ramp || Math.min(0.025, (bd.b - bd.a) * 0.35)), 0, 1);
      if (bd.first) k = Math.max(k, loadK);
      if (Math.abs(op - bd.op) > 0.004) { bd.op = op; bd.el.style.opacity = op; bd.el.style.visibility = op > 0 ? 'visible' : 'hidden'; }
      if (Math.abs(k - bd.k) > 0.008 || (k === 1 && bd.k !== 1)) { bd.k = k; bd.el.style.setProperty('--k', k.toFixed(3)); }
    }
  }

  // ---------- loop que descansa, normalizado por dt ----------
  function tick(now) {
    const dt = Math.min(100, now - (lastTick || now));
    lastTick = now;
    shown += (target - shown) * (1 - Math.pow(1 - 0.16, dt / 16.667));
    const parado = Math.abs(target - shown) < 0.0005 && loadK >= 1;
    if (parado) { shown = target; rafId = null; lastTick = 0; } else rafId = requestAnimationFrame(tick);
    requestSeek(shown * video.duration);
    legendas(shown, now);
  }
  function onScroll() {
    target = progresso();
    if (rafId === null && naTela && ligado) rafId = requestAnimationFrame(tick);
  }

  // ---------- carregamento: pôster primeiro, depois Blob transmitido com watchdog ----------
  function falhar() {
    if (sec.classList.contains('is-failed')) return;
    sec.classList.add('is-failed');   // pôster fica; as faixas continuam no scroll
  }
  async function baixar() {
    const ctrl = new AbortController();
    let wd = setTimeout(() => ctrl.abort(), 20000);
    const res = await fetch(sec.dataset.src, { priority: 'low', signal: ctrl.signal });
    if (!res.ok || !res.body) throw new Error('vídeo ' + res.status);
    const total = Number(res.headers.get('Content-Length')) || Number(sec.dataset.bytes) || 6e6;
    const reader = res.body.getReader();
    const partes = []; let got = 0, lastRing = 0;
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      clearTimeout(wd); wd = setTimeout(() => ctrl.abort(), 20000);   // 20 s sem progresso: aborta
      partes.push(value); got += value.length;
      const now = performance.now();
      if (ring && (now - lastRing > 100)) { lastRing = now; ring.style.setProperty('--ld', Math.round(126 * (1 - Math.min(1, got / total)))); }
    }
    clearTimeout(wd);
    if (ring) ring.style.setProperty('--ld', 0);
    video.src = URL.createObjectURL(new Blob(partes, { type: 'video/mp4' }));
    video.load();
    video.addEventListener('canplay', () => { requestSeek(progresso() * video.duration); sec.classList.add('is-ready'); }, { once: true });
  }
  function iniciarUmaVez() {
    if (iniciado) return;
    iniciado = true;
    poster.style.backgroundImage = `url("${sec.dataset.poster}")`;
    let foi = false;
    const vai = () => { if (foi) return; foi = true; baixar().catch(falhar); };
    const img = new Image(); img.onload = vai; img.onerror = vai; img.src = sec.dataset.poster;
    setTimeout(vai, 4000);   // pôster travado nunca segura o vídeo
  }

  // ---------- portões vivos ----------
  function ligar() {
    if (ligado) return; ligado = true;
    iniciarUmaVez();
    addEventListener('scroll', onScroll, { passive: true });
    bands.forEach((b) => { b.op = -1; b.k = -1; b.el.style.removeProperty('visibility'); });
    target = shown = progresso();
    legendas(shown);
    if (naTela) rafId = requestAnimationFrame(tick);
  }
  function desligar() {
    if (!ligado) return; ligado = false;
    removeEventListener('scroll', onScroll);
    if (rafId !== null) { cancelAnimationFrame(rafId); rafId = null; }
    bands.forEach((b) => { b.el.style.removeProperty('opacity'); b.el.style.removeProperty('visibility'); b.el.style.setProperty('--k', '1'); });
  }
  const mqls = GATES.map((q) => matchMedia(q));   // manter referência
  const aplicar = () => (mqls.some((m) => m.matches) ? desligar() : ligar());
  mqls.forEach((m) => m.addEventListener('change', aplicar));
  new IntersectionObserver(([e]) => { naTela = e.isIntersecting; if (naTela) onScroll(); }).observe(sec);
  aplicar();
  return { ligar, desligar, progresso };
}

document.querySelectorAll('[data-scrub]').forEach(montar);
