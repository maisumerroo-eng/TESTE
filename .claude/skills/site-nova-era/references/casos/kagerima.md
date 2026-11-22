# Caso: KAGERIMA (canal de rap geek, 22/11/2026)

Site completo de um canal de rap de anime, feito a partir do banner oficial enviado pelo dono. Primeiro site da skill a **passar a régua mínima Vexter (13/13) e os tetos de performance**. Código: `kagerima/` no repositório. Preview: artefato "KAGERIMA Rap Geek".

## Estratégia
- Dois públicos: fã de anime (ouvir o rap do personagem) e marca/canal (encomendar, collab, publi). Cada seção serve a um dos dois, e a personalização por segmento (`personaliza.js`) destaca a placa e a coluna do comparativo certas.
- Diferencial: os concorrentes vivem só no YouTube; o site vira um hub por anime e uma porta de encomenda.
- Sem arte oficial de anime: capas feitas por composição (kanji + cor da obra), nomes só como referência. 卍 sempre junto de 解 e com a legenda "Bankai".
- Dados que o dono não mandou entram como **exemplo marcado** (gráfico, faixas, votação) e são trocados em `dados.json` + `python3 montar.py`.

## Objeto-herói e assinatura
- Tipografia como objeto: bloco lima com 影 (glitch RGB em rajadas curtas) + silhueta de rapper atrás (presença humana sem rosto). Une as duas metades do nome: 影 (sombra) + rima.
- Momento-assinatura: seletor guiado por scroll com os 12 kanjis do banner; cada etapa acende a coluna da obra, faz decrypt do par de kanjis, troca a cor e a textura do palco (anéis do Infinito, explosão de ki, corte de espada, ondas, tomoe, sombras que escorrem).

## Inovações devolvidas (em `templates/componentes/interacoes-canal.js`)
1. Tema por interesse: `?anime=` (ou chip/cartão) troca acento, kanji, título, textura e ordem das faixas; lembrado no aparelho; aviso curto (toast) e flash de troca.
2. Texto decrypt: letras embaralham até formar o texto (respeita reduced motion e aria-label).
3. Player facade: miniatura que só carrega o YouTube (nocookie) no clique + mini player fixo quando o card sai da tela.
4. Spoiler velado: capa desfocada com aviso do arco até o fã aceitar; botão "mostrar spoilers" para todas.
5. Votação local (prévia) com barras, "seu voto" e troca de voto; a oficial fica na comunidade do YouTube.
6. Monte seu pedido: rádios/checkboxes estilizados → resumo vivo → link do WhatsApp com a mensagem pronta.
7. Abas acessíveis (setas, Home/End) com equalizador que só anima visível.
8. Busca + filtro + ordenar faixas, com estado vazio que leva à votação/encomenda.
9. Janela de conteúdo (`<dialog>`) com anterior/próxima e cor por obra.
10. Modo leve no rodapé: desliga glitch, piscadas e grão (fotossensibilidade e bateria).
11. Painel de privacidade: mostra o que fica no aparelho e apaga as preferências (LGPD sem banner genérico).
12. Pontos de navegação do pin, scroll-spy no menu, header que some ao descer, barra de progresso, comparativo em tabela que vira cartões no celular, menu gaveta acessível.

## Lições medidas (viraram regra em `qualidade.md`)
- **Variável CSS no `:root` a cada quadro** (barra de progresso) recalculava a página inteira: bloqueio no teste mobile 4x caiu de **26,8 s para 0,8 s** ao mover a variável para o próprio elemento.
- O **marquee do `motion.js` lia `offsetWidth` a cada quadro** (layout forçado) e **capturava o ponteiro no `pointerdown`**, o que mandava o clique para a caixa e impedia os links de abrir. Os dois corrigidos no template.
- `getComputedStyle` dentro de observer/scroll força recálculo: ler do `style` inline.
- Animações infinitas: trocar `background-position` e `filter` animados por `translate`/`scale`; pausar seções fora da tela (`.is-fora-tela`) e a hero fora da tela; sem skeleton infinito.
- CSS em vários arquivos para editar, **um `site.css` minificado no build** (14 → 1 requisição bloqueante).
- `content-visibility: auto` derruba o `innerText` (a régua contou 859 palavras em vez de 2.421): não usar sem medir.
- `auditar-contraste.js` lia `color(srgb 0–1)` de `color-mix()` como quase preto: parser corrigido. Ainda dá falso positivo quando o elemento tem selo com fundo próprio (rótulo, "Nova"): conferir no print.
- `motion.css` traz `--accent` genérico: o acento da marca precisa ser redeclarado depois dele (senão o lima virou dourado).

## Números na entrega
Régua (1440, sem limitação): regras CSS 1552, keyframes 76, hover 119, transições 127, gradientes 95, máscaras 22, clip-path 14, SVG 739, imagens 47, h3 82, palavras 2421, links 128, variáveis 91; LCP 0,3 s, CLS 0,02, peso inicial 581 KB, CSS 165 KB, bloqueio inicial 92 ms. Auditoria mobile (4G lento + CPU 4x, com brotli): LCP ~2,4 s, CLS 0,003, peso 446 KB; bloqueio na rolagem completa ~2,7 s (Meridiano: 1,7 s no mesmo teste). Contraste, flick e gate de texto aprovados; sem rolagem lateral em 360/768/1440; zero erros no console.
