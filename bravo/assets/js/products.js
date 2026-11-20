/* =========================================================
   products.js · catálogo REAL da BRAVO (3 modelos de conjunto).
   Cada cor é um produto (como na Zara/John John).
   Imagens: produto-<slug>-1.jpg (modelo frente), -2.jpg (só a peça), -3.jpg (modelo costas).
   preco: null → card mostra "Consulte o preço" e o botão vai pro WhatsApp.
   PENDENTE: preços reais e composição dos modelos Jacquard e Canelado.
   ========================================================= */

const COR = {
  branco: { nome: 'Branco', hex: '#F4F2EE' },
  offwhite: { nome: 'Off-white', hex: '#EAE4D8' },
  bege: { nome: 'Bege', hex: '#CDBA9C' },
  khaki: { nome: 'Khaki', hex: '#8A8170' },
  cinza: { nome: 'Cinza', hex: '#9A9A9A' },
  preto: { nome: 'Preto', hex: '#151515' },
  verdeMilitar: { nome: 'Verde militar', hex: '#5A6440' },
  verdePetroleo: { nome: 'Verde petróleo', hex: '#3F7A78' },
};

const TAMANHOS = ['P', 'M', 'G', 'GG'];

/* Os 3 modelos. Textos só com o que dá para ver nas peças. */
const MODELOS = {
  ondas: {
    nome: 'Conjunto Ondas',
    subcategoria: 'Camisa + Bermuda',
    tecido: 'Texturizado',
    codigo: 'KA-711',
    descricao: 'Camisa de gola cubana e manga curta com bermuda de cós elástico e cordão. Tecido com relevo de ondas, leve e com caimento solto. Botões e cordão na cor da peça, bolsos laterais e bolso traseiro com botão.',
    composicao: '100% poliéster.',
    cores: ['branco', 'khaki', 'preto', 'verdeMilitar', 'bege', 'cinza'],
  },
  jacquard: {
    nome: 'Conjunto Jacquard',
    subcategoria: 'Camisa + Bermuda',
    tecido: 'Jacquard',
    codigo: null,
    descricao: 'Camisa de colarinho com botões e bermuda de cós elástico com cordão. Jacquard com relevo de losangos que aparece de longe e dá corpo à peça.',
    composicao: null,
    cores: ['offwhite', 'bege', 'cinza', 'preto'],
  },
  canelado: {
    nome: 'Conjunto Canelado',
    subcategoria: 'Camiseta + Bermuda',
    tecido: 'Canelado',
    codigo: null,
    descricao: 'Camiseta de gola careca e bermuda com cordão e ponteiras metálicas. Malha canelada com textura de grade, fresca e de toque macio.',
    composicao: null,
    cores: ['preto', 'verdePetroleo'],
  },
};

const slugCor = (chave) => chave.replace(/[A-Z]/g, (l) => '-' + l.toLowerCase());

export const PRODUCTS = Object.entries(MODELOS).flatMap(([modelo, m], iModelo) =>
  m.cores.map((chaveCor, iCor) => {
    const cor = COR[chaveCor];
    const slug = `${modelo}-${slugCor(chaveCor)}`;
    return {
      id: `bv-${slug}`,
      slug,
      modelo,
      nome: `${m.nome} ${cor.nome}`,
      categoria: 'conjuntos',
      subcategoria: m.subcategoria,
      tecido: m.tecido,
      codigo: m.codigo,
      preco: null,            // PENDENTE: preço real (número, ex.: 189.9)
      precoOriginal: null,
      selo: null,
      cor,
      // todas as cores do mesmo modelo (bolinhas no card / seletor na PDP)
      cores: m.cores.map((c) => ({ ...COR[c], id: `bv-${modelo}-${slugCor(c)}` })),
      tamanhos: TAMANHOS,
      descricao: m.descricao,
      composicao: m.composicao,
      ordem: iModelo * 10 + iCor,
      // -1 modelo de frente · -2 só a peça (hover) · -3 modelo de costas
      imagens: [`assets/img/produto-${slug}-1.jpg`, `assets/img/produto-${slug}-2.jpg`, `assets/img/produto-${slug}-3.jpg`],
    };
  })
);

export const getProduct = (id) => PRODUCTS.find((p) => p.id === id);
export const porModelo = (modelo) => PRODUCTS.filter((p) => p.modelo === modelo);
