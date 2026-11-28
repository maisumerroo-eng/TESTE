---
name: regras-midia
description: Regras para gerar imagem, vídeo, áudio, voz e 3D com IA (Lovable, Figma, Higgsfield, ElevenLabs, Canva, Blender) gastando menos crédito e token. Carregar antes de qualquer geração de mídia.
---

# Regras: mídia

## Crédito
1. Geração gasta crédito: confirmar antes de lote grande ou vídeo longo. Estimar custo quando a ferramenta tiver estimativa.
2. Nunca repetir chamada de geração para "tentar de novo" sem decidir: cada chamada cobra.
3. Testar o prompt com 1 imagem antes de gerar 20.
4. Rodízio de workspaces do Lovable: ver `site-hibrido-ia` passo 3.
5. Higgsfield precisa estar autorizado nos conectores do claude.ai. Sem autorização: Lovable ou Figma.

## Prompt de imagem
6. Uma direção de arte fixa, repetida igual em todo prompt (luz, paleta, fundo, lente, grão).
7. Descrever a peça/produto igual em todos os prompts; trocar só a variável (cor, pose).
8. Sem texto, sem logo, sem marca real na imagem: dizer isso no prompt.
9. Anti cara de IA: 1 pessoa por cena, "candid, 35mm film, natural skin texture, slightly wrinkled fabric, not symmetrical".
10. Variar etnia e idade entre produtos quando houver modelo.
11. Foto de produto real: pedir edição fiel (mesma peça, textura, cor), removendo etiqueta de terceiros.

## Depois de gerar
12. Inspecionar antes de usar: folha de contato (`montage`) e não abrir imagem por imagem no contexto.
13. Conferir: logo de terceiros, mãos e anatomia, cor batendo com o catálogo.
14. Comprimir (JPEG q78, 2000px hero, 1200px resto).
15. Guardar o prompt que funcionou em Aprendizados da skill do projeto.

## Vídeo e áudio
16. Vídeo: roteiro e quadros-chave aprovados antes de gerar.
17. Voz (ElevenLabs): voice_id só da lista ou do usuário; nunca de memória.
18. Esperar job com a ferramenta de espera, não com polling curto.

## 3D
19. Blender só no computador do usuário, com o Blender aberto.
