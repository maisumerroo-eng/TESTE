/* =========================================================
   layout.js · partes que se repetem em todas as páginas.
   Cada página tem marcadores vazios:
     <div data-include="anuncio"></div>
     <div data-include="header"></div>
     <div data-include="footer"></div>
     <div data-include="globais"></div>  (drawers, busca, overlay)
   e este arquivo injeta o HTML neles. Assim você edita o
   header/footer num lugar só.
   ========================================================= */

/* ---------- ÍCONES SVG (traço fino 1.5px) ---------- */
const svg = (d, extra = '') =>
  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" aria-hidden="true" ${extra}>${d}</svg>`;

export const ICONES = {
  busca: svg('<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/>'),
  conta: svg('<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>'),
  coracao: svg('<path d="M12 20s-7.5-4.6-9-9.3C2 7.4 4.2 4.5 7.4 4.5c2 0 3.6 1.1 4.6 2.7 1-1.6 2.6-2.7 4.6-2.7 3.2 0 5.4 2.9 4.4 6.2C19.5 15.4 12 20 12 20Z"/>'),
  sacola: svg('<path d="M5 8h14l-1 13H6L5 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>'),
  menu: svg('<path d="M3 7h18M3 12h18M3 17h18"/>'),
  fechar: svg('<path d="M5 5l14 14M19 5 5 19"/>'),
  esquerda: svg('<path d="M15 5l-7 7 7 7"/>'),
  direita: svg('<path d="M9 5l7 7-7 7"/>'),
  filtro: svg('<path d="M4 6h16M7 12h10M10 18h4"/>'),
  grid2: svg('<rect x="4" y="4" width="7" height="16"/><rect x="13" y="4" width="7" height="16"/>'),
  grid3: svg('<rect x="3" y="4" width="4.5" height="16"/><rect x="9.75" y="4" width="4.5" height="16"/><rect x="16.5" y="4" width="4.5" height="16"/>'),
  grid4: svg('<rect x="3" y="4" width="3.5" height="16"/><rect x="8" y="4" width="3.5" height="16"/><rect x="13" y="4" width="3.5" height="16"/><rect x="18" y="4" width="3" height="16"/>'),
  instagram: svg('<rect x="3.5" y="3.5" width="17" height="17"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".6" fill="currentColor"/>'),
  tiktok: svg('<path d="M14 4v10.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 4c.5 2.5 2.3 4 5 4"/>'),
  youtube: svg('<rect x="3" y="6" width="18" height="12"/><path d="M10 9.5v5l4.5-2.5L10 9.5Z" fill="currentColor"/>'),
};

/* ---------- LOGO: monograma "B" geométrico + wordmark ---------- */
export const LOGO_MONOGRAMA = `
<svg viewBox="0 0 100 76" fill="currentColor" aria-hidden="true">
  <path d="M0 0H82L96 14V27L88 35L98 45V61L83 76H0V40H15V62H76L83 55V49L77 44H30V32H74L81 25V19L75 14H0Z"/>
</svg>`;

export const logo = (classe = '') => `
<a href="index.html" class="logo ${classe}" aria-label="BRAVO Menswear, página inicial">
  ${LOGO_MONOGRAMA}
  <span class="logo-texto">BRAVO</span>
</a>`;

/* ---------- DADOS DO MENU (edite aqui) ---------- */
const MENU = [
  { rotulo: 'New', href: 'categoria.html?c=new' },
  { rotulo: 'Coleções', href: 'categoria.html?c=colecoes', mega: 'colecoes' },
  { rotulo: 'Roupas', href: 'categoria.html', mega: 'roupas' },
  { rotulo: 'Alfaiataria', href: 'categoria.html?c=alfaiataria', mega: 'roupas' },
  { rotulo: 'Jeans', href: 'categoria.html?c=jeans' },
  { rotulo: 'Best Sellers', href: 'categoria.html?c=best' },
  { rotulo: 'Guia de Estilo', href: '#' },
  { rotulo: 'Black Sale', href: 'categoria.html?c=sale', mega: 'sale', classe: 'destaque-sale' },
];

