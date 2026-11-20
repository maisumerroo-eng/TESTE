/* =========================================================
   search.js — BUSCA (esqueleto para você implementar)
   Ganchos prontos no HTML (overlay de busca):
     [data-search-form]    → formulário
     [data-search-input]   → campo de texto
     [data-search-chip]    → sugestões rápidas
     [data-search-results] → grid onde mostrar os resultados
   Dica: renderLista(container, lista) em render.js já monta os cards.
   ========================================================= */
// import { renderLista } from './render.js';

export function initSearch(produtos) {
  const form = document.querySelector('[data-search-form]');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    // TODO: chamar buscar() com o valor do input e renderizar.
  });

  // TODO: busca enquanto digita (input event) com debounce de ~200ms.
  // TODO: clique em [data-search-chip] preenche o input e busca.
}

export function buscar(produtos, termo) {
  // TODO: normalizar (minúsculas + remover acentos com .normalize('NFD'))
  //       e filtrar por nome, categoria, subcategoria e material.
  return [];
}
