# Ajuste 2 — alinhar estrutura com johnjohndenim.com.br

Mantenha tudo em HTML + CSS + JS puro. Ajuste a estrutura para ficar idêntica ao fluxo da John John Denim, com a identidade BRAVO:

1. **Barra de anúncio**: mensagem principal "EM ATÉ 6X SEM JUROS" (mantém rotação com as outras).
2. **Menu principal** (nesta ordem): NEW · COLEÇÕES · ROUPAS · ALFAIATARIA · JEANS · BEST SELLERS · GUIA DE ESTILO · BLACK SALE. Link secundário "ATENDIMENTO" no topo.
3. **Mega-menu**: grupos ROUPAS / CALÇADOS / ACESSÓRIOS com subcategorias + blocos "COMPRE POR TAMANHO" (PP P M G GG XGG) e "COMPRE POR PREÇO" (até R$ 199 · até R$ 299 · até R$ 399 · até R$ 499) e "DESCONTOS" (40% · 50% · 60% OFF) no item BLACK SALE.
4. **Home**: logo abaixo do header, **banner de campanha** "BLACK SALE BRAVO" (desktop + mobile, imagens diferentes) antes do hero slider; depois seção **"COMPRE POR CATEGORIA"** (tiles com imagem). Resto da home mantém.
5. **categoria.html**: título "Masculino"; **sidebar de filtros à esquerda** (Subcategoria, Cor, Material, Modelagem, Tamanho, Faixa de preço) com acordeões e checkboxes, vira drawer no mobile; acima do grid, contagem "30 de 112 resultados" + select ordenar (Relevância, Mais vendidos, Mais recentes, Desconto, Maior preço, Menor preço, Nome A-Z, Nome Z-A); grid; botão **"VER MAIS"**; abaixo, bloco de **texto SEO** ("Moda masculina BRAVO", "Alfaiataria masculina").
6. **Card de produto**: selo (NEW / BLACK SALE / BEST SELLER), 2 imagens (hover), nome, **preço riscado + preço promocional** quando tiver desconto, parcelamento "3x de R$ xx", favoritar e compra rápida por tamanho.
7. Adicione `precoOriginal` e `selo` ao `products.js`.
8. Mantenha os arquivos `cart.js`, `filters.js`, `search.js`, `wishlist.js` como esqueleto com `// TODO:` — o dono vai codar.
