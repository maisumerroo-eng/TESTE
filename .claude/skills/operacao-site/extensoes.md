# Extensões reais para a operação de sites

Pesquisado em nov/2026. Contagens de estrelas variam entre fontes; confira o repo antes de instalar. Cuidado com forks com nome parecido: use o dono indicado.

## Já disponíveis nesta conta (não instalar de novo)
| O quê | Para quê na operação |
|---|---|
| Lovable (conector) | CSS + imagens, rodízio de workspaces (F1) |
| Figma (conector) | `generate_image` de reserva (F1) |
| Vercel (conector + `api.vercel.com`) | deploy (F5) |
| Playwright + Chromium pré-instalados | `scripts/qa.mjs` (F3) |
| Skills `frontend-design`, `impeccable`, `site-sem-cara-de-ia`, `site-de-10k`, `web-design-guidelines` | qualidade visual e de texto |
| shadcn MCP, 21st.dev Magic MCP | componentes, se o projeto for React |
| Higgsfield | imagem/vídeo, **precisa autorizar** em claude.ai › conectores |

## Custo zero: free-claude-code
- Repo: `github.com/Alishahryar1/free-claude-code` (licença AGPL-3.0). Não é da Anthropic.
- O que é: proxy local em `http://127.0.0.1:8082` que fala o protocolo da Anthropic e repassa para 60+ provedores (NVIDIA NIM, OpenRouter free, Groq, Cerebras, Cloudflare Workers AI, Ollama, LM Studio).
- Instalar (macOS/Linux, no computador do usuário):
  ```
  curl -fsSL "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/install.sh" | sh
  fcc-server      # sobe o proxy; o log mostra o link da Admin UI
  fcc-claude      # abre o Claude Code apontado para o proxy
  ```
  Na Admin UI: Providers › Add key (ex.: chave grátis da NVIDIA NIM) › Apply. Em Model Config dá para mapear `MODEL_OPUS`, `MODEL_SONNET`, `MODEL_HAIKU`.
- Headless em lote (o proxy expõe endpoint estilo Anthropic, então deve funcionar com a variável padrão do Claude Code; teste com 1 item antes):
  ```
  ANTHROPIC_BASE_URL=http://127.0.0.1:8082 claude -p "Gere alt text curto em PT-BR para cada linha" < lista.txt > alt.txt
  ```
- Limites: os do provedor (mudam sem aviso). Falha pode consumir cota de mais de um provedor no fallback. Respeite os termos de cada provedor.
- Qualidade: modelos grátis erram mais chamada de ferramenta. Só para texto em lote.

## Roteador de modelos: claude-code-router
- Repo: `github.com/musistudio/claude-code-router`. Proxy parecido, com regras por tipo de tarefa (modelo barato para tarefas de fundo, outro para raciocínio).
- Use se quiser misturar Claude pago com modelo barato (ex.: DeepSeek) em vez de só grátis.

## Medir gasto: ccusage
- Repo: `github.com/ryoppippi/ccusage`. Lê os logs locais do Claude Code.
- `npx ccusage@latest daily` e `npx ccusage@latest monthly`. Rode no fim de cada site e anote em Aprendizados.

## Skills e plugins
- Oficiais da Anthropic: `/plugin marketplace add anthropics/skills`. Útil: `webapp-testing` (Playwright), `frontend-design`.
- `github.com/wshobson/agents`: marketplace com dezenas de plugins e subagentes. Instale **um plugin por vez**, só o que a fase usa; cada um custa contexto.
- Listas para garimpar: `github.com/hesreallyhim/awesome-claude-code`, `github.com/jqueryscript/awesome-claude-code`.

## MCPs que valem para sites
- Context7 (`github.com/upstash/context7`): documentação atual de bibliotecas, evita código de API velha.
  `claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp`
- Playwright MCP: `claude mcp add playwright npx @playwright/mcp@latest`. Aqui não precisa, `qa.mjs` já faz o mesmo sem custo de schema.

## Empacotar repo para outra IA: repomix
- `github.com/yamadashy/repomix`. `npx repomix --include "bravo/**/*.html,bravo/**/*.js" --style markdown` gera um arquivo só com contagem de tokens.
- Use para mandar o projeto inteiro ao Lovable ou a outro modelo numa mensagem.

## Regra de instalação
Antes de instalar qualquer coisa: qual fase usa, quanto contexto custa, e se algo já disponível resolve. Na dúvida, não instale.
