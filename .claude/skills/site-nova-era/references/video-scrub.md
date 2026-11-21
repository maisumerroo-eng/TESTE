# Vídeo no scroll (scrub): quando usar, como gerar, como montar

Hero em que um vídeo avança quando o visitante rola para baixo e volta quando rola para cima. É **uma forma de momento-assinatura**, não um extra: na página com scrub, ele é a assinatura (não somar com outra seção fixada grande).

## Usar ou não (pensamento crítico)

Usar quando uma jornada de câmera contínua **é** a metáfora do negócio (entrar na casa, descer no café, atravessar a fábrica) e há verba para gerar vídeo. Não usar quando:
- a metáfora funciona com SVG/CSS (mais leve, editável, grátis): o "sol atravessando a obra" da Meridiano é um exemplo;
- o público é majoritariamente mobile e a jornada é o argumento principal (no celular o scrub vira imagem estática, por regra);
- não há créditos para o vídeo e pelo menos uma repetição.

Custo de página: 4 a 8 MB de vídeo para 6 s em 1080p (carregado depois do pôster, em baixa prioridade, só em desktop). Não entra no LCP se o pôster for leve.

## As 12 leis do vídeo (desenhar antes de gerar)

1. **O movimento concorda com o scroll:** rolar para baixo lê como descer, abrir, chegar. Assunto que sobe enquanto a página desce sempre perde.
2. **Um assunto, um movimento, sem cortes.** Nada de transformar uma coisa em outra (é a tomada mais cara e instável). Se inevitável, esconder a troca num flash/nuvem mantendo a trajetória.
3. **Trave o caminho, liberte o corpo:** trajetória rígida, assunto e cena vivos (ondulação, vapor, luz mudando). Assunto congelado = filmagem morta.
4. **Planeje o final primeiro:** o último quadro é onde a página descansa; descrever no prompt como chegada composta, com margem acima e abaixo (o cabeçalho senta em cima; o corte de cobertura come bordas). Alternativa segura: final de textura sangrada.
5. **Assuntos tolerantes:** fluidos, névoa, vapor, luz, tecido, silhuetas distantes. Mãos, teclados, controles e animais em detalhe mostram erro.
6. **Prefira eixo vertical:** casa 1:1 com o eixo do scroll.
7. **Componha para o layout:** decidir onde a ação senta e deixar espaço calmo para as legendas.
8. **Venda os cruzamentos de fronteira:** atravessar água, névoa ou vidro pede o momento físico na lente (respingo, gotas, desfoque).
9. **Produto no hero:** com a marca aplicada (edição de imagem antes de animar) ou enquadrado de perto.
10. **Texto sobre vídeo conquista legibilidade:** scrim por faixa, sombra de texto e contraste medido no **pior** quadro (sistema em `qualidade.md`).
11. **Ritmo em distância de scroll, não em segundos:** cada batida com platô de 80 a 130vh; validar com `teste-flick.js`.
12. **Guardas permanentes:** "no text, no logos, no lettering anywhere" em todo prompt; recusar presets do gerador quando há tomada desenhada; nunca montar o site em volta de vídeo não aprovado pelo usuário.

Mundos abstratos (luz, partículas, atmosfera) são os mais confiáveis, principalmente para produtos digitais.

## Prompts (sempre em inglês)

Quadro inicial (imagem 16:9, ~2k):
```
[SUBJECT] at [POSITION IN FRAME], composed as the first moment of a motion that will [ONE-SENTENCE JOURNEY].
[LIGHTING: source, direction, mood]. [PALETTE as materials and light, not hex]. [AMBIENT LIFE].
Calm area at [WHERE CAPTIONS LIVE] described as part of a continuous scene filling the frame edge to edge
(soft shadow, receding depth, a smooth surface). Cinematic, photorealistic, 16:9. No text, no logos, no lettering anywhere.
```
**Armadilha do espaço negativo:** nunca peça "empty darkness/void" para reservar lugar de texto; o modelo pinta painéis pretos. Descreva a área calma como parte do mundo. Assunto centralizado: dizer que ele "bissecta o quadro, mesma distância das bordas" e proibir objetos e brilhos fortes nas laterais. (Vale também para as imagens estáticas do site.)

Vídeo (imagem → vídeo, 1080p, ~6 s, sem áudio):
```
One continuous shot, no cuts. [SUBJECT] [JOURNEY VERB: pours, descends, approaches, assembles] from [START] to [END]
along [EXPLICIT TRAJECTORY]. The [SUBJECT] stays alive: [SMALL NATURAL MOTION]. The scene stays alive: [AMBIENT LIFE].
[IF BOUNDARY: the physical lens moment]. The shot ends at rest: [FINAL FRAME fully described, why it feels arrived].
No text or lettering anywhere.
```
Gerar em 1080p (4K só multiplica custo; a web recomprime). Pessoa real: só com foto e consentimento dela, usada como referência de personagem e inspecionada por semelhança.

## Pipeline com gates (economia de crédito)

