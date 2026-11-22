# Plano: KAGERIMA (canal de rap geek)

> Arte oficial do canal (enviada pelo dono em 22/11/2026) usada como identidade. Dados reais ainda não enviados: números e links entram como **exemplo marcado** até o dono mandar. Aprovação: [x] aprovado pelo dono em 22/11/2026 (coluna 6 = Jujutsu Kaisen, Megumi)

## 0. Estratégia antes do design
- **Públicos:** (1) fã de anime 13–30 anos que busca o rap do personagem favorito; (2) marcas, eventos e outros canais que querem rap encomendado, collab ou publi.
- **Critérios de escolha (fã):** o personagem/anime que ele ama, qualidade do beat e da rima, fidelidade à história, frequência de lançamento. **(marca):** alcance, perfil do público, profissionalismo, preço e prazo.
- **Medos:** fã: "rap genérico que não entende o anime", spoiler sem aviso. Marca: "canal pequeno demais", "não entrega no prazo", "conteúdo arriscado para a marca".
- **Buscas Google:** "rap do gojo", "rap do sukuna", "rap do naruto", "rap de anime", "rap geek", "rap do luffy", "rap do goku", "rap do ichigo". **IA (ChatGPT/Gemini):** "qual o melhor rap de anime em português?", "rap do Gojo brasileiro".
- **Concorrentes:** 7 Minutoz (gigante, 3 bi+ views em 2021), M4rkim, Basara, Enygma, MHRap ([Omelete](https://www.omelete.com.br/mangas-animes/rap-geek-anime)). Vivem do YouTube; **não há site oficial forte** organizando os raps por anime e abrindo parcerias.
- **Diferencial:** o único canal com um **site-hub por anime**: escolha seu anime e o site vira o dele (cores, kanji, raps); e uma porta clara para **encomendar rap/collab**.
- **Posicionamento:** Para fãs de anime que querem o rap do seu personagem com a história respeitada, a KAGERIMA é o canal de rap geek que transforma cada anime em sombra e rima, com faixas organizadas por obra e encomendas abertas para marcas e canais.
- **Mapa do site:** Home (rap de anime) · /naruto, /jujutsu-kaisen, /one-piece, /bleach, /dragon-ball (rap do [anime]) · /parcerias (rap encomendado, collab) · /letras (letra do rap de [personagem]). Primeira entrega: home completa com âncoras; páginas por anime planejadas.
- **Rascunho no celular (1ª tela):** logo glitch · título 2 linhas · seletor "seu anime" (6 chips) · botão "Ouvir agora" · cartões de prova.

## 1. Premissa e oferta
- Premissa: **sombra** (影 KAGE + RIMA): cada anime tem uma sombra, e a rima dá voz a ela.
- Ofertas: fã → **Ouvir agora** (YouTube/Spotify); marca → **Encomendar rap** (selo: "resposta em 48 h", a confirmar).

## 2. Objeto-herói (inovação: não repetir a mão da Meridiano)
- **Tipografia como objeto + presença humana por sombra:** o bloco lima **影** gigante, com glitch RGB e scanlines da arte, e atrás dele a **sombra de um rapper com microfone** projetada na parede (silhueta, sem rosto). Kanji = marca; sombra = humano; une as duas metades do nome.
- Silhueta: gerada no Figma (1 geração) ou desenhada em SVG (grátis).
- Ambiente: grão de filme + linhas de varredura + kanjis das 6 obras piscando em baixa opacidade (do banner).
- Celular: 影 centralizado em cima, sombra atrás em menor escala.

## 2b. Reuso e inovação
- Reusos: btn3d, cartão de prova, faixa de ícones (vira faixa de animes), lista de serviços (parcerias), número gigante, gráfico interativo, carrossel, form → WhatsApp, rodapé com wordmark, personaliza.js, motion.js.
- Inovações (4):
  1. **Seletor de animes guiado por scroll** (momento-assinatura): seção fixada com os 12 kanjis do banner; cada etapa acende uma coluna (anime), o par de kanjis faz "decrypt" glitch, o fundo muda para a cor da obra e aparece o rap em destaque.
  2. **Personalização por anime favorito** (`?anime=jjk`): hero, cor de acento, kanji e ordem dos raps viram do anime do fã; links das descrições do YouTube saem com `?anime=` + UTM.
  3. **Texto decrypt** (letras embaralham até formar o título, ecoando glitch): componente novo.
  4. **Player facade leve** (miniatura que só carrega o YouTube no clique) com placar de faixa.
- Portfólio: Meridiano = mão + maquete + brises + estudo solar 3D. Aqui: tipografia + sombra + glitch + seletor por scroll. Sem repetição.

## 3. Mapa de seções
| # | Seção | Estratégia | Componente | Interação |
|---|---|---|---|---|
| 1 | Hero 影 + sombra | dor/desejo + objeto + prova | objeto tipográfico, prova, btn3d, chips de anime | escolher anime troca o site |
| 2 | Faixa das obras | amplitude | faixa de animes (kanji + nome + nº de raps) | arrastar |
| 3 | Seletor por scroll | assinatura | pin com 6 etapas | scroll controla anime |
| 4 | Lançamentos | prova + conteúdo | carrossel de faixas com facade | tocar |
| 5 | Números do canal | prova quantificada | número gigante + gráfico de views por anime (interativo) | hover/toque |
| 6 | Encomendar rap | escopo + tipo de contrato | placas com aba + lista de serviços (rap encomendado, collab, publi, jingle geek) | hover |
| 7 | Como funciona a encomenda | redução de risco | etapas com entregável | — |
| 8 | Valores "Da sombra à rima" | manifesto | valores escalonados + ícones isométricos (mic, fone, kanji, onda, palco...) | — |
| 9 | Letras/guias | autoridade/SEO | carrossel de letras ("Rap do Gojo: letra") | — |
| 10 | FAQ | medos | details | — |
| 11 | CTA parcerias | conversão | form → WhatsApp/e-mail | — |
| 12 | Rodapé | assinatura | colunas por anime + wordmark KAGERIMA glitch | — |

## 4. Régua mínima
Piso Vexter obrigatório: atingir com 12 seções, estados completos, animações nomeadas por tipo (glitch, decrypt, scan, pulse de kanji), ícones isométricos (12+), imagens (capas de faixa e letras), texto de letras/guias e FAQ.

## 5. Assets e custo
| Asset | Ferramenta | Custo |
|---|---|---|
| Silhueta do rapper com microfone | Figma generate_image (fundo preto) ou SVG | 1 geração Figma ou 0 |
| Capas de faixa | composição CSS (kanji + cor da obra), sem arte oficial de anime | 0 |
| Ícones isométricos | gerar-icones-iso.py | 0 |

## 6. Riscos
- **Direitos de anime:** nomes das obras e personagens só como referência descritiva; nenhuma arte oficial de anime no site.
- **卍:** no banner é o 卍 de 卍解 (Bleach), símbolo budista; para público ocidental pode ser mal lido. Manter, sempre junto de 解, e com legenda "Bankai".
- Coluna 6 (伏/子): confirmada pelo dono, Jujutsu Kaisen (Megumi Fushiguro).
- Números reais: aguardando o dono; até lá, "exemplo".
