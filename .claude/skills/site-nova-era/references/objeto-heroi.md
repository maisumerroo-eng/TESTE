# Objeto-herói

Na Vexter, a hero é uma **mão segurando uma moeda de real** ao lado da pergunta "Sua empresa está pagando mais imposto do que deveria?". A moeda é o dinheiro que o cliente vai recuperar; a mão é a escala humana e a confiança. Em meio segundo o visitante entende **o que está em jogo**, antes de ler qualquer coisa.

Todo site da skill planeja o seu objeto-herói (fase de plano), adaptado ao nicho.

## A mão: diferencial para REUSAR (não obrigação)

A mão funciona porque é **humana**: dá escala, aproxima, transmite cuidado e confiança, e afasta a cara de "render de IA". Por isso ela é o padrão recomendado e **deve ser reusada** sempre que servir ao cliente. Mas não é prisão: em temas novos, pode e deve haver variação. O objetivo é **presença humana + promessa visível**, não "sempre uma mão segurando algo".

### Variações com presença humana (reusar a ideia, inovar a forma)
| Forma | Quando |
|---|---|
| Mão segurando/apresentando (padrão) | promessa que cabe na palma (moeda, maquete, chave, frasco) |
| Mão em ação (traçando, montando, assinando, regando) | serviço que é um gesto (arquitetura, advocacia, estética, agro) |
| Duas mãos (entregando, protegendo, encaixando) | entrega, cuidado, parceria |
| Silhueta/contraluz de pessoa | lifestyle, morar, viajar, esporte |
| Sombra humana sobre o objeto/cena | sutileza, alto padrão |
| Ponto de vista em 1ª pessoa (POV) | experiência (entrar na casa, sentar à mesa) |
| Rosto parcial/olhar (com consentimento e foto real) | saúde, beleza, educação, marca pessoal |

### Sem mão (quando o objeto fala sozinho)
| Forma | Quando |
|---|---|
| Objeto levitando ou em pedestal, com luz de produto | produto físico premium, joia, embalagem |
| Objeto 3D interativo (gira com o mouse/scroll) | produto, maquete, peça técnica (`tres.js`) |
| Macro de material (textura, grão, gota, fio) | marca de material/acabamento |
| Cena viva mínima (vapor, luz, água) em vez de objeto | gastronomia, bem-estar |
| Tipografia como objeto (palavra/número gigante esculpido) | marca de dado, finanças, tecnologia |

Decisão consciente no `plano.md`: reusar a mão (e de que forma) ou justificar a alternativa. Ver `inovacao.md` e `portfolio.md` (não repetir a mesma composição em clientes seguidos).

## Regras

1. **O objeto é a promessa, não o produto genérico.** Mostra o resultado que o cliente quer ter na mão (dinheiro recuperado, a casa antes de existir, o sorriso alinhado), não "um escritório" ou "um prédio".
2. **Escala humana:** quase sempre uma mão segurando, apresentando ou pousando o objeto. Mão em close, natural, sem joias chamativas; anatomia conferida (mão é assunto difícil, ver `video-scrub.md` lei 5).
3. **Material e luz da marca:** o objeto e a luz carregam a paleta (moeda dourada no site preto e ouro). Luz lateral dramática, fundo que funde com a hero.
4. **Invade a composição:** o objeto sai da borda da hero (corte embaixo ou na lateral), fica atrás ou ao lado do título, nunca dentro de uma caixa. Profundidade: objeto > título > ambiente.
5. **Um só objeto**, sem cenário. O ambiente da hero vem de CSS/canvas (barras, raios, brises), não da foto.
6. **Celular:** objeto reposicionado (centralizado embaixo, menor) e texto acima; testar contraste do título sobre ele (`auditar-contraste.js`).
7. **Entrada:** surge do desfoque com leve subida (`data-reveal="blur"`), depois o título, depois os cartões de prova contando.

## Ideias por nicho (ponto de partida, cada cliente pede a sua)

| Nicho | Objeto na mão | Promessa |
|---|---|---|
| Contabilidade/tributário | moeda | dinheiro que volta |
| Construtora alto padrão | maquete branca da casa na palma, com sol rasante e sombra | ver a casa antes de existir, desenhada pela luz |
| Incorporadora | chave com chaveiro do empreendimento | a chave na mão |
| Arquitetura | rolo de planta / esquadro | o desenho sob medida |
| Energia solar | célula solar com reflexo do sol | conta de luz menor |
| Clínica estética | gota de sérum suspensa / espelho de mão | pele refeita |
| Odontologia | alinhador transparente contra a luz | sorriso sem metal |
| Advocacia | caneta-tinteiro sobre o documento assinado | causa resolvida |
| Restaurante | colher com a garfada do prato assinatura | o sabor |
| Academia | anilha / fita métrica | o corpo que quer |
| Agro | punhado de grãos / broto | safra |
| SaaS/tecnologia | cartão ou chip translúcido com luz interna | operação automática |
| Moda | tecido escorrendo entre os dedos | caimento |
| Pet | pata pousando na mão | cuidado |
| Seguro | guarda-chuva pequeno sobre a casa de brinquedo | proteção |
| Educação | lápis/caneta virando trajetória de luz | futuro |
| Automotivo | chave do carro com reflexo | o carro pronto |

## Como produzir (do grátis ao pago)

- **Foto real do cliente** segurando o objeto dele (melhor de todas para negócio real).
- **Gerada** (Figma `generate_image` primeiro): fundo **preto puro ou da cor exata da hero**, para fundir sem recorte:
```
Close-up of a natural human hand [presenting/holding] [OBJECT], [material and finish], dramatic warm side light from the [left],
deep [black/brand-color] seamless background, the [object] catching a rim of light, shallow depth of field, editorial product
photography, 85mm, f/4, photorealistic. The hand enters from the [bottom left] corner. No text, no logos, no lettering anywhere.
```
- **Fusão sem recorte:** sobre hero escura, `mix-blend-mode: lighten` faz o preto da foto sumir; reforçar com `mask-image` radial nas bordas. Recorte de verdade (transparência) só quando necessário: `ai-background-remover` (muapi) ou `remove_background` (Higgsfield), pagos.
- Inspecionar: dedos (número, dobras), marcas registradas no objeto, coerência com a marca. Dois takes no máximo; depois mudar o objeto.

## Ambiente da hero adaptado (o equivalente às barras douradas da Vexter)
| Nicho | Ambiente |
|---|---|
| Contabilidade | barras douradas ondulando (gráfico vivo) |
| Construtora | luz do sol passando por brises (ripas) e varrendo devagar |
| Energia solar | raios e reflexos girando lentamente |
| Clínica | gotas/bolhas desfocadas subindo |
| Tecnologia | grade/pacotes de dados correndo |
| Restaurante | vapor em canvas |
Sempre: máscara diagonal para sumir atrás do texto, pausado fora da tela, parado em reduced motion.
