/* =========================================================
   filters.js — FILTROS + ORDENAÇÃO da categoria (esqueleto)
   Ganchos prontos em categoria.html:
     input[data-filter="subcategoria|cor|material|modelagem|tamanho|preco"]
        (checkboxes na sidebar e no drawer mobile, value = opção)
     select[data-sort]   → relevancia | vendidos | recentes | desconto |
                           maior-preco | menor-preco | az | za
     [data-ver-mais]     → botão "VER MAIS"
     [data-limpar-filtros]
   main.js chama initFilters(PRODUCTS, pintar) — chame pintar(lista)
   sempre que o resultado mudar (ele renderiza e atualiza a contagem).
   ========================================================= */

const POR_PAGINA = 12;

export function initFilters(produtos, pintar) {
  const estado = {
    filtros: {},      // ex.: { tamanho: ['M','G'], cor: ['Preto'] }
    ordem: 'relevancia',
    pagina: 1,
  };

  // TODO: ler filtros iniciais da URL (?c=, ?tamanho=, ?max=, ?off=).
  // TODO: ouvir 'change' em [data-filter] → atualizar estado.filtros → aplicar().
  // TODO: ouvir 'change' em [data-sort]   → estado.ordem → aplicar().
  // TODO: [data-ver-mais] → estado.pagina++ → aplicar().
  // TODO: [data-limpar-filtros] → desmarcar tudo → aplicar().

  function aplicar() {
    let lista = filtrar(produtos, estado.filtros);
    lista = ordenar(lista, estado.ordem);
    pintar(lista.slice(0, estado.pagina * POR_PAGINA));
    // TODO: esconder [data-ver-mais] quando não houver mais itens.
  }
}

export function filtrar(produtos, filtros) {
  // TODO: manter produto se, para CADA grupo marcado, ele bater com ALGUMA opção do grupo.
  //   cor     → p.cores.some(c => opcoes.includes(c.nome))
  //   tamanho → p.tamanhos.some(t => opcoes.includes(t))
  //   preco   → faixas "0-299", "300-599", "600-999", "1000-9999"
  return produtos;
}

export function ordenar(lista, ordem) {
  // TODO: switch(ordem) usando [...lista].sort(...)
  //   desconto → (precoOriginal - preco) / precoOriginal
  return lista;
}
