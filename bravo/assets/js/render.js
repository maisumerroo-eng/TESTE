/* =========================================================
   render.js · transforma os dados de products.js em HTML.
   ========================================================= */
import { ICONES } from './layout.js';

/* ---------- FORMATAÇÃO ---------- */
export const brl = (valor) =>
  valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

/* Parcelamento: até 6x sem juros, parcela mínima R$ 50 */
export function parcelas(valor, max = 6, minimo = 50) {
  const n = Math.max(1, Math.min(max, Math.floor(valor / minimo)));
  return { n, valor: valor / n };
}

/* ---------- FALLBACK DE IMAGEM ----------
   Se uma imagem não existir: tenta data-alt, depois o placeholder. */
const PLACEHOLDER = 'assets/img/placeholder.svg';
function trocarImagem(img) {
  if (img.dataset.alt) {
    img.src = img.dataset.alt;
    img.dataset.alt = '';
  } else if (!img.src.endsWith(PLACEHOLDER)) {
    img.src = PLACEHOLDER;
  }
}
export function ativarFallbackImagens() {
  // Imagens que falharem daqui em diante
  document.addEventListener('error', (e) => {
    if (e.target instanceof HTMLImageElement) trocarImagem(e.target);
  }, true);
  // Imagens que já falharam antes deste script rodar
  document.querySelectorAll('img').forEach((img) => {
    if (img.complete && img.naturalWidth === 0 && img.getAttribute('src')) trocarImagem(img);
  });
}

/* ---------- CARD DE PRODUTO ---------- */
export function cardHTML(p) {
  const [img1, img2] = p.imagens;
  const parc = parcelas(p.preco);
  const seloClasse = p.selo === 'BLACK SALE' ? 'sale' : '';
  return `
  <article class="card" data-product-id="${p.id}">
    <a href="produto.html?id=${p.id}" class="card-midia" aria-label="${p.nome}">
      ${p.selo ? `<span class="card-selo eyebrow ${seloClasse}">${p.selo}</span>` : ''}
      <img src="${img1}" data-alt="${img2}" alt="${p.nome}, foto principal" loading="lazy">
      <img src="${img2}" data-alt="${img1}" alt="" class="img-2" loading="lazy">
    </a>
    <button class="icone-btn card-fav" aria-label="Favoritar ${p.nome}" aria-pressed="false" data-wishlist-toggle="${p.id}">${ICONES.coracao}</button>
    <div class="card-tamanhos" aria-label="Compra rápida">
      <p class="eyebrow">Adicionar tamanho</p>
      ${p.tamanhos.map((t) => `<button data-add-to-cart="${p.id}" data-size="${t}">${t}</button>`).join('')}
    </div>
    <a href="produto.html?id=${p.id}" class="card-nome">${p.nome}</a>
    <div class="card-precos preco">
      <span class="linha-preco">
        ${p.precoOriginal ? `<s class="preco-de">${brl(p.precoOriginal)}</s>` : ''}
        <span>${brl(p.preco)}</span>
      </span>
      <span class="card-parcela">${parc.n}x de ${brl(parc.valor)} sem juros</span>
    </div>
    <div class="cores" aria-label="Cores disponíveis">
      ${p.cores.map((c) => `<span class="cor-bolinha" style="background:${c.hex}" title="${c.nome}"></span>`).join('')}
    </div>
  </article>`;
}

/* Renderiza uma lista de produtos dentro de um container */
export function renderLista(container, lista) {
  if (!container) return;
  container.innerHTML = lista.map(cardHTML).join('');
}

/* ---------- PÁGINA DE PRODUTO ---------- */
export function renderPDP(p) {
  const raiz = document.querySelector('[data-pdp]');
  if (!raiz || !p) return;
  document.title = `${p.nome} · BRAVO Menswear`;
  const parc = parcelas(p.preco);

  raiz.querySelector('[data-pdp-breadcrumb]').textContent = p.nome;
  raiz.querySelector('[data-pdp-nome]').textContent = p.nome;
  raiz.querySelector('[data-pdp-ref]').textContent = `REF. ${p.id.toUpperCase()}`;
  raiz.querySelector('[data-pdp-preco]').innerHTML =
    `${p.precoOriginal ? `<s class="preco-de">${brl(p.precoOriginal)}</s> ` : ''}${brl(p.preco)}`;
  raiz.querySelector('[data-pdp-parcela]').textContent = `${parc.n}x de ${brl(parc.valor)} sem juros`;
  raiz.querySelector('[data-pdp-descricao]').textContent = p.descricao;
  raiz.querySelector('[data-pdp-composicao]').textContent = p.composicao;

  // Galeria: as 2 imagens + 2 repetidas como "detalhe" (troque por fotos reais)
  const [a, b] = p.imagens;
  raiz.querySelector('[data-pdp-galeria]').innerHTML = [a, b, b, a]
    .map((src, i) => `<img src="${src}" data-alt="${i % 2 ? a : b}" alt="${p.nome}, foto ${i + 1}" ${i > 1 ? 'loading="lazy"' : ''}>`)
    .join('');

  raiz.querySelector('[data-pdp-cores]').innerHTML = p.cores
    .map((c, i) => `<button class="cor-opcao" style="background:${c.hex}" aria-label="${c.nome}" aria-pressed="${i === 0}" data-color="${c.nome}"></button>`)
    .join('');
  raiz.querySelector('[data-pdp-cor-nome]').textContent = p.cores[0].nome;

  raiz.querySelector('[data-pdp-tamanhos]').innerHTML = p.tamanhos
    .map((t) => `<button class="tamanho" aria-pressed="false" data-size="${t}">${t}</button>`)
    .join('');

  raiz.querySelector('[data-add-to-cart]').dataset.addToCart = p.id;
  raiz.querySelector('[data-wishlist-toggle]').dataset.wishlistToggle = p.id;
}
