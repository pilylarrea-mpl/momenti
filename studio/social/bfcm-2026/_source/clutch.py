import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tour import *
OUT=SP+'/out/clutch'; os.makedirs(OUT,exist_ok=True)
for f in os.listdir(OUT): os.remove(OUT+'/'+f)
def M(url,brand,name,note,was,now,off=None,code=None,scale=1):
    return dict(src=packshot(url),thumb=packshot(url),kind='pack',brand=brand,name=name,note=note,was=was,now=now,off=off or f'{round(100*(1-now/was))}% off',code=code,scale=scale,pos='')
items=[
 M('https://cdn.shopify.com/s/files/1/1131/0390/files/1-MAKE_PDP_Lipstick_CapOff_Flourescense_NewBeautyAwards2024.jpg','MAKE Beauty','Cream Supreme Lipstick','Refillable, and half off in the listed price. $13.',26,13,scale=.9),
 M('https://cdn.shopify.com/s/files/1/1951/2637/files/3022076-hero.jpg','Chantecaille','Lip Cristal, Bijoux d\'Or','Limited edition. 25% off sitewide with the code.',55,41.25,code='CYBER',scale=.9),
 I('heavenmayhem.com','edith-earrings',0,'pack','Heaven Mayhem','Edith Earrings','For when the first pair starts to hurt at 11pm. 60% off.',scale=.85),
 I('jenniferbehr.com','abbie-barrette-crystal',0,'pack','Jennifer Behr','Abbie Barrette, Crystal','25% comes off at checkout on orders over $150.',was=228,now=171,scale=.85),
 I('pastmidnight.com','the-flare-blue-gradient',0,'pack','Past Midnight','The Flare, Blue Gradient','For the walk home at sunrise. Their only sale of the year.',now=109,off='60% off',code='THESEASON',scale=1.1),
 I('jetsetcandy.com','silver-trunk-suitcase-charm-stickers',0,'pack','Jet Set Candy','Vintage Suitcase Charm','Clip it to the chain. 41% off.',scale=.8),
]
S=[]
S.append(f'''{head()}<style>.h{{position:absolute;left:72px;right:72px;top:290px;font-size:120px;line-height:.96}}
.bagc{{position:absolute;left:30px;width:1020px;top:760px;filter:drop-shadow(0 34px 30px rgba(60,40,20,.28))}}
.p{{position:absolute;left:72px;right:160px;top:1360px;font-family:Newsreader;font-style:italic;font-size:44px;line-height:1.25;color:#3d3832}}</style>
<body><div class=top><img class=wm src="{WM}"><span class=lab>Black Friday, by size</span></div>
<h1 class="ser h">Six sale finds that fit in <span class=it>a clutch.</span></h1><img class=bagc src="{bag('monaco')}">
<p class=p>An evening bag holds about six things. These six are all on sale this week, from $13.</p></body>''')
for k,it in enumerate(items):
    code=f' &nbsp;·&nbsp; code {it["code"]}' if it['code'] else ''
    S.append(f'''{head()}<body><img class=pack src="{it["src"]}" style="transform:scale({it["scale"]})">
    <div class=chip><img src="{bag('monaco')}"><span class=lab>Fits in the clutch</span></div><div class="lab count dark">{k+1} / {len(items)}</div>
    <div class=info><div class="lab brand">{esc(it["brand"])}</div><h2>{esc(it["name"])}</h2>
    <div class=price><span class=was>{money(it["was"])}</span><span class=now>{money(it["now"])}</span><span class=off>{it["off"]}</span></div>
    <p class=note>{it["note"]}{code}</p></div></body>''')
tot_w=sum(i['was'] for i in items); tot_n=sum(i['now'] for i in items)
cells=''.join(f'<div><img src="{it["thumb"]}"><div class=lab>{esc(it["brand"])}</div><div class="ser n">{money(it["now"])}</div></div>' for it in items)
S.append(f'''{head()}<style>.t{{position:absolute;left:72px;top:262px;font-size:92px;line-height:1}}
.g{{position:absolute;left:72px;right:72px;top:410px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:22px 20px}}
.g div{{text-align:center}} .g img{{width:280px;height:280px;object-fit:contain;mix-blend-mode:multiply}} .g .lab{{font-size:17px;color:var(--acc)}} .g .n{{font-size:46px}}
.tot{{position:absolute;left:72px;right:72px;top:1260px;border-top:1.5px solid var(--hair);padding-top:26px;display:flex;justify-content:space-between;align-items:baseline}}
.tot .ser{{font-size:88px}} .tot s{{font-family:Newsreader;font-size:42px;color:var(--muted);margin-right:20px}}
.f{{position:absolute;left:72px;right:150px;top:1420px;font-family:Newsreader;font-style:italic;font-size:36px;color:#3d3832}}</style>
<body><div class=top><img class=wm src="{WM}"><span class=lab>Save this one</span></div><h2 class="ser t">The whole <span class=it>bag</span></h2>
<div class=g>{cells}</div><div class=tot><span class=lab>All six</span><span><s>{money(tot_w)}</s><span class=ser>{money(tot_n)}</span></span></div>
<p class=f>Prices checked Nov 26. The bag is ours. It isn't on sale.</p></body>''')
for i,s in enumerate(S): open(f'{OUT}/slide-{i+1:02d}.html','w').write(s)
subprocess.run(['node',B+'/shoot.js',OUT],check=True)
