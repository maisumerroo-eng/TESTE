# Anúncio Skull (reels 1080×1920, 22 s)

- `fonte.html` → animação (GSAP, timeline pausada). `build.py` injeta o logo e gera `anuncio.html`.
- `render.js` grava quadro a quadro com Playwright (30 fps). `trilha.sh` sintetiza a trilha (drone + kick 120 bpm, drop em 6 s).
- Montagem: `ffmpeg -framerate 30 -i frames/%04d.jpg -i trilha.wav -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -shortest skull-anuncio.mp4`

Agenda e textos são exemplo — trocar pelos reais.
