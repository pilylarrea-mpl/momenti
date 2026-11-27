"""Cut the boots video to Pily's voice memo."""
import sys,os,json,shutil,subprocess,glob,math
sys.path.insert(0,'.')
import fast
from fast import SP,B,esc
VO='/tmp/claude-0/-home-user/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/vo/vo.m4a'
OUT=SP+'/out12'; shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT+'/ov'); os.makedirs(OUT+'/seg'); os.makedirs(OUT+'/au')
L=json.load(open(SP+'/out6/boots-picks.json'))          # the eight boots, prices and photo plates already checked
G=0.20; P=0.05; TEMPO=1.0
# (label, audio start, audio end, gap after)
CH=[('h1',2.88,7.86,0.18),('h2',8.18,11.98,0.22),('h3',12.46,14.44,0.25),
    ('b0',15.22,17.16,G),('b1',17.68,20.88,G),('b2',29.34,31.20,0.0),('b3',31.20,36.64,0.28),
    ('b4a',38.56,39.88,0.15),('b4b',40.36,42.94,G),('b5',43.50,46.16,G),('b6',46.78,48.30,0.0),('b7',48.30,50.54,0.30),('end',51.52,54.50,0.9)]
# ---- audio
parts=[]
for k,(n,a,b,g) in enumerate(CH):
    f=f'{OUT}/au/{k:02d}.wav'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(a),'-to',str(b),'-i',VO,'-af',f'afade=t=in:d=0.02,afade=t=out:st={b-a-0.03}:d=0.03,atempo={TEMPO},apad=pad_dur={g}','-ar','48000','-ac','1',f],check=True); parts.append(f)
