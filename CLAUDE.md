# Edição de vídeo: referências antes de editar

Sempre que for editar ou criar vídeo, antes de decidir cortes, efeitos, texto e som, buscar referências e se inspirar nelas (ou usar direto quando couber):

1. **Instagram / TikTok / Shorts virais** do mesmo gênero: ritmo de corte, ganchos dos primeiros 2s, estilo de legenda, trilha e efeitos sonoros em alta.
2. **Higgsfield Katana**: catálogo de presets (`get_preset_instructions` sem preset lista títulos e descrições; `get_presets` com `source: "katana"` abre o catálogo). Usar como referência de linguagem visual de edits. Gerar com Katana só com créditos e com o custo avisado antes.
3. **Higgsfield Viral / Genjutsu / Marketing Studio** (`get_presets`): efeitos e motion em alta.
4. **21st.dev video blocks** (`video_search_blocks`, `video_list_blocks`): títulos animados, transições, overlays (ex.: Chromatic Slam, Shattered Title Assembly, HUD Corners, Scramble Resolve). Usar como inspiração ou renderizar e encaixar no vídeo.

Regras:
- Referência serve de inspiração de técnica, não para copiar o vídeo dos outros.
- Escolher só o que serve ao conteúdo, ao tom e ao público do vídeo.
- Dizer na entrega quais referências e templates inspiraram a edição.

# Gosto da cliente (aprendido nas revisões do reel @anajcilios)

Aplicar por padrão em qualquer conteúdo, sem esperar ela pedir de novo.

**Fluidez acima de tudo**
- Nada de começo tremido: sem rajada de cortes curtos, sem "impacto de zoom" a cada corte. Viral não é caótico.
- Timelapse curto (~6s), um plano só, velocidade constante, aproximação lenta.
- Transições por dissolve (`xfade` fade ~0,5s; `fadewhite` ~0,4s no reveal). Nada de corte seco nem flash branco bruto.
- Fim com fade de vídeo e música juntos.

**Zoom / close**
- Close nunca é corte seco para um recorte. É uma aproximação contínua e suave (easing smoothstep), começando no plano inteiro e chegando no detalhe (olhos, cílios, produto).
- Fazer com `zoompan` sobre a imagem escalada 2x (movimento sub-pixel, sem tremido) + lanczos + unsharp leve.
- Não perder qualidade: com fonte de baixa resolução (ex.: 464x832) o zoom máximo é ~1,45x. Exportar com CRF ~19.
- Se ela disser "tira o zoom", é o zoom bruto ou andando sem propósito. A aproximação suave é o que ela quer.

**Menos informação**
- Um único antes e depois. Sem repetir com tela dividida, segundo ângulo como outro antes/depois, etiquetas demais.
- Cortar gestos e mãos que só servem de transição (dedinho, mão cobrindo a câmera). Trocar por mais tempo e close no que importa (o resultado).
- Usar todos os vídeos que ela mandar para ter mais closes do resultado, sem montar outra comparação.
- Câmera lenta nos closes (fontes de 60fps dão slow-mo limpo).

**Cor e efeito**
- Cor natural no resultado. Sem filtro rosado, sem brilho/glow, sem grade puxado.
- Brilhinhos sutis no reveal podem ficar.

**Música**
- Música contínua do começo ao fim, sem recomeçar nem cortar seco.
- Truque que funcionou: o mesmo trecho toca abafado (lowpass) até o reveal, o filtro abre aos poucos e o drop limpo cai exatamente no reveal.
- Sem som acelerado (chipmunk) de ambiente.
- Remover quadros escuros perto das transições.

**Texto**
- Pouco texto, com as palavras que ela der (ex.: "treinando antes", "o resultado"). Serif itálico elegante + sombra.
- No final, o @ da conta dela (ex.: `@anajcilios`) + "agende seu horário". Não usar título genérico tipo "Lash Designer". Perguntar o @ se não souber.

**Processo**
- Conferir frames e onda do áudio antes de entregar, e avisar o que ela deve ouvir.
- Duração: seguir o que ela pedir. Se uma mudança impedir a duração combinada, avisar e propor como chegar nela.
- O script base da última versão está em `ferramentas/reel_antes_depois.py` para reaproveitar.

# Lições do trailer de terror
- Título não pode estourar a largura: limitar a 1000px e quebrar em duas linhas.
- Footage noturna escura: levantar as sombras (gamma) antes do grade escuro, senão o rosto some.
