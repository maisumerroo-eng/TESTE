// motion.js: comportamentos da skill site-nova-era. Sem dependências.
// Uso: <script type="module" src="main.js"></script> com `import './motion.js'` ou copiar direto.
// Módulos independentes: cada um só roda se achar seus elementos.

const root = document.documentElement;
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
const motionOn = !reduce.matches;
if (motionOn) root.classList.add('motion');

/* ---------- words: quebra títulos em palavras mascaradas ---------- */
function splitWords(el) {
  if (el.dataset.split) return;
  el.dataset.split = '1';
  const text = el.textContent.replace(/\s+/g, ' ').trim();
  el.setAttribute('aria-label', text);
  let n = 0;
  const walk = (node) => {
    [...node.childNodes].forEach((child) => {
      if (child.nodeType === 3) {
        const frag = document.createDocumentFragment();
        let texto = child.textContent;
        // pontuação logo depois de um trecho marcado (<em>, <strong>) gruda na palavra anterior, senão quebra sozinha na linha de baixo
        const pont = texto.match(/^[.,;:!?)»”]+/);
        if (pont && el.querySelectorAll('.rv-wi').length) {
          const ult = [...el.querySelectorAll('.rv-wi')].pop();
          ult.textContent += pont[0];
          texto = texto.slice(pont[0].length);
        }
        texto.split(/(\s+)/).forEach((part) => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.append(' '); return; }
          const w = document.createElement('span');
          w.className = 'rv-w'; w.setAttribute('aria-hidden', 'true');
          const wi = document.createElement('span');
          wi.className = 'rv-wi'; wi.style.setProperty('--wi', n++); wi.textContent = part;
          w.append(wi); frag.append(w);
        });
        child.replaceWith(frag);
      } else if (child.nodeType === 1) walk(child);
    });
  };
  walk(el);
}

