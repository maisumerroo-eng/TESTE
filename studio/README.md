# KAGE.EXE STUDIO 影

Produtora automatizada de videoclipes de **rap geek/anime**. Você entrega a música (gerada no Google Flow),
o estúdio entrega o pacote para o YouTube: vídeo 1080p editado no ritmo, legendas dinâmicas + SRT,
áudio masterizado (-14 LUFS), thumbnail, título/descrição/tags e relatório de QC.

```
python3 studio.py new musica.mp3 --char sasuke --hook "Ódio e Sharingan" --lyrics letra.txt --track 01
#   coloque a mídia em projects/<projeto>/assets/{clips,images,manga}
python3 studio.py produce 01-sasuke-odio-e-sharingan
```

## O que cada etapa faz

| etapa | módulo | o que faz |
|---|---|---|
| `master` | `mastering.py` | high-pass, limpeza de lama, presença vocal, de-esser, compressão leve, loudnorm 2 passadas -14 LUFS / -1 dBTP, 48 kHz. Corta silêncio morto do início/fim. **Não** mexe em timbre, pitch ou voz. |
| `analyze` | `audio_analysis.py` | BPM, batidas, compassos (downbeat), kick/snare/hats por banda, curva de energia, seções (intro/verso/pré/refrão/ponte/final por novidade + repetição do refrão), drops, pausas. |
| `lyrics` | `lyrics_sync.py` | Demucs isola a voz → Whisper (palavra a palavra) → alinhamento com a **letra oficial** (`input/lyrics.txt`), tolerante a erro de pronúncia. Texto vem da letra = sem erro de português. |
| `subs` | `subtitles.py` | ASS dinâmico: palavra aparece quando é cantada, palavra-chave na cor do personagem com brilho, pulso no kick, refrão no centro, **palavra de impacto** gigante no drop. + SRT limpo. |
| `ingest` | `assets.py` | corta vídeos em planos (detecção de cena), recorta painéis de mangá, mede movimento/brilho, gera *contact sheets* para etiquetar. |
| `plan` | `planner.py` | o "diretor": cortes no grid de batidas com ritmo por seção, cena casada com a letra, speed ramp/slow/reverse, transições, receitas de drop variadas, eventos sincronizados. |
| `sfx` | `sfx.py` | impactos, whoosh e zaps sintetizados (próprios), mixados baixo sob a música. |
| `render` | `renderer.py` + `fx.py` | motor próprio (OpenCV→FFmpeg, multiprocesso): parallax 2.5D com profundidade (Depth Anything), painel de mangá animado, shake, zoom punch, RGB split, aberração cromática, glitch, flash, impact frame, linhas de velocidade, raios, brasas, light leak, ondas de choque, grão, scanlines, grade de cor do personagem, HUD/cartela/end card. |
| `thumb` | `thumbnail.py` | 1280x720: personagem recortado por profundidade, texto gigante atrás, rim light na cor dele, selo do canal. |
| `meta` | `metadata.py` | título no padrão do canal, descrição com capítulos, letra, créditos e aviso; tags e hashtags. |
| `qc` | `qc.py` | resolução, FPS, codecs, duração, telas pretas, congelamentos, loudness, true peak, repetição de cena, plano parado, sobreposição de legenda, alinhamento da letra, thumbnail. |

Etapas avulsas: `python3 studio.py <etapa> <projeto>` · preview rápido: `python3 studio.py preview <projeto> --from 40 --to 55`.

## Estrutura

```
studio/
  studio.py               CLI
  setup.sh                instala dependências
  configs/brand.yaml      identidade, padrões de áudio/vídeo, padrão de título
  configs/characters/     paleta, kanji, elemento (raio/vazio/corte/ki), palavras→tags por personagem
  brand/                  logo, avatar, banner, vinheta, prancha de estilo, fontes (OFL)
  pipeline/               módulos acima
  tools/                  geradores de música/mídia de teste (procedurais, sem direitos de terceiros)
  docs/                   ROTEIRO.md (roteiro manual), IDENTIDADE.md, LIMITES.md
  projects/<projeto>/
    project.yaml          personagem, hook, faixa, thumbnail, fps, modelo do whisper
    input/                música + lyrics.txt (*palavra* = destaque)
    assets/               clips/ images/ manga/ panels/ assets.yaml sources.yaml scenes.yaml
    work/                 análise, stems, timeline, legendas .ass, profundidade, chunks
    output/               .mp4, _thumb.jpg, .srt, _youtube.md/.json, _qc.json
```

## Novo personagem

Copie `configs/characters/sasuke.yaml`, troque cores (`primary/secondary/dark/accent`), `kanji`,
`element` (`lightning | void | slash | ki | fire`) e `tag_map` (palavra da letra → tags de cena).

## Desempenho (CPU, 4 núcleos)

Render ≈ 4x o tempo da música (3 min → ~12 min, incluindo encode final). Demucs ~1 min/música, Whisper small ~15 s.
Vídeo final H.264 CRF 18, teto 24 Mbps (≈ 500 MB por 3 min — o grão de filme pesa).
