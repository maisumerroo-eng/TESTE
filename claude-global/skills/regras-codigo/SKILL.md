---
name: regras-codigo
description: Regras de economia e qualidade para programação, debug, git, terminal e deploy. Carregar no início de qualquer tarefa de código, bug, commit, PR, build ou deploy.
---

# Regras: código

## Antes de mexer
1. Entender o pedido em 1 frase. Se tiver 2 leituras possíveis e elas mudarem o código, perguntar.
2. Achar o ponto exato com Grep (nome de função, texto da tela, classe CSS). Não abrir pasta inteira.
3. Ler só a região relevante (offset/limit). Arquivo de 2000 linhas não se lê inteiro.
4. Ver convenção do projeto (nome, estilo, lib já usada) e seguir. Não trazer lib nova sem motivo.
5. Bug: reproduzir primeiro. Sem reprodução, sem conserto "no escuro".
6. Busca ampla em muitos arquivos: subagente Explore, que devolve só a conclusão.

## Escrevendo
7. Mudança mínima. Não renomear, reformatar ou "melhorar" o que não foi pedido.
8. Edit com trecho único; Write só para arquivo novo ou reescrita total.
9. Não reler o arquivo depois de editar: o Edit já falharia se não aplicasse.
10. Várias edições independentes: mandar na mesma mensagem.
11. Comentário só onde o porquê não é óbvio. Nada de comentário narrando o óbvio.
12. Sem código morto, sem console.log esquecido, sem TODO sem dono.
13. Segredo nunca no código nem no commit. Variável de ambiente ou secret do ambiente.
14. Tratamento de erro onde a falha é provável (rede, arquivo, entrada do usuário), não em todo lugar.

## Terminal
15. Comando longo ou repetido vira script em arquivo (scratchpad ou `scripts/`).
16. Saída grande: filtrar com `| tail`, `| head`, `grep`. Nunca despejar log inteiro no contexto.
17. Servidor ou watcher: em background, e matar no fim.
18. Instalar dependência só se não existir equivalente já instalado. Fixar versão.
19. `rm`, `reset --hard`, `push --force`: só com confirmação.

## Testes
20. Rodar o teste do que mudou, não a suíte inteira, a não ser que seja rápida.
21. Teste falhou: ler a primeira falha, não todas. Corrigir a causa, não o teste.
22. Nunca desativar, pular ou afrouxar teste para ficar verde.
23. UI: testar no navegador (Playwright), 1440 e 390px, zero erro de console.

## Git
24. Branch de trabalho, nunca direto na main sem pedido.
25. Commit pequeno, mensagem em português no imperativo, dizendo o quê e por quê.
26. `git status` antes de commitar; não commitar `.env`, build, cache, screenshots de trabalho.
27. Push rejeitado: fetch + merge, nunca force.
28. PR só quando pedido.

## Deploy
29. Conferir build local antes. Depois do deploy, abrir a URL e confirmar que carregou.
30. Erro em produção: logs primeiro (runtime errors), hipótese depois.

## Entrega
31. Dizer o que mudou (arquivo:linha), como foi testado e o que ficou pendente. Máximo 6 linhas.
32. Se algo não foi testado, dizer que não foi.
