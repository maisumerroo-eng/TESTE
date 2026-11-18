---
name: showreel-marca
description: Cria showreel de identidade visual (brand reveal) em vídeo com HyperFrames — logo sendo desenhado em traço, wordmark, ícone montando, mockups de produto, fotos recortadas pelo símbolo, posts de redes sociais, tagline e assinatura final. Estilo dos reels de designers que entregam marca "100% com Claude + Hyperframes". Use quando pedirem "showreel", "apresentação de marca em vídeo", "brand reveal", "vídeo da identidade visual", "reel do branding".
---

# Showreel de marca (Claude + HyperFrames)

Base técnica: skills `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use` (já neste projeto). **Ler `/hyperframes` primeiro** — ele tem o contrato de render. Esta skill só define o roteiro e o padrão visual.

Só marca do usuário/cliente ou fictícia. Nunca recriar identidade de marca real de terceiros.

## Insumos (pedir o que faltar)
- Nome da marca, logo em **SVG** (essencial: o traço animado depende dos paths), paleta, fonte.
- Tagline (1 frase).
- 3–6 imagens: mockups de produto, fotos de pessoas/lifestyle, posts. Se não houver, gerar (ver "Mídia").
- Formato: 1920×1080 (padrão, como mostrado na tela do PC) ou 1080×1920 (reel direto).

## Roteiro padrão (~30–40 s, 30 fps) — uma sub-composição por cena
| # | Cena | Tempo | Técnica |
|---|---|---|---|
| 1 | Fundo escuro, linhas guia surgem | 0–3 s | `stroke-dashoffset` em linhas finas |
| 2 | Wordmark desenhado em contorno (outline + pontos de bézier visíveis) | 3–7 s | SVG paths, `drawSVG`-like via dashoffset, pontos em `circle` com stagger |
| 3 | Corte para fundo claro: logo completo (símbolo + nome) | 7–10 s | wipe/cut seco, fill entra depois do traço |
| 4 | Palavra-conceito grande em tipografia (ex.: "iluminação") deslizando | 10–13 s | kinetic type, track horizontal |
| 5 | Símbolo construído em wireframe → preenchido | 13–17 s | grid de construção + morph para fill |
| 6 | Mockups de produto (embalagens) | 17–22 s | parallax/push-in suave, sombras |
| 7 | Foto de pessoa + logo lado a lado | 22–25 s | split layout |
| 8 | Fotos **mascaradas pelo símbolo** | 25–28 s | `clip-path`/`mask` com o SVG do símbolo |
| 9 | Posts de Instagram entrando | 28–32 s | cards com stagger, leve rotação 3D |
| 10 | Tagline em texto pequeno central | 32–35 s | fade + tracking |
| 11 | Assinatura: símbolo + nome, hold final | 35–38 s | hold ≥ 1,5 s |

Música: trilha ambiente/minimal + SFX nos cortes (ver `hyperframes` → `references/sound.md`).

## Padrão visual
- Paleta da marca, no máximo 3 cores + neutros. Contraste alto entre cena escura (abertura) e clara (revelação).
- Easing: `power3.out` em entradas, `power2.inOut` em movimentos de câmera; nada de bounce em marca premium.
- Movimento lento e confiante; cada cena com 1 ideia só.
- Tipografia: wordmark da marca + 1 sans neutra para textos de apoio (`@font-face` em `assets/fonts/`).

## Fluxo
1. Ler `/hyperframes`, depois `references/types/launch.md` e `references/motion.md`.
2. `npx hyperframes init <pasta> --skip-skills --skill=hyperframes` (via launcher: `node .claude/skills/hyperframes/scripts/plugin-cli.mjs ...`).
3. Colocar logo SVG, fontes e imagens em `assets/`.
4. Montar uma sub-composição por cena do roteiro (variáveis para textos/cores/imagens).
5. Procurar blocos prontos antes de fazer à mão: `/hyperframes-registry` (títulos, kinetic type, transições).
6. `check --json` → corrigir; `snapshot --review` → olhar quadros-chave.
7. Preview para o usuário aprovar → `render` → MP4.
8. Para o reel "gravado da tela": opcional, compor o MP4 sobre a filmagem de um monitor, ou só exportar 1080×1920 com título no topo.

## Mídia (mockups e fotos)
Ordem de preferência:
1. Material real do cliente.
2. `/media-use` (HeyGen ou ferramentas locais grátis).
3. Higgsfield MCP (se autorizado) ou fal.ai via `.claude/skills/site-scroll-produto/scripts/gerar.mjs imagem` (Nano Banana / GPT Image para mockups de embalagem com o logo aplicado — passar o logo como `--imagem` com modelo `.../edit`).

## Combina com
- `site-scroll-produto`: mesmo mockup/vídeo vira o site animado.
- `frontend-design`, `impeccable`: direção visual antes de animar.
