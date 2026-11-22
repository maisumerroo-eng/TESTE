// interacoes-canal.js: implementação de referência (site KAGERIMA, 22/11/2026). Copiar o bloco que precisar.
// Cada bloco numerado é independente e tem o contrato HTML no comentário/seletores: tema por interesse (?anime=),
// filtro, player facade, decrypt, glitch, abas acessíveis, monte seu pedido → WhatsApp, votação local, spoiler,
// progresso, menu gaveta, busca, janela de conteúdo com anterior/próxima, mini player, aviso (toast), header auto-hide,
// modo leve, destaque, compartilhar, privacidade (apagar preferências), pontos do pin, ordenar, scroll-spy, pausa fora da tela.
// Trocar ANIMES/textos pelo interesse do novo nicho (ex.: ?bairro=, ?servico=). Importar depois do personaliza.js e antes do motion.js.
const raiz = document.documentElement;
const reduz = matchMedia('(prefers-reduced-motion: reduce)').matches;
const guarda = { get: (k) => { try { return localStorage.getItem(k); } catch { return null; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch { /* privado */ } } };
const ANIMES = {
  'naruto': { nome: 'Naruto', kanji: '写', titulo: 'Rap de Naruto com <em>a sombra</em> de quem carrega o Sharingan.' },
  'jujutsu-kaisen': { nome: 'Jujutsu Kaisen', kanji: '無', titulo: 'Rap de Jujutsu Kaisen com <em>a sombra</em> do mais forte.' },
  'one-piece': { nome: 'One Piece', kanji: '海', titulo: 'Rap de One Piece com <em>a sombra</em> de quem quer ser o Rei dos Piratas.' },
  'bleach': { nome: 'Bleach', kanji: '卍', titulo: 'Rap de Bleach com <em>a sombra</em> de cada Bankai.' },
  'dragon-ball': { nome: 'Dragon Ball', kanji: '超', titulo: 'Rap de Dragon Ball com <em>a sombra</em> de quem passa do limite.' },
};
const PADRAO = document.querySelector('h1')?.innerHTML;

/* ---------- 1. anime favorito ---------- */
function aplicaAnime(a, origem) {
  const d = ANIMES[a];
  const h1 = document.querySelector('h1');
  document.querySelectorAll('[data-anime-choose]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.animeChoose === a)));
  if (!d) { delete raiz.dataset.anime; if (h1 && PADRAO) h1.innerHTML = PADRAO; const k0 = document.querySelector('.hero__kanji'); if (k0) { k0.textContent = '影'; k0.dataset.k = '影'; } return; }
  raiz.dataset.anime = a;
  if (h1) { h1.innerHTML = d.titulo; delete h1.dataset.split; }
  const k = document.querySelector('.hero__kanji'); if (k) { k.textContent = d.kanji; k.dataset.k = d.kanji; }
  if (origem === 'escolha' && !reduz) { raiz.classList.remove('is-trocando'); void raiz.offsetWidth; raiz.classList.add('is-trocando'); setTimeout(() => raiz.classList.remove('is-trocando'), 800); }
  const lista = document.querySelector('.faixas');   // faixas do anime sobem para o topo
  if (lista) [...lista.children].sort((x, y) => (y.dataset.anime === a) - (x.dataset.anime === a)).forEach((li) => lista.append(li));
  document.dispatchEvent(new CustomEvent('anime_escolhido', { detail: { anime: a, origem } }));
  if (Array.isArray(window.dataLayer)) window.dataLayer.push({ event: 'anime_escolhido', anime: a, origem });
}
const q = new URLSearchParams(location.search);
const pedido = (q.get('anime') || '').toLowerCase();
const inicial = ANIMES[pedido] ? pedido : guarda.get('kg_anime');
if (ANIMES[pedido]) guarda.set('kg_anime', pedido);
if (inicial && ANIMES[inicial]) aplicaAnime(inicial, ANIMES[pedido] ? 'url' : 'lembrado');
document.addEventListener('click', (e) => {
  const b = e.target.closest('[data-anime-choose]');
  if (!b) return;
  const a = b.dataset.animeChoose;
  const mesmo = raiz.dataset.anime === a;
  guarda.set('kg_anime', mesmo ? '' : a);
  aplicaAnime(mesmo ? '' : a, 'escolha');
});

/* ---------- 2. filtro de faixas ---------- */
document.querySelectorAll('.filtros').forEach((grupo) => grupo.addEventListener('click', (e) => {
  const b = e.target.closest('[data-filtro]'); if (!b) return;
  grupo.querySelectorAll('[data-filtro]').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
  const f = b.dataset.filtro;
  document.querySelectorAll('.faixas > .faixa').forEach((li) => { const ok = f === 'todos' || li.dataset.anime === f; li.classList.toggle('is-fora', !ok); li.toggleAttribute('inert', !ok); });
}));

/* ---------- 3. player facade: só carrega o YouTube no clique ---------- */
document.addEventListener('click', (e) => {
  const b = e.target.closest('.faixa__play'); if (!b) return;
  const id = b.dataset.player;
  const card = b.closest('.faixa');
  document.querySelectorAll('.faixa.is-tocando').forEach((c) => c !== card && c.classList.remove('is-tocando'));
  card.classList.add('is-tocando');
  if (!id) { window.open(document.querySelector('.btn-ouvir')?.href || 'https://www.youtube.com', '_blank', 'noopener'); return; }   // sem ID oficial ainda: abre o canal
  const f = document.createElement('iframe');
  f.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(id)}?autoplay=1`;
  f.title = b.getAttribute('aria-label'); f.allow = 'autoplay; encrypted-media; picture-in-picture'; f.allowFullscreen = true; f.className = 'faixa__iframe';
  b.replaceWith(f);
});

/* ---------- 4. texto decrypt (letras embaralham até formar o texto) ---------- */
const SIMB = '影無超卍海写伏処解王眼子#%&$@!?<>/\\█▓▒░';
function decrypt(el, dur = 900) {
  if (reduz || el.dataset.decrypting) return;
  const final = el.dataset.final || el.textContent; el.dataset.final = final; el.dataset.decrypting = '1';
  if (!el.getAttribute('aria-label') && final.length > 2) el.setAttribute('aria-label', final);
  const t0 = performance.now();
  const passo = (t) => {
    const p = Math.min(1, (t - t0) / dur); const fixos = Math.floor(p * final.length);
    el.textContent = final.split('').map((c, i) => (i < fixos || c === ' ' ? c : SIMB[(Math.random() * SIMB.length) | 0])).join('');
    if (p < 1) requestAnimationFrame(passo); else { el.textContent = final; delete el.dataset.decrypting; }
  };
  requestAnimationFrame(passo);
}
const ioD = new IntersectionObserver((es) => es.forEach((x) => { if (x.isIntersecting) { decrypt(x.target); ioD.unobserve(x.target); } }), { rootMargin: '0px 0px -10% 0px' });
document.querySelectorAll('[data-reveal="decrypt"]').forEach((el) => ioD.observe(el));
// no seletor por scroll: decrypt dos kanjis da etapa que ficou ativa
document.querySelectorAll('[data-pin]').forEach((pin) => {
  const capas = pin.querySelectorAll('[data-sel-capa]');
  new MutationObserver(() => {
    const i = Number(pin.dataset.current || 0);
    pin.querySelectorAll('[data-step]')[i]?.querySelectorAll('[data-decrypt]').forEach((k) => decrypt(k, 500));
    capas.forEach((c, n) => c.classList.toggle('is-ativa', n === i));
    pin.style.setProperty('--cor-ativa', pin.querySelectorAll('[data-step]')[i]?.style.getPropertyValue('--cor') || '');   // do style inline: getComputedStyle forçaria recálculo
  }).observe(pin, { attributes: true, attributeFilter: ['data-current'] });
});

/* ---------- 5. glitch do kanji (rajadas curtas, só visível e sem reduced motion) ---------- */
const g = document.querySelector('[data-glitch]');
if (g && !reduz) {
  const leveOn = () => raiz.classList.contains('modo-leve');
  let vis = true; new IntersectionObserver(([x]) => (vis = x.isIntersecting)).observe(g);
  setInterval(() => { if (!vis || document.hidden || leveOn()) return; g.classList.add('is-glitch'); setTimeout(() => g.classList.remove('is-glitch'), 420); }, 3600);
}

/* ---------- 6. estúdio: abas acessíveis (setas, Home/End) ---------- */
document.querySelectorAll('.estudio__tabs').forEach((lista) => {
  const tabs = [...lista.querySelectorAll('[role="tab"]')];
  const mesa = lista.closest('.estudio__mesa');
  const ativa = (t) => {
    tabs.forEach((x) => { const on = x === t; x.setAttribute('aria-selected', String(on)); x.tabIndex = on ? 0 : -1; document.getElementById(x.getAttribute('aria-controls')).hidden = !on; });
    mesa.dataset.camada = t.dataset.camada;
  };
  lista.addEventListener('click', (e) => { const t = e.target.closest('[role="tab"]'); if (t) ativa(t); });
  lista.addEventListener('keydown', (e) => {
    const i = tabs.indexOf(document.activeElement); if (i < 0) return;
    const n = { ArrowRight: i + 1, ArrowDown: i + 1, ArrowLeft: i - 1, ArrowUp: i - 1, Home: 0, End: tabs.length - 1 }[e.key];
    if (n === undefined) return; e.preventDefault();
    const t = tabs[(n + tabs.length) % tabs.length]; t.focus(); ativa(t);
  });
  mesa.dataset.camada = tabs[0].dataset.camada;
});

/* ---------- 7. monte sua encomenda: resumo vivo → mensagem do WhatsApp ---------- */
document.querySelectorAll('[data-monte]').forEach((f) => {
  const cta = f.querySelector('[data-monte-wa]');
  let pronto = false;
  const atualiza = () => {
    const fd = new FormData(f);
    const r = { formato: fd.get('m-formato'), clima: fd.get('m-clima'), extras: fd.getAll('m-extra').join(', ') || 'nenhum' };
    Object.entries(r).forEach(([k, v]) => { const el = f.querySelector(`[data-r="${k}"]`); if (el && el.textContent !== v) { el.textContent = v; if (pronto) { el.classList.remove('is-novo'); void el.offsetWidth; el.classList.add('is-novo'); } } });
    pronto = true;
    const msg = `Olá, KAGERIMA! Pedido: ${r.formato}, beat ${r.clima}. Extras: ${r.extras}.`;
    cta.href = `https://wa.me/${cta.dataset.monteWa}?text=${encodeURIComponent(msg)}`;
  };
  f.addEventListener('change', atualiza); f.addEventListener('submit', (e) => e.preventDefault()); atualiza();
});

