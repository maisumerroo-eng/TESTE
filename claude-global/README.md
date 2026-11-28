# claude-global

Configuração global do Claude Code deste usuário. O setup do ambiente na nuvem copia isto para `~/.claude/` em toda sessão nova.

- `CLAUDE.md`: núcleo curto (carrega em todo turno). Regras universais e roteador por assunto.
- `skills/regras-*`: regras por assunto. Só o nome e a descrição pesam por turno; o corpo carrega quando o assunto aparece.
- Também copiadas do repo: `.claude/skills/{operacao-site,evolucao-ia,site-hibrido-ia}` e `.claude/agents/*.md`.

Para mudar uma regra: editar aqui, commitar, e a próxima sessão já pega. No computador local, copiar manualmente:
```
cp claude-global/CLAUDE.md ~/.claude/CLAUDE.md
cp -r claude-global/skills/* .claude/skills/{operacao-site,evolucao-ia,site-hibrido-ia} ~/.claude/skills/
mkdir -p ~/.claude/agents && cp .claude/agents/*.md ~/.claude/agents/
```
