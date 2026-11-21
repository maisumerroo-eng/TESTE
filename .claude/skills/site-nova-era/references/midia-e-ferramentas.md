# Mídia e ferramentas: imagens, vídeo, voz e Figma

## Status verificado (21/11/2026)

| Recurso | Como o Claude acessa | Status | O que faz |
|---|---|---|---|
| **Figma** | MCP `Figma` | conectado; plano Starter com assento **View** | arquivo do projeto, imagem por IA (`generate_image`), ícone/logo vetorial (`generate_vector_illustration`), shader, upload de assets, exportar animação em MP4 (`export_video`), modelos Weave (`weave_find_model`/`weave_run_model`). Gasta créditos de IA do Figma. Assento View pode bloquear edição: testar no 1º uso; se bloquear, o usuário precisa de assento Full/Dev |
| **ElevenLabs** | MCP `ElevenLabs` (restrito) + host `api.elevenlabs.io` | conectado | voz (TTS), design de voz, transcrição. Vozes pt-BR disponíveis, incluindo vozes próprias da conta. Música/efeitos/imagem/vídeo: só no conector completo (`https://api.elevenlabs.io/v1/mcp`, adicionar em Settings → Connectors) |
| **muapi** | host `api.muapi.ai` (credencial injetada pelo proxy) | conectado; **saldo US$ 0** | +1300 endpoints: imagem (gpt-image-2.6, Midjourney v7/v8, Flux, Seedream, Nano Banana, Qwen), vídeo (Veo 3, Kling, Seedance, Sora 2, Runway, Wan), remover fundo, upscale, expandir imagem, lipsync, música (Suno), 3D |
| **Higgsfield** | MCP `Higgsfield` | conectado; plano free, ~0,25 crédito | imagem, vídeo, Marketing Studio, remover fundo, upscale. Sem crédito na prática |
| **Openverse** | HTTP sem chave | ok | busca em Flickr, Wikimedia e outros com filtro de licença |
| **Wikimedia Commons** | HTTP sem chave (exige User-Agent) | ok | fotos domínio público/CC |
| **Unsplash / Pexels / Pixabay** | HTTP com chave | **sem chave** (401) | bancos de foto. O usuário cria a chave grátis e salva nas configurações do ambiente (Unsplash usa `Client-ID`, Pexels usa a chave pura e Pixabay usa parâmetro de URL: formatos que o formulário de credencial não cobre) |
| **Logos de marcas** | MCP `21st` → `search_logo` | ok, grátis | SVG de logos (svgl.app) para parceiros/integrações, com permissão |
| **Lovable** | MCP `Lovable` | conectado | gera CSS e imagens (fluxo da skill `site-hibrido-ia`) |
| **Higgsfield 3D Jutsu** | MCP `Higgsfield` (`scene_builder_3d_*`) | conectado; **montar/editar/renderizar cena é grátis** | modelagem 3D por Python e exportação GLB (ver `3d.md`) |
| **Poly Haven** | HTTP sem chave (`api.polyhaven.com`) | ok | modelos, texturas PBR e HDRIs CC0 |
| **Blender** | MCP `blender` | só no computador do usuário com Blender aberto | modelagem 3D completa |

Status muda: antes de gerar, confirme com 1 chamada barata (`Higgsfield balance`, `GET https://api.muapi.ai/api/v1/account/balance`, `Figma whoami`, `ElevenLabs creative_list_voices`).

## Regras de custo

1. Toda geração paga: estimar antes (`estimate_only` no ElevenLabs, `estimate_*_cost` no Higgsfield, custo do modelo no Weave) e **pedir ok do usuário** com o valor.
2. Nunca repetir uma chamada de geração para "tentar de novo": cobra duas vezes. Esperar o resultado ou consultar o status.
3. Gerar poucas imagens-chave bem dirigidas, não dezenas aleatórias.

## Figma: o hub de todo projeto (sempre)

Todo site tem um arquivo Figma. Fluxo:
1. `whoami` → pegar o `planKey`; carregar a skill `/figma-create-new-file` se existir; `create_new_file` (design) com o nome do cliente.
2. `create_session` com o fileKey e reutilizar o `sessionId` em todas as chamadas.
3. Antes de `use_figma`, carregar a skill `/figma-use` (ou o recurso `skill://figma/figma-use/SKILL.md` via ReadMcpResource).
4. Páginas do arquivo:
   - `00 DNA` moodboard, referências, prompt-mestre de imagem
   - `01 Tokens` cores, tipografia, espaçamentos (variáveis)
   - `02 Assets` imagens geradas, ícones vetoriais, logo
   - `03 Telas` screenshots do site em 390 e 1440 (via `upload_assets`) para revisão e comentários do cliente
   - `04 Reel` quadros/animação do vídeo
