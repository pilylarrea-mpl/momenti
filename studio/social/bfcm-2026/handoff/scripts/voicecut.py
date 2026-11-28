"""Cut a film spec to a voice memo.
voicecut.run(dir, spec_in, marks, drops, pools, slug)
  dir: folder with vo.m4a + words.json     marks: [(name, original_time_of_first_word)] in order, first is the first brand, last is 'end'
  drops: [(t0,t1)] original-time ranges to remove (retakes)     pools: {brand: [clips]} more shots for longer lines
Trims pauses over 0.45s, levels volume, nothing else."""
import json,subprocess,os,shutil,sys
FD='/tmp/claude-0/-home-user/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/film'
def run(d,spec_in,marks,drops,pools,slug,shot=2.7,thr=0.45,gb=0.42,gs=0.22):
    W=[w for w in json.load(open(f'{d}/words.json')) if not any(a<=w[0]<b for a,b in drops)]
    ch=[[W[0]]]
    for a,b in zip(W,W[1:]):
        if b[0]-a[1]>thr: ch.append([b])
        else: ch[-1].append(b)
    mt=[m[1] for m in marks]; isb=lambda w:any(abs(w[0]-x)<0.02 for x in mt)
    shutil.rmtree(f'{d}/au',ignore_errors=True); os.makedirs(f'{d}/au'); t=0; newt={}; parts=[]
    for k,c in enumerate(ch):
        s=max(0,c[0][0]-0.08); e=c[-1][1]+0.14
        if k+1<len(ch): e=min(e,ch[k+1][0][0]-0.02)
        nxt=ch[k+1][0] if k+1<len(ch) else None
        gap=0.7 if nxt is None else (gb if isb(nxt) else gs)
        for w in c:
            for name,x in marks:
                if abs(w[0]-x)<0.02: newt[name]=round(t+(w[0]-s),2)
        f=f'{d}/au/{k:02d}.wav'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(s),'-to',str(e),'-i',f'{d}/vo.m4a','-af',f'afade=t=in:d=0.03,afade=t=out:st={max(0,e-s-0.05)}:d=0.05,apad=pad_dur={gap}','-ar','48000','-ac','1',f],check=True); parts.append(f); t+=(e-s)+gap
    open(f'{d}/au/list.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',f'{d}/au/list.txt','-af','loudnorm=I=-15:TP=-1.5:LRA=11','-ar','48000',f'{d}/voice.wav'],check=True)
    total=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{d}/voice.wav'],capture_output=True,text=True).stdout)
    assert len(newt)==len(marks),(newt,marks)
    st=[newt[m[0]] for m in marks]; lead=0.12; S=json.load(open(spec_in)); S['slug']=slug
    S['hook']['dur']=round(st[0]-lead,2)
    for i,b in enumerate(S['brands']):
        dd=round(st[i+1]-st[i],2); b['dur']=dd; pool=pools.get(b['brand']) or b['clips']; n=max(1,min(len(pool),round(dd/shot))); b['clips']=pool[:n]
    S['end']['dur']=round(total-(st[-1]-lead),2)
    json.dump(S,open(f'{d}/spec.json','w'),indent=1,ensure_ascii=False); print('voice',round(total,2),newt)
    sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import film; film.run(f'{d}/spec.json')
    out=f'{FD}/{slug}-voiced.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'{FD}/{slug}.mp4','-i',f'{d}/voice.wav','-c:v','libx264','-preset','slow','-b:v','6M','-maxrate','8M','-bufsize','12M','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],check=True)
    print(out); return out
