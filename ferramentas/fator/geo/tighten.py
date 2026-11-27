import json,wave,numpy as np,subprocess,sys
from faster_whisper import WhisperModel
src,dst,tempo=sys.argv[1],sys.argv[2],float(sys.argv[3])
w=wave.open(src); sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
hop=int(sr*0.01); db=np.array([20*np.log10(np.sqrt(np.mean(a[i:i+hop]**2))+1e-9) for i in range(0,len(a)-hop,hop)])
th=np.percentile(db,15)+10; v=db>th; cuts=[]; i=0; n=len(v)
while i<n:
    if not v[i]:
        j=i
        while j<n and not v[j]: j+=1
        L=(j-i)*0.01
        if L>0.2 and i>0 and j<n: keep=0.15; cuts.append((i*0.01+keep/2, j*0.01-keep/2))
        i=j
    else: i+=1
dur=len(a)/sr; segs=[]; prev=0
for c0,c1 in cuts: segs.append((prev,c0)); prev=c1
segs.append((prev,dur))
f="".join(f"[0:a]atrim={x:.3f}:{y:.3f},asetpts=PTS-STARTPTS,afade=in:d=0.008,afade=out:st={max(0,y-x-0.01):.3f}:d=0.01[s{k}];" for k,(x,y) in enumerate(segs))
f+="".join(f"[s{k}]" for k in range(len(segs)))+f"concat=n={len(segs)}:v=0:a=1,atempo={tempo}[o]"
subprocess.run(f'ffmpeg -y -v error -i {src} -filter_complex "{f}" -map "[o]" {dst}',shell=True,check=True)
subprocess.run(f'ffmpeg -y -v error -i {dst} -ac 1 -ar 16000 _t16.wav',shell=True,check=True)
w=wave.open('_t16.wav');b=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
m=WhisperModel("medium",device="cpu",compute_type="int8")
W=[(round(x.start,2),round(x.end,2),x.word.strip()) for s in m.transcribe(b,language="pt",word_timestamps=True,condition_on_previous_text=False)[0] for x in s.words]
json.dump(W,open(dst+'.words.json','w'),ensure_ascii=False)
print(round(len(b)/16000,2),'s'); print(" ".join(f"{x}@{s}" for s,e,x in W))
