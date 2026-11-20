/* =========================================================
   cart.js · SACOLA (esqueleto para você implementar)
   Ganchos prontos no HTML:
     [data-add-to-cart="ID"] + [data-size="M"]  → botões de compra
     [data-cart-count]      → contadores (header e drawer)
     [data-cart-items]      → onde listar os itens no drawer
     [data-cart-subtotal]   → subtotal no rodapé do drawer
     [data-checkout]        → botão finalizar
   Helpers úteis: getProduct (products.js), brl/parcelas (render.js),
   abrirDrawer('sacola') (main.js).
   ========================================================= */
// import { getProduct } from './products.js';
// import { brl } from './render.js';

const CHAVE = 'bravo:sacola';

/* Estado: [{ id, size, qtd }] */
let itens = [];

export function initCart() {
  // TODO: ler itens salvos (localStorage.getItem(CHAVE)) com try/catch e chamar renderCart().
  // TODO: ouvir cliques em [data-checkout].
}

export function addToCart(id, size) {
  // TODO: se o item (id + size) já existe, somar qtd; senão, push({ id, size, qtd: 1 }).
  // TODO: salvar(), renderCart() e abrir o drawer da sacola.
  console.info('[cart] TODO addToCart:', id, size);
}

export function removeFromCart(id, size) {
  // TODO: remover item e re-renderizar.
}

export function updateQty(id, size, qtd) {
  // TODO: alterar quantidade (mínimo 1) e re-renderizar.
}

function salvar() {
  // TODO: localStorage.setItem(CHAVE, JSON.stringify(itens)) dentro de try/catch.
}

function renderCart() {
  // TODO: atualizar todos os [data-cart-count] com a soma das quantidades.
  // TODO: montar HTML de cada item em [data-cart-items] (foto, nome, tamanho, qtd +/-, preço, remover).
  // TODO: mostrar .sacola-vazia quando itens.length === 0.
  // TODO: calcular subtotal e escrever em [data-cart-subtotal].
}
