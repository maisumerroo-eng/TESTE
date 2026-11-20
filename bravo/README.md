# BRAVO MENSWEAR — frontend (HTML + CSS + JS puro)

Estrutura de e-commerce no estilo John John, identidade minimalista preta.
Catálogo REAL: 3 modelos de conjunto (Ondas, Jacquard, Canelado) em 12 cores, do P ao GG.
Venda pelo WhatsApp (número em `assets/js/config.js`).

PENDENTE: preços, composição do Jacquard e do Canelado, e-mail, CNPJ, endereço.

## Rodar
ES modules não abrem via `file://`. Sirva a pasta:
```bash
cd bravo
python3 -m http.server 8000   # ou: npx serve .   ou Live Server no VS Code
```
Abra http://localhost:8000

## Imagens (geradas pelo Lovable a partir das fotos reais)
Projeto Lovable "BRAVO Menswear Produtos Reais" gera as fotos em `public/assets/img/`.
Imagem que faltar cai em `placeholder.svg` sozinha.

Padrão: `produto-<modelo>-<cor>-1.jpg` (still) e `-2.jpg` (no modelo), ex.: `produto-jacquard-preto-1.jpg`.
Fotos originais ficam em `referencias/` (fora do git, têm etiqueta de terceiros).

## Arquivos
| Arquivo | O que faz | Status |
|---|---|---|
| `index.html` `categoria.html` `produto.html` | páginas | prontas |
| `assets/css/style.css` | todo o visual (variáveis no `:root`) | pronto |
| `assets/js/layout.js` | header, mega-menu, footer, drawers (edite o menu aqui) | pronto |
| `assets/js/main.js` | slider, drawers, carrosséis, PDP, grid 2/3/4 | pronto |
| `assets/js/products.js` | catálogo | pronto |
| `assets/js/render.js` | cards e página de produto | pronto |
| `assets/js/cart.js` | sacola | **TODO — você coda** |
| `assets/js/wishlist.js` | favoritos | **TODO** |
| `assets/js/search.js` | busca | **TODO** |
| `assets/js/filters.js` | filtros + ordenar + ver mais | **TODO** |

Cada arquivo TODO lista no topo os `data-*` que o HTML já expõe.
Ordem sugerida: `cart.js` → `wishlist.js` → `filters.js` → `search.js`.

## Prompts
- `PROMPT-LOVABLE.md`: prompt principal usado no Lovable.
- `PROMPT-LOVABLE-AJUSTE-JOHNJOHN.md`: ajuste da estrutura (já aplicado aqui no código).
