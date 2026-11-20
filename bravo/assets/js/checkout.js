/* =========================================================
   checkout.js · monta o pedido e envia pelo WhatsApp da loja.
   ========================================================= */
import { getItens, subtotal, limparSacola } from './cart.js';
import { brl } from './render.js';
import { waLink } from './config.js';

const $ = (s, r = document) => r.querySelector(s);

function renderResumo() {
  const lista = getItens();
  const caixa = $('[data-ck-itens]');
  if (!lista.length) {
    $('[data-checkout-conteudo]').innerHTML = `
      <div class="sacola-vazia" style="grid-column:1/-1">
        <p>Sua sacola está vazia.</p>
        <a href="categoria.html" class="btn btn-escuro">Ver os conjuntos</a>
      </div>`;
    return false;
  }
  caixa.innerHTML = lista.map(({ produto: p, size, qtd }) => `
    <article class="sacola-item" style="grid-template-columns:64px 1fr">
      <img src="${p.imagens[0]}" alt="">
      <div>
        <h3>${p.nome}</h3>
        <p>Tamanho ${size} · ${qtd} ${qtd > 1 ? 'unidades' : 'unidade'}</p>
        <p class="preco">${p.preco == null ? 'Preço a combinar' : brl(p.preco * qtd)}</p>
      </div>
    </article>`).join('');
  return true;
}

/* Busca o endereço pelo CEP (ViaCEP, gratuito) */
async function buscarCep(cep) {
  const so = cep.replace(/\D/g, '');
  if (so.length !== 8) return;
  try {
    const r = await fetch(`https://viacep.com.br/ws/${so}/json/`);
    const d = await r.json();
    if (d.erro) return;
    $('[data-rua]').value = d.logradouro || '';
    $('[data-bairro]').value = d.bairro || '';
    $('[data-cidade]').value = `${d.localidade} / ${d.uf}`;
    $('#ck-numero').focus();
  } catch { /* sem internet ou bloqueado: a pessoa digita */ }
}

function validar(form) {
  const erros = [];
  const marcar = (el, ok) => el.setAttribute('aria-invalid', String(!ok));
  const nome = form.nome.value.trim();
  const tel = form.telefone.value.replace(/\D/g, '');
  marcar(form.nome, nome.length > 2); if (nome.length <= 2) erros.push('nome');
  marcar(form.telefone, tel.length >= 10); if (tel.length < 10) erros.push('WhatsApp');
  if (form.entrega.value.startsWith('Enviar')) {
    ['cep', 'rua', 'numero', 'cidade'].forEach((c) => {
      const ok = form[c].value.trim().length > 0;
      marcar(form[c], ok); if (!ok) erros.push(c === 'rua' ? 'endereço' : c);
    });
  }
  return erros;
}

function montarMensagem(form) {
  const lista = getItens();
  const sub = subtotal();
  const linhas = [
    'Olá, BRAVO! Quero fazer este pedido:',
    '',
    ...lista.map(({ produto: p, size, qtd }) =>
      `• ${qtd}x ${p.nome} (tam. ${size})${p.preco == null ? '' : ` · ${brl(p.preco * qtd)}`}`),
    '',
    `Subtotal: ${sub == null ? 'a combinar' : brl(sub)}`,
    '',
    `Nome: ${form.nome.value.trim()}`,
    `WhatsApp: ${form.telefone.value.trim()}`,
    form.email.value.trim() ? `E-mail: ${form.email.value.trim()}` : null,
    `Entrega: ${form.entrega.value}`,
    !form.entrega.value.startsWith('Enviar') ? null :
      `Endereço: ${form.rua.value}, ${form.numero.value}${form.complemento.value ? ' - ' + form.complemento.value : ''}, ${form.bairro.value}, ${form.cidade.value}, CEP ${form.cep.value}`,
    `Pagamento: ${form.pagamento.value}`,
    form.obs.value.trim() ? `Obs.: ${form.obs.value.trim()}` : null,
  ];
  return linhas.filter((l) => l != null).join('\n');
}

export function initCheckout() {
  if (!$('[data-checkout-page]')) return;
  if (!renderResumo()) return;
  const form = $('[data-form="checkout"]');

  // Máscara simples de CEP + busca do endereço
  $('[data-cep]').addEventListener('input', (e) => {
    const v = e.target.value.replace(/\D/g, '').slice(0, 8);
    e.target.value = v.length > 5 ? `${v.slice(0, 5)}-${v.slice(5)}` : v;
    if (v.length === 8) buscarCep(v);
  });

  // Retirada esconde o endereço
  form.addEventListener('change', (e) => {
    if (e.target.name === 'entrega') $('[data-endereco]').hidden = e.target.dataset.entrega === 'retirada';
  });

  $('[data-ck-enviar]').addEventListener('click', () => {
    const erros = validar(form);
    const aviso = $('[data-ck-erro]');
    if (erros.length) {
      aviso.textContent = `Preencha: ${erros.join(', ')}.`;
      aviso.hidden = false;
      form.querySelector('[aria-invalid="true"]')?.focus();
      return;
    }
    aviso.hidden = true;
    const link = waLink(montarMensagem(form));
    window.open(link, '_blank', 'noopener');
    // Tela de sucesso (com botão para reabrir, caso o navegador bloqueie a janela)
    $('[data-ck-reabrir]').href = link;
    $('[data-checkout-conteudo]').hidden = true;
    $('[data-ck-sucesso]').hidden = false;
    scrollTo({ top: 0, behavior: 'smooth' });
    limparSacola();
  });
}
