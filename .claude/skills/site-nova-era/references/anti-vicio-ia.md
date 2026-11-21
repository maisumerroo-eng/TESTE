# Anti-vício de IA

Complementa `anthropic-skills:site-sem-cara-de-ia`. Rodar esta lista **antes de entregar**; cada item marcado é retrabalho obrigatório.

## Visual

| Vício | Troque por |
|---|---|
| Gradiente roxo/azul neon, "aurora", blobs desfocados | paleta de 1 cor de marca + neutros; luz como recurso (brilho, reflexo) |
| Grade de 3 cards iguais com ícone de biblioteca (Lucide/Heroicons) no topo | placas de tamanhos diferentes, ícones próprios no mesmo estilo, foto real |
| Glassmorphism em tudo | vidro só no header ou num elemento; resto sólido |
| Sombra suave genérica em todo card | bordas finas de 1px na cor de linha, contraste por fundo |
| Ilustração 3D fofa estilo "blob people" | fotografia real do contexto do cliente, ou ícone isométrico próprio |
| Seções todas com mesma altura e mesmo layout centralizado | ritmo: cheia, curta, longa, gigante, respiro; alternar esquerda/direita/centro |
| Hero com mockup de laptop flutuando | objeto do nicho em close (mão, ferramenta, produto) |
| Botões arredondados `rounded-full` azuis padrão | botão com identidade (face 3D, frame, cantos retos se a marca for sóbria) |
| Fontes Inter em tudo sem hierarquia | 1 display com personalidade + 1 texto; escala com contraste forte |
| Banner de cookies padrão do plugin | estilizado com os tokens da marca |
| Emojis como ícones | SVG próprio ou nada |

## Texto

| Vício | Troque por |
|---|---|
| "Transforme seu negócio", "Leve sua empresa ao próximo nível", "soluções inovadoras" | resultado concreto + mecanismo ("Créditos de PIS/COFINS sobre diesel recuperados") |
| "Somos uma empresa apaixonada por..." | o que faz, para quem, onde |
| Trio de adjetivos ("rápido, seguro e eficiente") | um fato verificável |
| Números redondos inventados ("+500 clientes satisfeitos") | número real com fonte, ou nenhum |
| Depoimento genérico "Excelente serviço! - João S." | depoimento real com contexto, ou cortar |
| Travessão longo (—) e frases em três partes no texto visível | ponto final, vírgula, dois-pontos |
| "Saiba mais", "Clique aqui" | verbo + objeto + benefício |
| FAQ com perguntas que ninguém faz | perguntas do comercial/WhatsApp do cliente |
| Jargão de marketing em inglês sem necessidade | português do cliente, siglas do nicho |

## Movimento

| Vício | Troque por |
|---|---|
| Tudo faz fade-up igual | vocabulário: cada tipo de conteúdo tem seu reveal |
| Animação ao rolar para cima e para baixo toda vez | revela uma vez |
| Parallax em todas as imagens | 1 ou 2 pontos de profundidade |
| Elementos que flutuam sem parar (bounce infinito) | loops só no fundo, sutis, pausados fora da tela |
| Cursor custom em tudo | só onde ajuda (galeria, arrasto) |

## Detector rápido (rodar no projeto)

Gate oficial: `python3 templates/gate-texto.py <pasta>` (texto visível + variantes `<template>`: travessões, palavras de estoque, "não é só X, é Y", atribuições vagas, finais grandiosos, palavras entregadoras, emojis). Precisa sair limpo antes de qualquer pessoa ver o site. Atalhos manuais:

```bash
grep -rniE "transform(e|ar) seu|próximo nível|inovador|soluções completas|apaixonad|excelência|—|saiba mais|clique aqui" --include=*.html .
python3 -c "import re,glob;[print(f,re.findall('[\U0001F300-\U0001FAFF\u2600-\u27BF]',open(f).read())[:5]) for f in glob.glob('**/*.html',recursive=True)]"   # emojis
grep -rniE "from-purple|to-indigo|via-pink|bg-gradient-to" --include=*.{html,css} .
```

