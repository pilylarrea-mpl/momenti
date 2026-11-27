"""Category funnel video from a spec: 376 sales -> N stores -> all qualifying items -> her picks, each full screen. Silent; cut to her voice later.
usage: python3 funnel.py <spec.json>"""
import sys,os,json,shutil,subprocess,random,html,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import fast,pick
from fast import SP,B,esc
from PIL import Image
import numpy as np
NS='/tmp/claude-0/-home-user/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/tomorrow'
PW,PH=1080,1920
money=lambda x:f'${x:,.0f}' if abs(x-round(x))<.005 else f'${x:,.2f}'
def plate2(url,out):
    im=Image.open(fast.fetch(url,1600)).convert('RGB'); W,H=int(PW*1.2),int(PH*1.2)
    a=np.asarray(im.resize((120,120))).astype(float); e=np.concatenate([a[:3].reshape(-1,3),a[-3:].reshape(-1,3),a[:,:3].reshape(-1,3),a[:,-3:].reshape(-1,3)])
    if e.std()<10 and e.mean()>190:
        from PIL import ImageFilter
        bg=tuple(int(v) for v in np.median(np.asarray(im)[:8].reshape(-1,3),0))
        arr=np.asarray(im).astype(int); m=np.abs(arr-np.array(bg)).sum(2)>36; ys=np.nonzero(m.any(1))[0]; xs=np.nonzero(m.any(0))[0]
        tall=len(ys)>0 and len(xs)>0 and (ys[-1]-ys[0])/max(1,(xs[-1]-xs[0]))>1.7
        if not tall:
            if len(ys) and len(xs):
                pad=int(0.05*max(im.size)); im=im.crop((max(0,xs[0]-pad),max(0,ys[0]-pad),min(im.width,xs[-1]+pad),min(im.height,ys[-1]+pad)))
            r=min((W*0.92)/im.width,(H*0.50)/im.height); r=min(r,2.2); im2=im.resize((round(im.width*r),round(im.height*r)),Image.LANCZOS)
            x0=(W-im2.width)//2; y0=max(0,int(H*0.395-im2.height/2))
            # background = the photo's own edges stretched outward, then blurred: no box, no ghost
            A=np.asarray(im2); P=np.pad(A,((y0,max(0,H-y0-im2.height)),(x0,max(0,W-x0-im2.width)),(0,0)),mode='edge')[:H,:W]
            cv=Image.fromarray(P).filter(ImageFilter.GaussianBlur(70))
            f=max(8,int(min(im2.size)*0.04)); mk=Image.new('L',im2.size,0); mk.paste(255,(f,f,im2.width-f,im2.height-f)); mk=mk.filter(ImageFilter.GaussianBlur(f/2))
            cv.paste(im2,(x0,y0),mk); cv.save(out,quality=93); return 'pack'
    r=max(W/im.width,H/im.height); im=im.resize((round(im.width*r)+1,round(im.height*r)+1),Image.LANCZOS); x=(im.width-W)//2; y=int((im.height-H)*0.30)
    im.crop((x,y,x+W,y+H)).save(out,quality=93); return 'photo'
