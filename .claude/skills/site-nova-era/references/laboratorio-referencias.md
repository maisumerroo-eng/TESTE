# Laboratório de referências virais (função do imagem → HTML)

Para alimentar a skill com o que está viralizando em Reels/TikTok (páginas hiperpersonalizadas, demos por prospect, scroll cinematográfico), reconstruir **em estudo privado** algumas páginas de referência a partir de screenshots, entender como funcionam e devolver **técnicas e componentes próprios** à biblioteca.

## Regras (não negociáveis)
- **Estudo, não entrega.** A reconstrução de página de terceiros fica no scratchpad, fora do repositório e fora de qualquer publicação. Nunca vai para cliente, preview público, portfólio ou reel.
- **Do estudo sai só o que é genérico:** padrão de layout, mecânica de interação, ritmo, estratégia de conversão, técnica de personalização. Texto, marca, imagens, ícones e código da referência não entram na skill nem em sites de cliente.
- O que for devolvido é **reescrito do zero** e testado (`templates/componentes/`), com o crédito da inspiração em "Fontes incorporadas" do `SKILL.md`.
- Ativação: só quando o usuário pedir para estudar referências (regra do modo imagem → HTML).

## Processo
1. **Achar as referências:** reels que o usuário mandar (melhor fonte) + busca (WebSearch: "hyper-personalized landing page", "personalized demo website for prospect", "página personalizada para cliente reels", nichos do momento). Abrir o link do reel com web-fetch para pegar o site citado na legenda/comentários. Escolher 3 a 5 páginas com técnicas diferentes.
2. **Capturar:** `node templates/analisar-site.js <url> <scratchpad>/lab/<nome>` (screenshots desktop/mobile + stack, animações, data-attributes). Se só houver vídeo, extrair quadros do reel com ffmpeg.
3. **Reconstruir em estudo** com `references/imagem-para-html.md` (paleta medida, análise em camadas, `comparar-imagem.js` até ~85%): reconstruir é o jeito mais rápido de entender proporções, espaçamentos e a ordem dos elementos.
4. **Ficha da técnica** em `references/casos/lab-<nome>.md`: o que a página faz, que estratégia cumpre, como a personalização acontece (parâmetro de URL, dados do lead, IA, geolocalização), o que a torna "viral" (o primeiro segundo do reel), pontos fracos, e a **versão genérica** proposta.
5. **Devolver à skill:** componente original testado + linha em `estrategias-de-conversao.md`/`megapersonalizacao.md` + fonte registrada. Apagar a reconstrução do scratchpad.

## Padrões já mapeados do "hiperpersonalizado" (pesquisa de 22/11/2026)
- **Página por prospect** (demo feita para um lead, com nome, logo, cores e fotos dele): implementado em `templates/prospect/` (ver `pagina-por-prospect` em `megapersonalizacao.md`).
- **Troca de texto por parâmetro de URL** (campanha, cidade, nicho): `personaliza.js`.
- **Conteúdo por origem, dispositivo, horário e retorno:** `personaliza.js`.
- **Vídeo personalizado por lead** (ex.: gravação de tela do site do prospect com narração): possível com `gravar-reel.js` + ElevenLabs (`midia-e-ferramentas.md`); usar só com dados públicos do negócio.
