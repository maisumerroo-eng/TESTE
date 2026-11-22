# Imagem → HTML (print, mockup ou design do cliente)

Filtrado da skill pública "img2html" (análise por camadas, uma imagem por vez, estados de hover) e completado com o que ela não tinha: **medição** de cores e **loop de verificação** por comparação de pixels.

## Quando usar (pensamento crítico)
- **Sim:** o design é **do cliente** (mockup no Figma, export do Lovable, print do site antigo dele, desenho de designer contratado) e precisa virar código fiel; ou o site antigo existe só como imagem.
- **Não:** recriar pixel a pixel o site de terceiros. Referência de outra marca é para extrair princípios (`casos/`), nunca copiar.
- Fidelidade total é o objetivo só na **fase de conversão**. Depois, o site passa pelas fases da skill e sobe de nível (régua mínima, estratégias, acessibilidade): a cópia fiel é ponto de partida, não entrega.

## Processo (uma imagem por vez, do começo ao fim)
1. **Medir antes de escrever:** `python3 templates/paleta-da-imagem.py print.png` → tokens de cor reais. Fontes: identificar família por forma (serifa, largura, terminações) e confirmar no Google Fonts; tamanhos pela proporção em relação à largura da imagem.
2. **Analisar em camadas:**
   - estrutura: seções, contêineres, grid/flex, alinhamentos, espaçamentos (anotar em px relativos à largura);
   - visual: cores, tipografia, ícones, imagens, bordas, sombras, gradientes, efeitos;
   - componentes: header, navegação, cards, botões, campos, tabelas, selos, e os **estados** implícitos (hover, foco, ativo);
   - responsivo: como a composição se reorganiza no celular (decidir e anotar, a imagem não mostra).
3. **Construir** com o `templates/base/` (HTML semântico, tokens em `:root`, BEM ou classes por componente, Flex/Grid, CSS separado), reaproveitando `templates/componentes/` quando o elemento existir lá. Dados dinâmicos com conteúdo marcado como exemplo, nunca inventado como real.
4. **Verificar com números, não com olho:** `node templates/comparar-imagem.js <url> print.png diff --alvo=0.9`
   - mostra a semelhança (% de pixels quase iguais), a diferença média e **em que faixa da altura** está o erro, e gera o mapa em vermelho;
   - corrigir a faixa com mais vermelho, comparar de novo; parar ao atingir a meta (90% é um bom alvo para mockup; textos reescritos e fontes substitutas baixam o número sem ser erro).
5. **Próxima imagem** só depois da atual atingir a meta. Imagens do mesmo site compartilham `style.css` e componentes; nomes de arquivo pelo conteúdo (`servicos.html`, `contato.html`).

## Avisar o usuário (limites honestos)
- Fonte exata pode não existir no Google Fonts: usar a mais próxima e dizer qual.
- Efeitos sem técnica visível (blur, textura, 3D) são aproximados.
- Interações além de hover/foco precisam ser descritas pelo usuário.
- A imagem não mostra o celular: a versão mobile é decisão nossa, mostrada para aprovação.