5. Imagens: `generate_image` (modelos `gpt-image-2.5-flare` padrão, `gpt-image-2.5-sunburst`, `gemini-3.1-flash-image`, `gemini-3.1-flash-lite-image`). A resposta traz `image.url` em resolução cheia: baixar com curl para `assets/img/` e converter para WebP/AVIF.
6. Ícones e logo: `generate_vector_illustration` com `kind: "icon"` (glifo) ou `"illustration"` (cena); exportar SVG para `assets/icons/`. Todos no mesmo prompt de estilo.
7. Fundo animado/textura: `create_shader` quando o efeito couber num shader; senão canvas no site.
8. Animação de abertura ou vinheta: animar no Figma e `export_video` (MP4).
9. Modelos de vídeo (Veo, Kling etc.) dentro do Figma: `weave_find_model` → `weave_run_model`.

Se o Figma bloquear por assento ou crédito: avisar o usuário e seguir com muapi/Higgsfield/Lovable, registrando os assets na página `02 Assets` depois (upload).

## Imagens: ordem de preferência

1. **Fotos reais do cliente** (sempre melhores para confiança).
2. **Geradas** com prompt-mestre fixo (ver abaixo): Figma → muapi → Higgsfield → Lovable.
3. **Bancos públicos**: `templates/buscar-imagens.js "<busca em inglês>" 6 assets/img/banco --orient=wide`. Só licenças comerciais e editáveis (CC0, domínio público, CC BY, CC BY-SA). Gera `creditos.md`. CC BY/BY-SA exige crédito visível no site (rodapé ou página "Créditos"). Qualidade irregular: **olhar cada imagem** (Read) antes de usar; ótimo para textura, fundo, referência de moodboard e placeholder.
4. Nunca usar imagem de busca do Google, Pinterest ou do site analisado.

### Prompt-mestre (manter igual em todas as imagens do projeto)

```
[assunto da cena], [contexto do nicho e região],
fotografia editorial, luz [quente lateral / fria de janela / contraluz dourado], [hora do dia],
paleta [cores do DNA], fundo [escuro/claro] com profundidade, lente 50mm, f/2.8, grão fino de filme,
composição com espaço negativo à [esquerda/direita] para texto, sem texto, sem logos, pessoas reais e naturais
```
Variar só o assunto. Guardar o prompt-mestre na página `00 DNA` do Figma e no `dna.md`.

## Vídeo

| Uso | Como |
|---|---|
| Fundo da hero (loop) | gerar 4 a 6 s (muapi Veo/Kling/Seedance, Higgsfield, ou Weave no Figma) a partir de uma imagem-chave aprovada; exportar ≤ 2 MB, mudo, `playsinline`, `poster`; não carregar com `saveData` |
| Vinheta/abertura | animação no Figma → `export_video` |
| Vídeo do site para o reel | `templates/gravar-reel.js` (grava rolando, 1080x1920) |
| Reel com narração e trilha | `templates/montar-reel.sh video.webm narracao.mp3 [trilha.mp3] video/reel.mp4` (trilha abaixa sob a voz) |
| Legendas no reel | `creative_transcribe_audio` (ElevenLabs) → montar `.srt` → `ffmpeg -vf subtitles=legenda.srt` |

## Voz (ElevenLabs)

1. `creative_list_voices` com `languages: ["pt"]` e filtros (`gender`, `use_cases: ["advertisement"|"social_media"]`, `descriptives`). Escolher a voz pelo tom da marca e dizer qual foi; voice_id só da lista.
2. Roteiro do reel: 15 a 30 s, frases curtas, nome da marca, oferta e chamada final. Tags de direção do `eleven_v4` (`[confiante]`, `[pausa curta]`) com moderação.
3. Fluxo: `creative_create_flow` → `creative_generate_speech` (`model_id: eleven_v4`, `estimate_only: true` primeiro) → ok do usuário → gerar → `creative_get_flow_run_status` até concluir → baixar o áudio.
4. Voz própria da marca: `creative_design_voice` (descrição + frase de teste) → `creative_save_designed_voice`.
5. No site: nunca áudio com autoplay. Voz só em vídeo com controle, ou botão "ouvir" opcional.

## muapi (quando houver saldo)

- Documentação: `https://api.muapi.ai/docs` e `https://api.muapi.ai/openapi.json` (conferir o schema do endpoint antes de chamar).
- Fluxo: `POST https://api.muapi.ai/api/v1/<endpoint>` com JSON (`prompt`, `width`, `height`...) → a resposta traz o id da previsão → `GET /api/v1/predictions/{id}/result` até concluir → baixar as URLs de saída. O OpenAPI não descreve os campos da resposta: na 1ª chamada, imprimir o JSON inteiro e confirmar os nomes antes de automatizar.
- Autenticação injetada pelo proxy: não pedir chave nem colocar chave no código.
- Úteis: `ai-background-remover` (produto sem fundo), `ai-image-upscale`, `ai-image-extension` (expandir para 16:9/9:16), `gpt-image-2.6-*`, `midjourney-v8`, `veo3-fast-image-to-video`, `kling-*`, `seedance-*`, `suno-create-music` (trilha do reel).
