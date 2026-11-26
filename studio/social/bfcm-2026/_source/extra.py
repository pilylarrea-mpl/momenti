"""'I counted' and 'One thing' video templates."""
import sys,os,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from vid2 import *
XCSS='''<style>
.cl{position:absolute;left:72px;right:72px;top:250px}
.cl .who{font-family:'Inter Tight';font-weight:700;font-size:34px;letter-spacing:.18em;text-transform:uppercase;color:var(--acc)}
.cl .q{font-family:'Bodoni Moda';font-style:italic;font-size:150px;line-height:.95;margin-top:14px}
.cl .q.sm{font-size:84px;font-style:normal;line-height:1.02}
.big{position:absolute;left:72px;top:520px;font-family:'Bodoni Moda';font-size:250px;line-height:.9;letter-spacing:-.03em;font-variant-numeric:tabular-nums}
.big small{font-size:70px;letter-spacing:-.01em}
.what{position:absolute;left:72px;right:72px;top:770px;font-family:Newsreader;font-size:46px;line-height:1.2;color:#3d3832}
.dots{position:absolute;left:72px;top:930px;width:936px;display:flex;flex-wrap:wrap;gap:7px}
.dots i{width:24.4px;height:24.4px;border-radius:50%;border:2px solid rgba(28,26,24,.3)}
.dots i.on{background:var(--acc);border-color:var(--acc)}
.foot{position:absolute;left:72px;top:1500px;font-family:'Inter Tight';font-weight:600;font-size:22px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
.shot{position:absolute;left:0;top:0;width:1080px;height:1130px;object-fit:cover}
.shotp{position:absolute;left:90px;top:230px;width:900px;height:860px;object-fit:contain;mix-blend-mode:multiply}
.sp{position:absolute;left:72px;right:120px;top:1170px}
.sp .br{font-family:'Inter Tight';font-weight:700;font-size:26px;letter-spacing:.2em;text-transform:uppercase;color:var(--acc)}
.sp h2{font-family:'Bodoni Moda';font-weight:400;font-size:66px;line-height:1.02;margin:10px 0 14px}
.pr{display:flex;align-items:baseline;gap:24px}
.pr .w{font-family:Newsreader;font-size:60px;color:var(--ink)} .pr .w.x{color:var(--muted);text-decoration:line-through;text-decoration-thickness:3px;font-size:44px}
.pr .n{font-family:'Bodoni Moda';font-size:120px;line-height:1;font-variant-numeric:tabular-nums}
.pr .o{font-family:'Inter Tight';font-weight:700;font-size:26px;letter-spacing:.16em;text-transform:uppercase;background:var(--acc);color:#fff;padding:10px 18px 9px;border-radius:999px;align-self:center}
.rs{margin-top:16px} .rs div{font-family:Newsreader;font-size:40px;line-height:1.3;opacity:0} .rs div.on{opacity:1} .rs div.cv{font-style:italic;color:var(--muted)}
.rs b{font-family:'Bodoni Moda';font-style:italic;font-weight:400;color:var(--acc);margin-right:12px}
</style>'''
def hd(*a): return head(*a)+XCSS
def counted(spec):
    kick='<div class=kick><span class=lab>I read 376 sales</span><span class=lab>I counted</span></div>'
    tot,cnt=spec['total'],spec['count']; unit=max(1,round(tot/480)); nd=round(tot/unit); frames=[]
    frames.append((f'{hd()}<body>{kick}<div class=cl><div class=who>{esc(spec["brand"])} says</div><div class=q>&ldquo;{esc(spec["claim"])}&rdquo;</div></div></body>',1.7,'whoosh'))
    def grid(n): return '<div class=dots>'+''.join(f'<i class="{"on" if i<round(n/unit) else ""}"></i>' for i in range(nd))+'</div>'
    base=lambda n,what:f'{hd()}<body>{kick}<div class=cl><div class=who>{esc(spec["brand"])} says</div><div class="q sm">&ldquo;{esc(spec["claim"])}&rdquo;</div></div><div class=big>{n:,}<small> of {tot:,}</small></div><div class=what>{what}</div>{grid(n)}<div class=foot>Each dot is {unit} pieces in stock</div></body>'
    frames.append((base(0,'So I read the whole store.'),1.3,'whoosh'))
    steps=[round(cnt*f) for f in (.12,.3,.5,.7,.86,.95)]
    for k,n in enumerate(steps): frames.append((base(n,'So I read the whole store.'),0.2,f'pop{k+1}'))
    frames.append((base(cnt,spec['what']),3.0,'pop7')); card=len(frames)-1
    b=spec; its=[item(b['host'],x) for x in b['items']]; its.sort(key=lambda x:not x['hero'])
    for st in range(4):
        h=f'''{hd(84)}<body>{kick}{tile(its[0],'hero',st>=1)}<div class="pick {'on' if st>=1 else ''}">The one I'd buy</div>
        <div class=mid><div class=num>from the {cnt:,}</div><div class=b>{esc(spec.get("mid","Three worth it"))}</div><div class=d>{esc(spec["brand"])}</div><div class="c no">{esc(spec.get("terms","No code needed"))}</div></div>{tile(its[1],'s1',st>=2)}{tile(its[2],'s2',st>=3)}</body>'''
        frames.append((h,[0.4,0.5,0.32,3.2][st],'whoosh' if st==0 else f'pop{st}'))
    frames.append((f'{hd(100,140)}<body>{kick}<div class=ti><div class=a>Next</div><div class="ser h">{spec["next"]}</div><div class=s>Tell me a store and I\'ll count it.</div></div></body>',2.6,'whoosh'))
    render(frames,spec['slug'],[0,card,len(frames)-2])
