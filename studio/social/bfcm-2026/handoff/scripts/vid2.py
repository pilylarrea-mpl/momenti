"""Edition video v2: reads picks/<slug>.json. One hero tile per brand, two supporting tiles."""
import sys,os,json,shutil,subprocess,hashlib
import numpy as np
from PIL import Image
SP='/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad'
sys.path.insert(0,SP); import pick
import html as _h; esc=_h.escape
B=SP+'/build'; A=B+'/assets'; os.makedirs(A,exist_ok=True)
def money(x,c='$'):
    x=float(x); return f'{c}{x:,.0f}' if abs(x-round(x))<.005 else f'{c}{x:,.2f}'
def fetch(url,w=1400):
    u=url.split('?')[0]+f'?width={w}'; fn=A+'/'+hashlib.md5(u.encode()).hexdigest()
    if not os.path.exists(fn) or os.path.getsize(fn)<500: subprocess.run(['curl','-sL','-m','60','-A','Mozilla/5.0','-o',fn,u],check=True)
    return fn
def prep(url):
    """returns (kind, path): 'pack' = flat light background pushed to white for multiply blend; else 'photo'"""
    src=fetch(url); im=Image.open(src).convert('RGB'); a=np.asarray(im.resize((200,200))).astype(float)
    e=np.concatenate([a[:4].reshape(-1,3),a[-4:].reshape(-1,3),a[:,:4].reshape(-1,3),a[:,-4:].reshape(-1,3)])
    if e.mean()>218 and e.std()<16:
        out=src+'.pack.png'
        if not os.path.exists(out):
            f=np.asarray(im).astype(float); b=6; ed=np.concatenate([f[:b].reshape(-1,3),f[-b:].reshape(-1,3),f[:,:b].reshape(-1,3),f[:,-b:].reshape(-1,3)])
            o=np.clip(f/np.median(ed,0)*255*1.012,0,255); m=(255-o.min(2))>14; ys=np.nonzero(m.any(1))[0]; xs=np.nonzero(m.any(0))[0]
            if len(ys) and len(xs):
                pad=int(.04*max(f.shape[:2])); o=o[max(0,ys[0]-pad):ys[-1]+pad,max(0,xs[0]-pad):xs[-1]+pad]
            Image.fromarray(o.astype(np.uint8)).save(out)
        return 'pack',out
    out=src+'.jpg'
    if not os.path.exists(out): im.save(out,quality=92)
    return 'photo',out
def item(host,it):
    R={r['h']:r for r in pick.rows(host)}; r=R[it['handle']]
    assert r['av']>0, ('out of stock',it['handle'])
    i0=min(it.get('img',0),len(r['img'])-1); k,s=prep(r['img'][i0])
    now=it.get('now_override') or r['pr']; was=r['ca'] or it.get('was')
    d=dict(kind=k,src=s,name=it['name'],was=was,now=now,hero=it.get('hero',False),pos=it.get('pos'))
    if d['hero'] and len(r['img'])>1 and it.get('img2')!=-1:
        i1=it.get('img2', 0 if i0!=0 else 1); d['kind2'],d['src2']=prep(r['img'][i1])
    return d
