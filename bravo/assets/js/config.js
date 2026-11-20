/* =========================================================
   config.js · dados da loja num lugar só.
   ========================================================= */

/* WhatsApp de vendas (DDI + DDD + número, só dígitos) */
export const WHATSAPP = '556291545748';

/* Monta o link do WhatsApp já com a mensagem escrita */
export const waLink = (texto = 'Olá! Vim pelo site da BRAVO.') =>
  `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(texto)}`;
