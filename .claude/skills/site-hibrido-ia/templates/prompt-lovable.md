# BRAVO MENSWEAR — Prompt Lovable

Crie o FRONTEND (só interface, sem backend, sem banco, sem auth) de um e-commerce de moda masculina premium chamado **BRAVO MENSWEAR**.

## REGRA Nº 1 — STACK: SÓ HTML + CSS + JAVASCRIPT PURO
- O dono vai continuar codando à mão. NADA de React/TSX/JSX/shadcn na interface do site.
- Entregar páginas HTML estáticas + JavaScript vanilla (ES modules) + 1 CSS puro:
  - `index.html` (home), `categoria.html` (listagem), `produto.html` (página de produto)
  - `assets/css/style.css` (variáveis CSS no `:root`, sem Tailwind)
  - `assets/js/main.js` (header, mega-menu, slider, drawers, carrosséis)
  - `assets/js/products.js` (array de produtos `export const PRODUCTS = [...]`)
  - `assets/js/render.js` (render dos cards a partir do array)
  - `assets/js/cart.js`, `assets/js/filters.js`, `assets/js/search.js`, `assets/js/wishlist.js` → **só esqueleto com funções vazias e comentários `// TODO:`** explicando o que implementar.
  - `assets/img/` com todas as imagens geradas.
- Se a stack do Lovable obrigar React, deixe o React como casca mínima e coloque o site real como arquivos estáticos em `public/` (ex.: `public/index.html`, `public/assets/...`), servidos direto. A raiz `/` deve abrir o site estático.
- HTML semântico, comentado por seção (`<!-- ===== HERO ===== -->`), com `id` e `data-*` prontos para o JS (`data-add-to-cart`, `data-product-id`, `data-size`, `data-drawer="cart"`, `data-filter="tamanho"` etc.).

## ESTRUTURA — idêntica a um e-commerce premium brasileiro estilo John John
Home, de cima para baixo:
1. **Barra de anúncio** preta, texto rotativo: "FRETE GRÁTIS ACIMA DE R$ 499" / "ATÉ 6X SEM JUROS" / "PRIMEIRA COMPRA: 10% OFF COM BRAVO10".
2. **Header fixo**: menu à esquerda (NOVIDADES · ROUPAS · ALFAIATARIA · JEANS · CALÇADOS · ACESSÓRIOS · OUTLET), logo BRAVO centralizado, à direita ícones busca, conta, favoritos, sacola com contador. Transparente sobre o hero, fica sólido ao rolar. Mobile: hambúrguer + menu lateral.
3. **Mega-menu** ao passar no item: colunas de subcategorias + 1 imagem editorial à direita.
4. **Hero full-bleed** (100vh) em slider com 3 slides de campanha, título grande espaçado, CTA "COMPRAR AGORA", setas e bullets.
5. **Tiles de categoria** (4 colunas): Alfaiataria, Camisas, Tricô, Jaquetas — imagem + rótulo em caixa alta.
6. **Vitrine "LANÇAMENTOS"** — carrossel horizontal de cards de produto.
7. **Banner editorial dividido** 50/50: imagem grande + texto "A NOVA ALFAIATARIA" + CTA.
8. **Vitrine "MAIS VENDIDOS"** — carrossel.
9. **Campanha full-bleed** com frase manifesto ("FEITO PARA QUEM NÃO PEDE LICENÇA").
10. **Shop the look** — foto do look com pontos clicáveis (hotspots) que abrem o produto.
11. **Grid estilo Instagram** @bravomenswear (6 imagens).
12. **Newsletter** — "RECEBA EM PRIMEIRA MÃO" + input email.
13. **Footer** preto: colunas Institucional, Ajuda, Minha Conta, Atendimento; redes sociais; formas de pagamento; selos de segurança; CNPJ fictício.

**Card de produto**: imagem 3:4, troca para 2ª imagem no hover, coração de favoritar, selo "NOVO", nome, preço, "6x de R$ xx sem juros", bolinhas de cor, tamanhos aparecem no hover para compra rápida.