CSS='''<style>
.kick{position:absolute;left:72px;top:262px;right:72px;display:flex;justify-content:space-between}
.kick .lab{font-size:22px;color:var(--muted)} .kick .lab:first-child{color:var(--ink)}
.tile{background:var(--paper);border-radius:12px;overflow:hidden;position:absolute;opacity:0}
.tile.on{opacity:1}
.hero{left:60px;top:306px;width:960px;height:590px}
.s1{left:60px;top:1196px;width:440px;height:374px}.s2{left:520px;top:1196px;width:440px;height:374px}
.tile img{position:absolute;left:0;top:0;width:100%;height:calc(100% - 84px)}
.tile.k-pack img{left:5%;top:3%;width:90%;height:calc(94% - 84px);object-fit:contain;mix-blend-mode:multiply}
.tile.k-photo img{object-fit:cover}
.tag{position:absolute;left:0;right:0;bottom:0;height:84px;background:var(--paper);display:flex;align-items:center;justify-content:space-between;padding:0 22px;gap:10px}
.tag .n{font-family:'Inter Tight';font-weight:600;font-size:21px;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#3d3832}
.tag .p{white-space:nowrap;font-family:'Bodoni Moda';font-size:40px} .tag .p s{font-family:Newsreader;font-size:25px;color:var(--muted);margin-right:8px}
.hero .tag{height:104px}.hero img{height:calc(100% - 104px)}.hero.k-pack img{height:calc(94% - 104px)}
.hero .tag .n{font-size:27px}.hero .tag .p{font-size:62px}.hero .tag .p s{font-size:32px}
.pick{position:absolute;left:84px;top:330px;z-index:3;background:var(--acc);color:#fff;font-family:'Inter Tight';font-weight:700;font-size:20px;letter-spacing:.16em;text-transform:uppercase;padding:9px 16px 8px;border-radius:999px;opacity:0}
.pick.on{opacity:1}
.mid{position:absolute;left:60px;right:60px;top:902px;height:288px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.mid .num{display:flex;gap:12px;margin-bottom:12px;align-items:center;height:30px}.mid .num i{flex:0 0 20px;width:20px;height:20px;box-sizing:border-box;border-radius:50%;border:2.5px solid var(--acc);display:block}.mid .num i.d{background:var(--acc)}.mid .num i.c{flex:0 0 28px;width:28px;height:28px;background:var(--acc)}
.mid .b{font-family:'Bodoni Moda';font-size:BSpx;line-height:1;letter-spacing:-.015em;margin:2px 0 12px;white-space:nowrap}
.mid .d{font-family:'Inter Tight';font-weight:700;font-size:33px;letter-spacing:.13em;text-transform:uppercase}
.mid .c{margin-top:12px;font-family:'Inter Tight';font-weight:700;font-size:26px;letter-spacing:.12em;text-transform:uppercase;background:var(--ink);color:var(--ivory);padding:9px 20px 8px;border-radius:999px}
.mid .c.no{background:none;color:var(--muted);padding:0;font-weight:600;font-size:23px}
.ti{position:absolute;left:72px;right:72px;top:470px}.ti .h span.w{opacity:0}.ti .h span.w.on{opacity:1}.ti .s.off{opacity:0}
.ti .a{font-family:'Inter Tight';font-weight:700;font-size:40px;letter-spacing:.2em;text-transform:uppercase;color:var(--acc)}
.ti .h{font-family:'Bodoni Moda';font-size:HSpx;line-height:.93;letter-spacing:-.02em;margin:22px 0 40px}
.ti .s{font-family:Newsreader;font-style:italic;font-size:52px;line-height:1.2;color:#3d3832;max-width:880px}
</style>'''
def head(bs=100,hs=160): return f'<!doctype html><meta charset=utf-8><link rel=stylesheet href="{B}/base.css">'+CSS.replace('BS',str(bs)).replace('HS',str(hs))
DPOS='50% 22%'
def tile(it,cls,on):
    pos=it.get('pos') or DPOS
    if cls=='hero' and it.get('src2'):
        def half(k,s,x): 
            st=f'left:{x}px;width:480px;' + ('object-fit:cover;object-position:'+pos if k=='photo' else 'left:%dpx;width:440px;top:3%%;height:calc(94%% - 104px);object-fit:contain;mix-blend-mode:multiply'%(x+20))
            return f'<img src="{s}" style="{st}">'
        return f'<div class="tile hero k-x {"on" if on else ""}">{half(it["kind"],it["src"],0)}{half(it["kind2"],it["src2"],480)}<div class=tag><span class=n>{esc(it["name"])}</span><span class=p><s>{money(it["was"],it.get("cur","$"))}</s>{money(it["now"],it.get("cur","$"))}</span></div></div>'
    return f'<div class="tile {cls} k-{it["kind"]} {"on" if on else ""}"><img src="{it["src"]}" style="object-position:{pos}"><div class=tag><span class=n>{esc(it["name"])}</span><span class=p><s>{money(it["was"],it.get("cur","$"))}</s>{money(it["now"],it.get("cur","$"))}</span></div></div>'
def sfx(frames,slug,out3):
    t=0; pops=[]; whoosh=[]
    for k,(h,d,ev) in enumerate(frames):
        if ev=='whoosh': whoosh.append(t)
        elif ev and ev.startswith('pop'): pops.append((t,int(ev[3:] or 1)))
        t+=d
    ins=[]; fl=[]; n=0
    for tt,on in pops:
        f0=500+90*on; ins+=['-f','lavfi','-t','0.16','-i',f"aevalsrc=0.55*sin(2*PI*({f0}+900*exp(-45*t))*t)*exp(-30*t):s=44100"]; fl.append(f'[{n}]adelay={int(tt*1000)}:all=1[a{n}]'); n+=1
    for tt in whoosh:
        ins+=['-f','lavfi','-t','0.34','-i','anoisesrc=c=pink:r=44100:a=0.5']; fl.append(f"[{n}]highpass=f=500,lowpass=f=3500,afade=t=in:d=0.2,afade=t=out:st=0.22:d=0.12,adelay={max(0,int((tt-0.24)*1000))}:all=1[a{n}]"); n+=1
    fc=';'.join(fl)+';'+''.join(f'[a{i}]' for i in range(n))+f'amix=inputs={n}:normalize=0,apad,atrim=0:{t}[out]'
    subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',fc,'-map','[out]','-ar','44100',f'{out3}/{slug}.wav'],check=True)
