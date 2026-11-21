# Estratégias de conversão (catálogo, extraído da análise estrutural da Vexter)

Cada padrão: **o que é** na Vexter → **por que vende** → **como adaptar ao nicho** → **componente** (em `templates/componentes/` quando pronto). Usar no plano: cada seção do nosso site precisa cumprir pelo menos uma estratégia daqui. Nunca copiar forma literal, texto ou ícone; copiar a **função**.

## 1. Hero: dor nomeada + objeto-herói + prova imediata
- **Vexter:** pergunta-dor em caixa alta com o trecho crítico em dourado (`<em>`), mão com moeda, barras douradas ondulando ao fundo (30 barras com atraso escalonado, máscara diagonal), 2 cartões de número contando ("R$ 500 mil por ano / R$ 100 mil por mês") com rótulo "Economia gerada para clientes", CTA com botão 3D.
- **Por que vende:** em 3 s: o problema (dor), o que está em jogo (objeto), a prova de que resolvem (número) e o próximo passo (CTA). Prova **antes** de pedir.
- **Adaptar:** dor ou ganho nas palavras do comprador; trecho crítico na cor da marca; objeto-herói (`objeto-heroi.md`); ambiente do nicho; 2 números reais (um menor, um maior, hierarquia de tamanho).
- **Componentes:** `cartao-prova`, `btn-3d`, `ambiente-faixas`, `data-reveal="words"` com `<em>` colorido.

## 2. Faixa de competências com ícones (prova de amplitude)
- **Vexter:** "Um pouco do que a Vexter faz": 9 itens (ícone isométrico 72px + título + 1 linha), carrossel infinito arrastável com inércia, bordas que somem (máscara), divisórias verticais finas.
- **Por que vende:** mostra domínio do nicho em segundos (siglas, estados, serviços) sem pedir leitura; o movimento lento convida a arrastar.
- **Adaptar:** 6 a 10 competências concretas do cliente (serviços, certificações, regiões, tipos de obra), cada uma com ícone próprio.
- **Componente:** `faixa-icones` (usa o marquee do `motion.js` + máscara + ícones isométricos).

## 3. Frentes como placas empilhadas com aba (escopo + tipo de contrato)
- **Vexter:** 3 placas escuras sticky; cada uma tem **aba** (título + "Recorrente · Projeto") que continua visível quando a próxima placa sobe, corpo com texto + foto, **efeito de fundo temático** por placa (grade de varredura, barras que respiram, linhas de circuito) e uma **lista de serviços** (linha pontilhada que vira dourada no hover + botão "Ver serviço"); no fim, cortina de colunas escurece o fundo.
- **Por que vende:** organiza a oferta inteira sem página extra; o tipo de contrato (recorrente/avulso/projeto) remove a dúvida "posso contratar só uma parte?"; cada serviço já é um link (SEO + intenção).
- **Adaptar:** 3 frentes do cliente, cada uma com efeito de fundo da sua metáfora (planta, cronograma, cota) e lista dos serviços que pertencem a ela.
- **Componentes:** `placas-aba` (CSS do stack + aba), `lista-servicos`, `fx-planta`/`fx-barras`.

## 4. Resultados: número gigante + história com gráfico (prova quantificada)
- **Vexter:** número de 160px com gradiente metálico e brilho que varre uma vez, "R$" pequeno sobrescrito, "mais de" antes e unidade depois; ao lado, a **história**: cartões antes/depois ("Devedor" → "Credor", o depois com borda dourada e brilho) ou **gráfico acumulado** (12 barras, marcos em 3 e 6 meses, total destacado com glow, eixo com rótulos); título do caso, nota, disclaimer e CTA contextual ("Quer saber quanto a sua empresa pode recuperar?").
- **Por que vende:** número grande colorido é lido antes de tudo e fica na memória; o gráfico transforma número em história (antes, mudança, depois); disclaimer dá credibilidade; CTA aproveita o pico de interesse.
- **Adaptar:** a métrica que o cliente do nicho mais teme/deseja (economia, prazo, desvio, dias, % de aprovação); gráfico que prova a mudança; tudo com fonte real ou rótulo ilustrativo em demo.
- **Componentes:** `numero-gigante`, `antes-depois`, `grafico-barras` (interativo: foco/hover/toque mostra o valor).

