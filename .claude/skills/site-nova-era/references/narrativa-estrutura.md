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

## Premissa da marca (antes do roteiro)

Um parágrafo construído sobre **uma palavra ou ideia real do mundo do cliente** (Meridiano: "luz"). O site inteiro ensina e vende essa ideia: cada seção, o momento interativo e a linha final servem a ela. **Seção que não serve a premissa sai da página.**

## Escrever nas palavras de quem compra

Antes da copy, coletar frases reais de dor, desejo e objeção (método em `megapersonalizacao.md`). Usar as palavras deles nos títulos de dor, nas perguntas do FAQ e nas objeções respondidas. Regra aprendida: quando o assunto é **uma pessoa** (dono, chef, artesão, profissional liberal), o hero apresenta essa pessoa na voz confiante dela; a linguagem de dor dos compradores trabalha nas seções de baixo (gancho de dor sobre o rosto de alguém soa como reclamação alheia).

## Tipos de momento-assinatura

| Tipo | Quando | Base |
|---|---|---|
| Seção fixada com SVG/CSS (rota, sol, planta, extrato) | padrão: leve, editável, grátis | `data-pin` do `motion.js` |
| **Vídeo no scroll (scrub)** | jornada de câmera contínua é a metáfora e há verba de vídeo | `references/video-scrub.md`, `templates/scrub/` |
| 3D | produto físico ou símbolo da marca que ganha com rotação/explosão | `references/3d.md`, `tres.js` |

Um por página.

## Momento interativo único (opcional, um por site)

Uma ação que o visitante **executa** e que encena a ideia da marca (segurar para "assentar o concreto", arrastar o sol sobre o terreno, montar o kit). Mecânica que parece desenhada, não truque:
- o progresso cresce enquanto o visitante segura/arrasta;
- soltar cedo desce o progresso suavemente (nunca estala para zero);
- completar acende o conteúdo da seção em sequência (a ação conquista algo real);
- reduced motion recebe o estado final na hora; teclado tem alternativa (botão).
Não somar com a assinatura na mesma dobra. O seletor de perfil da personalização conta como interação útil; o momento interativo é sobre a marca.

## Formulário em site estático (dizer a verdade sobre o destino)

| Destino | Quando |
|---|---|
| WhatsApp com mensagem pronta (`data-wa`) | padrão BR, já personalizado por segmento |
| Serviço de formulário (Formspree e similares) | negócio real captando lead por e-mail; conta do cliente |
| `mailto:` | simples, abre o e-mail do visitante |
| Só estado de sucesso em JS | demo/portfólio (declarar que não envia) |
Escrever no `dna.md` onde a mensagem do visitante termina e fazer o estado de sucesso combinar com isso.
