#!/usr/bin/env bash
# Instala tudo que o estúdio KAGE.EXE precisa (Linux/macOS com Python 3.10+ e FFmpeg com libass).
set -euo pipefail
cd "$(dirname "$0")"

command -v ffmpeg >/dev/null || { echo "Instale o FFmpeg (com libass): apt install ffmpeg | brew install ffmpeg"; exit 1; }

pip install -q librosa soundfile scipy opencv-python-headless pyloudnorm faster-whisper pyyaml pillow numpy
# separação de voz (Demucs) e profundidade 2.5D (Depth Anything) — PyTorch CPU
pip install -q torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -q demucs transformers

# fontes da marca (SIL Open Font License, Google Fonts) — o render usa brand/fonts direto;
# instalar no sistema ajuda o libass a achar tudo.
mkdir -p ~/.fonts && cp brand/fonts/*.ttf ~/.fonts/ && (fc-cache -f >/dev/null 2>&1 || true)

python3 -c "import librosa, cv2, faster_whisper, demucs, transformers; print('estúdio pronto')"