CSS=fast.CSS.replace('HKpx','112px')+'''<style>
.rank{top:262px}
.lab{left:60px;right:150px;bottom:372px}
.br{font-size:24px;padding:8px 14px 7px}
.nm{font-size:54px;padding:6px 18px 12px;margin-top:8px}
.pr{margin-top:8px;gap:10px}
.now{font-size:124px;padding:4px 22px 16px}
.was{font-size:42px;padding:2px 12px 6px}
.off{font-size:27px;padding:8px 12px 7px}
.why{display:inline-block;margin-top:8px;background:var(--ink);color:var(--iv);font-family:'IT';font-style:normal;font-weight:700;font-size:25px;letter-spacing:.1em;text-transform:uppercase;padding:9px 14px 8px;border-radius:6px}
.hook{top:420px}
</style>'''
ECSS=fast.CSS+'''<style>html,body{background:#1C1A18}
.hd{position:absolute;left:60px;right:140px;top:252px;font-family:'IT';font-weight:700;font-size:31px;letter-spacing:.14em;text-transform:uppercase;color:#F4F0E8}
.cnt{position:absolute;left:54px;top:300px;font-family:'BM';font-size:270px;line-height:.9;color:#F4F0E8;letter-spacing:-.03em}
.cl{position:absolute;left:66px;top:556px;right:140px;font-family:'IT';font-weight:700;font-size:30px;letter-spacing:.16em;text-transform:uppercase;color:#e08a5c}
.wall{position:absolute;left:60px;right:130px;top:630px;height:940px;columns:5;column-gap:14px;column-fill:auto;font-family:'IT';font-weight:600;font-size:15.6px;line-height:1.3;color:#F4F0E8;text-transform:uppercase;letter-spacing:.02em}
.wall span{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.wall span.x{opacity:.17;text-decoration:line-through}
.wall span.k{background:#B4532A;color:#fff;padding:0 6px;margin:0 -6px;border-radius:4px}
.fin{position:absolute;left:60px;right:130px;top:420px}
.fin div{font-family:'BM';font-size:FSpx;line-height:1.14;color:#F4F0E8;letter-spacing:-.02em;display:flex;justify-content:space-between;align-items:baseline;gap:20px;border-bottom:1px solid rgba(244,240,232,.25);padding:14px 0}
.fin div b{font-family:'IT';font-weight:700;font-size:34px;letter-spacing:.08em;color:#e08a5c;white-space:nowrap}
.fin div.off{opacity:0}
.big{position:absolute;left:60px;right:130px;top:300px;font-family:'BM';font-size:88px;line-height:1;color:#F4F0E8;letter-spacing:-.02em}
.big i{color:#e08a5c}
.mo{position:absolute;left:60px;right:130px;top:560px;display:grid;grid-template-columns:repeat(6,1fr);gap:8px}
.mo div{aspect-ratio:1/1.12;background:#F4F0E8;border-radius:6px;overflow:hidden;position:relative}
.mo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.mo div.dim{opacity:.22}
.mo div.pk{outline:6px solid #e08a5c;outline-offset:-3px}
</style>'''
def run(spec_path,per_item=2.7):
    S=json.load(open(spec_path)); slug=S['slug']; OUT=f'{NS}/{slug}'; shutil.rmtree(OUT,ignore_errors=True)
    for d in ('ov','seg','pl','el','pick/b'): os.makedirs(f'{OUT}/{d}')
    T=S['threshold']; noun=S['noun']; label=S['label']; series=f'Black Friday · {label}'
    rowsof=lambda h:{x['h']:x for x in pick.rows(h)}
    # ---- picks: live check, plates
    L=[]; notes=[]
    for i,it in enumerate(S['picks']):
        r=rowsof(it['host'])[it['handle']]; lv=fast.live(it['host'],it['handle'])
        now,was=lv['now'],lv['was']
        if lv.get('stale'): notes.append(f"{it['brand']} {it['name']}: live check refused, price from catalog")
        elif lv['av']==0: notes.append(f"{it['brand']} {it['name']}: SOLD OUT live")
        elif abs(now-r['pr'])>0.5 or abs(was-r['ca'])>0.5: notes.append(f"{it['brand']} {it['name']}: live ${now:g} (was ${was:g}) vs catalog ${r['pr']:g} (was ${r['ca']:g})")
        if not was or was<=now: was=r['ca'];
        it.update(now=now,was=was,off=round(100*(1-now/was)) if was>now else 0,av=lv['av'],n=lv['n']); it['pl']=[]
        for j,ix in enumerate(it['imgs'][:3]):
            f=f'{OUT}/pl/{i}_{j}.jpg'; plate2(r['img'][min(ix,len(r['img'])-1)],f); it['pl'].append(f)
        L.append(it); print(f"{it['brand']:20} {it['name']:28} {money(was)}->{money(now)} {it['off']}% {lv['av']}/{lv['n']}")
    # ---- candidates: thumbnails for mosaic + picker
    C=[]; seen=set()
    for c in S['picks']+S['candidates']:
        if (c['host'],c['handle']) in seen: continue
        seen.add((c['host'],c['handle'])); r=rowsof(c['host']).get(c['handle'])
        if not r: print('missing candidate',c['handle']); continue
        k=len(C); fs=[]
        for j,ix in enumerate((c.get('imgs') or [0,1])[:2]):
            try:
                im=Image.open(pick._get(r['img'][min(ix,len(r['img'])-1)],600)).convert('RGB'); im.thumbnail((700,700)); f=f'b/{k:02d}_{j}.jpg'; im.save(f'{OUT}/pick/{f}',quality=84); fs.append(f)
            except Exception as e: print('img fail',c['handle'],e)
        if fs: C.append(dict(id=k,brand=c['brand'],name=c.get('name') or r['t'],was=r['ca'],now=r['pr'],off=r['off'],av=r['av'],n=r['n'],imgs=fs,handle=c['handle'],host=c['host'],pick=k<len(S['picks'])))
    json.dump(C,open(f'{OUT}/pick/items.json','w'),indent=0)
    # mosaic order: mix picks among the rest, 36 max
    random.seed(11); M=C[:36]; M=sorted(M,key=lambda c:random.random())
    # ---- overlays
    def hook(lines,sub=None): return f'{CSS}<body><div class=series>{esc(series)}</div><div class=hook>'+''.join(f'<div class="{"y" if y else ""}">{esc(t)}</div><br>' for t,y in lines)+(f'<p>{esc(sub)}</p>' if sub else '')+'</div></body>'
    O={'end':hook([('Which one',False),('would you buy?',True)],S.get('tease_short') and ('Next: '+S['tease_short']))}
    for i,it in enumerate(L):
        O[f'i{i}']=f'{CSS}<body><div class=rank><b>{i+1}</b> of {len(L)}</div><div class=lab><span class=br>{esc(it["brand"])}</span><br><span class=nm>{esc(it["name"])}</span><div class=pr><span class=now style="{"font-size:104px;padding-top:12px" if abs(it["now"]-round(it["now"]))>.005 else ""}">{money(it["now"])}</span><div><div class=was>{money(it["was"])}</div><div class=off>{it["off"]}% off</div></div></div><span class=why>{esc(it["chip"])}</span></div></body>'
    for k,h in O.items(): open(f'{OUT}/ov/{k}.html','w').write(h)
    subprocess.run(['node',B+'/shootpng.js',OUT+'/ov'],check=True)
    # ---- dark opening
    names=sorted({b['brand'] for b in pick.B.values()},key=str.lower); KEEP=set(S['per_store'])
    random.seed(7); order=[n for n in names if n not in KEEP]; random.shuffle(order); NST=S['stores_total']
    def wall(nx,final=False):
        gone=set(order[:nx]); remain=round(376-(376-NST)*nx/len(order))
        sp=''.join(f'<span class="{"x" if n in gone else ("k" if (final and n in KEEP) else "")}">{esc(n)}</span>' for n in names)
        return f'{ECSS}<body><div class=hd>I checked every sale for {esc(noun)}</div><div class=cnt>{remain}</div><div class=cl>{f"stores have {esc(noun)} {T}% off" if final else "Black Friday sales"}</div><div class=wall>{sp}</div></body>'
    steps=[0,0.05,0.12,0.22,0.34,0.47,0.6,0.72,0.82,0.9,0.96,1.0]
    for k,f in enumerate(steps): open(f'{OUT}/el/{k:02d}.html','w').write(wall(round(f*len(order)),final=(f==1.0)))
    top=sorted(S['per_store'].items(),key=lambda x:-x[1])[:5]; fs=118 if max(len(n) for n,_ in top)<=16 else 92
    def names_card(n): return ECSS.replace('FSpx',f'{fs}px')+f'<body><div class=hd>{"Only "+str(NST)+" stores had them" if NST<=5 else "Most of them are in "+str(len(top))+" stores"}</div><div class=fin>'+''.join(f'<div class="{"" if j<n else "off"}"><span>{esc(x)}</span><b>{c}</b></div>' for j,(x,c) in enumerate(top))+'</div></body>'
    for k in range(1,len(top)+1): open(f'{OUT}/el/8{k}.html','w').write(names_card(k))
    def mosaic(mode):
        t={'all':f'<div class=big>{S["items_total"]} {esc(noun)}<br>at <i>{T}% off</i> or more.</div>','pick':f'<div class=big>These are my<br><i>{len(L)} favorites.</i></div>'}[mode]
        cells=''.join(f'<div class="{("pk" if c["pick"] else "dim") if mode=="pick" else ""}"><img src="{OUT}/pick/{c["imgs"][0]}"></div>' for c in M)
        return f'{ECSS}<body><div class=hd>{esc(series)}</div>{t}<div class=mo>{cells}</div></body>'
    open(f'{OUT}/el/95.html','w').write(mosaic('all')); open(f'{OUT}/el/96.html','w').write(mosaic('pick'))
    subprocess.run(['node',B+'/shoot.js',OUT+'/el'],check=True)
    # ---- segments
    segs=[]; marks=[]
    def still(img,dur):
        f=f'{OUT}/seg/{len(segs):03d}.mp4'; fr=max(1,round(dur*30))
        subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-t',str(dur+0.5),'-i',img,'-vf','scale=1080:1920,format=yuv420p','-frames:v',str(fr),'-r','30','-c:v','libx264','-crf','18',f],check=True); segs.append(f); return fr/30
    def seg(img,ov,dur,zin=True):
        f=f'{OUT}/seg/{len(segs):03d}.mp4'; fr=max(2,round(dur*30)); z=f"'1+0.03*on/{fr}'" if zin else f"'1.03-0.03*on/{fr}'"
        subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-t',str(dur+0.5),'-i',img,'-i',ov,'-filter_complex',f"[0]scale=iw*4:ih*4:flags=bicubic,zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={PW}x{PH}:fps=30[b];[b][1]overlay=0:0,format=yuv420p",'-frames:v',str(fr),'-r','30','-c:v','libx264','-crf','18',f],check=True); segs.append(f); return fr/30
    t=0
    def mark(name):
        marks.append((name,round(t,2)))
    op=S.get('opening','funnel'); hl=S.get('hook_lines') or [[f'{NST} stores',True],[f'have {noun}',False],[f'{T}% off.',False]]
    def card(name,lines,sub=None,top=None):
        h=hook(lines,sub)
        if top: h=h.replace('.hook{top:420px}',f'.hook{{top:{top}px}}')
        open(f'{OUT}/ov/{name}.html','w').write(h)
    hero=L[S.get('hero',len(L)-1)]
    if op=='cold':
        # the best piece first, price on screen, then the claim, then a short mosaic
        card('c1',[(money(hero['now']),True),(f"It was {money(hero['was'])}.",False)],None,1000)
        card('c2',hl,'I read almost 400 Black Friday sales.')
    elif op=='take':
        card('c1',hl,S.get('take_sub'))
    elif op=='ladder':
        card('c1',hl,S.get('take_sub') or f"{money(min(x['now'] for x in L))} to {money(max(x['now'] for x in L))}.")
    if op!='funnel': subprocess.run(['node',B+'/shootpng.js',OUT+'/ov'],check=True)
    if op=='funnel':
        mark('wall')
        for k in range(len(steps)): t+=still(f'{OUT}/el/{k:02d}.jpg',0.24 if k<len(steps)-1 else 1.5)
        mark('stores')
        for k in range(1,len(top)+1): t+=still(f'{OUT}/el/8{k}.jpg',0.32 if k<len(top) else 1.1)
        mark('all'); t+=still(f'{OUT}/el/95.jpg',2.0)
        mark('favorites'); t+=still(f'{OUT}/el/96.jpg',1.5)
    elif op=='cold':
        mark('hero'); t+=seg(hero['pl'][0],f'{OUT}/ov/c1.png',2.2,True)
        mark('claim'); t+=seg(hero['pl'][-1],f'{OUT}/ov/c2.png',2.8,False)
        mark('all'); t+=still(f'{OUT}/el/95.jpg',1.6); mark('favorites'); t+=still(f'{OUT}/el/96.jpg',1.3)
    elif op=='take':
        mark('take'); t+=seg(hero['pl'][-1],f'{OUT}/ov/c1.png',3.4,True)
        mark('all'); t+=still(f'{OUT}/el/95.jpg',1.8); mark('favorites'); t+=still(f'{OUT}/el/96.jpg',1.3)
    elif op=='ladder':
        mark('hook'); n=len(L)
        for i,it in enumerate(L): t+=seg(it['pl'][0],f'{OUT}/ov/c1.png',3.2/n,i%2==0)
    for i,it in enumerate(L):
        mark(f'pick{i+1}'); n=len(it['pl'][:2]) or 1
        for j,p in enumerate(it['pl'][:2]): t+=seg(p,f'{OUT}/ov/i{i}.png',per_item/n,j%2==0)
    mark('end'); t+=seg(L[-1]['pl'][-1],f'{OUT}/ov/end.png',2.6,True)
    open(OUT+'/list.txt','w').write(''.join(f"file '{s}'\n" for s in segs))
    final=f'{NS}/black-friday-{slug}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',OUT+'/list.txt','-c','copy','-movflags','+faststart',final],check=True)
    json.dump(dict(marks=marks,duration=round(t,2),notes=notes,picks=[{k:v for k,v in it.items() if k!='pl'} for it in L]),open(f'{OUT}/build.json','w'),indent=1)
    print(final,round(t,2),'s'); print('marks',marks); print('notes',notes)
    return final
if __name__=='__main__': run(sys.argv[1])