1. **Storyboard aprovado antes de gerar** (gate mais barato): o que o visitante vê, as batidas (faixas) com o texto exato, o quadro final.
2. **Custo antes:** `get_cost`/`estimate_*` grátis no modelo planejado; dizer o preço.
3. **Quadro inicial** (barato). Inspecionar: marcas registradas contrabandeadas, anatomia, composição, **coerência de marca** (cor, materiais, detalhes assinatura da história). Mostrar ao usuário.
4. **Escolha do modelo de vídeo com números reais:** consultar a MESMA tomada em 2 ou 3 modelos (Higgsfield, muapi Veo/Kling/Seedance, Figma Weave); a diferença já mediu ~5x entre topo e intermediário. Usuário escolhe.
5. **Vídeo.** Inspecionar quadros (início, meio, fim) e o repouso do final objetivamente:
   `ffmpeg -i raw.mp4 -vf "tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG" -f null -` (a cauda da curva precisa cair).
6. **Gate do usuário:** ele assiste antes de qualquer montagem. Crítica honesta + custo de um novo take. Três falhas no mesmo conceito: trocar o conceito, não o prompt.
7. **Final ruim? Corte a cauda** antes de pagar outro take: `ffmpeg -i raw.mp4 -t 4.3 ...` no último quadro estável (a página usa progresso, não segundos).
8. **Encode de scrub** (keyframe a cada 8 quadros, senão o scrub engasga):
   `ffmpeg -i raw.mp4 -c:v libx264 -crf 18 -preset slow -g 8 -keyint_min 8 -pix_fmt yuv420p -movflags +faststart -an assets/hero-scrub.mp4`
   Detalhe agitado (partículas, textura) aceita crf 25-26 e `-vf scale=1728:-2`; gradiente suave faz degrau: crf mais baixo. Mexer uma variável por vez, avaliar fazendo scrub.
9. **Pôster e quadro final:**
   `ffmpeg -i assets/hero-scrub.mp4 -frames:v 1 -q:v 2 assets/hero-poster.jpg` e `ffmpeg -sseof -0.1 -i assets/hero-scrub.mp4 -update 1 -frames:v 1 -q:v 2 assets/hero-final.jpg` (o final é o hero estático do celular e um ótimo asset para outra seção).
10. Brutos e cópias de revisão **fora** da pasta publicada.

### Jornada encadeada (15 a 20 s)
Segmentos de 6 s: o quadro final do segmento N (PNG qualidade cheia, `-q:v 1`) vira o quadro inicial do N+1 (Higgsfield: `media_upload` → PUT → `media_confirm`). Prompt do próximo continua mesma direção, velocidade e luz; segmentos do meio terminam em movimento, só o último repousa. **Lei da costura:** textura fina não atravessa gerações; colocar cada costura dentro de movimento, desfoque ou virada de luz. Unir os brutos num encode único (`concat` no `-filter_complex` + flags de scrub); costura visível: `xfade` de 0,25 s. Hero de ~1000vh.

## Montagem: `templates/scrub/` (testado)

`scrub.js` + `scrub.css` + `exemplo.html`. O que o motor já resolve:
- Vídeo baixado como **Blob** (funciona em hospedagem sem HTTP Range), transmitido atrás de um **anel de progresso** com **watchdog** de 20 s; o pôster pinta primeiro.
- Tempo **interpolado** num loop rAF **normalizado por dt** (mesma sensação em 60 e 120 Hz) que **descansa** ao convergir e fora da tela.
- **Seeks travados** (um por vez, só o mais novo pendente, saída de deadlock no `error`).
- Escritas no DOM **só quando mudam** (opacidade e `--k` com tolerância).
- **Faixas** `data-band="a,b"` com platô e rampas suaves; a 1ª abre montada no carregamento; `data-ramp` ajusta a montagem sem mexer no código; `data-split` quebra o título em palavras com deslocamentos de **semente fixa**.
- **5 portões do hero estático**, idênticos no CSS e no JS e **vivos** (girar/redimensionar/ligar reduced motion arma e desarma): celular ≤ 720px, tablet em retrato, retrato com toque, celular deitado, reduced motion. No estático, nem vídeo nem pôster são baixados; o quadro final entra por `background` CSS sob a media query e só a faixa `data-static` aparece.
- **Completo sem vídeo:** erro ou timeout → `is-failed`, pôster fica e as faixas continuam funcionando.
- Testado no Chromium: tempo do vídeo acompanha o scroll (0 → 6 s), nenhum byte de vídeo no celular/reduced motion, página completa com o vídeo bloqueado, portão vivo ligando o scrub ao alargar a janela.

## Testes obrigatórios
- `exemplo.html` adaptado servido por HTTP (via `file://` o fetch é bloqueado e o estático aparece: é o recuo desenhado).
- `teste-flick.js <url> ".scrub" "[data-band]"`: batidas legíveis por 5+ flicks de 120px e nenhuma pulável em 360px.
- `auditar-contraste.js` com o texto das faixas, em 3 posições de scroll (pior quadro).
- Playwright: celular com `hasTouch` (portões reais), `reducedMotion`, `route('**/*.mp4', abort)`.
- Capturas de tela de camada de vídeo promovida podem sair em branco no headless: verificar pelo DOM (`currentTime`, opacidades), não por pixel.
