/* =========================================================
   render.js · transforma os dados de products.js em HTML.
   ========================================================= */
import { ICONES } from './layout.js';
import { waLink } from './config.js';

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

/* Bloco de preço: com preço → valor + parcelas; sem preço → consulta */
function precoHTML(p) {
  if (p.preco == null) return `<span class="card-parcela">Consulte o preço no WhatsApp</span>`;
  const parc = parcelas(p.preco);
  return `
      <span class="linha-preco">
        ${p.precoOriginal ? `<s class="preco-de">${brl(p.precoOriginal)}</s>` : ''}
        <span>${brl(p.preco)}</span>
      </span>
      <span class="card-parcela">${parc.n}x de ${brl(parc.valor)} sem juros</span>`;
}

/* ---------- CARD DE PRODUTO ---------- */
export function cardHTML(p) {
  const [img1, img2] = p.imagens;
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
    <div class="card-precos preco">${precoHTML(p)}</div>
    <div class="cores" aria-label="Outras cores">
      ${p.cores.map((c) => `<a href="produto.html?id=${c.id}" class="cor-bolinha" style="background:${c.hex}" title="${c.nome}" aria-label="${c.nome}"></a>`).join('')}
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

  raiz.querySelector('[data-pdp-breadcrumb]').textContent = p.nome;
  raiz.querySelector('[data-pdp-nome]').textContent = p.nome;
  raiz.querySelector('[data-pdp-ref]').textContent = p.codigo ? `REF. ${p.codigo}` : p.subcategoria;
  raiz.querySelector('[data-pdp-preco]').innerHTML = precoHTML(p);
  raiz.querySelector('[data-pdp-descricao]').textContent = p.descricao;
  raiz.querySelector('[data-pdp-composicao]').textContent =
    p.composicao || 'Pergunte a composição pelo WhatsApp.';

  // Galeria: as 2 imagens + 2 repetidas como "detalhe" (troque por fotos reais)
  const [a, b] = p.imagens;
  raiz.querySelector('[data-pdp-galeria]').innerHTML = [a, b, b, a]
    .map((src, i) => `<img src="${src}" data-alt="${src === a ? b : a}" alt="${p.nome}, foto ${i + 1}" ${i > 1 ? 'loading="lazy"' : ''}>`)
    .join('');

  // Cada cor é um produto: o seletor navega para a outra cor
  raiz.querySelector('[data-pdp-cores]').innerHTML = p.cores
    .map((c) => `<a href="produto.html?id=${c.id}" class="cor-opcao" style="background:${c.hex}" aria-label="${c.nome}" aria-current="${c.id === p.id}"></a>`)
    .join('');
  raiz.querySelector('[data-pdp-cor-nome]').textContent = p.cor.nome;

  // Botão WhatsApp com a peça na mensagem (tamanho entra quando escolhido, ver main.js)
  const wa = raiz.querySelector('[data-whatsapp-produto]');
  wa.href = waLink(`Olá! Quero o ${p.nome}.`);
  wa.dataset.produto = p.nome;

  raiz.querySelector('[data-pdp-tamanhos]').innerHTML = p.tamanhos
    .map((t) => `<button class="tamanho" aria-pressed="false" data-size="${t}">${t}</button>`)
    .join('');

  raiz.querySelector('[data-add-to-cart]').dataset.addToCart = p.id;
  raiz.querySelector('[data-wishlist-toggle]').dataset.wishlistToggle = p.id;
}
