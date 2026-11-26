import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tour import *
OUT=SP+'/out2/i-counted'; os.makedirs(OUT,exist_ok=True)
for f in os.listdir(OUT): os.remove(OUT+'/'+f)
CSS='''<style>
.claim{position:absolute;left:72px;right:72px;top:250px}
.claim .q{font-size:66px;line-height:1.05;margin-top:12px}
.big{position:absolute;left:72px;top:470px;font-size:230px;line-height:.9;letter-spacing:-.03em}
.big small{font-size:74px;letter-spacing:-.01em}
.what{position:absolute;left:72px;right:72px;top:700px;font-family:Newsreader;font-size:40px;line-height:1.2;color:#3d3832}
.dots{position:absolute;left:72px;top:810px;width:936px;display:flex;flex-wrap:wrap;gap:VGAPpx}
.dots i{width:VDpx;height:VDpx;border-radius:50%;border:2px solid rgba(28,26,24,.35)}
.dots i.on{background:var(--acc);border-color:var(--acc)}
.pick{position:absolute;left:72px;right:72px;top:1170px;display:flex;gap:28px;align-items:center;border-top:1.5px solid var(--hair);padding-top:22px}
.pick img{width:230px;height:230px;object-fit:contain;mix-blend-mode:multiply}
.pick img.ph{object-fit:cover;object-position:50% 20%;mix-blend-mode:normal;border-radius:4px}
.pick .nm{font-size:50px;line-height:1.05;margin:8px 0}
.pick .p{font-family:Newsreader;font-size:38px}.pick .p s{color:var(--muted)}
</style>'''
def slide(brand,claim,num,den,what,pick,k,n):
    cols=30 if den>400 else (20 if den>150 else 15)
    dots_n=den; 
    if den>400: # one dot = several pieces
        unit=round(den/300); dots_n=round(den/unit); on=round(num/unit); foot=f'Each dot is {unit} pieces.'
    else: on=num; foot=''
    gap=8; d=(936-gap*(cols-1))/cols
    rows=-(-dots_n//cols)
    if rows*(d+gap)>330: 
        cols=int(cols*1.4); d=(936-gap*(cols-1))/cols
    css=CSS.replace('VGAP',str(gap)).replace('VD',f'{d:.2f}')
    dots=''.join(f'<i class="{"on" if i<on else ""}"></i>' for i in range(dots_n))
    it=pick
    return f'''{head()}{css}<body><div class=top><span class=lab style="color:var(--ink)">I read 376 sales</span><span class=lab>{k} / {n}</span></div>
    <div class=claim><div class="lab" style="color:var(--acc)">{brand}</div><div class="it q">&ldquo;{claim}&rdquo;</div></div>
    <div class="ser big">{num}<small> of {den}</small></div>
    <div class=what>{what} {foot}</div>
    <div class=dots>{dots}</div>
    <div class=pick><img class="{'ph' if it['kind']=='photo' else ''}" src="{it['thumb']}"><div><div class=lab style="font-size:20px;color:var(--acc)">One that really is</div><div class="ser nm">{esc(it['name'])}</div><div class=p><s>{money(it['was'])}</s> &nbsp;{money(it['now'])} &nbsp;·&nbsp; {it['off']}</div></div></div>
    </body>'''
S=[]
S.append(f'''{head()}<style>.h{{position:absolute;left:72px;right:72px;top:330px;font-size:150px;line-height:.93}}
.s{{position:absolute;left:72px;right:140px;top:900px;font-size:74px;line-height:1.05}}
.p{{position:absolute;left:72px;right:160px;top:1180px;font-family:Newsreader;font-style:italic;font-size:42px;line-height:1.25;color:#3d3832}}</style>
<body><div class=top><span class=lab style="color:var(--ink)">I read 376 sales</span><span class=lab>Black Friday, checked</span></div>
<h1 class="it h">&ldquo;Up to<br>60% off.&rdquo;</h1><div class="ser s">I counted how many pieces actually are.</div>
<p class=p>I went through the full catalog of five stores, piece by piece. 2,074 in-stock items.</p></body>''')
P=[('Heaven Mayhem says','Up to 60% off sitewide',24,180,'in-stock pieces are 60% off or more. The usual markdown is 30%.',I('heavenmayhem.com','alma-clip-on-earrings',1,'pack','','Alma Clip-On Earrings','')),
   ('Jet Set Candy says','Up to 50% off',46,923,'pieces are 50% off. The usual markdown is 26%.',I('jetsetcandy.com','gold-enamel-poker-chips-charm',0,'pack','','Poker Chips Charm, Gold','')),
   ('alice + olivia says','Sale: 60% off',10,713,'pieces are 60% off. Another 69 are 40% off. The rest take 25% with the code.',I('aliceandolivia.com','willa-silk-blouse-75',0,'photo','','Willa Silk Blouse','')),
   ('Emme Parsons','Private sale, up to 80%',55,133,'pairs are 40% off or more. Nothing is at the 80% her affiliate listing mentions.',I('emmeparsons.com','salome-mary-jane-washed-gold-nappa',0,'pack','','Salomé Mary Jane, Gold','')),
   ('Alexandra Miro, listed as','20 to 50% off',63,125,'pieces are 50% off or more. She undersold it: 17 are at 60%.',I('alexandramiro.com','clementine-gown-red-capri',1,'photo','','Clementine Gown, Red Capri',''))]
for k,p in enumerate(P): S.append(slide(*p,k+1,len(P)))
S.append(f'''{head()}<style>.h{{position:absolute;left:72px;right:72px;top:300px;font-size:104px;line-height:1}}
.l{{position:absolute;left:72px;right:72px;top:760px}} .l div{{font-family:Newsreader;font-size:44px;line-height:1.25;padding:26px 0;border-top:1.5px solid var(--hair)}} .l b{{font-family:'Bodoni Moda';font-weight:400;font-size:54px}}
.f{{position:absolute;left:72px;right:150px;top:1330px;font-size:58px;line-height:1.08}}</style>
<body><div class=top><span class=lab style="color:var(--ink)">I read 376 sales</span><span class=lab>Save this one</span></div>
<h2 class="ser h">How to read<br><span class=it>&ldquo;up to.&rdquo;</span></h2>
<div class=l><div><b>Sort by price, low to high.</b><br>The top discount sits on a handful of pieces.</div><div><b>Check sizes before you fall for it.</b><br>The deepest cuts are often one size, final sale.</div></div>
<div class="ser f">I am going through all 376 sales this week. <span class=it>Follow for the next cut.</span></div></body>''')
for i,s in enumerate(S): open(f'{OUT}/slide-{i+1:02d}.html','w').write(s)
subprocess.run(['node',B+'/shoot.js',OUT],check=True)
