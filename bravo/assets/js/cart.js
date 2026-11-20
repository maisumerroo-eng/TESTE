/* =========================================================
   cart.js · SACOLA (funcionando)
   Guarda os itens no navegador (localStorage) e desenha o drawer.
   Ganchos no HTML:
     [data-add-to-cart="ID"] + [data-size="M"]  → botões de compra
     [data-cart-count]      → contadores (header e drawer)
     [data-cart-items]      → lista de itens no drawer
     [data-cart-subtotal]   → subtotal
     [data-checkout]        → botão "Finalizar compra" (vai para checkout.html)
   ========================================================= */
import { getProduct } from './products.js';
import { brl } from './render.js';

const CHAVE = 'bravo:sacola';

/* Estado: [{ id, size, qtd }] */
let itens = ler();

function ler() {
  try { return JSON.parse(localStorage.getItem(CHAVE)) || []; } catch { return []; }
}
function salvar() {
  try { localStorage.setItem(CHAVE, JSON.stringify(itens)); } catch { /* modo privado: segue só na memória */ }
}

/* ---------- API usada pelo resto do site ---------- */
export const getItens = () => itens.map((i) => ({ ...i, produto: getProduct(i.id) })).filter((i) => i.produto);
export const totalPecas = () => itens.reduce((s, i) => s + i.qtd, 0);

/* Subtotal: null se algum item ainda não tem preço ("a combinar") */
export function subtotal() {
  const lista = getItens();
  if (lista.some((i) => i.produto.preco == null)) return null;
  return lista.reduce((s, i) => s + i.produto.preco * i.qtd, 0);
}

export function addToCart(id, size) {
  if (!size) return;
  const item = itens.find((i) => i.id === id && i.size === size);
  if (item) item.qtd += 1;
  else itens.push({ id, size, qtd: 1 });
  salvar();
  renderCart();
  // Abre o drawer da sacola (mesma ação do ícone da sacola)
  document.querySelector('[data-abrir="sacola"]')?.click();
}

export function removeFromCart(id, size) {
  itens = itens.filter((i) => !(i.id === id && i.size === size));
  salvar();
  renderCart();
}

export function updateQty(id, size, qtd) {
  const item = itens.find((i) => i.id === id && i.size === size);
  if (!item) return;
  item.qtd = Math.max(1, Math.min(20, qtd));
  salvar();
  renderCart();
}

export function limparSacola() {
  itens = [];
  salvar();
  renderCart();
}

/* ---------- Desenho ---------- */
export function renderCart() {
  const total = totalPecas();
  document.querySelectorAll('[data-cart-count]').forEach((el) => (el.textContent = total));

  const caixa = document.querySelector('[data-cart-items]');
  if (!caixa) return;
  const lista = getItens();

  if (!lista.length) {
    caixa.innerHTML = `
      <div class="sacola-vazia">
        <p>Sua sacola está vazia.</p>
        <a href="categoria.html" class="btn btn-escuro">Ver os conjuntos</a>
      </div>`;
  } else {
    caixa.innerHTML = lista.map(({ produto: p, size, qtd }) => `
      <article class="sacola-item">
        <img src="${p.imagens[0]}" alt="">
        <div>
          <h3>${p.nome}</h3>
          <p>Tamanho ${size}</p>
          <p class="preco">${p.preco == null ? 'Preço a combinar' : brl(p.preco * qtd)}</p>
          <div class="qtd" aria-label="Quantidade">
            <button aria-label="Diminuir" data-qtd="-1" data-id="${p.id}" data-size="${size}">−</button>
            <span>${qtd}</span>
            <button aria-label="Aumentar" data-qtd="1" data-id="${p.id}" data-size="${size}">+</button>
          </div>
        </div>
        <button class="sacola-remover" data-remover data-id="${p.id}" data-size="${size}">Remover</button>
      </article>`).join('');
  }

  const sub = subtotal();
  document.querySelectorAll('[data-cart-subtotal]').forEach((el) => {
    el.textContent = !lista.length ? brl(0) : sub == null ? 'A combinar' : brl(sub);
  });
  document.querySelectorAll('[data-checkout]').forEach((b) => (b.disabled = !lista.length));
}

export function initCart() {
  renderCart();

  // Botões dentro do drawer (+, −, remover)
  document.addEventListener('click', (e) => {
    const q = e.target.closest('[data-qtd]');
    if (q) {
      const item = itens.find((i) => i.id === q.dataset.id && i.size === q.dataset.size);
      if (item) updateQty(item.id, item.size, item.qtd + Number(q.dataset.qtd));
      return;
    }
    const r = e.target.closest('[data-remover]');
    if (r) return removeFromCart(r.dataset.id, r.dataset.size);
    if (e.target.closest('[data-checkout]')) location.href = 'checkout.html';
  });

  // Sacola alterada em outra aba
  addEventListener('storage', (e) => { if (e.key === CHAVE) { itens = ler(); renderCart(); } });
}