/* ---------- 8. votação: prévia local (a oficial é na comunidade do YouTube) ---------- */
document.querySelectorAll('[data-voto]').forEach((lista) => {
  const msg = document.querySelector('[data-voto-msg]');
  const marca = (id, novo) => {
    lista.classList.add('is-votado');
    lista.querySelectorAll('.voto__btn').forEach((b) => {
      const on = b.dataset.votoId === id; b.setAttribute('aria-pressed', String(on)); b.closest('li').classList.toggle('is-meu', on);
      const pct = b.querySelector('.voto__pct'); const v = Number(pct.dataset.pct) + (on && novo ? 1 : 0); pct.textContent = `${v}%`;
    });
    if (msg) msg.textContent = 'Voto registrado neste aparelho. Toque em outro nome para mudar.';
  };
  const salvo = guarda.get('kg_voto'); if (salvo) marca(salvo, false);
  lista.addEventListener('click', (e) => { const b = e.target.closest('.voto__btn'); if (!b) return; guarda.set('kg_voto', b.dataset.votoId); marca(b.dataset.votoId, true); });
});

/* ---------- 9. estúdio só anima quando visível (economia de CPU) ---------- */
document.querySelectorAll('.estudio, .destaque').forEach((s) => new IntersectionObserver(([x]) => s.classList.toggle('is-visivel', x.isIntersecting), { threshold: .25 }).observe(s));