const MEGAS = {
  roupas: `
    <div><h3>Roupas</h3><ul>
      <li><a href="categoria.html?c=blazers">Blazers</a></li>
      <li><a href="categoria.html?c=camisas">Camisas</a></li>
      <li><a href="categoria.html?c=polos">Polos</a></li>
      <li><a href="categoria.html?c=camisetas">Camisetas</a></li>
      <li><a href="categoria.html?c=trico">Tricô</a></li>
      <li><a href="categoria.html?c=jaquetas">Jaquetas e Casacos</a></li>
      <li><a href="categoria.html?c=calcas">Calças</a></li>
      <li><a href="categoria.html?c=jeans">Jeans</a></li>
    </ul></div>
    <div><h3>Calçados</h3><ul>
      <li><a href="categoria.html?c=tenis">Tênis</a></li>
      <li><a href="categoria.html?c=mocassins">Mocassins</a></li>
    </ul>
    <h3 style="margin-top:28px">Acessórios</h3><ul>
      <li><a href="categoria.html?c=cintos">Cintos</a></li>
      <li><a href="categoria.html?c=bolsas">Bolsas</a></li>
    </ul></div>
    <div><h3>Compre por tamanho</h3><ul class="mega-chips">
      ${['PP', 'P', 'M', 'G', 'GG', 'XGG'].map((t) => `<li><a href="categoria.html?tamanho=${t}">${t}</a></li>`).join('')}
    </ul></div>
    <a href="categoria.html?c=alfaiataria" class="mega-imagem">
      <img src="assets/img/editorial-alfaiataria.jpg" alt="Homem de terno escuro em ambiente de concreto" loading="lazy">
      <span class="eyebrow">A nova alfaiataria</span>
    </a>`,
  colecoes: `
    <div><h3>Coleções</h3><ul>
      <li><a href="#">Inverno 26 · Concreto</a></li>
      <li><a href="#">Essenciais Pretos</a></li>
      <li><a href="#">Couro & Lã</a></li>
      <li><a href="#">Linha Noite</a></li>
    </ul></div>
    <div></div><div></div>
    <a href="#" class="mega-imagem">
      <img src="assets/img/hero-1-campanha-sobretudo.jpg" alt="Campanha de inverno com sobretudo de lã" loading="lazy">
      <span class="eyebrow">Inverno 26</span>
    </a>`,
  sale: `
    <div><h3>Compre por preço</h3><ul>
      <li><a href="categoria.html?c=sale&max=199">Até R$ 199</a></li>
      <li><a href="categoria.html?c=sale&max=299">Até R$ 299</a></li>
      <li><a href="categoria.html?c=sale&max=399">Até R$ 399</a></li>
      <li><a href="categoria.html?c=sale&max=499">Até R$ 499</a></li>
    </ul></div>
    <div><h3>Descontos</h3><ul>
      <li><a href="categoria.html?c=sale&off=40">40% OFF</a></li>
      <li><a href="categoria.html?c=sale&off=50">50% OFF</a></li>
      <li><a href="categoria.html?c=sale&off=60">60% OFF</a></li>
    </ul></div>
    <div><h3>Compre por tamanho</h3><ul class="mega-chips">
      ${['PP', 'P', 'M', 'G', 'GG', 'XGG'].map((t) => `<li><a href="categoria.html?c=sale&tamanho=${t}">${t}</a></li>`).join('')}
    </ul></div>
    <a href="categoria.html?c=sale" class="mega-imagem">
      <img src="assets/img/hero-3-campanha-couro.jpg" alt="Jaqueta de couro preta em campanha" loading="lazy">
      <span class="eyebrow">Black Sale · até 60% off</span>
    </a>`,
};

/* ---------- TEMPLATES ---------- */
const anuncioHTML = () => `
<div class="anuncio" role="region" aria-label="Avisos" data-anuncio>
  <p class="anuncio-item ativo">EM ATÉ 6X SEM JUROS</p>
  <p class="anuncio-item">FRETE GRÁTIS ACIMA DE R$ 499</p>
  <p class="anuncio-item">PRIMEIRA COMPRA: 10% OFF COM BRAVO10</p>
  <a href="#" class="anuncio-atendimento">ATENDIMENTO</a>
</div>`;

