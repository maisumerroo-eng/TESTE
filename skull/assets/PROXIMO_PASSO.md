# Próximo passo: vídeo das regras com a caveira gesticulando (Higgsfield)

Pedido do usuário: a caveira do vídeo `skull/skull_regras.mp4` precisa **gesticular mais, ser móvel de verdade**
(braços/mãos mexendo enquanto explica), mesma voz e personalidade, 3D realista.

## Material pronto
- `caveira_sofa.png` — caveira (óculos escuros, camiseta preta larga, corrente dourada, copo preto com caveira dourada)
  sentada no sofá vermelho numa balada preta e dourada, neon de caveira atrás. Imagem aprovada pelo usuário.
- `voz_regras.mp3` — locução final (voz ElevenLabs "Skull - Caveira Grave", acelerada), 24,0 s:
  "Ô rapaziada, presta atenção nas regras da SKULL! Primeira: arma branca, faca, arma de fogo, nem pensar, não entra!
  Segunda: nada de futebol, nada de torcida organizada. Ninguém quer cair no soco, né? Terceira: nem tenta entrar sem
  nome na lista! Tá tudo certinho? Então vem curtir com nós!"
- `beat_phonk_regras.mp3` — beat de fundo (deixar baixo, abaixar quando a voz entra).
- `logo_skull.png` — logo SKULL Lounge & Nightclub.
- `regras_editor.html` — editor em canvas usado na versão atual (legendas palavra a palavra, cards das regras,
  check verde, cartão final 11.12 Espaço Terraço Goiânia). Tempos das palavras estão no array `C`.

## Plano com Higgsfield
1. Image-to-video / avatar falante com `caveira_sofa.png` + `voz_regras.mp3` (lip sync), prompt pedindo
   gesticulação expressiva: contar 1-2-3 nos dedos nas regras, mãos pra cima "calma" no soco, apontar pra câmera,
   braços abertos no "vem curtir". 9:16, até 30 s.
2. Remontar por cima as legendas, cards das regras, beat baixo e cartão final (mesmo visual de `skull_regras.mp4`).
