/* =========================================================
   admin.js · PAINEL BRAVO (ESQUELETO, tudo TODO)
   Ganchos prontos em admin.html:
     [data-tela="..."]       telas (login, dashboard, produtos, produto-form, pedidos, banners, config)
     [data-ir="tela"]        links/botões que trocam de tela
     [data-form="login|produto|config"]
     [data-tabela="produtos|pedidos"] + <template id="tpl-linha-produto">
     [data-lista="banners"]  + <template id="tpl-banner">
     [data-kpi="..."]        números do dashboard
     [data-toast]            aviso rápido
   Dados de partida: PRODUCTS em products.js. Backend: a definir
   (Supabase, Firebase ou API própria).
   ========================================================= */
// import { PRODUCTS } from './products.js';

/* Enquanto não houver login, mostra o app direto para testar o layout.
   TODO: remover estas 3 linhas quando o login existir. */
document.querySelector('[data-tela="login"]').hidden = true;
document.querySelector('[data-app]').hidden = false;

/* ---------- AUTENTICAÇÃO ---------- */
// TODO: submit de [data-form="login"] → autenticar → esconder login, mostrar [data-app].
// TODO: [data-sair] → logout e voltar ao login.

/* ---------- NAVEGAÇÃO ENTRE TELAS ---------- */
// TODO: ao clicar em [data-ir], trocar .ativa da tela, marcar .ativo no menu,
//       atualizar [data-titulo-tela] e location.hash. Ler o hash ao carregar.
// TODO: [data-adm-toggle] abre/fecha .adm-menu.aberto no celular (aria-expanded).

/* ---------- DASHBOARD ---------- */
// TODO: buscar números e preencher [data-kpi]. Sem dado → manter "—".

/* ---------- PRODUTOS ---------- */
// TODO: renderizar a tabela clonando #tpl-linha-produto para cada produto.
// TODO: busca [data-busca-produto] e filtro [data-filtro-modelo].
// TODO: [data-editar] → abrir produto-form preenchido. [data-novo-produto] → form vazio.
// TODO: [data-duplicar] → copiar produto (útil para nova cor do mesmo modelo).

/* ---------- FORMULÁRIO DE PRODUTO ---------- */
// TODO: validar nome, modelo e cor. Preço vazio = null ("consulte no WhatsApp").
// TODO: upload [data-upload-fotos]: prévia em [data-lista="fotos"], arrastar para ordenar.
// TODO: salvar → backend → toast "Produto salvo".
// TODO: [data-excluir-produto] → confirmação NA PÁGINA (confirm() pode não existir) → excluir.

/* ---------- PEDIDOS ---------- */
// TODO: listar pedidos, filtrar por [data-filtro-pedido].
// TODO: [data-novo-pedido] → registrar venda fechada no WhatsApp.

/* ---------- BANNERS ---------- */
// TODO: clonar #tpl-banner para os 3 slides, trocar imagem, salvar foco X/Y (vira --foco).

/* ---------- CONFIGURAÇÕES ---------- */
// TODO: carregar/salvar WhatsApp, anúncio e dados da empresa (hoje fixos em config.js e layout.js).

/* ---------- TOAST ---------- */
export function toast(texto) {
  // TODO: mostrar [data-toast] com o texto por ~3s.
}