/* ---------- contador ---------- */
function runCount(el) {
  if (el.dataset.counted) return;
  el.dataset.counted = '1';
  const to = parseFloat(el.dataset.count);
  const dec = (el.dataset.count.split('.')[1] || '').length;
  const pre = el.dataset.countPrefix || '';
  const suf = el.dataset.countSuffix || '';
  const fmt = (v) => pre + v.toLocaleString('pt-BR', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suf;
  if (!motionOn) { el.textContent = fmt(to); return; }
  const dur = parseFloat(el.dataset.countDuration || 1600);
  const t0 = performance.now() + parseFloat(el.dataset.countDelay || 0);
  const tick = (t) => {
    const p = Math.min(1, Math.max(0, (t - t0) / dur));
    el.textContent = fmt(to * (1 - Math.pow(1 - p, 3)));
    if (p < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

/* ---------- reveal ---------- */
function initReveal() {
  document.querySelectorAll('[data-reveal-group]').forEach((g) => {
    if (g.dataset.stagger) g.style.setProperty('--stagger', g.dataset.stagger + 'ms');
    g.querySelectorAll(':scope [data-reveal]').forEach((el, i) => el.style.setProperty('--i', i));
  });
  document.querySelectorAll('[data-reveal]').forEach((el) => {
    if (el.dataset.delay) el.style.setProperty('--delay', el.dataset.delay + 'ms');
    if (el.dataset.reveal === 'words') splitWords(el);
  });
  const targets = document.querySelectorAll('[data-reveal], [data-count]');
  if (!motionOn || !('IntersectionObserver' in window)) {
    targets.forEach((el) => { el.classList.add('is-in'); if (el.dataset.count) runCount(el); });
    return;
  }
  const TRANSICAO = ['rise', 'fade', 'wipe', 'blur', 'develop', 'flip', 'track'];
  // aposenta a regra de reveal quando a entrada termina (transições próprias do elemento voltam a valer)
  const aposentar = (el) => {
    if (!TRANSICAO.includes(el.dataset.reveal)) return;
    let feito = false;
    const fim = () => { if (feito) return; feito = true; el.dataset.revealed = el.dataset.reveal; el.removeAttribute('data-reveal'); };
    el.addEventListener('transitionend', (ev) => { if (ev.target === el) fim(); });
    const cs = getComputedStyle(el);
    const ms = (v) => Math.max(...v.split(',').map((x) => parseFloat(x) * (x.includes('ms') ? 1 : 1000)));
    setTimeout(fim, ms(cs.transitionDuration) + ms(cs.transitionDelay) + 150);   // garantia se transitionend não vier
  };
  const revelar = (el) => { el.classList.add('is-in'); if (el.dataset.count) runCount(el); if (el.dataset.reveal) aposentar(el); };
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      revelar(e.target);
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -15% 0px' });
  // o que já está visível ao carregar revela na hora (senão itens perto do rodapé da 1ª dobra ficam escondidos)
  targets.forEach((el) => {
    const r = el.getBoundingClientRect();
    if (r.top < innerHeight && r.bottom > 0) revelar(el);
    else io.observe(el);
  });
}

/* ---------- header esperto ---------- */
function initHeader() {
  const header = document.querySelector('.site-header');
  if (!header) return;
  const hero = document.querySelector('[data-hero]') || document.querySelector('.hero');
  let lastY = scrollY, ticking = false;
  const update = () => {
    const y = scrollY;
    const limit = hero ? hero.offsetHeight - header.offsetHeight : 80;
    header.classList.toggle('is-scrolled', y > limit);
    const menuOpen = root.classList.contains('menu-open');
    header.classList.toggle('is-hidden', !menuOpen && y > lastY && y > 200);
    lastY = y; ticking = false;
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  update();
}

/* ---------- marquee arrastável com inércia ---------- */
function initMarquee(box) {
  const track = box.firstElementChild;
  if (!track) return;
  const clone = track.cloneNode(true);
  clone.setAttribute('aria-hidden', 'true');
  clone.inert = true;
  clone.querySelectorAll('[data-reveal]').forEach((n) => { n.removeAttribute('data-reveal'); });
  box.append(clone);
  box.tabIndex = 0;
  box.setAttribute('aria-roledescription', 'carrossel');

  const speed = parseFloat(box.dataset.marquee || 30); // px por segundo
  let x = 0, vel = 0, raf = 0, last = 0, visible = false, hover = false, drag = null;
  let largura = track.offsetWidth;   // em cache: ler offsetWidth a cada quadro força layout da página inteira
  new ResizeObserver(() => (largura = track.offsetWidth)).observe(track);
  const width = () => largura;
  const loop = (t) => {
    const dt = Math.min(0.05, (t - last) / 1000); last = t;
    if (!drag) {
      vel *= Math.pow(0.04, dt);                 // inércia que decai
      x += vel * dt + ((hover || reduce.matches) ? 0 : speed * dt);
    }
    const w = width();
    x = ((x % w) + w) % w;
    box.scrollLeft = x;
    raf = requestAnimationFrame(loop);
  };
  const sync = () => {
    const run = visible && !document.hidden;
    if (run && !raf) { last = performance.now(); x = box.scrollLeft; raf = requestAnimationFrame(loop); }
    if (!run && raf) { cancelAnimationFrame(raf); raf = 0; }
  };
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; sync(); }).observe(box);
  document.addEventListener('visibilitychange', sync);
  if (finePointer.matches) {
    box.addEventListener('pointerenter', () => (hover = true));
    box.addEventListener('pointerleave', () => (hover = false));
  }
  box.addEventListener('focusin', () => (hover = true));
  box.addEventListener('focusout', () => (hover = false));
  box.addEventListener('pointerdown', (e) => {
    if (e.button !== 0) return;
    drag = { x: e.clientX, start: x, lastX: e.clientX, lastT: e.timeStamp, v: 0, moved: false };
    // sem setPointerCapture aqui: capturar no pointerdown manda o clique para a caixa e os links de dentro param de abrir
  });
  box.addEventListener('pointermove', (e) => {
    if (!drag) return;
    const dx = e.clientX - drag.x;
    if (Math.abs(dx) > 4 && !drag.moved) { drag.moved = true; box.classList.add('is-dragging'); try { box.setPointerCapture(e.pointerId); } catch { /* ponteiro já solto */ } }
    x = drag.start - dx;
    const dt = Math.max(1, e.timeStamp - drag.lastT);
    drag.v = -(e.clientX - drag.lastX) / dt * 1000;
    drag.lastX = e.clientX; drag.lastT = e.timeStamp;
  });
  const end = () => {
    if (!drag) return;
    vel = drag.v; box.classList.remove('is-dragging');
    if (drag.moved) box.addEventListener('click', (ev) => ev.preventDefault(), { capture: true, once: true });
    drag = null;
  };
  box.addEventListener('pointerup', end);
  box.addEventListener('pointercancel', end);
  box.addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    e.preventDefault();
    const step = (track.firstElementChild?.offsetWidth || 200) * (e.key === 'ArrowLeft' ? -1 : 1);
    x += step;
  });
}

/* ---------- seção fixada com progresso (momento-assinatura) ----------
   <section data-pin style="--pin-h: 500svh">
     <div data-pin-stage>
       <svg><path data-pin-path d="..."/><circle data-pin-marker r="6"/></svg>
       <article data-step>...</article> x N
     </div>
   </section>
   Expõe --p (0..1) e data-current no [data-pin]; classes is-current / is-past nos passos. */
function initPin(sec) {
  const steps = [...sec.querySelectorAll('[data-step]')];
  const path = sec.querySelector('[data-pin-path]');
  const marker = sec.querySelector('[data-pin-marker]');
  const len = path ? path.getTotalLength() : 0;
  if (path) { path.style.strokeDasharray = `${len} ${len}`; }
  let current = -1, ticking = false;
  const update = () => {
    ticking = false;
    const r = sec.getBoundingClientRect();
    const total = sec.offsetHeight - innerHeight;
    const p = motionOn ? Math.min(1, Math.max(0, -r.top / (total || 1))) : 1;
    sec.style.setProperty('--p', p.toFixed(4));
    if (path) path.style.strokeDashoffset = String(len * (1 - p));
    if (marker && path) {
      const pt = path.getPointAtLength(len * p);
      marker.setAttribute('transform', `translate(${pt.x} ${pt.y})`);
    }
    const idx = Math.min(steps.length - 1, Math.floor(p * steps.length * 0.9999));
    if (idx !== current) {
      current = idx;
      sec.dataset.current = String(idx);
      steps.forEach((s, i) => {
        s.classList.toggle('is-current', i === idx);
        s.classList.toggle('is-past', i < idx);
        s.setAttribute('aria-hidden', motionOn && i !== idx ? 'true' : 'false');
      });
    }
  };
  if (!motionOn) { steps.forEach((s) => s.classList.add('is-current')); update(); return; }
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
  addEventListener('resize', update);
  update();
}

/* ---------- elemento que aparece depois da hero (ex.: WhatsApp flutuante) ---------- */
function initAfterHero() {
  const hero = document.querySelector('[data-hero]') || document.querySelector('.hero');
  const els = document.querySelectorAll('[data-after-hero]');
  if (!hero || !els.length) { els.forEach((e) => e.classList.add('is-visible')); return; }
  new IntersectionObserver(([e]) => els.forEach((el) => el.classList.toggle('is-visible', !e.isIntersecting)))
    .observe(hero);
}

/* ---------- smooth scroll opcional (se Lenis estiver carregado) ---------- */
function initLenis() {
  if (!motionOn || !window.Lenis) return;
  const lenis = new window.Lenis({ lerp: 0.1, smoothWheel: true });
  const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
  requestAnimationFrame(raf);
  window.__lenis = lenis;
}

initReveal();
initHeader();
document.querySelectorAll('[data-marquee]').forEach(initMarquee);
document.querySelectorAll('[data-pin]').forEach(initPin);
initAfterHero();
initLenis();
