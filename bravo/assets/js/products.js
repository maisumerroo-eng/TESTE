/* =========================================================
   products.js — catálogo fictício BRAVO.
   Para adicionar produto: copie um objeto e troque os dados.
   Imagens: assets/img/produto-<slug>-1.jpg (frente) e -2.jpg (hover).
   Se a imagem não existir, render.js usa a outra ou o placeholder.
   ========================================================= */

const img = (slug) => [`assets/img/produto-${slug}-1.jpg`, `assets/img/produto-${slug}-2.jpg`];

const CORES = {
  preto: { nome: 'Preto', hex: '#0B0B0B' },
  grafite: { nome: 'Grafite', hex: '#3A3A3A' },
  areia: { nome: 'Areia', hex: '#CDBFAE' },
  offwhite: { nome: 'Off-white', hex: '#EDE8E2' },
  marinho: { nome: 'Marinho', hex: '#1C2433' },
  caramelo: { nome: 'Caramelo', hex: '#8A5A36' },
  indigo: { nome: 'Índigo', hex: '#22304A' },
  oliva: { nome: 'Oliva', hex: '#4B4A36' },
};

const ROUPA = ['PP', 'P', 'M', 'G', 'GG', 'XGG'];
const CALCA = ['38', '40', '42', '44', '46', '48'];
const CALCADO = ['38', '39', '40', '41', '42', '43', '44'];

