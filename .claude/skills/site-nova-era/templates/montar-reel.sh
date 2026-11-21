#!/usr/bin/env bash
# montar-reel.sh: junta o vídeo do site (gravar-reel.js) com a narração (ElevenLabs) e, opcional, uma trilha.
# A trilha abaixa sozinha quando a voz fala (ducking). Saída: MP4 H.264 1080x1920 pronto para Reels/TikTok.
# Uso: bash montar-reel.sh video/site.webm narracao.mp3 [trilha.mp3] [saida.mp4]
set -euo pipefail
VID="${1:?vídeo do site (.webm/.mp4)}"
VOZ="${2:?narração (.mp3/.wav)}"
TRILHA="${3:-}"
OUT="${4:-video/reel.mp4}"
mkdir -p "$(dirname "$OUT")"

# duração final = a maior entre vídeo e voz (+0,8 s de respiro); o vídeo congela no último quadro se a voz for maior
DV=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VID")
DA=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VOZ")
DUR=$(python3 -c "print(round(max($DV,$DA)+0.8,2))")

VF="scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,fps=30,tpad=stop_mode=clone:stop_duration=30"

if [[ -n "$TRILHA" ]]; then
  ffmpeg -y -v error -i "$VID" -i "$VOZ" -stream_loop -1 -i "$TRILHA" -filter_complex \
    "[1:a]aresample=48000,apad,volume=1.0,asplit=2[voz][sc];\
     [2:a]aresample=48000,volume=0.35[mus];\
     [mus][sc]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400[duck];\
     [voz][duck]amix=inputs=2:duration=longest:normalize=0,afade=t=out:st=$(python3 -c "print($DUR-1)"):d=1[a];\
     [0:v]$VF[v]" \
    -map "[v]" -map "[a]" -t "$DUR" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$OUT"
else
  ffmpeg -y -v error -i "$VID" -i "$VOZ" -filter_complex \
    "[1:a]aresample=48000,apad[a];[0:v]$VF[v]" \
    -map "[v]" -map "[a]" -t "$DUR" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$OUT"
fi
echo "ok: $OUT (${DUR}s)"
