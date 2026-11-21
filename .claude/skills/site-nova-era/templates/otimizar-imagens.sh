#!/usr/bin/env bash
# otimizar-imagens.sh: gera AVIF + WebP em larguras responsivas e imprime o <picture> pronto.
# Uso: bash otimizar-imagens.sh <imagem ou pasta> [saida=assets/img/opt] [larguras="640 1280 1920"]
# Não amplia: larguras maiores que o original são puladas. Qualidade visual alta (AVIF crf 30, WebP q 80).
set -euo pipefail
IN="${1:?imagem ou pasta}"
OUT="${2:-assets/img/opt}"
WIDTHS="${3:-640 1280 1920}"
mkdir -p "$OUT"

processa() {
  local f="$1" base w0 h0 srcavif="" srcwebp="" maior=0
  base=$(basename "${f%.*}")
  IFS=x read -r w0 h0 < <(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x "$f")
  for w in $WIDTHS; do
    [[ $w -gt $w0 ]] && continue
    ffmpeg -nostdin -y -v error -i "$f" -vf "scale=$w:-2:flags=lanczos" -c:v libaom-av1 -still-picture 1 -crf 30 -cpu-used 6 "$OUT/$base-$w.avif"
    ffmpeg -nostdin -y -v error -i "$f" -vf "scale=$w:-2:flags=lanczos" -c:v libwebp -quality 80 "$OUT/$base-$w.webp"
    srcavif+="$OUT/$base-$w.avif ${w}w, "; srcwebp+="$OUT/$base-$w.webp ${w}w, "; maior=$w
  done
  if [[ $maior -eq 0 ]]; then  # original menor que todas as larguras: mantém o tamanho
    maior=$w0
    ffmpeg -nostdin -y -v error -i "$f" -c:v libaom-av1 -still-picture 1 -crf 30 -cpu-used 6 "$OUT/$base-$w0.avif"
    ffmpeg -nostdin -y -v error -i "$f" -c:v libwebp -quality 80 "$OUT/$base-$w0.webp"
    srcavif="$OUT/$base-$w0.avif ${w0}w, "; srcwebp="$OUT/$base-$w0.webp ${w0}w, "
  fi
  local h=$(( h0 * maior / w0 )) antes depois
  antes=$(stat -c %s "$f"); depois=$(stat -c %s "$OUT/$base-$maior.avif")
  echo "<!-- $base: $((antes/1024)) KB original -> $((depois/1024)) KB avif ${maior}px -->"
  cat <<EOF
<picture>
  <source type="image/avif" srcset="${srcavif%, }" sizes="100vw">
  <source type="image/webp" srcset="${srcwebp%, }" sizes="100vw">
  <img src="$OUT/$base-$maior.webp" width="$maior" height="$h" alt="[descrever]" loading="lazy" decoding="async">
</picture>
EOF
}

if [[ -d "$IN" ]]; then
  find "$IN" -maxdepth 1 -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' \) | sort | while read -r f; do processa "$f"; done
else
  processa "$IN"
fi
echo "<!-- imagem do LCP (hero): trocar loading=\"lazy\" por fetchpriority=\"high\" e ajustar sizes -->"
