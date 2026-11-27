#!/bin/bash
# uso: add_cover.sh capa.png video_in.mp4 video_out.mp4  -> capa em 2 quadros no inicio (1o frame = capa do reel)
set -e
C=$1; IN=$2; OUT=$3; N=2
FPS=$(ffprobe -v error -select_streams v -show_entries stream=r_frame_rate -of csv=p=0 "$IN")
D=$(python3 -c "from fractions import Fraction as F;print(round($N/float(F('$FPS')),4))")
MS=$(python3 -c "print(int(round($D*1000)))")
ffmpeg -y -v error -loop 1 -framerate "$FPS" -t "$D" -i "$C" -i "$IN" -filter_complex \
 "[0:v]scale=1080:1920,setsar=1,format=yuv420p,fps=$FPS[c];[1:v]scale=1080:1920,setsar=1,format=yuv420p,fps=$FPS[v];[c][v]concat=n=2:v=1:a=0[vo];[1:a]adelay=${MS}|${MS}[ao]" \
 -map "[vo]" -map "[ao]" -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "$OUT"
