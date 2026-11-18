#!/usr/bin/env bash
# Uso: frames.sh video.mp4 pasta_saida [fps=30] [largura=1600]
set -euo pipefail
IN="$1"; OUT="$2"; FPS="${3:-30}"; W="${4:-1600}"
mkdir -p "$OUT"; rm -f "$OUT"/*.webp
ffmpeg -loglevel error -i "$IN" -vf "fps=$FPS,scale=$W:-2:flags=lanczos" -c:v libwebp -quality 72 "$OUT/%04d.webp"
N=$(ls "$OUT"/*.webp | wc -l)
printf '{"count":%d,"pattern":"%%04d.webp"}\n' "$N" > "$OUT/manifest.json"
echo "$N frames, $(du -sh "$OUT" | cut -f1)"
