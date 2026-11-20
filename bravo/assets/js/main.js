/* =========================================================
   main.js · ponto de entrada de TODAS as páginas.
   Interface pronta: anúncio, header, mega-menu, drawers,
   slider, carrosséis, galeria e seletores da PDP.
   Lógica de negócio (sacola, favoritos, busca, filtros)
   fica nos arquivos de esqueleto com // TODO: para você codar.
   ========================================================= */
import { montarLayout } from './layout.js';
import { PRODUCTS, getProduct } from './products.js';
import { renderLista, renderPDP, ativarFallbackImagens } from './render.js';
import { initCart, addToCart } from './cart.js';
import { initWishlist, toggleWishlist } from './wishlist.js';
import { initSearch } from './search.js';
import { initFilters } from './filters.js';

const $ = (sel, raiz = document) => raiz.querySelector(sel);
const $$ = (sel, raiz = document) => [...raiz.querySelectorAll(sel)];
const reduzMovimento = matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- 1. BARRA DE ANÚNCIO (rotação) ---------- */
function initAnuncio() {
  const itens = $$('[data-anuncio] .anuncio-item');
  if (itens.length < 2 || reduzMovimento) return;
  let i = 0;
  setInterval(() => {
    itens[i].classList.remove('ativo');
    i = (i + 1) % itens.length;
    itens[i].classList.add('ativo');
  }, 4000);
}

/* ---------- 2. HEADER (sólido ao rolar) ---------- */
function initHeader() {
  const header = $('[data-header]');
  if (!header?.classList.contains('transparente')) return;
  const atualizar = () => header.classList.toggle('solido', scrollY > 40);
  addEventListener('scroll', atualizar, { passive: true });
  atualizar();
}

/* ---------- 3. MEGA-MENU (hover + teclado) ---------- */
function initMegaMenu() {
  const header = $('[data-header]');
  $$('[data-nav-item]').forEach((item) => {
    const link = $('.nav-link', item);
    if (!$('.mega', item)) return;
    const abrir = (sim) => {
      item.classList.toggle('aberto', sim);
      link.setAttribute('aria-expanded', String(sim));
      header.classList.toggle('menu-aberto', sim);
    };
    item.addEventListener('mouseenter', () => abrir(true));
    item.addEventListener('mouseleave', () => abrir(false));
    item.addEventListener('focusin', () => abrir(true));
    item.addEventListener('focusout', (e) => { if (!item.contains(e.relatedTarget)) abrir(false); });
  });
}

/* ---------- 4. DRAWERS (sacola, menu mobile, busca) ---------- */
let ultimoFoco = null;

export function abrirDrawer(nome) {
  const drawer = $(`[data-drawer="${nome}"]`);
  if (!drawer) return;
  ultimoFoco = document.activeElement;
  drawer.classList.add('aberto');
  $('[data-overlay]').classList.add('visivel');
  document.body.classList.add('trava-scroll');
  $$(`[data-abrir="${nome}"]`).forEach((b) => b.setAttribute('aria-expanded', 'true'));
  // foca o primeiro campo/botão do drawer
  setTimeout(() => (drawer.querySelector('input, button, a') || drawer).focus(), 50);
}

export function fecharDrawers() {
  $$('[data-drawer].aberto').forEach((d) => d.classList.remove('aberto'));
  $('[data-overlay]')?.classList.remove('visivel');
  document.body.classList.remove('trava-scroll');
  $$('[data-abrir]').forEach((b) => b.setAttribute('aria-expanded', 'false'));
  ultimoFoco?.focus();
}

