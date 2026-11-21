// personaliza.js: motor de variantes por visitante (Camada 2 da megapersonalização).
// Só sinais de primeira parte, sem dado pessoal. Conteúdo padrão continua no HTML (SEO e sem JS).
//
// Marcação:
//   <h1 data-p="hero-title">Texto padrão</h1>
//   <template data-p-variant="hero-title" data-seg="pis-cofins">Texto do segmento</template>
//   <div data-p-order> <article data-seg="pis-cofins">..</article> ... </div>   → segmento sobe pro topo
//   <a data-wa="5562999999999">WhatsApp</a>                                    → link com mensagem do segmento
//   <button data-p-choose="transportadora">Sou transportadora</button>          → escolha explícita, salva
//   <a href="?seg=padrao">ver versão padrão</a>                                 → sempre oferecer

const CONFIG = {
  padrao: 'padrao',
  // palavra encontrada em utm_campaign / utm_term / utm_content → segmento
  palavras: {
    'pis': 'pis-cofins', 'cofins': 'pis-cofins',
    'reforma': 'reforma', 'cbs': 'reforma', 'ibs': 'reforma',
  },
  // origem (document.referrer) → segmento, usado só se nada mais decidir
  origens: { 'instagram.com': 'social', 'facebook.com': 'social', 'linkedin.com': 'b2b' },
  // mensagem do WhatsApp por segmento ({pagina} = título da página)
  whatsapp: {
    padrao: 'Olá! Vim pelo site e quero o diagnóstico gratuito.',
    'pis-cofins': 'Olá! Vi o conteúdo sobre créditos de PIS/COFINS e quero o diagnóstico gratuito.',
    reforma: 'Olá! Quero entender o impacto da CBS e do IBS na minha empresa.',
  },
  horario: { inicio: 8, fim: 18, diasUteis: [1, 2, 3, 4, 5] },
  chave: 'p_seg',
};

const html = document.documentElement;
const store = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { localStorage.setItem(k, v); } catch { /* modo privado */ } },
};

function resolverSegmento() {
  const q = new URLSearchParams(location.search);
  const direto = q.get('seg');
  if (direto) { if (direto !== CONFIG.padrao) store.set(CONFIG.chave, direto); return { seg: direto, fonte: 'url' }; }
  const utm = ['utm_campaign', 'utm_term', 'utm_content'].map((k) => (q.get(k) || '').toLowerCase()).join(' ');
  for (const [palavra, seg] of Object.entries(CONFIG.palavras)) {
    if (utm.includes(palavra)) { store.set(CONFIG.chave, seg); return { seg, fonte: 'utm' }; }
  }
  const salvo = store.get(CONFIG.chave);
  if (salvo) return { seg: salvo, fonte: 'escolha' };
  let host = '';
  try { host = document.referrer ? new URL(document.referrer).hostname.replace(/^www\./, '') : ''; } catch { /* referrer inválido */ }
  for (const [dominio, seg] of Object.entries(CONFIG.origens)) {
    if (host.endsWith(dominio)) return { seg, fonte: 'origem' };
  }
  return { seg: CONFIG.padrao, fonte: 'padrao' };
}

function aplicar(seg) {
  html.dataset.seg = seg;

  // textos/blocos
  document.querySelectorAll('[data-p]').forEach((alvo) => {
    const chave = alvo.dataset.p;
    if (!alvo.dataset.pOriginal) alvo.dataset.pOriginal = alvo.innerHTML;
    const tpl = document.querySelector(`template[data-p-variant="${CSS.escape(chave)}"][data-seg="${CSS.escape(seg)}"]`);
    alvo.innerHTML = tpl ? tpl.innerHTML.trim() : alvo.dataset.pOriginal;
    delete alvo.dataset.split; // permite o motion.js re-quebrar palavras, se precisar
  });

  // ordem: itens do segmento sobem
  document.querySelectorAll('[data-p-order]').forEach((box) => {
    const itens = [...box.children];
    itens.sort((a, b) => (b.dataset.seg === seg) - (a.dataset.seg === seg)).forEach((el) => box.append(el));
  });

  // WhatsApp com mensagem do segmento
  const msg = CONFIG.whatsapp[seg] || CONFIG.whatsapp.padrao;
  document.querySelectorAll('a[data-wa]').forEach((a) => {
    a.href = `https://wa.me/${a.dataset.wa}?text=${encodeURIComponent(msg)}`;
    a.target = '_blank'; a.rel = 'noopener';
  });

  // estado dos botões de escolha
  document.querySelectorAll('[data-p-choose]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.pChoose === seg)));
}

function contexto() {
  const agora = new Date();
  const { inicio, fim, diasUteis } = CONFIG.horario;
  const aberto = diasUteis.includes(agora.getDay()) && agora.getHours() >= inicio && agora.getHours() < fim;
  html.dataset.horario = aberto ? 'aberto' : 'fechado';
  const visitas = Number(store.get('p_visitas') || 0) + 1;
  store.set('p_visitas', String(visitas));
  html.dataset.visita = visitas > 1 ? 'retorno' : 'primeira';
  html.dataset.tela = matchMedia('(max-width: 899px)').matches ? 'mobile' : 'desktop';
}

function emitir(nome, dados) {
  document.dispatchEvent(new CustomEvent(nome, { detail: dados }));
  if (Array.isArray(window.dataLayer)) window.dataLayer.push({ event: nome, ...dados }); // GTM já depende do consentimento
}

contexto();
const { seg, fonte } = resolverSegmento();
aplicar(seg);
emitir('seg_resolvido', { seg, fonte });

document.addEventListener('click', (e) => {
  const escolha = e.target.closest('[data-p-choose]');
  if (escolha) {
    const novo = escolha.dataset.pChoose;
    store.set(CONFIG.chave, novo);
    aplicar(novo);
    emitir('seg_escolhido', { seg: novo });
    return;
  }
  const cta = e.target.closest('[data-cta], a[data-wa]');
  if (cta) emitir(cta.matches('a[data-wa]') ? 'whatsapp_open' : 'cta_click', { seg: html.dataset.seg, posicao: cta.dataset.cta || '' });
});

export { aplicar, resolverSegmento, CONFIG };
