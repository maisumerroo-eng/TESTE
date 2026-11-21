# Narrativa e estrutura

Um site da nova era é **um roteiro**, não uma pilha de seções. Cada dobra responde a uma pergunta que o visitante tem naquele momento.

## O roteiro em 8 atos

| Ato | Pergunta do visitante | Bloco | Regra |
|---|---|---|---|
| 1. Gancho | "É pra mim?" | Hero | Dor ou ganho **específico do nicho** + número + 1 CTA. Nicho aparece nos primeiros 3 s |
| 2. Credibilidade | "Posso confiar?" | Faixa de prova | Logos, selos, números reais, ou frentes de atuação. Curta (≤ 300 px) |
| 3. Oferta | "O que exatamente vocês fazem?" | Frentes/serviços | Máx. 3 a 5 frentes. Cada uma: resultado, como, para quem, tipo de contrato |
| 4. Prova | "Funciona mesmo?" | Resultados | Casos com contexto (segmento, UF, antes→depois), número grande, disclaimer honesto |
| 5. Processo | "Como vai ser?" | Como funciona | Etapas com **entregável** cada. Lugar ideal do momento-assinatura |
| 6. Identidade | "Quem são?" | Método/manifesto | Valores como verbos ou atributos encadeados, nunca parágrafo institucional |
| 7. Autoridade | "Sabem do assunto?" | Conteúdo/FAQ | Artigos ou perguntas com o vocabulário técnico do cliente |
| 8. Ação | "Como começo?" | CTA final + rodapé | Mesma oferta da hero, com qualificação e canais (WhatsApp, e-mail, região) |

Corte atos que o negócio não sustenta com verdade (sem casos reais: troque Prova por garantia ou demonstração). Nunca invente.

## Momento-assinatura (obrigatório: 1 por site)

A peça que alguém grava a tela para mostrar. Nasce da **metáfora do negócio**:

| Nicho | Metáfora | Interação |
|---|---|---|
| Transporte/logística | estrada, rota | marcador percorre caminho SVG no scroll, paradas = etapas |
| Contabilidade/finanças | balanço, extrato | linhas de um extrato se somando, saldo virando de vermelho para verde |
| Clínica/estética | antes e depois, camadas | slider de revelação, camadas de pele/tecido no scroll |
| Arquitetura/imóveis | planta, luz do dia | planta que vira volume, sol atravessando o dia no scroll |
| Restaurante | preparo, fogo | ingredientes caindo na ordem do prato, vapor em canvas |
| Advocacia | processo, prazos | linha do tempo processual com marcos que travam no lugar |
| Academia/esporte | ritmo, carga | barra de carga enchendo, contagem de repetições |
| Tecnologia/SaaS | fluxo de dados | pacotes viajando entre nós, painel montando-se |
| Moda | caimento, tecido | peça girando/costas, tecido ondulando com o cursor |
| Agro | safra, estações | campo mudando de estação com o scroll |

Regras: ocupa 1 seção; funciona sem animação (lista estática legível); no mobile tem atalho para pular.

## Arquitetura de cada seção

```
[kicker com traço]  ← rótulo curto em caixa alta, tracking +0.2em
[título 2 linhas]   ← à esquerda, afirmação concreta
[explicação 2-3 linhas] ← à direita no desktop, abaixo no mobile
[conteúdo]
[CTA secundário contextual] ← "Quer saber quanto a sua empresa pode recuperar?" + botão
```

Alternar fundo escuro/claro para marcar capítulos. Transição entre eles com degradê longo ou cortina, nunca corte seco sem intenção.

## Fórmulas de copy (preencher com dado real do cliente)

- Hero afirmação: "[Resultado mensurável] para [nicho] em [região/condição]."
- Hero pergunta-dor: "Sua [empresa do nicho] está [perdendo X] sem saber?" (usar com moderação)
- Subtítulo: o que acontece hoje (dor) + o que a empresa faz (mecanismo) + para quem.
- Frente: título = resultado; texto = mecanismo com 1 termo técnico; rodapé = tipo de contrato.
- Resultado: "[Segmento] · [UF]" / "mais de R$ [n] mil" / "de economia por [período]" / 2 linhas de como.
- Etapa: verbo no substantivo ("Diagnóstico") + o que fazemos + "Entrega: [artefato]".
- CTA final: benefício de saber antes ("Descubra o que [x] diz antes de decidir") + condição + botão.
- Microcopy de botão: verbo + objeto + benefício ("Pedir diagnóstico gratuito"), nunca "Saiba mais".

## Arquivos

```
index.html        semântico, conteúdo completo sem JS
style.css         tokens → base → layout → componentes → motion
motion.css        sistema de reveal (templates/motion.css)
main.js           comportamentos (templates/motion.js)
personaliza.js    variantes por visitante (templates/personaliza.js)
assets/img, assets/icons (SVG próprios), assets/fonts (woff2 subset)
```