const headerHTML = (transparente) => `
<header class="header ${transparente ? 'transparente' : ''}" id="header" data-header>
  <div class="container header-inner">
    <button class="icone-btn btn-hamburguer" aria-label="Abrir menu" aria-expanded="false" aria-controls="drawer-menu" data-abrir="menu">${ICONES.menu}</button>

    <!-- Menu desktop -->
    <nav class="nav-principal" aria-label="Principal">
      ${MENU.map((item, i) => `
        <div class="nav-item" data-nav-item>
          <a href="${item.href}" class="nav-link ${item.classe || ''}" ${item.mega ? `aria-haspopup="true" aria-expanded="false" aria-controls="mega-${i}"` : ''}>${item.rotulo}</a>
          ${item.mega ? `<div class="mega" id="mega-${i}"><div class="mega-inner">${MEGAS[item.mega]}</div></div>` : ''}
        </div>`).join('')}
    </nav>

    <div class="header-logo">${logo()}</div>

    <div class="header-acoes">
      <button class="icone-btn" aria-label="Buscar" data-abrir="busca">${ICONES.busca}</button>
      <a href="#" class="icone-btn so-desktop" aria-label="Minha conta">${ICONES.conta}</a>
      <a href="#" class="icone-btn so-desktop" aria-label="Favoritos" data-wishlist-link>${ICONES.coracao}</a>
      <button class="icone-btn" aria-label="Sacola" aria-expanded="false" aria-controls="drawer-sacola" data-abrir="sacola">
        ${ICONES.sacola}
        <span class="contador"><span data-cart-count>0</span></span>
      </button>
    </div>
  </div>
</header>`;

const footerHTML = () => `
<footer class="footer">
  <div class="container">
    <div class="footer-topo">
      <div class="footer-marca">
        ${logo('logo-grande')}
        <p>Moda masculina com corte preciso, matéria-prima nobre e nenhuma concessão.</p>
        <div class="footer-linha social">
          <a href="#" aria-label="Instagram">${ICONES.instagram}</a>
          <a href="#" aria-label="TikTok">${ICONES.tiktok}</a>
          <a href="#" aria-label="YouTube">${ICONES.youtube}</a>
        </div>
      </div>
      <div><h4>Institucional</h4><ul>
        <li><a href="#">Sobre a BRAVO</a></li><li><a href="#">Nossas lojas</a></li>
        <li><a href="#">Trabalhe conosco</a></li><li><a href="#">Sustentabilidade</a></li></ul></div>
      <div><h4>Ajuda</h4><ul>
        <li><a href="#">Trocas e devoluções</a></li><li><a href="#">Prazos de entrega</a></li>
        <li><a href="#">Guia de medidas</a></li><li><a href="#">Perguntas frequentes</a></li></ul></div>
      <div><h4>Minha conta</h4><ul>
        <li><a href="#">Entrar / Cadastrar</a></li><li><a href="#">Meus pedidos</a></li>
        <li><a href="#">Favoritos</a></li><li><a href="#">Endereços</a></li></ul></div>
      <!-- PENDENTE: WhatsApp, e-mail e horário reais da marca -->
      <div><h4>Atendimento</h4><ul>
        <li><a href="#" data-pendente="whatsapp">WhatsApp</a></li><li><a href="#" data-pendente="email">E-mail</a></li>
        <li><a href="#">Central de ajuda</a></li></ul></div>
    </div>

    <div class="footer-meio">
      <div><h4>Formas de pagamento</h4>
        <div class="footer-linha">
          ${['VISA', 'MASTER', 'ELO', 'AMEX', 'PIX', 'BOLETO'].map((p) => `<span class="pagamento">${p}</span>`).join('')}
        </div></div>
      <div><h4>Segurança</h4>
        <div class="footer-linha">
          <span class="pagamento">SITE SEGURO SSL</span><span class="pagamento">COMPRA PROTEGIDA</span>
        </div></div>
      <div class="footer-embalagens">
        <img src="assets/img/embalagem-etiqueta.jpg" alt="Sacola e etiqueta pretas com logo BRAVO prata" loading="lazy">
      </div>
    </div>

    <div class="footer-base">
      <!-- PENDENTE: razão social, CNPJ e endereço reais -->
      <span>© ${new Date().getFullYear()} BRAVO Menswear</span>
      <span>Marca em desenvolvimento. Imagens geradas por IA.</span>
    </div>
  </div>
</footer>`;

