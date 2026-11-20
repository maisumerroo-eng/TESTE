/* =========================================================
   wishlist.js · FAVORITOS (esqueleto para você implementar)
   Ganchos prontos no HTML:
     [data-wishlist-toggle="ID"] → corações (cards e PDP);
        main.js já alterna aria-pressed e chama toggleWishlist(id)
     [data-wishlist-link]        → ícone de favoritos do header
   ========================================================= */

const CHAVE = 'bravo:favoritos';
let favoritos = new Set();

export function initWishlist() {
  // TODO: carregar favoritos do localStorage (try/catch).
  // TODO: marcar aria-pressed="true" em todos os [data-wishlist-toggle] já favoritados.
}

export function toggleWishlist(id) {
  // TODO: adicionar/remover id do Set, salvar e atualizar outros corações do mesmo produto.
  console.info('[wishlist] TODO toggleWishlist:', id);
}

export function getWishlist() {
  return [...favoritos];
}
