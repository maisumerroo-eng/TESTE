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