**categoria.html**: breadcrumb, título, contagem, barra de filtros no topo (Tamanho, Cor, Preço, Categoria) + drawer de filtros, ordenar, toggle de grid 2/3/4 colunas, grid de produtos, botão "CARREGAR MAIS".

**produto.html**: galeria vertical de imagens à esquerda, à direita nome, preço, parcelamento, cores, seletor de tamanho (P M G GG / 38–46), "ADICIONAR À SACOLA", favoritar, calcular frete (CEP), acordeões Descrição / Composição / Cuidados / Trocas, "COMPLETE O LOOK" e "VOCÊ TAMBÉM PODE GOSTAR".

**Componentes globais**: drawer da sacola (lado direito), overlay de busca em tela cheia, drawer menu mobile.

## IDENTIDADE VISUAL — linguagem Hugo Boss (sem usar nome/logo dela)
- Minimalismo de luxo, muito preto, contraste alto, espaço negativo generoso, sem bordas arredondadas (radius 0), sem sombras, sem gradientes.
- Paleta: preto `#0B0B0B`, grafite `#1A1A1A`, cinza pedra `#8C8984`, off-white quente `#EDE8E2` (cor do logo), branco `#FAFAF8`.
- Tipografia: títulos e menu em caixa alta, sans geométrica larga com letter-spacing grande (0.3em) — usar **Jost** (Google Fonts); corpo **Manrope**. Preço em tabular-nums.
- Logo: recriar em SVG inline o monograma "B" geométrico com cortes diagonais + wordmark "BRAVO" bem espaçado (ver imagem anexada `bravo-logo.webp`). Versão clara sobre fundo preto e escura sobre claro.
- Moodboard anexado (`bravo-moodboard.webp`) define o clima: preto, concreto, luz baixa, etiquetas e sacolas pretas com logo prata.
- Microinterações discretas: fade/slide curto (200–300ms, ease-out), sublinhado animado no menu, zoom leve na imagem do card. Respeitar `prefers-reduced-motion`.

## PRODUTOS — catálogo estilo Zara masculino (peças, não marca)
Criar ~16 produtos fictícios BRAVO em `products.js` (id, nome, categoria, preço, cores, tamanhos, imagens, novo, descrição, composição):
Blazer de lã estruturado · Sobretudo longo de lã · Camisa oxford slim · Camisa de linho · Polo de malha piquet · Camiseta heavyweight oversized · Tricô gola alta merino · Cardigan texturizado · Calça de alfaiataria pregas · Calça chino · Jeans reto lavagem escura · Jaqueta de couro · Bomber técnica · Tênis de couro minimal · Mocassim de couro · Cinto de couro.
Preços entre R$ 199 e R$ 1.499.

## IMAGENS — use a geração de imagens do Lovable
Gere TODAS as imagens com IA, mesma direção de arte do moodboard: fotografia de moda masculina editorial, luz baixa e lateral, tons preto/grafite/bege-concreto, modelos masculinos diversos, granulação sutil, nada de texto nas fotos.
- 3 heros de campanha (horizontal, 16:9)
- 4 tiles de categoria (3:4)
- 2 editoriais (alfaiataria e manifesto)
- 1 shop the look
- 6 grid Instagram (1:1)
- Fotos de produto (3:4) de cada peça em fundo off-white/concreto, still ou em modelo, com 2ª imagem para hover
- Etiqueta, sacola e embalagem com logo BRAVO para o rodapé/sobre
Salvar em `assets/img/` com nomes descritivos e `alt` em português.

## QUALIDADE
- Responsivo (mobile-first, 375px → 1440px+), sem scroll horizontal.
- Acessível: contraste AA, foco visível, `aria-label` nos ícones, drawers com `aria-expanded` e Esc para fechar.
- Ícones em SVG inline (traço fino 1.5px).
- Código limpo, indentado e comentado em português — é para estudo e continuação manual.
