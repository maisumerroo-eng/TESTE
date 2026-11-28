---
name: regras-automacao
description: Regras para criar skills, subagentes, fluxos automáticos, tarefas agendadas e integrações (níveis 4 e 5). Carregar quando o usuário quiser automatizar, delegar um processo, criar skill/agente ou agendar algo.
---

# Regras: automação (níveis 4 e 5)

## Decidir o artefato
1. Regra que vale sempre e é curta: CLAUDE.md (núcleo, máximo 50 linhas).
2. Regra de um assunto: skill `regras-*`.
3. Processo com passos: skill (`.claude/skills/<nome>/SKILL.md`).
4. Tarefa isolada e repetível com modelo barato: subagente (`.claude/agents/<nome>.md`).
5. Rodar sozinho no horário: tarefa agendada. Rodar quando algo acontecer: webhook ou assinatura de PR.

## Skill boa
6. `description` diz QUANDO usar, com as palavras que o usuário fala. É o gatilho.
7. Corpo curto; detalhe em arquivos separados lidos sob demanda (`extensoes.md`, `templates/`).
8. Script determinístico (`scripts/`) para tudo que é mecânico. Script testado antes de commitar.
9. Seção "Aprendizados" no fim, atualizada a cada uso.
10. Uma skill, um trabalho. Duas skills que se chamam são melhores que uma gigante.

## Subagente bom
11. Nome verbo + objeto. Ferramentas mínimas. Modelo mínimo (haiku para mecânico).
12. Entrada e saída por arquivo com caminho fixo. Responde no máximo 10 linhas.
13. Proibir no prompt do agente o que ele não deve fazer (ex.: "não corrija, só reporte").

## Sistema (nível 5)
14. Fases com handoff por arquivo; paralelo onde não há dependência.
15. Checkpoint humano só onde a decisão importa.
16. Limite de voltas no ciclo de correção (ex.: 2).
17. Medir: tempo, tokens (`npx ccusage@latest daily`), erros. Anotar em Aprendizados.

## Onde guardar
18. Skills de projeto: no repo (`.claude/`), versionadas no git.
19. Regras globais: `claude-global/` no repo TESTE; o setup do ambiente copia para `~/.claude` em toda sessão nova.
20. Nunca segredo em skill, agente ou script. Chave vai em secret do ambiente.
