# Megapersonalização

Duas camadas. A primeira é obrigatória em todo site; a segunda entra quando há tráfego segmentado (anúncios, nichos múltiplos, regiões).

## Camada 1: site feito sob medida para o cliente (build time)

Extraia o **DNA do cliente** antes de escrever uma linha. Preencha `dna.md` na raiz do projeto:

```md
# DNA: [marca]
Negócio em 1 frase:
Nicho e subnichos:
Região de atuação:
Cliente ideal (cargo, porte, faturamento, dor principal):
Oferta de entrada (o "diagnóstico gratuito" deste cliente):
Vocabulário do nicho (10+ termos, siglas, leis, ferramentas):
Objeções que o comercial mais ouve (5):
Provas reais (números, casos, selos, anos, clientes que podem ser citados):
Metáfora do negócio → momento-assinatura:
Premissa da marca (1 palavra/ideia que o site inteiro vende):
Frases reais dos compradores (dor / desejo / objeção, com fonte):
Imagens: fotos reais / IA declarada / IA temporária até fotos reais:
Personalidade (3 pares "é / não é"): ex. sóbria / não fria
Cor de marca + neutros; fonte display + texto:
Canal de contato principal (WhatsApp nº, e-mail):
```

Fontes do DNA: briefing, site atual, Instagram, Google Business, conversas de WhatsApp que o cliente mostrar, concorrentes. Lacuna sem resposta: marcar `[A CONFIRMAR]` no texto, nunca inventar.

### Pesquisa da voz do comprador (antes de escrever)
Busca na web (WebSearch) em avaliações e conversas reais do nicho, priorizando fontes brasileiras: Google Maps do cliente e dos concorrentes, Reclame Aqui, iFood/marketplaces, grupos e fóruns do nicho. Um punhado de fontes basta. Coletar **frases exatas** recorrentes em três listas: dores, resultados desejados, objeções. Sem busca disponível: pedir ao usuário 5 avaliações reais ou as objeções que o comercial mais ouve. Uso: títulos de dor, perguntas do FAQ, objeções respondidas, variantes por segmento. Registrar as frases (com a fonte) no `dna.md`.

### Imagens de negócio real sem fotos
Decidir com o usuário, em voz alta: o site declara que as imagens são geradas por IA, ou elas serão trocadas por fotos reais depois? As duas respostas funcionam; o que não pode é não decidir. Marca fictícia/demo: rodapé declara.

Saídas personalizadas obrigatórias:
- Copy com o vocabulário do nicho (veja `narrativa-estrutura.md`).
- Ícones SVG próprios num estilo derivado da marca (isométrico, linha, sólido).
- Imagens: fotos do cliente ou geradas (Higgsfield, quando autenticado) com prompt-mestre fixo de luz, paleta e enquadramento para todas parecerem da mesma sessão.
- Motion derivado da personalidade: marca sóbria = curvas `--ease-out` lentas, poucos loops; marca jovem = `--ease-pop`, mais stagger.
- SEO local e de nicho: title/meta com nicho + região, `LocalBusiness`/`ProfessionalService` em JSON-LD.

## Camada 2: o site muda para cada visitante (runtime)

Princípio: **o visitante sente que a página foi escrita para ele, sem sentir que foi vigiado.**

### Sinais permitidos (sem consentimento extra, sem dado pessoal)

| Sinal | Origem | Exemplo de uso |
|---|---|---|
| Campanha/tema | `?utm_campaign=`, `?utm_term=`, `?seg=` | anúncio "PIS/COFINS" abre hero sobre créditos de PIS/COFINS |
| Origem | `document.referrer` (Instagram, Google, LinkedIn) | vindo do Instagram: prova social visual primeiro |
| Escolha explícita | seletor "Sou transportadora / indústria / comércio" | troca casos, termos e CTA; guarda em `localStorage` |
| Visita repetida | `localStorage` | "Bem-vindo de volta" discreto + atalho para o CTA; pula preloader |
| Horário local | `new Date().getHours()` | fora do expediente: CTA "deixe mensagem, respondemos às 8h" |
| Dispositivo | `matchMedia` | mobile: CTA WhatsApp; desktop: agenda/e-mail |
| Idioma | `navigator.language` | só se houver tradução real |

Geolocalização por IP ou cookies de terceiros: **só com consentimento LGPD** e com valor claro. Na dúvida, não usar.

### Motor de variantes (sem framework)

Marcação: o conteúdo padrão fica no HTML (SEO e sem JS); variantes ficam em `<template>`:

```html
<h1 data-p="hero-title">Contabilidade para transportadoras em GO, PR, MG, SP e RJ.</h1>
<template data-p-variant="hero-title" data-seg="pis-cofins">
  Créditos de PIS/COFINS sobre diesel e pneus, recuperados e validados.
</template>
<template data-p-variant="hero-title" data-seg="reforma">
  CBS e IBS no frete: o que muda no seu caixa a partir de 2027.
</template>
```

`templates/personaliza.js` resolve o segmento (URL > escolha salva > referrer > padrão), troca os textos, ajusta a mensagem pré-preenchida do WhatsApp, marca `<html data-seg="...">` para CSS e dispara um evento de análise. Funciona com qualquer número de blocos.

### O que personalizar (por impacto)

1. H1 e subtítulo da hero (casa com o anúncio que trouxe a pessoa).
2. Ordem dos casos de resultado (o do segmento dela primeiro).
3. Mensagem do WhatsApp: `?text=` com segmento e página ("Vim pelo anúncio de PIS/COFINS e quero o diagnóstico").
4. Prova social e artigos do blog do mesmo tema.
5. CTA por horário/dispositivo.
6. Imagem da hero por segmento (ter 1 por segmento principal).

### Interativos que personalizam por escolha

- **Diagnóstico em 3 perguntas** (porte, regime, dor): mostra resultado estimado com faixa e aviso, e leva ao WhatsApp com as respostas no texto.
- **Calculadora** do benefício principal (ex. crédito estimado por litros de diesel/mês). Fórmula do cliente, revisada por ele.
- **Seletor de perfil** fixo no topo da seção de frentes.

### Limites éticos e legais

- Nada de "Olá, [nome]" sem login. Nada de cidade exata detectada por IP sem consentimento.
- Sempre um jeito de ver a versão padrão (`?seg=padrao`) e de trocar a escolha.
- Variante nunca promete o que a padrão não cumpre.
- Registrar no `dna.md` cada variante e a fonte do texto.

### Medição

Eventos mínimos: `seg_resolvido`, `cta_click` (com segmento e posição), `whatsapp_open`, `diagnostico_concluido`. Comparar conversão por segmento depois de 2 a 4 semanas e cortar variante que não ganha.
