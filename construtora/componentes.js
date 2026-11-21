// componentes.js: comportamento da biblioteca de componentes (skill site-nova-era). Sem dependências.
// Importar DEPOIS do motion.js (usa html.motion e as classes is-in que ele aplica).

const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- 1. Botão 3D: <a class="btn3d" href="...">Texto</a> vira cubo de 2 faces ---------- */
document.querySelectorAll('.btn3d').forEach((b) => {
  if (b.querySelector('.btn3d__f')) return;
  const html = b.innerHTML;
  b.setAttribute('aria-label', b.textContent.trim().replace(/\s+/g, ' '));
  b.innerHTML = `<span class="btn3d__f" aria-hidden="true">${html}</span><span class="btn3d__t" aria-hidden="true">${html}</span>`;
});

/* ---------- 2. Elementos vivos só quando visíveis (ambiente, efeitos de fundo) ---------- */
const vivo = new IntersectionObserver((es) => es.forEach((e) => e.target.classList.toggle('is-vivo', e.isIntersecting && !reduz)), { rootMargin: '100px' });
document.querySelectorAll('.fx, .amb-brise').forEach((el) => vivo.observe(el));
document.addEventListener('visibilitychange', () => document.body.classList.toggle('pausado', document.hidden));
document.querySelectorAll('.fx-barras').forEach((f) => f.querySelectorAll('i').forEach((i, n) => i.style.setProperty('--i', n)));

/* ---------- 3. Componentes que revelam ao entrar (número gigante, antes/depois, gráfico, wordmark, prova) ---------- */
const sel = '.num-g, .ad, .grafico, .wm, .prova';
const io = new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -12% 0px' });
document.querySelectorAll(sel).forEach((el) => {
  const r = el.getBoundingClientRect();
  if (r.top < innerHeight && r.bottom > 0) el.classList.add('is-in'); else io.observe(el);
});

/* ---------- 4. Gráfico de barras interativo ----------
   <figure class="grafico" data-grafico='{"titulo":"...","rotulos":["A","B"],"series":[{"nome":"Previsto","cor":"#7a6f62","valores":[2,3]},
   {"nome":"Realizado","cor":"var(--accent)","valores":[2,2.5]}],"unidade":" meses","max":4,"nota":"..."}'></figure>
   Acessível: cada grupo é um botão com rótulo completo; tabela escondida para leitor de tela; legenda liga/desliga séries. */
function montarGrafico(fig) {
  let d; try { d = JSON.parse(fig.dataset.grafico); } catch { return; }
  const max = d.max || Math.max(...d.series.flatMap((s) => s.valores)) * 1.1;
  const fmt = (v) => v.toLocaleString('pt-BR', { maximumFractionDigits: 1 }) + (d.unidade || '');
  const n = d.rotulos.length;
  fig.style.setProperty('--n', n);
  const leg = d.series.map((s, k) => `<li><button type="button" aria-pressed="true" data-serie="${k}" style="--cor:${s.cor}"><i></i>${s.nome}</button></li>`).join('');
  const grupos = d.rotulos.map((r, g) => {
    const barras = d.series.map((s, k) => `<span class="grafico__barra" data-serie="${k}" style="--v:${(s.valores[g] / max).toFixed(4)};--cor:${s.cor};--g:${g}"></span>`).join('');
    const dica = d.series.map((s) => `${s.nome}: <strong>${fmt(s.valores[g])}</strong>`).join('<br>');
    const rot = `${r}: ` + d.series.map((s) => `${s.nome} ${fmt(s.valores[g])}`).join(', ');
    return `<button type="button" class="grafico__grupo" aria-label="${rot}">${barras}<span class="grafico__dica" aria-hidden="true"><b>${r}</b>${dica}</span></button>`;
  }).join('');
  const tabela = `<table class="sr"><caption>${d.titulo || ''}</caption><tr><th>Etapa</th>${d.series.map((s) => `<th>${s.nome}</th>`).join('')}</tr>` +
    d.rotulos.map((r, g) => `<tr><th>${r}</th>${d.series.map((s) => `<td>${fmt(s.valores[g])}</td>`).join('')}</tr>`).join('') + '</table>';
  fig.innerHTML = `${d.titulo ? `<figcaption>${d.titulo}</figcaption>` : ''}<ul class="grafico__leg">${leg}</ul>
    <div class="grafico__area" aria-hidden="false">${grupos}</div><div class="grafico__eixo" aria-hidden="true">${d.rotulos.map((r) => `<span>${r}</span>`).join('')}</div>
    ${d.nota ? `<p class="grafico__nota">${d.nota}</p>` : ''}${tabela}`;
  fig.querySelectorAll('.grafico__leg button').forEach((b) => b.addEventListener('click', () => {
    const on = b.getAttribute('aria-pressed') !== 'true';
    b.setAttribute('aria-pressed', String(on));
    fig.querySelectorAll(`.grafico__barra[data-serie="${b.dataset.serie}"]`).forEach((x) => (x.hidden = !on));
  }));
  // toque: alterna a dica do grupo tocado
  fig.querySelectorAll('.grafico__grupo').forEach((g) => g.addEventListener('click', () => {
    fig.querySelectorAll('.grafico__grupo.is-ativo').forEach((x) => x !== g && x.classList.remove('is-ativo'));
    g.classList.toggle('is-ativo');
  }));
}
document.querySelectorAll('.grafico[data-grafico]').forEach(montarGrafico);

/* ---------- 5. Odômetro sincronizado com a seção fixada (motion.js escreve data-current no [data-pin]) ---------- */
document.querySelectorAll('[data-pin]').forEach((pin) => {
  const rolo = pin.querySelector('.odo__rolo');
  const icones = pin.querySelectorAll('[data-etapa-icone]');
  if (!rolo && !icones.length) return;
  const aplica = () => {
    const i = Number(pin.dataset.current || 0);
    if (rolo) rolo.style.setProperty('--idx', i);
    icones.forEach((ic, k) => ic.classList.toggle('is-ativo', k === i));
  };
  new MutationObserver(aplica).observe(pin, { attributes: true, attributeFilter: ['data-current'] });
  aplica();
});

/* ---------- 6. Formulário curto → mensagem pronta no WhatsApp (sem backend) ----------
   <form class="form-wa" data-wa="5511999999999" data-msg="Olá! Quero o estudo solar. Momento: {momento}. Local: {local}. Lote: {lote}.">  */
document.querySelectorAll('form.form-wa').forEach((f) => {
  f.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!f.reportValidity()) return;
    const dados = Object.fromEntries(new FormData(f).entries());
    const msg = (f.dataset.msg || '').replace(/\{(\w+)\}/g, (_, k) => (dados[k] || '').toString().trim() || 'a definir');
    const a = document.createElement('a');
    a.href = `https://wa.me/${f.dataset.wa}?text=${encodeURIComponent(msg)}`;
    a.target = '_blank'; a.rel = 'noopener';
    document.body.append(a); a.click(); a.remove();
    const nota = f.querySelector('.form-wa__nota');
    if (nota) nota.textContent = 'Abrimos o WhatsApp com a sua mensagem pronta. Se não abriu, chame no número abaixo.';
    document.dispatchEvent(new CustomEvent('whatsapp_open', { detail: { origem: 'form' } }));
  });
});

/* ---------- 7. Smooth scroll leve (se Lenis estiver na página e sem reduced motion) ---------- */
if (window.Lenis && !reduz && !window.__lenis) {
  const lenis = new window.Lenis({ lerp: 0.11, smoothWheel: true, anchors: true });
  const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
  requestAnimationFrame(raf);
  window.__lenis = lenis;
}
