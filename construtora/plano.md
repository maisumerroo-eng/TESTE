# Plano: Meridiano Construtora v2 (demo)

> Aprovação do usuário: direção pedida em 21/11/2026 ("objeto-herói adaptado ao nicho, estrutura e estratégias da Vexter, gráficos interativos, número grande colorido, planejar antes"). Marca e números fictícios.

## 1. Premissa e oferta
- Premissa: **luz** (a casa certa nasce da luz do terreno).
- Oferta única: **estudo solar do terreno**, selo **Gratuito**.
- Qualificação no CTA final: lotes em Campinas e região a partir de 450 m².

## 2. Objeto-herói
- Objeto: maquete branca da casa na palma da mão, sol rasante desenhando a sombra da casa sobre a mão (Figma, node 3:2).
- Composição: hero escura (#1a1816); mão entra pela direita e invade a borda inferior; título à esquerda; fusão com `mix-blend-mode: lighten`.
- Celular: objeto embaixo, centralizado, menor; título acima com gradiente de leitura.
- Ambiente: **luz do sol atravessando brises** (ripas inclinadas, faixa de luz varrendo devagar), máscara diagonal.
- Prova na 1ª dobra: 2 cartões de vidro com número metálico: "14 meses · prazo médio de obra" e "2,1% · desvio médio de orçamento" (rótulo "Casas entregues · média ilustrativa").
- Título com trecho colorido: "Casas de alto padrão desenhadas pela *luz do seu terreno*."

## 3. Vexter → Meridiano (função, não forma)
| Vexter | Estratégia | Meridiano |
|---|---|---|
| Mão + moeda, pergunta-dor | o que está em jogo + dor | mão + maquete ao sol, ganho nomeado |
| Barras douradas ondulando | ambiente do nicho (gráfico vivo) | luz atravessando brises (arquitetura) |
| Cartões R$ 500 mil / R$ 100 mil | prova antes do pedido | prazo médio e desvio de orçamento |
| Faixa "Um pouco do que a Vexter faz" com ícones | amplitude/domínio | 9 competências com ícones isométricos próprios |
| Placas com aba + lista de serviços + efeito por placa | escopo + tipo de contrato | 3 frentes com aba, lista de serviços, efeitos planta/cronograma/cotas |
| Número gigante + antes/depois + gráfico acumulado | prova quantificada | "14 meses" + gráfico interativo previsto x realizado por etapa; "R$ 0 fora do memorial" + antes/depois |
| Rota com odômetro, ícones e entregas | redução de risco | estudo solar 3D da maquete com odômetro, ícones de etapa, selo Gratuito |
| "Do dado à direção" + 7 valores escalonados | manifesto em transformação | "Da luz à casa." + 7 valores com ícones |
| Carrossel de 14 artigos | autoridade/SEO | 6 guias com perguntas reais de quem constrói |
| CTA com qualificação + contatos | conversão | formulário curto → WhatsApp + contatos |
| Rodapé 4 colunas + wordmark 2 camadas com feixe | assinatura final | idem com "MERIDIANO" |

## 4. Mapa de seções
| # | Seção | Componente | Ícones | Interação | Fundo vivo |
|---|---|---|---|---|---|
| 1 | Hero | objeto-herói, prova, btn3d, perfil | — | perfil troca textos | brises |
| 2 | Competências | faixa-icones (arrastável) | 9 | arrastar, setas | marquee lento |
| 3 | Frentes | placas com aba + servicos | — | hover nos serviços | fx-planta / fx-barras / fx-cotas |
| 4 | Resultados | num-g + grafico + ad | — | hover/toque/teclado no gráfico, legenda liga/desliga | — |
| 5 | Um dia na obra | estudo-solar-3d + odo | 4 (etapas) | scroll controla o sol | sol/sombras |
| 6 | Da luz à casa | valores escalonados | 7 | — | traço que cresce |
| 7 | Guias | carrossel de conteúdo | — | arrastar | — |
| 8 | Perguntas | details | — | abrir/fechar | — |
| 9 | CTA | form-wa + btn3d + contatos | — | formulário monta WhatsApp | — |
| 10 | Rodapé | 4 colunas + wm | — | — | feixe uma vez |

## 5. Gráfico
- Previsto x realizado (meses) por etapa da Casa Pátio: Projeto 3/3 · Aprovação 2/1,8 · Estrutura 4/3,8 · Vedação e instalações 3/3,2 · Acabamento 2/2 → total 14/13,8. Interação: hover, foco por teclado e toque mostram os dois valores; legenda liga/desliga série; tabela para leitor de tela.

## 6. Metas de densidade (referência: Vexter)
ícones ≥ 20 usos · hovers ≥ 25 · keyframes ≥ 12 · palavras ≥ 1.400 · links ≥ 40.

## 7. Assets e custo
| Asset | Ferramenta | Custo |
|---|---|---|
| Objeto-herói | Figma generate_image | 1 geração Figma |
| Ícones (13) | SVG gerado por código | 0 |
| Estudo solar 3D | Three.js procedural | 0 |
| Imagens dos guias | crops das 5 existentes | 0 |

## 8. Riscos
- Mão gerada: conferida (dedos ok). 3D sem WebGL/reduced motion: mantém o desenho 2D existente.
