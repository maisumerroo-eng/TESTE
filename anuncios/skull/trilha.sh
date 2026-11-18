#!/usr/bin/env bash
# trilha: drone grave + riser até o drop em 6 s, depois kick 120 bpm. Uso: trilha.sh DUR saida.wav
D=$1; OUT=$2
ffmpeg -loglevel error -y -f lavfi -i "aevalsrc='0.12*sin(2*PI*55*t)*min(1,t/2)+0.05*sin(2*PI*(110+60*t)*t)*between(t,3,6)*(t-3)/3+(gte(t,6)*lt(t,$D-1.2))*0.9*sin(2*PI*(45+140*exp(-28*mod(t,0.5)))*mod(t,0.5))*exp(-7*mod(t,0.5))+gte(t,6)*0.03*sin(2*PI*220*t)*exp(-14*mod(t+0.25,0.5))':s=44100:d=$D" -af "afade=t=out:st=$(echo "$D-1.5"|bc):d=1.5,alimiter=limit=0.9" "$OUT"
