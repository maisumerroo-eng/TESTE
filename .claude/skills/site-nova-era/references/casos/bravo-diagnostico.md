# Caso: Bravo (loja do repositório), diagnóstico de site existente em 22/11/2026

Primeiro uso real do modo `aprimorar-existente.md` (só leitura, nada alterado). Serve de exemplo do formato do diagnóstico.

## Medições
| Ferramenta | Resultado |
|---|---|
| `regua-minima.js` | **reprovada em 12/13**: CSS 362/1550, keyframes 1/57, hovers 27/59, transições 24/91, gradientes 4/87, mask 0/21, clip-path 0/7, SVG 44/223, h3 3/64, palavras 519/1676, variáveis 21/89. Passa em imagens (53) e links (220) |
| Teto de performance | **peso inicial 2.665 KB (estoura 1.500)**; LCP desktop 616 ms, CLS 0,004, CSS 44 KB, bloqueio 0 ms ok |
| `auditar-site.js` (celular 4G, CPU 4x) | LCP 3.700 ms (P2), 2.110 KB (P2), **33 links/botões sem nome acessível (P1)**, 40 imagens maiores que o exibido, 53 JPG/PNG sem AVIF/WebP, 53 sem width/height; sem og:image, canonical e JSON-LD (P3) |
| `gate-texto.py` | 1 travessão em `admin.html` |

## Leitura (o que manter, o que mudar)
- **Manter:** catálogo, fotos de produto e fluxo de checkout pelo WhatsApp (funcionam); identidade visual existente.
- **Corrigir já:** nomes acessíveis nos 33 links/botões; imagens (AVIF/WebP, srcset, width/height, LCP com fetchpriority) derrubam peso e LCP de uma vez.
- **Subir de nível:** estados de hover/foco em todos os cards e botões, animações nomeadas, ícones próprios, texto de autoridade por categoria (guias de caimento/tecido), prova no topo, SEO por categoria (palavra-chave por página), personalização por origem (Instagram).
- **Caminho sugerido:** evolução no lugar (HTML/JS próprio, código acessível), em lotes medidos.

Status: diagnóstico entregue; aprimoramento aguardando ok do usuário.
