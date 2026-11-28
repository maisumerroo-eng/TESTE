---
name: regras-pesquisa
description: Regras para pesquisar na web, comparar ferramentas, checar fatos, preços e notícias gastando pouco token. Carregar antes de qualquer pesquisa ou pergunta tipo "qual o melhor", "isso existe", "quanto custa".
---

# Regras: pesquisa

1. Definir a pergunta exata e o que conta como resposta antes de buscar.
2. Buscas independentes: todas na mesma mensagem.
3. WebSearch modo standard primeiro; extended só se vier fraco, velho ou contraditório.
4. Ler página: agente `web-fetch` com a pergunta junto, para voltar só a resposta.
5. Não buscar o que já está no contexto ou na memória da conversa.
6. Fonte primária vence blog: repo oficial, documentação, página do fabricante.
7. Repo do GitHub: conferir dono (forks com nome igual são comuns), licença e data do último commit.
8. Número que varia entre fontes (estrelas, preço, limite): dar faixa e dizer que varia.
9. Dizer o que não foi confirmado. Não preencher buraco com memória.
10. Instagram, Google Docs e páginas com login não abrem: pedir print ou texto colado logo.
11. Resultado longo vai para arquivo; no chat, só a conclusão e a recomendação.
12. Recomendar 1 opção com o porquê, não listar 10 iguais.
13. Sempre terminar com a lista de fontes em link.
