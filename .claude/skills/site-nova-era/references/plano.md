# Fase de plano (obrigatória antes de criar qualquer arquivo do site)

Regra: **nenhuma linha de HTML/CSS e nenhuma geração paga antes do `plano.md` escrito e aprovado.** O plano é onde o site é desenhado por inteiro; a construção só executa. Plano fraco = site médio, por mais polida que seja a execução. (Lição da Meridiano v1: passou em todas as auditorias técnicas e ainda ficou abaixo da Vexter porque foi construída sem planejar densidade, objeto-herói, ícones e gráficos.)

## O que o plano decide (preencher `templates/plano.md`)

1. **Premissa e oferta** (do `dna.md`): a palavra/ideia que o site vende e a oferta única com o selo dela ("Gratuito").
2. **Objeto-herói** (`objeto-heroi.md`): o objeto do nicho que representa a promessa, quem segura, luz, material, como invade a borda da hero e para onde vai no celular. Prompt escrito.
3. **Mapa seção a seção**, cada linha com: ato (8 atos), estratégia de venda que cumpre (catálogo em `estrategias-de-conversao.md`), componente que a implementa, texto-chave final, ícones, imagem, número, interação, efeito de fundo.
4. **Inventário de componentes** que a página terá (botão 3D, cartões de prova, faixa de ícones, placas com aba + lista de serviços, número gigante, antes/depois, gráfico interativo, valores escalonados, carrossel de conteúdo, formulário curto, rodapé com wordmark) e quais vêm prontos de `templates/componentes/`.
5. **Sistema de ícones**: lista de 8 a 16 ícones (nome, onde aparece, metáfora), estilo (isométrico 3 tons por padrão, ver `icones-isometricos.md`).
6. **Momento-assinatura**: tipo (SVG fixado, 3D, scrub), o que o scroll controla, versão estática.
7. **Números de prova**: cada número com fonte real (ou rótulo "ilustrativo" em demo) e onde aparece grande e colorido.
8. **Gráficos**: o que cada um prova (antes/depois, acumulado, previsto x realizado), dados, interação (hover/foco/toque mostra valor).
9. **Ambiente e microdetalhes**: o elemento vivo de cada seção (em nível de sussurro), estados de hover previstos, efeitos de fundo por placa.
10. **Régua mínima obrigatória** (`qualidade.md`): como cada parâmetro do piso Vexter será atingido com conteúdo e estados reais, seção por seção.
10b. **Reuso e inovação** (`inovacao.md`): reusos declarados + no mínimo 3 inovações de 2 tipos, checadas contra `portfolio.md`.
11. **Assets e custo**: cada imagem/vídeo/voz/3D com ferramenta, modelo, custo estimado e alternativa grátis. Total.
12. **Personalização**: segmentos, sinais, o que muda por segmento.
13. **Riscos e cortes**: o que sai se faltar dado real ou verba.

## Gate
Mostrar ao usuário um resumo do plano (objeto-herói, mapa de seções, custo) e pedir ok com pergunta clicável. Mudanças grandes depois da aprovação voltam para o plano antes do código.

## Análise de referência dentro do plano
Quando houver site de referência (do cliente ou da régua), o plano inclui a **tabela de estratégias da referência → adaptação ao nicho**: para cada seção da referência, qual estratégia de venda ela cumpre, como o nosso cliente cumpre a mesma estratégia com a metáfora dele (nunca copiando forma literal, texto ou ícone).
