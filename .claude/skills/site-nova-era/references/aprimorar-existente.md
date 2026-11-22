# Aprimorar um site que já existe

Use quando o cliente já tem site (nosso, de outra agência, Wix, WordPress, Lovable, HTML antigo) e quer subir de nível sem perder o que já funciona (posição no Google, links, conteúdo, marca).

## 1. Raio-x (só leitura, sem tocar em nada)
| Ferramenta | Mede |
|---|---|
| `templates/analisar-site.js <url>` | estrutura, libs, fontes, cores, seções, screenshots desktop/mobile |
| `templates/regua-minima.js <url>` | piso Vexter (13 parâmetros) + teto de performance |
| `templates/auditar-site.js <url>` | LCP, CLS, peso, imagens, código não usado, SEO, a11y (prioridade P1→P3) |
| `templates/auditar-contraste.js <url> 390` e `1440` | contraste do pior pixel |
| `templates/gate-texto.py <pasta>` (se houver código) | clichês, travessões, emojis |
| `templates/comparar-densidade.js <ref> <url>` | acabamento contra a referência do nicho |
| `templates/paleta-da-imagem.py <screenshot>` | paleta real em uso |
Mais: anotar URLs que recebem tráfego/posicionam (Search Console do cliente se houver acesso, senão as páginas que aparecem no Google para a marca e para o serviço+cidade), formulários, integrações (pixel, analytics, chat), domínio e hospedagem.

Exemplo real (Bravo, loja deste repositório, 22/11/2026): régua reprovada em 12/13, peso inicial 2,6 MB, LCP mobile 3,7 s, 33 links/botões sem nome acessível, 53 imagens JPG/PNG sem dimensões, sem og:image/canonical/JSON-LD, 1 travessão no admin.

## 2. Diagnóstico para o cliente (o que manter, o que mudar)
Relatório curto, priorizado:
- **Manter:** marca, URLs que posicionam, conteúdo que converte, integrações que funcionam.
- **Corrigir já (P1):** erros, acessibilidade, quebra de layout, LCP/CLS.
- **Subir de nível:** o que falta da régua mínima e das estratégias (`estrategias-de-conversao.md`): objeto-herói, prova no topo, ícones, gráficos, momento-assinatura, personalização.
- Antes/depois esperado em números (régua, LCP, peso, contraste).

## 3. Escolher o caminho (pergunta clicável ao usuário)
| Caminho | Quando | Como |
|---|---|---|
| **Evolução no lugar** (recomendado quando o código é acessível e razoável) | site em HTML/JS, React, Lovable, WordPress com tema editável | manter a stack do cliente; adaptar componentes da skill para ela; mudanças em lotes pequenos, cada lote medido |
| **Refazer na skill preservando o que vale** | código ruim, stack sem saída, ou redesign total pedido | fases normais da skill (estratégia → plano → construção) + **mapa de redirecionamento 301** de todas as URLs antigas, mesmos títulos/metas onde já posicionam, mesmo domínio, analytics e pixels reinstalados |
| **Plataforma fechada** (Wix, Shopify, Webflow) | cliente quer continuar nela | aplicar o que a plataforma permite: conteúdo, imagens otimizadas, SEO, seções e código customizado; Wix tem skills próprias (`wix:wix-manage` e afins); não prometer o que a plataforma não deixa |
| **Só existe imagem** (sem acesso ao código, ou cliente mandou print/mockup) | recriar a partir de screenshots | `references/imagem-para-html.md`, depois subir de nível |

## 4. Executar em lotes medidos
Ordem de maior retorno: (1) erros e acessibilidade P1 → (2) imagens (`otimizar-imagens.sh`, width/height, AVIF/WebP, LCP com `fetchpriority`) → (3) fontes e CSS/JS crítico → (4) texto (gate, posicionamento, prova no topo, CTA único) → (5) componentes e estratégias que faltam para a régua → (6) momento-assinatura e personalização.
Cada lote: diff pequeno, teste só do que mudou (`economia.md`), medir de novo, commit separado (fácil de reverter).

## 5. Provar o ganho
- Tabela antes/depois: régua mínima, LCP/CLS mobile, peso, contraste, nº de problemas P1/P2.
- Screenshots lado a lado (mesma largura, mesma seção) e, se o cliente quiser, reel "antes → depois" (`gravar-reel.js` nas duas versões + `montar-reel.sh`).
- SEO: conferir que nenhuma URL antiga ficou sem destino (404) e que títulos/metas que posicionavam continuam.

## Regras
- Nunca apagar conteúdo que posiciona sem plano de substituição/redirecionamento.
- Nunca trocar a stack do cliente sem ele pedir.
- Mudanças em produção só com ok do usuário; preferir branch/preview.
- O site aprimorado também precisa passar na régua mínima (exceção só se o cliente pedir escopo menor, registrada no `plano.md`).
