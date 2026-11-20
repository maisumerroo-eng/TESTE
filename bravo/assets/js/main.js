/* =========================================================
   main.js · ponto de entrada de TODAS as páginas.
   Interface pronta: anúncio, header, mega-menu, drawers,
   slider, carrosséis, galeria e seletores da PDP.
   Lógica de negócio (sacola, favoritos, busca, filtros)
   fica nos arquivos de esqueleto com // TODO: para você codar.
   ========================================================= */
import { montarLayout } from './layout.js';
import { PRODUCTS, getProduct, porModelo } from './products.js';
import { waLink } from './config.js';
import { renderLista, renderPDP, ativarFallbackImagens } from './render.js';
import { initCart, addToCart } from './cart.js';
import { initWishlist, toggleWishlist } from './wishlist.js';
import { initSearch } from './search.js';
import { initFilters } from './filters.js';
import { initCheckout } from './checkout.js';

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
  const header = $('#header');
  if (!header?.classList.contains('transparente')) return;
  const anuncio = document.querySelector('[data-anuncio]');
  const atualizar = () => {
    // Header acompanha a barra de anúncio subindo, sem deixar vão nem sobrepor
    const altura = anuncio ? anuncio.offsetHeight : 0;
    header.style.top = Math.max(0, altura - scrollY) + 'px';
    // Vidro só depois que a hero saiu da tela
    const hero = document.querySelector('[data-hero]');
    const limite = hero ? hero.offsetTop + hero.offsetHeight - header.offsetHeight : altura;
    header.classList.toggle('solido', scrollY > limite);
  };
  addEventListener('scroll', atualizar, { passive: true });
  atualizar();
}

/* ---------- 3. MEGA-MENU (hover + teclado) ---------- */
function initMegaMenu() {
  const header = $('#header');
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

/* ---------- 5. HERO (troca sozinha, sem setas nem bolinhas) ---------- */
function initHero() {
  const hero = $('[data-hero]');
  if (!hero) return;
  const slides = $$('.slide', hero);
  if (slides.length < 2) return;
  let atual = 0;
  setInterval(() => {
    // Aba escondida: não troca (economiza bateria e evita "pulo" ao voltar)
    if (document.hidden) return;
    slides[atual].classList.remove('ativo');
    atual = (atual + 1) % slides.length;
    slides[atual].classList.add('ativo');
  }, 5500);
}

/* ---------- 6. VITRINES (andam sozinhas, sem setas) ----------
   Avança 1 card a cada 3,5s e volta ao início no fim.
   Pausa enquanto a pessoa está com o mouse/dedo na vitrine. */
function initCarrosseis() {
  $$('[data-carrossel]').forEach((wrap) => {
    const trilho = $('.carrossel-trilho', wrap);
    if (!trilho) return;
    let pausado = false;
    ['mouseenter', 'touchstart', 'focusin'].forEach((ev) => wrap.addEventListener(ev, () => (pausado = true), { passive: true }));
    ['mouseleave', 'touchend', 'focusout'].forEach((ev) => wrap.addEventListener(ev, () => (pausado = false), { passive: true }));
    setInterval(() => {
      if (pausado || document.hidden || trilho.scrollWidth <= trilho.clientWidth) return;
      const card = trilho.firstElementChild;
      const passo = card ? card.getBoundingClientRect().width + parseFloat(getComputedStyle(trilho).columnGap || 0) : trilho.clientWidth;
      const fim = trilho.scrollLeft + trilho.clientWidth >= trilho.scrollWidth - 4;
      trilho.scrollTo({ left: fim ? 0 : trilho.scrollLeft + passo, behavior: reduzMovimento ? 'auto' : 'smooth' });
    }, 3500);
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
  renderLista($('[data-shelf="lancamentos"]'), PRODUCTS);
  renderLista($('[data-shelf="mais-vendidos"]'), porModelo('ondas'));

  // Shop the look: lista as cores do modelo
  $$('[data-look-lista]').forEach((lista) => {
    lista.innerHTML = porModelo(lista.dataset.lookLista).map((p) => `
      <a href="produto.html?id=${p.id}" class="look-item" data-look-item="${p.id}">
        <img src="${p.imagens[0]}" data-alt="${p.imagens[1]}" alt="" loading="lazy">
        <div><p class="card-nome">${p.nome}</p><p class="card-parcela">Tamanhos ${p.tamanhos.join(' · ')}</p></div>
      </a>`).join('');
  });

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

  // Filtro inicial vindo do menu (?modelo= / ?cor= / ?tamanho=).
  // Os checkboxes da sidebar são TODO seu em filters.js.
  const url = new URLSearchParams(location.search);
  const modelo = url.get('modelo');
  const cor = url.get('cor');
  const tamanho = url.get('tamanho');
  let inicial = PRODUCTS;
  if (modelo) inicial = inicial.filter((p) => p.modelo === modelo);
  if (cor) inicial = inicial.filter((p) => p.cor.nome === cor);
  if (tamanho) inicial = inicial.filter((p) => p.tamanhos.includes(tamanho));
  if (modelo) $('[data-cat-titulo]').textContent = `Conjunto ${modelo}`;
  else if (cor) $('[data-cat-titulo]').textContent = `Conjuntos ${cor}`;

  // Render inicial (filters.js deve chamar este callback com a lista filtrada)
  const pintar = (lista) => {
    renderLista(grid, lista);
    $$('[data-total]').forEach((el) => (el.textContent = lista.length));
  };
  pintar(inicial);
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

  // Seleção de tamanho: atualiza botão da sacola e mensagem do WhatsApp
  const raiz = $('[data-pdp]');
  const botaoAdd = $('[data-add-to-cart]', raiz);
  const wa = $('[data-whatsapp-produto]', raiz);
  raiz.addEventListener('click', (e) => {
    // Troca de ângulo na galeria (Frente / Costas / Peça)
    const ang = e.target.closest('[data-angulo]');
    if (ang) {
      const i = Number(ang.dataset.angulo);
      $$('[data-angulo]', raiz).forEach((b) => b.setAttribute('aria-pressed', String(b === ang)));
      $$('.pdp-visor img', raiz).forEach((img, n) => img.classList.toggle('ativa', n === i));
      return;
    }
    const tam = e.target.closest('.tamanho');
    if (!tam) return;
    $$('.tamanho', raiz).forEach((b) => b.setAttribute('aria-pressed', String(b === tam)));
    botaoAdd.dataset.size = tam.dataset.size;
    wa.href = waLink(`Olá! Quero o ${p.nome}, tamanho ${tam.dataset.size}.`);
    $('[data-pdp-aviso]', raiz).hidden = true;
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

  renderLista($('[data-shelf="complete-look"]'), porModelo(p.modelo).filter((x) => x.id !== p.id).slice(0, 4));
  renderLista($('[data-shelf="relacionados"]'), PRODUCTS.filter((x) => x.modelo !== p.modelo));
}

/* Links genéricos de WhatsApp na página */
function initWhatsapp() {
  $$('[data-whatsapp]').forEach((a) => (a.href = waLink()));
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
initWhatsapp();
paginaHome();
paginaCategoria();
paginaProduto();
initCarrosseis();
initCart();
initWishlist();
initCheckout();
initSearch(PRODUCTS);