## 5. Processo com entregáveis (redução de risco)
- **Vexter:** seção fixada: estrada em S, marcador, paradas rotuladas, número gigante com o zero vazado e rolo de dígitos ("0" + "4" que gira), ícone da etapa, "Entrega" por etapa, selo "Gratuito" na primeira, cortina que clareia o fundo no fim.
- **Por que vende:** o comprador vê o caminho inteiro e o que recebe em cada passo; a primeira etapa grátis baixa a barreira.
- **Adaptar:** metáfora do nicho (rota, sol, obra, linha do tempo); selo de grátis na etapa de entrada.
- **Componentes:** `data-pin` do `motion.js`, `odometro`, ícones, 3D (`tres.js`) ou SVG.

## 6. Manifesto em valores escalonados ("Do dado à direção")
- **Vexter:** palco da marca (logo se formando com chuva em canvas, 3 fatos em linha), título curto em duas partes com a segunda colorida ("Do dado **à direção.**"), intro de 2 linhas, rótulo "Nossos valores" entre linhas, **7 atributos numa grade de 8 colunas** em que a segunda linha começa deslocada (5º item na coluna 2: ritmo escalonado, não grade de cards), cada atributo com linha superior, traço dourado que cresce, ícone isométrico 88px, título e 1 frase; entram em sequência.
- **Por que vende:** traduz "quem somos" em transformação (de X para Y) e em atributos verificáveis; o escalonamento e os ícones evitam o molde "3 cards iguais".
- **Adaptar:** título "Da [matéria-prima do nicho] à [resultado]" (Meridiano: "Da luz à casa."), 4 a 7 atributos com ícones.
- **Componente:** `valores-escalonados`.

## 7. Conteúdo de autoridade (SEO + confiança)
- **Vexter:** carrossel de 14 artigos com imagem, categoria, título com termo do nicho e "Ler artigo".
- **Por que vende:** prova conhecimento técnico, captura busca de cauda longa, dá motivo para voltar.
- **Adaptar:** 6+ guias com perguntas reais do comprador (do `dna.md`).
- **Componente:** `carrossel-conteudo` (marquee + cards).

## 8. CTA final com qualificação + contatos completos
- **Vexter:** "Descubra o que os seus números dizem antes de decidir.", qualificação ("faturamento acima de R$ 500 mil"), botão 3D, 3 contatos (WhatsApp, e-mail, região).
- **Por que vende:** benefício de agir agora + filtro de lead + todos os canais visíveis.
- **Adaptar:** benefício de saber antes; filtro do nicho; formulário curto que monta a mensagem do WhatsApp (sem backend).
- **Componentes:** `btn-3d`, `form-whatsapp`.

## 9. Rodapé como assinatura
- **Vexter:** 4 colunas (marca + tagline, Soluções, Empresa, Contato), slogan em caixa alta com tracking ("Contabilidade. Estratégia. Tecnologia. Evolução."), wordmark gigante em **2 camadas** (vazada + preenchida com gradiente revelada por um feixe de luz) e linha.
- **Por que vende:** o fim também vende: navegação completa, todos os serviços como link, marca memorável.
- **Componente:** `rodape-wordmark`.

## 10. Sistema global (o "peso" premium)
- Smooth scroll (Lenis), header que some ao descer, WhatsApp flutuante só depois da hero, eyebrow com traço, títulos com palavras subindo e um trecho colorido, botões 3D em todos os CTAs, ~57 animações nomeadas por tipo de conteúdo, transição de página e preloader (fazer leve: só 1ª visita), banner LGPD.
- **Medição:** o link da bio do Instagram vai com UTM (`utm_source=ig&utm_medium=social&utm_content=link_in_bio`). Disciplina de canal: todo link externo do cliente sai com UTM, e a nossa personalização usa esses sinais (`megapersonalizacao.md`).

## 11. Estratégias de venda transversais (checar no plano)
- [ ] Uma oferta só, com selo ("Gratuito") e repetida em todo CTA.
- [ ] Número grande e colorido como prova, com contexto e disclaimer.
- [ ] Prova antes do pedido (hero com números).
- [ ] Tipo de contrato/forma de compra visível (reduz atrito).
- [ ] Entregáveis por etapa (reduz risco percebido).
- [ ] Trecho crítico do título na cor da marca.
- [ ] Qualificação no CTA final.
- [ ] Conteúdo com o vocabulário do comprador.
- [ ] Todos os canais de contato visíveis; WhatsApp como canal principal (BR).
- [ ] Links externos com UTM; personalização lendo UTM.
