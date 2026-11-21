# Ícones isométricos (o "quase 3D" da Vexter, feito do zero)

Técnica medida na Vexter: SVG à mão em projeção isométrica, **3 tons por objeto + 1 acento**, traço escuro fino, 1 ou 2 linhas de brilho. Leve (um sprite de ~5 KB para 7 ícones), nítido em qualquer tamanho, sem IA, sem crédito.

## Receita
- **Grade:** viewBox `0 0 80 72`. Eixos isométricos: x para a direita-baixo (+20, +12), z para a esquerda-baixo (−20, +12)... na prática, losangos com vértices `(x, y) → (x+20, y−12) → (x+56, y+1) → (x+36, y+13)` para o topo de uma placa, e a lateral descendo 7px.
- **Tons** (tokens da marca): topo claro (`--iso-top`), lateral escura (`--iso-side`), frente média (`--iso-front`), acento da marca no topo da peça principal (`--iso-accent`) e sombra do acento (`--iso-accent-dark`). Traço `--iso-stroke` 1,6px, `stroke-linejoin: round`.
- **Brilho:** 1 ou 2 traços curtos na cor clara do acento sobre a face de topo (`stroke-linecap: round`).
- **Empilhamento:** objetos feitos de camadas (placas, blocos, folhas) deslocadas 12px na vertical: é o que dá a sobreposição "quase 3D".
- **Sprite:** todos os ícones como `<symbol id>` num arquivo (`assets/icons/<marca>.svg`) usados com `<svg viewBox="0 0 80 72"><use href="assets/icons/marca.svg#nome"/></svg>`; ou inline no HTML quando forem poucos (evita requisição).
- **Animação discreta:** traço do acento que se desenha na entrada, ou a peça de topo que sobe 2px no hover do card pai.
- Mesma família: todos com a mesma grade, tons e traço. Um ícone fora do padrão quebra o sistema.

## Metáforas por nicho (exemplos)
Construtora: lote com sol, pilha de plantas, estrutura de pilares, chave, régua/nível, janela, bloco de concreto, cronograma (barras), capacete, guindaste, casa, escudo (garantia).
Contabilidade: pilha de documentos, moeda com seta, calculadora, caminhão, cubos trocando (reforma), escudo.
Clínica: frasco, espelho, gota, agenda, mão, folha.

Exemplo completo pronto: `templates/componentes/icones-meridiano.svg` (12 ícones de construtora).
