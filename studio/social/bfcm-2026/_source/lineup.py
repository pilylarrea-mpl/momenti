import sys,json; sys.path.insert(0,'.')
from extra import *
LC=XCSS+'''<style>
.op{position:absolute;left:72px;right:72px;top:350px}
.op .a{font-family:'Inter Tight';font-weight:700;font-size:34px;letter-spacing:.2em;text-transform:uppercase;color:var(--acc)}
.op .h{font-family:'Bodoni Moda';font-size:132px;line-height:.95;letter-spacing:-.02em;margin:22px 0 34px}
.op .s{font-family:Newsreader;font-style:italic;font-size:50px;line-height:1.2;color:#3d3832;max-width:860px}
.op .g{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-top:54px}
.op .g div{height:250px;background:var(--paper);border-radius:10px;position:relative;overflow:hidden}
.op .g img{position:absolute;inset:6%;width:88%;height:88%;object-fit:contain;mix-blend-mode:multiply}
.op .g img.ph{inset:0;width:100%;height:100%;object-fit:cover;mix-blend-mode:normal}
.nb{position:absolute;left:72px;top:262px;font-family:'Bodoni Moda';font-style:italic;font-size:54px;color:var(--acc);z-index:4}
.pips{position:absolute;right:72px;top:282px;display:flex;gap:12px;z-index:4}.pips i{width:20px;height:20px;border-radius:50%;border:2.5px solid var(--acc);box-sizing:border-box}.pips i.d{background:var(--acc)}
.shotp{top:330px;height:760px}
.why{font-family:Newsreader;font-size:42px;line-height:1.25;margin-top:16px;opacity:0;max-width:820px}.why.on{opacity:1}
</style>'''
def hd2(): return head()+LC
def lineup(slug,kick_r,opener_h,opener_s,items,end_a,end_h):
    kick=f'<div class=kick><span class=lab>I read 376 sales</span><span class=lab>{kick_r}</span></div>'
    P=[]
    for it in items:
        R={r['h']:r for r in pick.rows(it['host'])}; r=R[it['handle']]; assert r['av']>0
        k,s=prep(r['img'][it.get('img',0)]); P.append(dict(it,kind=k,src=s,was=r['ca'],now=r['pr'],off=round(100*(1-r['pr']/r['ca']))))
    g=''.join(f'<div><img class="{"ph" if p["kind"]=="photo" else ""}" src="{p["src"]}"></div>' for p in P)
    frames=[(f'{hd2()}<body>{kick}<div class=op><div class=a>Black Friday</div><div class="ser h">{opener_h}</div><div class=s>{esc(opener_s)}</div><div class=g>{g}</div></div></body>',4.2,'whoosh')]
    cards=[0]
    for i,p in enumerate(P):
        media=f'<img class={"shot" if p["kind"]=="photo" else "shotp"} src="{p["src"]}" style="object-position:{p.get("pos","50% 60%")}">'
        pips='<div class=pips>'+''.join(f'<i class="{"d" if j<=i else ""}"></i>' for j in range(len(P)))+'</div>'
        def fr(stage):
            price=(f'<span class=w>{money(p["was"])}</span>' if stage==0 else f'<span class="w x">{money(p["was"])}</span><span class=n>{money(p["now"])}</span><span class=o>{p["off"]}% off</span>')
            return f'{hd2()}<body>{media}<div class=nb>{i+1}</div>{pips}<div class=sp><div class=br>{esc(p["brand"])}</div><h2>{esc(p["name"])}</h2><div class=pr>{price}</div><div class="why {"on" if stage==2 else ""}">{esc(p["why"])}</div></div></body>'
        frames+= [(fr(0),0.7,'whoosh'),(fr(1),1.2,'pop2'),(fr(2),p.get('hold',3.2),'pop3')]; cards.append(len(frames)-1)
    frames.append((f'{hd2()}<body>{kick}<div class=op><div class=a>{end_a}</div><div class="ser h" style="font-size:118px">{end_h}</div><div class=s>Follow so you see it before the sales end.</div></div></body>',3.0,'whoosh')); cards.append(len(frames)-1)
    render(frames,slug,cards)
if __name__=='__main__':
    IB='intentionallyblank.us'
    lineup('boots-edition','Boots','Four boots.<br><span class=it>All half off.</span>','I checked the sizes an hour ago. They are still there.',[
      dict(host=IB,handle='hiperson-leather-knee-high-boot',brand='Intentionally Blank',name='Hiperson Knee Boot',why='Leather, kitten heel. Black in every size.',img=0),
      dict(host=IB,handle='filmore-suede-knee-boot',brand='Intentionally Blank',name='Filmore Suede Boot',why='Suede, low heel, inside zip. Every size in stock.',img=0),
      dict(host=IB,handle='florence-curved-heel-leather-ankle-boot',brand='Intentionally Blank',name='Florence Chelsea Boot',why='The ankle version. Leather, every size.',img=0),
      dict(host='nisolo.com',handle='go-to-lace-lug-boot-black',brand='Nisolo',name='Go-To Lace Lug Boot',why='Water-resistant suede. Final sale; 10 and 11 are gone.',img=0)],
      'Tomorrow','Jewelry:<br><span class=it>from $26.</span>')
