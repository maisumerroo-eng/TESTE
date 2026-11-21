#!/usr/bin/env bash
# otimizar-3d.sh: deixa um GLB pronto para a web (geometria comprimida, texturas WebP redimensionadas,
# malha simplificada). Poster do fallback: screenshot do bloco .tres já renderizado (ver references/3d.md).
# Uso: bash otimizar-3d.sh entrada.glb [saida.glb] [textura_max=1024] [simplificar=0.75]
# Meta: GLB ≤ 1,5 MB para hero, ≤ 500 KB para elementos secundários.
set -euo pipefail
IN="${1:?arquivo .glb/.gltf de entrada}"
OUT="${2:-${IN%.*}.web.glb}"
TEX="${3:-1024}"
RATIO="${4:-0.75}"
CLI="npx -y @gltf-transform/cli@4.5.1"

$CLI inspect "$IN" --format md > /dev/null 2>&1 || true
# optimize = dedup + instance + prune + weld + simplify + resample + meshopt + texturas
$CLI optimize "$IN" "$OUT" \
  --compress meshopt \
  --texture-compress webp \
  --texture-size "$TEX" \
  --simplify true --simplify-ratio "$RATIO" --simplify-error 0.001

antes=$(stat -c %s "$IN"); depois=$(stat -c %s "$OUT")
python3 -c "print(f'ok: $OUT  {${antes}/1024:.0f} KB -> {${depois}/1024:.0f} KB ({100-${depois}*100/${antes}:.0f}% menor)')"
echo "use no site com tres.js (já decodifica meshopt e draco)."
