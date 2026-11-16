# Limites concretos e o que destrava cada um

| tema | situação hoje | como destravar |
|---|---|---|
| **Cenas de anime** | O estúdio **não baixa episódios** nem contorna DRM/paywall. Usa mídia que você fornece ou que tem licença (PVs/trailers oficiais com permissão, artes promocionais liberadas, material próprio). | Coloque os arquivos em `assets/` e registre a fonte/licença em `assets/sources.yaml` (vai para a descrição). |
| **Image-to-video com IA** | Higgsfield está conectado mas **precisa de autorização** (conector do claude.ai). Geração gasta créditos → só com seu OK. | Autorizar o Higgsfield nas configurações de conectores e me dizer o orçamento. O motor já anima painéis em 2.5D localmente sem custo. |
| **Música do Flow Music** | Não há conector oficial. Há o MCP pago de terceiro (useapi.net, US$15/mês) — não assinado. | Exporte a música do Flow e me envie o arquivo (mp3/wav) + letra. |
| **Content ID** | Nenhuma garantia contra reivindicação. Material de terceiros pode ser reivindicado. | Priorizar material autorizado; descrição já tem créditos e aviso. |
| **Rotoscopia / motion tracking avançado** | Recorte por profundidade (Depth Anything) e parallax 2.5D funcionam; rotoscopia quadro a quadro de vídeo não está ligada (CPU lenta). | Possível com SAM2/GPU ou via ferramenta externa. |
| **After Effects / DaVinci / Blender** | Não disponíveis na nuvem. Pipeline é 100% código (FFmpeg + OpenCV). | Blender MCP funciona só no seu computador com o Blender aberto. |
| **GPU** | Ambiente só CPU: render ~7–9 min por música de 3 min. | — |
| **Ambiente efêmero** | O container da sessão some: código e configs ficam no git; mídia/vídeos grandes **não** vão pro git. | Baixe os outputs ao final de cada produção. |
