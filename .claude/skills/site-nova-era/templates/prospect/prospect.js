// prospect.js: página por prospect (hiperpersonalização por lead). Uma única página serve N leads:
// ?para=<slug> (ou #para-<slug>) carrega prospects/<slug>.json e troca nome, cidade, logo, cores, fotos e WhatsApp.
// Sem parâmetro: conteúdo padrão do HTML (a página continua íntegra e indexável só na versão padrão).
//
// Marcação: <span data-pp="nome">Seu negócio</span> · <img data-pp-src="logo" ...> · <a data-pp-wa>...</a>
//           <span data-pp="cidade">sua cidade</span> · <img data-pp-src="fotos.0"> · qualquer chave do JSON (aceita "a.b.0")
// Importar DEPOIS do personaliza.js e ANTES do motion.js: o prospect tem a palavra final no WhatsApp e os textos já entram animados.
const raiz = document.documentElement;
const q = new URLSearchParams(location.search);
const slug = (q.get('para') || (location.hash.match(/^#para-([\w-]+)$/) || [])[1] || '').replace(/[^\w-]/g, '');
const pega = (o, caminho) => caminho.split('.').reduce((v, k) => (v == null ? v : v[k]), o);

async function aplicar() {
  if (!slug) return;
  let d;
  try {
    const r = await fetch(`prospects/${slug}.json`, { cache: 'no-store' });
    if (!r.ok) throw new Error(r.status);
    d = await r.json();
  } catch { return; }   // lead inexistente: fica a versão padrão
  raiz.dataset.prospect = slug;
  // página de prospect não deve ir para o Google
  const m = document.createElement('meta'); m.name = 'robots'; m.content = 'noindex, nofollow'; document.head.append(m);
  if (d.nome) document.title = document.title.replace(/^[^|]*/, `${d.nome} `);
  document.querySelectorAll('[data-pp]').forEach((el) => { const v = pega(d, el.dataset.pp); if (v != null && v !== '') el.textContent = v; });
  document.querySelectorAll('[data-pp-src]').forEach((el) => { const v = pega(d, el.dataset.ppSrc); if (v) { el.src = v; el.removeAttribute('srcset'); el.closest('picture')?.querySelectorAll('source').forEach((s) => s.remove()); if (el.dataset.ppAlt && pega(d, el.dataset.ppAlt)) el.alt = pega(d, el.dataset.ppAlt); } });
  document.querySelectorAll('[data-pp-show]').forEach((el) => { el.hidden = !pega(d, el.dataset.ppShow); });
  if (d.cores) Object.entries(d.cores).forEach(([k, v]) => raiz.style.setProperty(`--${k}`, v));   // ex.: {"accent":"#c4703f","accent-claro":"#e7a274"}
  if (d.whatsapp || d.whatsappAgencia || d.mensagem) {
    const msg = d.mensagem || `Olá! Vi a página que vocês fizeram para a ${d.nome || 'minha empresa'} e quero conversar.`;
    document.querySelectorAll('a[data-pp-wa], a[data-wa]').forEach((a) => { a.dataset.wa = d.whatsappAgencia || d.whatsapp || a.dataset.wa; a.href = `https://wa.me/${a.dataset.wa}?text=${encodeURIComponent(msg)}`; a.target = '_blank'; a.rel = 'noopener'; });
  }
  document.dispatchEvent(new CustomEvent('prospect_aberto', { detail: { slug } }));
  if (Array.isArray(window.dataLayer)) window.dataLayer.push({ event: 'prospect_aberto', slug });
}
await aplicar();
export { aplicar };
