---
name: site-scroll-produto
description: Cria landing page de produto com animação cinematográfica no scroll (estilo Apple / reels de webdesigner) — produto gira, explode ou se monta conforme o usuário rola. Gera imagem e vídeo do produto com IA (fal.ai por padrão, Open Higgsfield ou Higgsfield MCP como alternativa), quebra o vídeo em frames e liga ao scroll com canvas + GSAP ScrollTrigger. Use quando pedirem "site animado", "site igual reel", "produto girando no scroll", "landing de produto premium".
---

# Site de produto com animação no scroll

Pipeline: **imagem do produto → vídeo curto → frames → canvas ligado ao scroll → resto da página → deploy**.

## 0. Briefing (perguntar só o que faltar)
- Produto e marca. **Só marca do usuário ou fictícia** — nunca publicar site imitando marca real.
- Foto real do produto? (melhor resultado: partir de foto real, fundo limpo)
- Movimento desejado: girar 360°, explodir (grãos/peças voando), abrir embalagem, câmera orbitando, líquido caindo.
- Provedor de mídia (ver passo 1).

## 1. Gerar mídia — escolher provedor

| Provedor | Como | Quando |
|---|---|---|
| **fal.ai** (padrão) | `scripts/gerar.mjs` via API REST, chave `FAL_KEY` | Automático pelo Claude, paga por uso, mesmos modelos (Kling, Veo, Seedance, Nano Banana) |
| **Open Higgsfield** | Interface web open-source, usuário gera e salva o mp4 em `media/` | Usuário prefere UI própria / self-host. Não tem MCP nem CLI: Claude não dirige |
| **Higgsfield MCP** | `mcp__Higgsfield__generate_image` / `generate_video` | Se o conector estiver autorizado; tem presets próprios (Marketing Studio, câmeras) |

Se `FAL_KEY` faltar: chamar `request_credential` para host `queue.fal.run` (header `Authorization`, prefixo `Key`). Nunca pedir chave no chat.

### Imagem base (keyframe)
```bash
node .claude/skills/site-scroll-produto/scripts/gerar.mjs imagem \
  --modelo fal-ai/nano-banana \
  --prompt "pacote de café premium, fundo preto, luz de estúdio, centralizado, 16:9" \
  --saida media/keyframe.png
# com foto real: --modelo fal-ai/nano-banana/edit --imagem caminho/ou/url
```

### Vídeo a partir da imagem
```bash
node .claude/skills/site-scroll-produto/scripts/gerar.mjs video \
  --modelo fal-ai/kling-video/v2.1/master/image-to-video \
  --imagem media/keyframe.png \
  --prompt "câmera orbita 180° lentamente ao redor do produto, grãos de café explodem em câmera lenta, fundo preto estável, sem cortes" \
  --saida media/produto.mp4
```
Regras de prompt para vídeo de scroll:
- **Câmera contínua, sem cortes**, fundo estável e liso (preto/cor da marca) — facilita encaixar na página.
- 5–10 s. Movimento lento e uniforme (scroll amplifica tranco).
- Produto centralizado o tempo todo.
- Gerar 2–3 variações e escolher (custo baixo).
- Modelos mudam rápido: conferir IDs atuais em fal.ai/models antes (buscar "image-to-video").

## 2. Vídeo → frames
```bash
bash .claude/skills/site-scroll-produto/scripts/frames.sh media/produto.mp4 public/frames 30 1600
```
Gera `public/frames/0001.webp…` + `public/frames/manifest.json`. Alvo: 90–180 frames, ≤ 8 MB total. Mobile: gerar segundo set com largura 900 em `public/frames-m`.

## 3. Página
Copiar `template/index.html` como ponto de partida (canvas fixo + GSAP ScrollTrigger + preload + `prefers-reduced-motion`). Depois aplicar as skills, nesta ordem:
1. `frontend-design` / `site-sem-cara-de-ia` / `site-de-10k` — direção visual, tipografia, paleta da marca.
2. MCP `21st` (`get_inspiration`, `search`) e MCP `shadcn` — seções de apoio (features, CTA, footer).
3. `choreograph` + `animate` — textos que entram em sincronia com os frames (marcadores por progresso do scroll).
4. `animation-performance` — canvas só redesenha quando frame muda; nada de animar layout.
5. `mobile-native` — `100svh`, sem zoom em input, toque.
6. `impeccable` + `web-design-guidelines` — auditoria final de acessibilidade/UX.

## 4. Verificar
- Abrir com Chrome DevTools MCP (ou Playwright), rolar e tirar screenshots em 3 pontos do scroll, desktop e iPhone.
- Lighthouse: LCP < 2.5 s. Primeiro frame deve aparecer antes do preload completo.

## 5. Publicar
Vercel MCP (`create_project` / `create_deployment`) ou Artifact. Passar o link ao usuário.

## Qualidade — notas
- Qualidade vem do **modelo** (Kling/Veo/Seedance), não da interface. fal.ai, Open Higgsfield e Higgsfield rodam os mesmos modelos → resultado bruto equivalente.
- Higgsfield tem extras proprietários (presets de câmera, Soul, Marketing Studio) que os outros não têm.
- Para produto com rótulo/texto legível: partir de **foto real** + image-to-video; text-to-video deforma logotipo.