def render(frames,slug,cards=None):
    out3=SP+'/out5'; out=f'{out3}/{slug}'; shutil.rmtree(out,ignore_errors=True); os.makedirs(out+'/f')
    for k,(h,_,_) in enumerate(frames): open(f'{out}/f/{k:03d}.html','w').write(h)
    subprocess.run(['node',B+'/shoot.js',out+'/f'],check=True)
    open(out+'/f/list.txt','w').write(''.join(f"file '{out}/f/{k:03d}.jpg'\nduration {d}\n" for k,(_,d,_) in enumerate(frames))+f"file '{out}/f/{len(frames)-1:03d}.jpg'\n")
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',out+'/f/list.txt','-vf','fps=30,format=yuv420p','-c:v','libx264','-crf','19',f'{out3}/{slug}-silent.mp4'],check=True)
    shutil.copy(f'{out3}/{slug}-silent.mp4',f'{out3}/{slug}.mp4')
    json.dump([dict(t=round(sum(d for _,d,_ in frames[:k]),2),ev=e) for k,(_,_,e) in enumerate(frames) if e],open(f'{out3}/{slug}-cues.json','w'))
    if cards:
        ims=[Image.open(f'{out}/f/{k:03d}.jpg').resize((300,533)) for k in cards]; S=Image.new('RGB',(len(ims)*300,533))
        for i,im in enumerate(ims): S.paste(im,(i*300,0)); im.close()
        S.save(f'{out3}/{slug}-cards.jpg',quality=85)
        os.makedirs(out+'/cards',exist_ok=True)
        for i,k in enumerate(cards): shutil.copy(f'{out}/f/{k:03d}.jpg',f'{out}/cards/card-{i+1:02d}.jpg')
    print('ok',slug,round(sum(d for _,d,_ in frames),1),'s')
def edition(spec,kick_l='Black Friday',kick_r=None,title_a='Black Friday',title_h=None,nxt=None,hold=3.3,title_words=None):
    global DPOS; DPOS=spec.get('pos','50% 22%')
    slug=spec['slug']; kr=kick_r or f"{spec['title']} edition"
    kick=f'<div class=kick><span class=lab>{kick_l}</span><span class=lab>{kr}</span></div>'
    words=spec.get('title_words') or ([(w,False) for w in spec['title'].split()]+[('edition.',True)])
    if title_h: words=title_words or words
    def tcard(n,sub):
        hh=''.join(f'<span class="w {"on" if j<n else ""}">'+(f'<span class=it>{esc(w)}</span>' if it else esc(w))+'</span>'+('<br>' if br else ' ') for j,(w,it,br) in enumerate([(w,it,(j==len(words)-2) if len(words)<4 else (j%2==1)) for j,(w,it) in enumerate(words)]))
        return f'{head()}<body>{kick}<div class=ti><div class=a>{title_a}</div><div class="ser h">{hh}</div><div class="s {"" if sub else "off"}">{esc(spec["sub"])}</div></div></body>'
    frames=[(tcard(j+1,False),0.22,f'pop{j+1}') for j in range(len(words))]+[(tcard(len(words),True),2.0,None)]
    cards=[]
    for i,b in enumerate(spec['brands']):
        its=[dict(item(b['host'],x),cur=b.get('cur','$')) for x in b['items']]; its.sort(key=lambda x:not x['hero']); hero,s1,s2=its[0],its[1],its[2]
        L=len(b['brand']); bs=100 if L<=14 else (82 if L<=19 else 68)
        code=f'<div class=c>Code {esc(b["code"])}</div>' if b.get('code') else ('<div class="c no">Final sale</div>' if b.get('final_sale') else '<div class="c no">No code needed</div>')
        for st in range(4):
            h=f'''{head(bs)}<body>{kick}{tile(hero,'hero',st>=1)}<div class="pick {'on' if st>=1 else ''}">The one I'd buy</div>
            <div class=mid><div class=num>{''.join('<i class="'+('d' if j<i else ('c' if j==i else ''))+'"></i>' for j in range(len(spec['brands'])))}</div><div class=b>{esc(b['brand'])}</div><div class=d>{esc(b['deal'])}</div>{code}</div>
            {tile(s1,'s1',st>=2)}{tile(s2,'s2',st>=3)}</body>'''
            frames.append((h,[0.45,0.5,0.32,b.get('hold',hold)][st],'whoosh' if st==0 else f'pop{st}'))
        cards.append(len(frames)-1)
    if nxt: frames.append((f'{head(100,150)}<body>{kick}<div class=ti><div class=a>Next</div><div class="ser h">{nxt}</div><div class=s>Follow so it finds you before the sales end.</div></div></body>',2.6,'whoosh'))
    render(frames,slug,cards)
if __name__=='__main__':
    for s in sys.argv[1:]:
        spec=json.load(open(f'{SP}/picks/{s}.json')); edition(spec)
