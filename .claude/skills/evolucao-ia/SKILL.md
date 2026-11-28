---
name: evolucao-ia
description: Escada de 5 níveis do usuário de IA (perguntas, prompts, contexto, agentes, sistemas). Use quando o usuário perguntar em que nível está, como subir de nível, pedir para transformar uma tarefa em prompt, skill, agente ou fluxo automático, ou disser "nível 2/3/4/5". Diagnostica o nível da tarefa e entrega o próximo degrau pronto.
---

# Evolução do usuário de IA

| Nível | Nome | O que muda | Artefato que fica |
|---|---|---|---|
| 1 | Faz perguntas | IA como Google | nada |
| 2 | Escreve prompts | resultado bom na 1ª | prompt salvo |
| 3 | Domina o contexto | IA já sabe quem você é | CLAUDE.md, pasta de referência |
| 4 | Cria agentes | delega um processo inteiro | skill ou subagente (`.claude/`) |
| 5 | Orquestra sistemas | vários agentes rodando sozinhos | pipeline + gatilho + checkpoint |

Regra de ouro: cada nível **gera um arquivo**. Se nada ficou salvo, o usuário não subiu de nível.

## Como agir

1. **Diagnostique** pela tarefa, não pela pessoa: "isso hoje é nível N porque…". Uma linha.
2. **Entregue o próximo degrau pronto**, não uma aula:
   - 1→2: reescreva o pedido no esqueleto abaixo e salve em `prompts/<tarefa>.md`.
   - 2→3: extraia o que se repete (marca, tom, público, regras) para o CLAUDE.md do projeto ou `referencias/`. Máximo 50 linhas no CLAUDE.md; o resto vai para arquivos lidos sob demanda.
   - 3→4: transforme em skill (`.claude/skills/<nome>/SKILL.md`) ou subagente (`.claude/agents/<nome>.md`). Use `anthropic-skills:skill-creator` se disponível.
   - 4→5: encadeie skills/agentes num fluxo com fases, handoff por arquivo, gatilho (agendamento, webhook) e checkpoint humano. Modelo pronto: skill `operacao-site`.
3. **Teste** o artefato uma vez com dado real e ajuste.

## Esqueleto de prompt (nível 2)
```
Papel: você é <especialista>.
Tarefa: <verbo> <entrega> (quantidade).
Contexto: <negócio, público, objetivo, restrições>.
Formato: <estrutura, tamanho, tom>.
Exemplo: <1-2 exemplos do resultado bom>.
Não faça: <erros comuns>.
```

## Anatomia de agente (nível 4)
- Um agente, um trabalho. Nome = verbo + objeto (`escreve-copy`, `testa-site`).
- `description` diz **quando** usar (é o gatilho).
- Entradas e saídas por arquivo com caminho fixo.
- Ferramentas mínimas. Modelo mínimo que resolve (haiku para mecânico, sonnet para texto, opus para decisão).
- Termina com checklist de autoteste.

## Anatomia de sistema (nível 5)
- **Fases** com entrada e saída em arquivo (`docs/briefing.md` → `docs/ref.md` → código → `docs/qa.md`).
- **Paralelo** onde não há dependência (visual, copy e estrutura juntos).
- **Checkpoint humano** só onde decisão importa (briefing aprovado, entrega final).
- **Gatilho**: agendamento (`create_trigger`), webhook, ou o usuário digita um comando.
- **Métrica**: tempo, tokens, erros. Anote em `Aprendizados` da skill para o próximo ciclo.