/* ---------- 10. spoiler: capa velada até o fã aceitar (por faixa ou todas) ---------- */
document.addEventListener('click', (e) => {
  const t = e.target.closest('[data-spoiler-toggle]');
  if (t) { const on = t.getAttribute('aria-pressed') !== 'true'; t.setAttribute('aria-pressed', String(on)); t.textContent = on ? 'Esconder spoilers' : 'Mostrar spoilers'; document.querySelectorAll('.faixa[data-spoiler]').forEach((c) => c.classList.toggle('is-revelada', on)); return; }
  const c = e.target.closest('.faixa[data-spoiler]:not(.is-revelada)');
  if (c && e.target.closest('.faixa__play')) { e.stopImmediatePropagation(); e.preventDefault(); c.classList.add('is-revelada'); }
}, true);

/* ---------- 11. barra de progresso de leitura ---------- */
const barra = document.querySelector('.progresso');
if (barra) { let pend = false; let alto = 1; new ResizeObserver(() => { alto = document.documentElement.scrollHeight - innerHeight; }).observe(document.body); /* altura em cache: ler scrollHeight a cada quadro força layout */ const atualiza = () => { pend = false; barra.style.setProperty('--progresso', alto > 0 ? Math.min(1, scrollY / alto).toFixed(4) : 0); }; addEventListener('scroll', () => { if (!pend) { pend = true; requestAnimationFrame(atualiza); } }, { passive: true }); atualiza(); }