function initDrawers() {
  document.addEventListener('click', (e) => {
    const abrir = e.target.closest('[data-abrir]');
    if (abrir) return abrirDrawer(abrir.dataset.abrir);
    if (e.target.closest('[data-fechar]') || e.target.matches('[data-overlay]')) fecharDrawers();
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') fecharDrawers(); });
}

/* ---------- 5. HERO SLIDER ---------- */
function initHero() {
  const hero = $('[data-hero]');
  if (!hero) return;
  const slides = $$('.slide', hero);
  const bullets = $$('.hero-bullet', hero);
  let atual = 0;
  let timer;

  const ir = (n) => {
    slides[atual].classList.remove('ativo');
    bullets[atual]?.classList.remove('ativo');
    bullets[atual]?.setAttribute('aria-current', 'false');
    atual = (n + slides.length) % slides.length;
    slides[atual].classList.add('ativo');
    bullets[atual]?.classList.add('ativo');
    bullets[atual]?.setAttribute('aria-current', 'true');
  };
  const auto = () => {
    if (reduzMovimento) return;
    clearInterval(timer);
    timer = setInterval(() => ir(atual + 1), 6000);
  };

  $('[data-hero-prev]', hero)?.addEventListener('click', () => { ir(atual - 1); auto(); });
  $('[data-hero-next]', hero)?.addEventListener('click', () => { ir(atual + 1); auto(); });
  bullets.forEach((b, i) => b.addEventListener('click', () => { ir(i); auto(); }));
  hero.addEventListener('mouseenter', () => clearInterval(timer));
  hero.addEventListener('mouseleave', auto);
  auto();
}

/* ---------- 6. CARROSSÉIS (setas) ---------- */
function initCarrosseis() {
  $$('[data-carrossel]').forEach((wrap) => {
    const trilho = $('.carrossel-trilho', wrap);
    const passo = () => trilho.clientWidth * 0.8;
    $('[data-prev]', wrap)?.addEventListener('click', () => trilho.scrollBy({ left: -passo(), behavior: 'smooth' }));
    $('[data-next]', wrap)?.addEventListener('click', () => trilho.scrollBy({ left: passo(), behavior: 'smooth' }));
  });
}

/* ---------- 7. AÇÕES GLOBAIS (delegação de clique) ---------- */
function initAcoes() {
  document.addEventListener('click', (e) => {
    // Compra rápida no card (data-add-to-cart + data-size no mesmo botão)
    const add = e.target.closest('[data-add-to-cart]');
    if (add && add.dataset.size) {
      addToCart(add.dataset.addToCart, add.dataset.size);
      return;
    }
    const fav = e.target.closest('[data-wishlist-toggle]');
    if (fav) {
      const ativo = fav.getAttribute('aria-pressed') !== 'true';
      fav.setAttribute('aria-pressed', String(ativo));
      toggleWishlist(fav.dataset.wishlistToggle);
    }
  });

  // Newsletter (só evita reload · envio real é TODO)
  $$('[data-newsletter]').forEach((form) => form.addEventListener('submit', (e) => {
    e.preventDefault();
    // TODO: enviar e-mail para sua API / serviço de newsletter.
    form.innerHTML = '<p class="eyebrow">Obrigado. Você está na lista.</p>';
  }));
}

/* ---------- 8. PÁGINAS ---------- */
function paginaHome() {
  renderLista($('[data-shelf="lancamentos"]'), PRODUCTS.filter((p) => p.selo === 'NEW'));
  renderLista($('[data-shelf="mais-vendidos"]'), PRODUCTS.filter((p) => p.bestSeller));

  // Shop the look: destaca o item ao passar no hotspot
  $$('[data-hotspot]').forEach((h) => {
    const item = $(`[data-look-item="${h.dataset.hotspot}"]`);
    h.addEventListener('mouseenter', () => item?.classList.add('destaque'));
    h.addEventListener('mouseleave', () => item?.classList.remove('destaque'));
  });
}

function paginaCategoria() {
  const grid = $('[data-grid]');
  if (!grid) return;

  // Título a partir de ?c= na URL
  const c = new URLSearchParams(location.search).get('c');
  if (c) $('[data-cat-titulo]').textContent = c === 'sale' ? 'Black Sale' : c.replace(/-/g, ' ');

  // Render inicial (filters.js deve chamar este callback com a lista filtrada)
  const pintar = (lista) => {
    renderLista(grid, lista);
    $$('[data-total]').forEach((el) => (el.textContent = lista.length));
  };
  pintar(PRODUCTS);
  initFilters(PRODUCTS, pintar);

  // Toggle 2 / 3 / 4 colunas
  $$('[data-colunas-btn]').forEach((btn) => btn.addEventListener('click', () => {
    grid.dataset.colunas = btn.dataset.colunasBtn;
    $$('[data-colunas-btn]').forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
  }));
}

function paginaProduto() {
  if (!$('[data-pdp]')) return;
  const id = new URLSearchParams(location.search).get('id') || PRODUCTS[0].id;
  const p = getProduct(id) || PRODUCTS[0];
  renderPDP(p);

  // Seleção de cor e tamanho (só visual; o valor fica em data-*)
  const raiz = $('[data-pdp]');
  const botaoAdd = $('[data-add-to-cart]', raiz);
  raiz.addEventListener('click', (e) => {
    const cor = e.target.closest('.cor-opcao');
    if (cor) {
      $$('.cor-opcao', raiz).forEach((b) => b.setAttribute('aria-pressed', String(b === cor)));
      $('[data-pdp-cor-nome]', raiz).textContent = cor.dataset.color;
    }
    const tam = e.target.closest('.tamanho');
    if (tam) {
      $$('.tamanho', raiz).forEach((b) => b.setAttribute('aria-pressed', String(b === tam)));
      botaoAdd.dataset.size = tam.dataset.size;
    }
  });
  // Botão principal sem tamanho escolhido → avisa
  botaoAdd.addEventListener('click', () => {
    if (!botaoAdd.dataset.size) $('[data-pdp-aviso]', raiz).hidden = false;
  });

  // Calcular frete (TODO: integrar API de frete)
  $('[data-frete]', raiz)?.addEventListener('submit', (e) => {
    e.preventDefault();
    // TODO: consultar CEP (ex.: ViaCEP) e calcular frete na sua API.
    $('[data-frete-resultado]', raiz).textContent = 'TODO: resultado do frete aparece aqui.';
  });

  const relacionados = PRODUCTS.filter((x) => x.id !== p.id);
  renderLista($('[data-shelf="complete-look"]'), relacionados.filter((x) => x.categoria !== p.categoria).slice(0, 4));
  renderLista($('[data-shelf="relacionados"]'), relacionados.filter((x) => x.subcategoria === p.subcategoria).concat(relacionados).slice(0, 8));
}

/* ---------- START ---------- */
montarLayout();
ativarFallbackImagens();
initAnuncio();
initHeader();
initMegaMenu();
initDrawers();
initHero();
initAcoes();
paginaHome();
paginaCategoria();
paginaProduto();
initCarrosseis();
initCart();
initWishlist();
initSearch(PRODUCTS);