## Prova de autoria (o site precisa ter pelo menos 5)

- [ ] Metáfora do negócio virou uma interação (momento-assinatura)
- [ ] Vocabulário técnico do nicho em títulos e cards
- [ ] Lugar, público e oferta declarados acima da dobra
- [ ] Ícones/ilustrações próprios num estilo só
- [ ] Fotos reais do contexto (ou geradas com consistência de luz, paleta e enquadramento)
- [ ] Um detalhe tipográfico de assinatura (número vazado, kicker com traço, wordmark gigante)
- [ ] Números com contexto e disclaimer honesto
- [ ] Copy que só serve para este cliente (trocar o nome da marca quebraria o texto)

## Vícios adicionais (filtrados de site-de-10k e site-sem-cara-de-ia)

### Composição e direção
| Vício | Troque por |
|---|---|
| Hero centralizada com título + subtítulo + 2 botões como única composição | composição assimétrica, texto ancorado num lado, mídia com peso |
| Duas seções vizinhas com o mesmo esqueleto (kicker + título + lede na mesma grade) | remodelar uma delas: lista, editorial, número gigante, placa, mídia sangrada |
| Acento em tudo | acento em doses raras: CTA, foco, 1 ou 2 ênfases |
| Fundo `#000` ou `#fff` puro | tingir na direção da marca/fotografia |
| Paleta de framework (indigo/violet do Tailwind, azul padrão de botão) e componente de biblioteca sem personalização | tokens próprios, componentes redesenhados |
| Dark mode com neon por padrão | escuro só se a marca ou a referência pedirem |
| Elementos paralelos desiguais (3 passos e só 2 com imagem; um card estilizado diferente) | tratamento igual para itens paralelos |

**Looks "reflexo de IA"** (proibidos como padrão automático, permitidos quando são o mundo material do assunto): creme + serifa + acento terracota; quase-preto + verde-ácido; quase-preto + âmbar quente + serifa de alto contraste (o reflexo de "escuro, rico, cinematográfico"); brutalismo de borda fininha. Quando um deles for genuinamente o mundo do cliente (ateliê de cerâmica = creme e terracota), mereça: amostre os tons da fotografia real, invente a assinatura, fuja do molde, e **declare o desvio** no `dna.md`. Caso Meridiano: pedra + terracota veio do concreto, do freijó e da luz do pôr do sol das imagens, com display sem serifa expandida, e foi declarado.

### Texto (sinais quietos)
- Palavras de estoque: alavancar, robusto, empoderar, destravar, acionável, orientado a dados, soluções, sinergia, escalável.
- Construções "não é só X, é Y"; faixas falsas ("de X a Y" que é só uma lista); atribuições vagas ("muitos especialistas dizem"); finais grandiosos ("o futuro é promissor"); palavras entregadoras (testamento, panorama, mergulhar, elevar).
- **Exceção que importa:** dispositivo de marca deliberado, decidido no `dna.md` (um trio desenhado "Colher. Coar. Servir.", um staccato planejado), é ofício e fica. Sinal é o que apareceu sem convite.
- O texto do site fala na **voz da marca**, não na voz de amigo: casa de luxo e streetwear são ambas simples, mas não soam iguais. Frases do tamanho de um flick de scroll.

### Referência do cliente
Se o cliente mandar um site e disser "quero assim", siga **estrutura, ritmo, tipografia e clima** com fidelidade (não "melhore" trocando por layout padrão), mas nunca copie texto, código, imagens ou ícones. Sites estudados para a régua (`casos/`) são outra coisa: princípios, não molde.

### Prova de autoria: teste de remoção
Se a assinatura fosse retirada, a página mudaria de verdade? Se mal mudaria, não é assinatura: gastar o orçamento de ousadia em algo cuja ausência seria notada.