/* ---------- 12. menu no celular (gaveta acessível: Esc fecha, foco volta ao botão) ---------- */
const menuBtn = document.querySelector('.menu-btn');
if (menuBtn) {
  const nav = document.getElementById(menuBtn.getAttribute('aria-controls'));
  const abre = (on) => { menuBtn.setAttribute('aria-expanded', String(on)); menuBtn.setAttribute('aria-label', on ? 'Fechar menu' : 'Abrir menu'); raiz.classList.toggle('menu-aberto', on); if (on) nav.querySelector('a')?.focus(); };
  menuBtn.addEventListener('click', () => abre(menuBtn.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', (e) => { if (e.target.closest('a')) abre(false); });
  addEventListener('keydown', (e) => { if (e.key === 'Escape' && raiz.classList.contains('menu-aberto')) { abre(false); menuBtn.focus(); } });
}

/* ---------- 13. busca de faixas (junta com o filtro por anime) ---------- */
const busca = document.querySelector('[data-busca]');
if (busca) {
  const n = document.querySelector('[data-busca-n]'); const vazio = document.querySelector('[data-vazio]');
  const norm = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  busca.addEventListener('input', () => {
    const t = norm(busca.value.trim()); let vis = 0;
    document.querySelectorAll('.faixas > .faixa').forEach((li) => { const ok = !t || norm(li.textContent).includes(t); li.classList.toggle('is-busca-fora', !ok); if (ok && !li.classList.contains('is-fora')) vis++; });
    if (n) n.textContent = t ? `${vis} ${vis === 1 ? 'faixa' : 'faixas'}` : '';
    if (vazio) vazio.hidden = vis > 0;
  });
}

/* ---------- 14. letra: janela com a estrutura e as referências ---------- */
const dlg = document.querySelector('.letra-dlg');
if (dlg) {
  document.addEventListener('click', (e) => {
    if (e.defaultPrevented) return;   // arrastou o carrossel: não abre
    const a = e.target.closest('[data-letra]'); if (!a) return;
    const tpl = document.getElementById(`tpl-letra-${a.dataset.letra}`); if (!tpl || !dlg.showModal) return;
    e.preventDefault();
    dlg.querySelector('[data-dlg-cat]').textContent = tpl.dataset.cat;
    dlg.querySelector('[data-dlg-k]').textContent = tpl.dataset.k;
    dlg.querySelector('[data-dlg-tit]').textContent = tpl.dataset.tit;
    dlg.querySelector('[data-dlg-corpo]').replaceChildren(tpl.content.cloneNode(true));
    dlg.showModal();
  });
  dlg.addEventListener('click', (e) => { if (e.target === dlg || e.target.closest('[data-dlg-fechar]')) dlg.close(); });
}

/* ---------- 15. mini player: segue a faixa tocando quando o card sai da tela ---------- */
const mini = document.querySelector('[data-mini]');
if (mini) {
  let card = null; let io = null;
  document.addEventListener('click', (e) => {
    const b = e.target.closest('.faixa__play'); if (!b) return;
    card = b.closest('.faixa'); if (card.matches('[data-spoiler]:not(.is-revelada)')) return;
    mini.querySelector('[data-mini-tit]').textContent = card.querySelector('h3')?.textContent || '';
    mini.querySelector('[data-mini-pers]').textContent = card.querySelector('.faixa__pers')?.textContent || '';
    mini.style.setProperty('--cor', card.style.getPropertyValue('--cor'));
    const img = card.querySelector('img'); mini.querySelector('[data-mini-capa]').style.backgroundImage = img ? `url("${img.currentSrc || img.src}")` : '';
    io?.disconnect(); io = new IntersectionObserver(([x]) => { mini.hidden = x.isIntersecting; }); io.observe(card);
  });
  mini.querySelector('[data-mini-fechar]').addEventListener('click', () => { io?.disconnect(); mini.hidden = true; card?.classList.remove('is-tocando'); });
  mini.querySelector('.mini__ir').addEventListener('click', (e) => { if (card) { e.preventDefault(); card.scrollIntoView({ behavior: reduz ? 'auto' : 'smooth', block: 'center' }); } });
}

/* ---------- 16. aviso curto quando o site troca de anime ---------- */
const toast = document.querySelector('[data-toast]');
document.addEventListener('anime_escolhido', (e) => {
  if (!toast || e.detail.origem !== 'escolha') return;
  toast.textContent = `Site no clima de ${ANIMES[e.detail.anime].nome}. Toque de novo no anime para voltar ao padrão.`;
  toast.classList.add('is-on'); clearTimeout(toast._t); toast._t = setTimeout(() => toast.classList.remove('is-on'), 3200);
});

/* ---------- 17. header some ao descer e volta ao subir (mais área de leitura no celular) ---------- */
{ let ultimo = scrollY, pend = false; const hdr = document.querySelector('.site-header');
  addEventListener('scroll', () => { if (pend) return; pend = true; requestAnimationFrame(() => { pend = false; const y = scrollY; const desce = y > ultimo + 6; const sobe = y < ultimo - 6;
    if (desce && y > innerHeight * .8) hdr?.classList.add('is-escondido'); else if (sobe || y < 80) hdr?.classList.remove('is-escondido'); ultimo = y; }); }, { passive: true });
  document.addEventListener('focusin', (e) => { if (e.target.closest('.site-header')) hdr?.classList.remove('is-escondido'); }); }

/* ---------- 18. modo leve: desliga glitch, piscadas e grão (lembrado no aparelho) ---------- */
const leve = document.querySelector('[data-modo-leve]');
const aplicaLeve = (on) => { raiz.classList.toggle('modo-leve', on); leve?.setAttribute('aria-pressed', String(on)); };
aplicaLeve(guarda.get('kg_leve') === '1');
leve?.addEventListener('click', () => { const on = !raiz.classList.contains('modo-leve'); guarda.set('kg_leve', on ? '1' : '0'); aplicaLeve(on); });

/* ---------- 19. lançamento em destaque: toca a faixa no card dela ---------- */
document.querySelector('[data-destaque]')?.addEventListener('click', () => {
  const alvo = [...document.querySelectorAll('.faixa__play')].find((b) => b.getAttribute('aria-label')?.includes('Vazio Infinito'));
  if (alvo) { alvo.closest('.faixa').scrollIntoView({ behavior: reduz ? 'auto' : 'smooth', block: 'center' }); alvo.click(); }
});

/* ---------- 20. compartilhar (Web Share no celular, copia o link no computador) ---------- */
document.addEventListener('click', async (e) => {
  const b = e.target.closest('[data-compartilhar]'); if (!b) return;
  const url = location.href.split('#')[0] + '#lancamentos'; const title = b.dataset.titulo || document.title;
  try {
    if (navigator.share) await navigator.share({ title, url });
    else { await navigator.clipboard.writeText(url); b.classList.add('is-copiado'); b.textContent = 'Link copiado'; setTimeout(() => { b.classList.remove('is-copiado'); b.textContent = 'Compartilhar'; }, 2000); }
  } catch { /* cancelado */ }
});

/* ---------- 21. privacidade: mostra e apaga o que o site guarda ---------- */
const priv = document.querySelector('.priv');
if (priv) {
  document.querySelector('[data-priv]')?.addEventListener('click', () => priv.showModal?.());
  priv.addEventListener('click', (e) => {
    if (e.target === priv || e.target.closest('[data-priv-fechar]')) priv.close();
    if (e.target.closest('[data-priv-apagar]')) {
      ['kg_anime', 'kg_voto', 'kg_leve'].forEach((k) => { try { localStorage.removeItem(k); } catch { /* privado */ } });
      aplicaAnime('', 'apagar'); aplicaLeve(false);
      document.querySelector('[data-voto]')?.classList.remove('is-votado'); document.querySelectorAll('.voto__item.is-meu').forEach((li) => li.classList.remove('is-meu'));
      e.target.closest('[data-priv-apagar]').textContent = 'Preferências apagadas';
    }
  });
}

/* ---------- 22. pontos do seletor: pulam direto para cada sombra dentro da seção fixada ---------- */
document.querySelectorAll('.sel').forEach((sel) => {
  const pontos = [...sel.querySelectorAll('[data-ir]')]; if (!pontos.length) return;
  const n = sel.querySelectorAll('[data-step]').length;
  const marca = () => { const i = Number(sel.dataset.current || 0); pontos.forEach((p, k) => (k === i ? p.setAttribute('aria-current', 'step') : p.removeAttribute('aria-current'))); };
  new MutationObserver(marca).observe(sel, { attributes: true, attributeFilter: ['data-current'] }); marca();
  sel.addEventListener('click', (e) => {
    const p = e.target.closest('[data-ir]'); if (!p || !raiz.classList.contains('motion')) return;
    e.preventDefault();
    const topo = sel.getBoundingClientRect().top + scrollY; const curso = sel.offsetHeight - innerHeight;
    scrollTo({ top: topo + curso * ((Number(p.dataset.ir) + .5) / n), behavior: reduz ? 'auto' : 'smooth' });
  });
});

/* ---------- 23. janela da letra: anterior / próxima ---------- */
if (dlg) {
  const ids = [...new Set([...document.querySelectorAll('[data-letra]')].map((a) => a.dataset.letra))];
  let atual = 0;
  const abre = (i) => { atual = (i + ids.length) % ids.length; const tpl = document.getElementById(`tpl-letra-${ids[atual]}`); if (!tpl) return;
    dlg.querySelector('[data-dlg-cat]').textContent = tpl.dataset.cat; dlg.querySelector('[data-dlg-k]').textContent = tpl.dataset.k; dlg.querySelector('[data-dlg-tit]').textContent = tpl.dataset.tit;
    dlg.querySelector('[data-dlg-corpo]').replaceChildren(tpl.content.cloneNode(true)); dlg.querySelector('[data-dlg-pos]').textContent = `${atual + 1} de ${ids.length}`; dlg.dataset.letra = ids[atual]; };
  document.addEventListener('click', (e) => { const a = e.target.closest('[data-letra]'); if (a) abre(ids.indexOf(a.dataset.letra)); }, true);
  dlg.addEventListener('click', (e) => { const b = e.target.closest('[data-dlg-ir]'); if (b) abre(atual + Number(b.dataset.dlgIr)); });
  dlg.addEventListener('keydown', (e) => { if (e.key === 'ArrowRight') abre(atual + 1); if (e.key === 'ArrowLeft') abre(atual - 1); });
}

/* ---------- 24. ordenar faixas ---------- */
document.querySelector('[data-ordem]')?.addEventListener('change', (e) => {
  const lista = document.querySelector('.faixas'); const itens = [...lista.children];
  const seg = (d) => { const [m, s] = (d || '0:0').split(':').map(Number); return m * 60 + s; };
  const ord = { obra: (a, b) => itens.indexOf(a) - itens.indexOf(b), az: (a, b) => a.querySelector('h3').textContent.localeCompare(b.querySelector('h3').textContent, 'pt'), dur: (a, b) => seg(b.dataset.dur) - seg(a.dataset.dur) }[e.target.value];
  if (e.target.value === 'obra') itens.sort((a, b) => Number(a.dataset.i) - Number(b.dataset.i)); else itens.sort(ord);
  itens.forEach((li) => lista.append(li));
});
document.querySelectorAll('.faixas > .faixa').forEach((li, i) => (li.dataset.i = i));

/* ---------- 25. scroll-spy: o menu marca a seção que está na tela ---------- */
{ const links = [...document.querySelectorAll('.site-header nav a[href^="#"]')];
  const alvos = links.map((a) => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const io = new IntersectionObserver((es) => es.forEach((x) => { if (!x.isIntersecting) return; links.forEach((a) => (a.getAttribute('href') === `#${x.target.id}` ? a.setAttribute('aria-current', 'true') : a.removeAttribute('aria-current'))); }), { rootMargin: '-45% 0px -50% 0px' });
  alvos.forEach((s) => io.observe(s)); }

/* ---------- 26. hero fora da tela: pausa as animações dela (bateria e CPU) ---------- */
{ const hero = document.querySelector('.hero'); if (hero) new IntersectionObserver(([x]) => raiz.classList.toggle('hero-fora', !x.isIntersecting)).observe(hero); }

/* ---------- 27. animações infinitas pausam fora da tela (seções inteiras) ---------- */
{ const io = new IntersectionObserver((es) => es.forEach((x) => x.target.classList.toggle('is-fora-tela', !x.isIntersecting)), { rootMargin: '100px 0px' });
  document.querySelectorAll('.sel, .hub, .numeros, .dic, .cta, .rodape, .lanc, .etapas').forEach((s) => io.observe(s)); }
