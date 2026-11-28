---
name: operacao-site
description: Operação nível 5 para criar sites e lojas com o mínimo de tokens. Orquestra fases com handoff por arquivo, subagentes baratos em paralelo (referência, copy, QA), a skill site-hibrido-ia para visual (Lovable/Figma) e scripts prontos de QA e compressão. Use quando o usuário pedir "site", "loja", "landing", "operação de site", "fluxo completo" ou quiser produzir sites em série com pouco custo.
---

# Operação Site (nível 5)

Princípio: **o chat não é memória, o arquivo é.** Cada fase lê um arquivo e escreve outro. Subagente devolve no máximo 10 linhas; o detalhe fica no disco. Nada é refeito do zero: scripts e templates são reaproveitados.

## Mapa

```
F0 briefing ──► [CHECKPOINT 1: usuário aprova docs/briefing.md]
      │
      ├─► F1a ref-estrutura (haiku)  → docs/ref.md
      ├─► F1b Lovable/Figma visual   → assets/css, assets/img   (site-hibrido-ia passos 2-4)
      └─► F1c copywriter (sonnet)    → docs/copy.md
                 │ (as 3 em paralelo)
F2 montagem (sessão principal) → HTML + JS lendo ref.md + copy.md
F3 qa-site (haiku) → scripts/qa.mjs → docs/qa.md (só falhas)
F4 correção (só o que qa.md listou) → repete F3 até 0 falhas, máx 2 voltas
      ▼
[CHECKPOINT 2: screenshots + link de preview]
F5 deploy + commit + aprendizado
```

Pasta de trabalho: `<projeto>/` na raiz do repo. `docs/` e `referencias/` dentro dela.

## F0 Briefing (1 mensagem)
Copie `templates/briefing.md` para `<projeto>/docs/briefing.md` e preencha com o que o usuário já disse. Pergunte **só** o que falta e muda o resultado (marca, referência, público, páginas, contato real). Não invente telefone, CNPJ, preço ou depoimento: campo vazio vira `PENDENTE`.

## F1 Paralelo (mesma mensagem, 3 chamadas)
- `Agent(subagent_type: "ref-estrutura")`: URL da referência → `docs/ref.md`. Se o tipo não existir na sessão, use `web-fetch` pedindo só a estrutura, e grave você.
- Visual: siga `site-hibrido-ia` passos 2 a 4 (Lovable com rodízio de workspaces; Figma `generate_image` de reserva; Higgsfield se autorizado). Dispare e **não fique fazendo poll**: cheque `get_project` só ao final da F2.
- `Agent(subagent_type: "copywriter")`: `docs/briefing.md` + `docs/ref.md` (se já existir) → `docs/copy.md`.

## F2 Montagem
Sessão principal. Estrutura e JS como em `site-hibrido-ia` passo 5. Leia `ref.md` e `copy.md`, nunca o site de referência de novo. Use `Grep` para achar trechos, não `Read` de arquivos inteiros já conhecidos.

## F3 QA
`Agent(subagent_type: "qa-site")` ou direto:
```
cd <projeto> && python3 -m http.server 8123 >/dev/null 2>&1 &
node $S/scripts/qa.mjs http://localhost:8123 index.html categoria.html produto.html
```
`$S` = pasta desta skill: `.claude/skills/operacao-site` no repo, ou `~/.claude/skills/operacao-site` global.
Saída: `docs/qa.md` com falhas (overflow horizontal, erro de JS, imagem quebrada, emoji, travessão, clichê) e screenshots em `docs/shots/`. Sem falha = 1 linha "OK".

## F4 Correção
Corrija **só** o listado em `qa.md`. Rode F3 de novo. Máximo 2 voltas; o que sobrar vira pendência na entrega.

## F5 Entrega
- Imagens: `python3 $S/scripts/comprimir.py <projeto>/assets/img`.
- Deploy: `vercel.json` com `outputDirectory` = pasta do projeto (Vercel via conector) ou `deploy_project` do Lovable.
- Commit na branch de trabalho, push.
- Resposta caveman: links, o que cada IA fez, créditos gastos, pendências.
- **Aprendizado**: 1 a 3 linhas em `site-hibrido-ia` › Aprendizados. É isso que faz o sistema melhorar sozinho.

## Economia de tokens (obrigatório)
| Regra | Por quê |
|---|---|
| Handoff por arquivo, subagente responde ≤10 linhas | contexto principal não incha |
| Modelo por tarefa: haiku (busca, QA), sonnet (copy, montagem), opus só para decisão de arquitetura | custo por token cai 5-15x nas fases mecânicas |
| Scripts prontos (`qa.mjs`, `comprimir.py`) em vez de reescrever teste toda vez | zero tokens de geração repetida |
| Lovable: `get_project`, nunca `get_message` em loop | cada poll devolve o prompt inteiro |
| Screenshot a `deviceScaleFactor: 1` para conferência | imagem menor no contexto |
| Uma sessão por site; `/clear` entre sites | sem compressão de histórico |
| MCPs só os da fase (Lovable/Figma na F1, nenhum na F2-F4) | schemas não carregam à toa |
| Tarefa em massa sem raciocínio (alt text, descrições de 200 produtos) | vai para o nível custo zero (abaixo) |

## Nível custo zero (opcional, no computador do usuário)
`free-claude-code` (github.com/Alishahryar1/free-claude-code, AGPL-3.0) é um proxy local que faz o Claude Code usar modelos grátis (NVIDIA NIM, OpenRouter free, Groq, Ollama…). Instalação e uso em `extensoes.md`.
- Use para: lotes repetitivos e baratos (descrições de produto, alt text, traduções, variações de copy).
- Não use para: montagem, decisões de design, nada que precise de ferramenta confiável. Os modelos grátis **não são Claude**, erram chamada de ferramenta e têm limite do provedor.
- Padrão: rode headless num lote (comando em `extensoes.md`) e revise a saída na sessão Claude antes de usar.

## Extensões
Lista curada e verificada com comandos de instalação: `extensoes.md` (ler só quando for instalar algo).