def spotlight(sp,slug,nxt="Follow. I'm reading the rest."):
    R={r['h']:r for r in pick.rows(sp['host'])}; r=R[sp['handle']]; assert r['av']>0
    imgs=[prep(r['img'][min(i,len(r['img'])-1)]) for i in sp['imgs']][:3]
    while len(imgs)<3: imgs.append(imgs[-1])
    was,now=r['ca'],r['pr']; off=round(100*(1-now/was))
    kick='<div class=kick><span class=lab style="color:#fff;mix-blend-mode:difference">I read 376 sales</span><span class=lab style="color:#fff;mix-blend-mode:difference">One thing</span></div>'
    def media(i):
        k,s=imgs[i]; return f'<img class={"shot" if k=="photo" else "shotp"} src="{s}" style="object-position:50% 25%">'
    def fr(i,price,nre=0,cav=False):
        rs=''.join(f'<div class="{"on" if j<nre else ""}"><b>{j+1}</b>{esc(x)}</div>' for j,x in enumerate(sp['reasons'][:3]))+f'<div class="cv {"on" if cav else ""}">{esc(sp["caveat"])}</div>'
        return f'{hd()}<body>{media(i)}{kick}<div class=sp><div class=br>{esc(sp["brand"])}</div><h2>{esc(sp["name"])}</h2><div class=pr>{price}</div><div class=rs>{rs}</div></div></body>'
    P0=f'<span class=w>{money(was)}</span>'; frames=[(fr(0,P0),1.1,'whoosh')]
    for k,f in enumerate((.8,.55,.3,.12)): frames.append((fr(0,f'<span class="w x">{money(was)}</span><span class=n>{money(round(now+(was-now)*f))}</span>'),0.12,f'pop{k+1}'))
    PF=f'<span class="w x">{money(was)}</span><span class=n>{money(now)}</span><span class=o>{off}% off</span>'
    frames.append((fr(0,PF),1.5,'pop6')); card=len(frames)-1
    frames.append((fr(1,PF,1),1.5,'pop2')); frames.append((fr(2,PF,2),1.5,'pop3')); frames.append((fr(0,PF,3),1.5,'pop4')); frames.append((fr(0,PF,3,True),2.2,'whoosh')); last=len(frames)-1
    frames.append((f'{hd(100,140)}<body><div class=kick><span class=lab>I read 376 sales</span><span class=lab>One thing</span></div><div class=ti><div class=a>Sale ends {esc(sp.get("ends_txt","Dec 1"))}</div><div class="ser h">{nxt}</div></div></body>',2.2,'whoosh'))
    render(frames,slug,[card,last])
