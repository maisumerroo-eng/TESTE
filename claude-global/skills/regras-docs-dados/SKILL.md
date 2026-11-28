---
name: regras-docs-dados
description: Regras para planilhas, documentos, slides, PDFs, dashboards e análise de dados (Google Drive, Docs, Notion, Canva, artifacts). Carregar antes de criar ou editar documento, planilha, apresentação ou gráfico.
---

# Regras: documentos e dados

## Escolha do formato
1. Texto que outras pessoas vão editar: documento (Claude Docs, Google Docs, Notion).
2. Coisa para olhar ou usar (painel, explicação visual, app): artifact.
3. Arquivo pedido explicitamente (.xlsx, .docx, .pptx, .pdf): skill do formato.
4. Planilha para preencher ou calcular: Spreadsheet/artifact com banco; não arquivo solto.

## Economia
5. Arquivo grande: ler a estrutura primeiro (abas, colunas, 5 linhas), não o arquivo inteiro.
6. Calcular com script (Python/pandas), não "de cabeça" no texto.
7. Gráfico: carregar a skill `dataviz` antes. Um gráfico, uma mensagem.
8. Documento longo: esqueleto com seções primeiro, depois preencher seção por seção.

## Qualidade
9. Número sempre com fonte (arquivo, aba, linha ou consulta).
10. Nunca inventar dado para "completar" tabela. Vazio = `—` ou `PENDENTE`.
11. Datas em DD/MM/AAAA, moeda em R$ com 2 casas, separador brasileiro.
12. Antes de sobrescrever arquivo do usuário: ler e confirmar.
13. Compartilhar, publicar ou mandar por e-mail: confirmar antes.

## Entrega
14. Link do documento + 1 linha do que tem nele. Não colar o documento no chat.