const globaisHTML = () => `
<div class="overlay" data-overlay></div>

<!-- ===== DRAWER SACOLA ===== -->
<aside class="drawer drawer-direita" id="drawer-sacola" aria-label="Sacola de compras" data-drawer="sacola">
  <div class="drawer-topo">
    <h2 class="eyebrow">Sacola (<span data-cart-count>0</span>)</h2>
    <button class="icone-btn" aria-label="Fechar sacola" data-fechar>${ICONES.fechar}</button>
  </div>
  <div class="drawer-corpo" data-cart-items>
    <!-- cart.js renderiza os itens aqui -->
    <div class="sacola-vazia">
      <p>Sua sacola está vazia.</p>
      <a href="categoria.html" class="btn btn-escuro">Continuar comprando</a>
    </div>
  </div>
  <div class="drawer-rodape">
    <div class="linha-total eyebrow"><span>Subtotal</span><span class="preco" data-cart-subtotal>R$ 0,00</span></div>
    <button class="btn btn-escuro btn-bloco" data-checkout>Finalizar compra</button>
  </div>
</aside>

<!-- ===== DRAWER MENU MOBILE ===== -->
<aside class="drawer drawer-esquerda" id="drawer-menu" aria-label="Menu" data-drawer="menu">
  <div class="drawer-topo">
    ${logo()}
    <button class="icone-btn" aria-label="Fechar menu" data-fechar>${ICONES.fechar}</button>
  </div>
  <nav class="drawer-corpo menu-mobile" aria-label="Menu mobile">
    ${MENU.map((item) => item.mega
      ? `<details><summary>${item.rotulo}<span aria-hidden="true">+</span></summary><ul>
           <li><a href="${item.href}">Ver tudo</a></li>
           ${[...MEGAS[item.mega].matchAll(/<li><a href="([^"]+)">([^<]+)<\/a><\/li>/g)].map((m) => `<li><a href="${m[1]}">${m[2]}</a></li>`).join('')}
         </ul></details>`
      : `<a href="${item.href}">${item.rotulo}</a>`).join('')}
    <a href="#">Minha conta</a>
    <a href="#">Favoritos</a>
    <a href="#">Atendimento</a>
  </nav>
</aside>

<!-- ===== BUSCA TELA CHEIA ===== -->
<div class="busca" id="busca" role="dialog" aria-modal="true" aria-label="Buscar produtos" data-drawer="busca">
  <div class="busca-topo">
    ${logo()}
    <button class="icone-btn" aria-label="Fechar busca" data-fechar>${ICONES.fechar}</button>
  </div>
  <form class="busca-campo" role="search" data-search-form>
    ${ICONES.busca}
    <label for="busca-input" class="sr-only">O que você procura?</label>
    <input id="busca-input" type="search" placeholder="O que você procura?" autocomplete="off" data-search-input>
  </form>
  <div class="busca-sugestoes">
    ${['Blazer', 'Sobretudo', 'Camisa oxford', 'Tricô', 'Couro', 'Jeans'].map((s) => `<button class="chip" data-search-chip>${s}</button>`).join('')}
  </div>
  <div class="busca-resultados grid-produtos" data-colunas="4" data-search-results>
    <!-- search.js renderiza os resultados aqui -->
  </div>
</div>`;

/* ---------- INJEÇÃO ---------- */
export function montarLayout() {
  const transparente = document.body.dataset.header === 'transparente';
  const partes = {
    anuncio: anuncioHTML,
    header: () => headerHTML(transparente),
    footer: footerHTML,
    globais: globaisHTML,
  };
  document.querySelectorAll('[data-include]').forEach((alvo) => {
    const fn = partes[alvo.dataset.include];
    if (fn) alvo.outerHTML = fn();
  });
}
