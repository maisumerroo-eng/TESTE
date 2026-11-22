# Estratégia antes do design (fase obrigatória, entre o DNA e o plano)

O erro mais comum de site feito com IA é pedir "cria um site" de cara: sai bonito e genérico. Aqui a ordem é fixa: **pensar como estrategista, depois escrever, depois rascunhar no celular, só então desenhar.** O resultado desta fase entra no `plano.md` (seção 0) e o texto embarca ao pé da letra na construção.

Entrada: tipo de negócio, cidade/região, público, objetivo do site (agendar, pedir orçamento, comprar, chamar no WhatsApp). Faltando algum, perguntar com opção clicável.

## 1. Análise estratégica do nicho
- **Cliente ideal:** quem decide, quem influencia, momento de vida/empresa, renda/porte.
- **O que move a escolha:** os 3 a 5 critérios reais de decisão (prazo, preço por etapa, confiança, proximidade, especialização).
- **Medos antes de contratar** (o que trava o "sim"): ex. construtora: obra atrasar, orçamento estourar, acabamento diferente do projeto, não conseguir acompanhar. Cada medo vira uma resposta no site (seção, prova, FAQ ou garantia).
- Fonte: voz real do comprador (avaliações, fóruns, Reclame Aqui, Google Maps; método em `megapersonalizacao.md`), nunca suposição apresentada como fato.

## 2. Como buscam (Google e IA) e o que os concorrentes prometem
- **Buscas no Google:** listar 10 a 20 consultas reais do nicho + região (ferramentas: WebSearch, sugestões do Google, "as pessoas também perguntam"). Separar por intenção: informacional ("quanto custa construir casa alto padrão"), comparativa ("construtora ou empreitada"), local/transacional ("construtora alto padrão Campinas").
- **Buscas em assistentes de IA (ChatGPT, Gemini, Perplexity, Claude):** as perguntas saem em frases completas ("qual construtora de alto padrão em Campinas entrega no prazo?"). Para aparecer nas respostas (GEO): fatos verificáveis e citáveis no site (região atendida, serviços, processo, números com fonte), perguntas e respostas diretas em FAQ com `FAQPage`, dados da empresa em `Organization`/`LocalBusiness`, páginas por serviço com resposta objetiva no primeiro parágrafo.
- **Concorrentes do topo:** abrir os 5 primeiros resultados orgânicos e os perfis mais citados. Para cada um: promessa principal, prova usada, oferta de entrada, o que **não** dizem. A lacuna vira o **diferencial** (ex. Meridiano: ninguém começa pelo estudo solar do terreno).

## 3. Posicionamento em uma frase + mapa do site com palavra-chave por página
**Posicionamento** (uma frase, testável): *Para [público] em [região] que [medo/desejo principal], a [marca] é [categoria] que [diferencial], porque [prova real].*
Ex.: Para quem vai construir casa de alto padrão em Campinas e tem medo de obra que atrasa e estoura, a Meridiano é a construtora que começa pelo estudo solar do terreno e fecha preço por etapa antes da obra, com cronograma aberto toda semana.

**Mapa do site** (mesmo que a primeira entrega seja só a home, planejar o resto):
| Página | Palavra-chave principal | Intenção | Objetivo | Link vindo de |
|---|---|---|---|---|
| Home | construtora alto padrão [cidade] | local/transacional | estudo solar (CTA) | todas |
| [Serviço 1] | [termo do serviço + cidade] | transacional | orçamento | home, rodapé |
| [Guia 1] | [pergunta informacional] | informacional | levar ao serviço | home (guias) |
Uma palavra-chave principal por página, sem duas páginas disputando a mesma. Título, H1, meta e URL usam a palavra-chave da página.

## 4. Texto da home, seção por seção (antes de qualquer visual)
- **Título entendido em 3 segundos** (quem, o quê, onde), trecho crítico destacado.
- **Prova perto do topo** (número com fonte, selo, casos), nunca no fim.
- **Um botão claro e o mesmo em toda a página** (WhatsApp, formulário ou agendamento).
- Uma seção por medo/critério de decisão; FAQ com as dúvidas reais e as buscas informacionais.
- Linguagem simples; **sem prometer resultado, sem número inventado** (demo: rotular "ilustrativo").
- Passar o texto no `gate-texto.py` ainda nesta fase. O texto aprovado embarca ao pé da letra; a construção não reescreve.

## 5. Rascunho de layout no celular, seção por seção
Antes do design, para cada seção: **o que aparece na primeira tela do celular (390x844)**, em ordem de leitura, e o que fica para depois da rolagem.
```
[1 Hero — 1ª tela]   kicker (região) · título 3 linhas · 1 frase · botão · 2 cartões de prova
                     objeto-herói logo abaixo (2ª tela)
[2 Competências]     título curto · faixa arrastável (2 itens visíveis + dica de arrasto)
[3 Frentes]          aba da placa 1 · frase-resultado · lista de serviços (3) · foto
...
```
Regras: botão principal visível na 1ª tela; prova antes da 2ª rolagem; nenhum texto essencial dentro de imagem; tocar sem errar (alvos de 44px).

## Saída desta fase (vai para o `plano.md`, seção 0)
Análise (cliente, critérios, medos com resposta) · buscas Google e IA por intenção · tabela de concorrentes e diferencial · frase de posicionamento · mapa do site com palavra-chave por página · texto completo da home aprovado · rascunho de layout no celular. Mostrar ao usuário e pedir ok antes do design.