export const PRODUCTS = [
  { id: 'bv-001', slug: 'blazer-la', nome: 'Blazer de Lã Estruturado', categoria: 'blazers', subcategoria: 'Alfaiataria',
    preco: 1199, precoOriginal: null, selo: 'NEW', cores: [CORES.preto, CORES.grafite], tamanhos: ROUPA,
    material: 'Lã', modelagem: 'Slim', bestSeller: true,
    descricao: 'Blazer de abotoamento simples, ombro estruturado e lapela entalhada. Forro interno em viscose.',
    composicao: '80% lã, 20% poliamida. Forro: 100% viscose.' },
  { id: 'bv-002', slug: 'sobretudo-la', nome: 'Sobretudo Longo de Lã', categoria: 'jaquetas', subcategoria: 'Casacos',
    preco: 1499, precoOriginal: null, selo: 'NEW', cores: [CORES.preto, CORES.caramelo], tamanhos: ROUPA,
    material: 'Lã', modelagem: 'Regular', bestSeller: true,
    descricao: 'Sobretudo abaixo do joelho, gola larga e bolsos embutidos. Peça-chave do inverno.',
    composicao: '70% lã, 30% poliéster.' },
  { id: 'bv-003', slug: 'camisa-oxford', nome: 'Camisa Oxford Slim', categoria: 'camisas', subcategoria: 'Camisas',
    preco: 349, precoOriginal: null, selo: 'BEST SELLER', cores: [CORES.offwhite, CORES.marinho, CORES.preto], tamanhos: ROUPA,
    material: 'Algodão', modelagem: 'Slim', bestSeller: true,
    descricao: 'Camisa em tecido oxford encorpado, gola com botões e barra arredondada.',
    composicao: '100% algodão.' },
  { id: 'bv-004', slug: 'camisa-linho', nome: 'Camisa de Linho', categoria: 'camisas', subcategoria: 'Camisas',
    preco: 449, precoOriginal: 599, selo: 'BLACK SALE', cores: [CORES.areia, CORES.offwhite], tamanhos: ROUPA,
    material: 'Linho', modelagem: 'Regular', bestSeller: false,
    descricao: 'Linho lavado com toque macio, gola padre e caimento solto.',
    composicao: '100% linho.' },
  { id: 'bv-005', slug: 'polo-piquet', nome: 'Polo de Malha Piquet', categoria: 'polos', subcategoria: 'Polos',
    preco: 299, precoOriginal: null, selo: null, cores: [CORES.preto, CORES.offwhite, CORES.marinho], tamanhos: ROUPA,
    material: 'Algodão', modelagem: 'Regular', bestSeller: true,
    descricao: 'Polo em piquet de algodão com monograma B bordado no peito.',
    composicao: '100% algodão.' },
  { id: 'bv-006', slug: 'camiseta-heavyweight', nome: 'Camiseta Heavyweight Oversized', categoria: 'camisetas', subcategoria: 'Camisetas',
    preco: 199, precoOriginal: null, selo: 'NEW', cores: [CORES.preto, CORES.offwhite, CORES.grafite], tamanhos: ROUPA,
    material: 'Algodão', modelagem: 'Oversized', bestSeller: false,
    descricao: 'Malha 280 g/m², ombro caído e gola canelada firme.',
    composicao: '100% algodão.' },
  { id: 'bv-007', slug: 'trico-gola-alta', nome: 'Tricô Gola Alta Merino', categoria: 'trico', subcategoria: 'Tricô',
    preco: 599, precoOriginal: null, selo: 'NEW', cores: [CORES.preto, CORES.areia], tamanhos: ROUPA,
    material: 'Lã', modelagem: 'Slim', bestSeller: true,
    descricao: 'Tricô fino de lã merino, gola alta dobrável e punhos canelados.',
    composicao: '100% lã merino.' },
  { id: 'bv-008', slug: 'cardigan-texturizado', nome: 'Cardigan Texturizado', categoria: 'trico', subcategoria: 'Tricô',
    preco: 479, precoOriginal: 689, selo: 'BLACK SALE', cores: [CORES.grafite, CORES.oliva], tamanhos: ROUPA,
    material: 'Algodão', modelagem: 'Regular', bestSeller: false,
    descricao: 'Cardigan em ponto texturizado com botões de chifre.',
    composicao: '60% algodão, 40% acrílico.' },
  { id: 'bv-009', slug: 'calca-alfaiataria', nome: 'Calça de Alfaiataria com Pregas', categoria: 'calcas', subcategoria: 'Alfaiataria',
    preco: 549, precoOriginal: null, selo: null, cores: [CORES.preto, CORES.grafite, CORES.areia], tamanhos: CALCA,
    material: 'Lã', modelagem: 'Reta', bestSeller: true,
    descricao: 'Calça de cintura média com pregas frontais e barra italiana.',
    composicao: '65% poliéster, 35% lã.' },
  { id: 'bv-010', slug: 'calca-chino', nome: 'Calça Chino', categoria: 'calcas', subcategoria: 'Calças',
    preco: 329, precoOriginal: 469, selo: 'BLACK SALE', cores: [CORES.areia, CORES.preto, CORES.oliva], tamanhos: CALCA,
    material: 'Algodão', modelagem: 'Slim', bestSeller: false,
    descricao: 'Sarja de algodão com elastano, bolso faca e caimento afunilado.',
    composicao: '98% algodão, 2% elastano.' },
  { id: 'bv-011', slug: 'jeans-reto', nome: 'Jeans Reto Lavagem Escura', categoria: 'jeans', subcategoria: 'Jeans',
    preco: 429, precoOriginal: null, selo: 'NEW', cores: [CORES.indigo, CORES.preto], tamanhos: CALCA,
    material: 'Denim', modelagem: 'Reta', bestSeller: true,
    descricao: 'Denim rígido 13 oz, lavagem escura uniforme e cinco bolsos.',
    composicao: '100% algodão.' },
  { id: 'bv-012', slug: 'jaqueta-couro', nome: 'Jaqueta de Couro', categoria: 'jaquetas', subcategoria: 'Jaquetas',
    preco: 1399, precoOriginal: 1999, selo: 'BLACK SALE', cores: [CORES.preto], tamanhos: ROUPA,
    material: 'Couro', modelagem: 'Slim', bestSeller: true,
    descricao: 'Couro ovino legítimo, gola padre e zíper metálico escurecido.',
    composicao: '100% couro ovino. Forro: 100% poliéster.' },
  { id: 'bv-013', slug: 'bomber-tecnica', nome: 'Bomber Técnica', categoria: 'jaquetas', subcategoria: 'Jaquetas',
    preco: 799, precoOriginal: null, selo: null, cores: [CORES.preto, CORES.oliva], tamanhos: ROUPA,
    material: 'Sintético', modelagem: 'Regular', bestSeller: false,
    descricao: 'Bomber em nylon técnico repelente à água com punhos em ribana.',
    composicao: '100% poliamida.' },
  { id: 'bv-014', slug: 'tenis-couro', nome: 'Tênis de Couro Minimal', categoria: 'tenis', subcategoria: 'Calçados',
    preco: 699, precoOriginal: null, selo: 'NEW', cores: [CORES.offwhite, CORES.preto], tamanhos: CALCADO,
    material: 'Couro', modelagem: '—', bestSeller: true,
    descricao: 'Tênis em couro liso, sola de borracha costurada e palmilha acolchoada.',
    composicao: 'Cabedal 100% couro bovino. Sola: borracha.' },
  { id: 'bv-015', slug: 'mocassim-couro', nome: 'Mocassim de Couro', categoria: 'mocassins', subcategoria: 'Calçados',
    preco: 649, precoOriginal: 899, selo: 'BLACK SALE', cores: [CORES.preto, CORES.caramelo], tamanhos: CALCADO,
    material: 'Couro', modelagem: '—', bestSeller: false,
    descricao: 'Mocassim penny loafer em couro escovado com sola de couro.',
    composicao: '100% couro bovino.' },
  { id: 'bv-016', slug: 'cinto-couro', nome: 'Cinto de Couro', categoria: 'cintos', subcategoria: 'Acessórios',
    preco: 249, precoOriginal: null, selo: null, cores: [CORES.preto, CORES.caramelo], tamanhos: ['90', '95', '100', '105'],
    material: 'Couro', modelagem: '—', bestSeller: false,
    descricao: 'Cinto 3,5 cm em couro, fivela metálica escovada com monograma B.',
    composicao: '100% couro bovino.' },
].map((p) => ({ ...p, imagens: img(p.slug) }));

/* Busca rápida por id */
export const getProduct = (id) => PRODUCTS.find((p) => p.id === id);