open(OUT+'/au/list.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',OUT+'/au/list.txt','-af','loudnorm=I=-15:TP=-1.5:LRA=11','-ar','48000',OUT+'/voice.wav'],check=True)
D={n:(b-a)/TEMPO+g for n,a,b,g in CH}
# ---- plates: the photo fills the top 1330px; labels sit on an ivory panel below, so the boot is never covered
from PIL import Image
import pick
PW,PH=1080,1920
import numpy as np
def plate2(url,out):
    im=Image.open(fast.fetch(url,1600)).convert('RGB'); W,H=int(PW*1.2),int(PH*1.2)
    a=np.asarray(im.resize((120,120))).astype(float); e=np.concatenate([a[:3].reshape(-1,3),a[-3:].reshape(-1,3),a[:,:3].reshape(-1,3),a[:,-3:].reshape(-1,3)])
    if e.std()<10 and e.mean()>190:      # flat light background: extend it
        bg=tuple(int(v) for v in np.median(np.asarray(im)[:8].reshape(-1,3),0)); cv=Image.new('RGB',(W,H),bg)
        arr=np.asarray(im).astype(int); m=np.abs(arr-np.array(bg)).sum(2)>36; ys=np.nonzero(m.any(1))[0]; xs=np.nonzero(m.any(0))[0]
        if len(ys) and len(xs):
            pad=int(0.03*max(im.size)); im=im.crop((max(0,xs[0]-pad),max(0,ys[0]-pad),min(im.width,xs[-1]+pad),min(im.height,ys[-1]+pad)))
        r=min((W*0.90)/im.width,(H*0.50)/im.height); im2=im.resize((round(im.width*r),round(im.height*r)),Image.LANCZOS)
        cv.paste(im2,((W-im2.width)//2,int(H*0.395-im2.height/2))); cv.save(out,quality=93); return 'pack'
    r=max(W/im.width,H/im.height); im=im.resize((round(im.width*r)+1,round(im.height*r)+1),Image.LANCZOS); x=(im.width-W)//2; y=int((im.height-H)*0.35)
    im.crop((x,y,x+W,y+H)).save(out,quality=93); return 'photo'
os.makedirs(OUT+'/pl')
for i,it in enumerate(L):
    r={x['h']:x for x in pick.rows(it['host'])}[it['handle']]; it['pl2']=[]
    for j,ix in enumerate(it['imgs']):
        f=f'{OUT}/pl/{i}_{j}.jpg'; plate2(r['img'][min(ix,len(r['img'])-1)],f); it['pl2'].append(f)
# ---- overlays
CSS=fast.CSS.replace('HKpx','112px')+'''<style>
.panel{display:none}
.rank{top:262px}
.lab{left:60px;right:150px;bottom:372px}
.br{font-size:24px;padding:8px 14px 7px}
.nm{font-size:54px;padding:6px 18px 12px;margin-top:8px}
.pr{margin-top:8px;gap:10px}
.now{font-size:124px;padding:4px 22px 16px}
.was{font-size:42px;padding:2px 12px 6px}
.off{font-size:27px;padding:8px 12px 7px}
.why{display:none}
.hook{top:420px}
</style>'''
money=lambda x:f'${x:,.0f}' if abs(x-round(x))<.005 else f'${x:,.2f}'
def hook(lines,sub=None): return f'{CSS}<body><div class=panel></div><div class=series>Black Friday · Boots</div><div class=hook>'+''.join(f'<div class="{c}">{esc(t)}</div><br>' for t,c in lines)+(f'<p>{esc(sub)}</p>' if sub else '')+'</div></body>'
O={'h1':hook([('I read almost','') ,('400 sales.','y')],'So you don’t have to. Today: boots.'),
   'h2':hook([('Only 3 stores','y'),('have boots',''),('40% off.','')]),
   'h3':hook([('My 8 favorites.',''),('Cheapest first.','y')]),
   'end':hook([('Tomorrow:','y'),('jewelry.','')],'Follow so you see it.')}
for i,it in enumerate(L):
    O[f'i{i}a']=f'{CSS}<body><div class=panel></div><div class=rank><b>{i+1}</b> of {len(L)}</div><div class=lab><span class=br>{esc(it["brand"])}</span><br><span class=nm>{esc(it["name"])}</span><div class=pr><span class=now>{money(it["now"])}</span><div><div class=was>{money(it["was"])}</div><div class=off>{it["off"]}% off</div></div></div></div></body>'
    O[f'i{i}b']=O[f'i{i}a']
for k,h in O.items(): open(f'{OUT}/ov/{k}.html','w').write(h)
subprocess.run(['node',B+'/shootpng.js',OUT+'/ov'],check=True)
segs=[]
def seg(img,ov,dur,zin=True):
    f=f'{OUT}/seg/{len(segs):03d}.mp4'; fr=max(2,round(dur*30)); z="'1.03'" if zin=='hold' else (f"'1+0.03*on/{fr}'" if zin else f"'1.03-0.03*on/{fr}'")
    subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-t',str(dur+0.5),'-i',img,'-i',ov,'-filter_complex',f"[0]scale=iw*4:ih*4:flags=bicubic,zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={PW}x{PH}:fps=30[b];[b][1]overlay=0:0,format=yuv420p",'-frames:v',str(fr),'-r','30','-c:v','libx264','-crf','18',f],check=True); segs.append(f); return fr/30
def fill(imgs,ov_first,ov_rest,dur,target=0.72,start=0):
    n=max(1,round(dur/target)); each=dur/n; used=0
    for j in range(n):
        d=each if j<n-1 else dur-used; used+=seg(imgs[(start+j)%len(imgs)],ov_first if j==0 else ov_rest,d,j%2==0)
hp=[]
for k,(i,ix) in enumerate([(1,1),(4,1),(7,1)]):
    r={x['h']:x for x in pick.rows(L[i]['host'])}[L[i]['handle']]; f=f'{OUT}/pl/hook{k}.jpg'; plate2(r['img'][ix],f); hp.append(f)
seg(hp[0],f'{OUT}/ov/h1.png',D['h1'],True); seg(hp[1],f'{OUT}/ov/h2.png',D['h2'],True); seg(hp[2],f'{OUT}/ov/h3.png',D['h3'],True)
dur_item=[D['b0'],D['b1'],D['b2'],D['b3'],D['b4a']+D['b4b'],D['b5'],D['b6'],D['b7']]
for i,it in enumerate(L): fill(it['pl2'],f'{OUT}/ov/i{i}a.png',f'{OUT}/ov/i{i}b.png',dur_item[i],1.7)
seg(hp[1],f'{OUT}/ov/end.png',D['end'],True)
open(OUT+'/list.txt','w').write(''.join(f"file '{s}'\n" for s in segs))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',OUT+'/list.txt','-c','copy',OUT+'/silent.mp4'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',OUT+'/silent.mp4','-i',OUT+'/voice.wav','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',OUT+'/boots-voiced.mp4'],check=True)
pr=lambda f:float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
print('video',round(pr(OUT+'/silent.mp4'),2),'voice',round(pr(OUT+'/voice.wav'),2),'final',round(pr(OUT+'/boots-voiced.mp4'),2)); print({k:round(v,2) for k,v in D.items()})
