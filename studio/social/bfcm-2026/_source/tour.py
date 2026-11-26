import sys,os,json,shutil
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from lib import *
B=SP+'/build'
WM='/home/user/momenti/assets/logo/momenti-wordmark-ink.svg'; WMI='/home/user/momenti/assets/logo/momenti-wordmark-ivory.svg'
def head(): return f'<!doctype html><meta charset=utf-8><link rel=stylesheet href="{B}/base.css">'
def I(host,handle,img,kind,brand,name,note,was=None,now=None,off=None,pos='50% 30%',code=None,scale=1):
    p=prod(host,handle); was=was or p['ca'] or p['pr']; now=now if now is not None else p['pr']
    pct=round(100*(1-now/was)); 
    return dict(src=(photo if kind=='photo' else packshot)(p['img'][img]),kind=kind,brand=brand,name=name,note=note,was=was,now=now,off=off or f'{pct}% off',pos=pos,code=code,url=f'https://{host}/products/{handle}',thumb=packshot(p['img'][img]) if kind=='pack' else photo(p['img'][img]),scale=scale)
CITIES=json.load(open(B+'/tour.json')) if False else None
def render(city,items,n,total,nxt,outdir,hook,sub):
    os.makedirs(outdir,exist_ok=True)
    for f in os.listdir(outdir): os.remove(outdir+'/'+f)
    name,year,bagk=city
    S=[]
    # cover
    S.append(f'''{head()}<style>
    .hook{{position:absolute;left:72px;right:72px;top:300px;font-size:112px;line-height:.98}}
    .bagc{{position:absolute;left:30px;width:1020px;top:720px;filter:drop-shadow(0 34px 30px rgba(60,40,20,.28))}}
    .stop{{position:absolute;left:72px;right:72px;top:1330px}}
    .stop .t{{font-size:84px;line-height:1.02;margin-top:14px}}
    .stop p{{font-family:Newsreader;font-style:italic;font-size:37px;color:#3d3832;margin-top:16px;max-width:820px;line-height:1.25}}
    </style><body>
    <div class=top><img class=wm src="{WM}"><span class=lab>The Grand Tour &nbsp;·&nbsp; N° {n} of {total}</span></div>
    <h1 class="ser hook">{hook}</h1>
    <img class=bagc src="{bag(bagk)}">
    <div class=stop><div class=lab style="color:var(--acc)">Stop {n}</div><div class="ser t">{name}, <span class=it>{year}</span></div><p>{sub}</p></div>
    </body>''')
    for k,it in enumerate(items):
        chip=f'<div class=chip><img src="{bag(bagk)}"><span class=lab>{name}, {year}</span></div>'
        cnt=f'<div class="lab count {"dark" if it["kind"]=="pack" else ""}" style="{"color:#fff" if it["kind"]=="photo" else ""}">{k+1} / {len(items)}</div>'
        media=(f'<img class=shot src="{it["src"]}" style="object-position:{it["pos"]}"><div class=shade></div>' if it['kind']=='photo'
               else f'<img class=pack src="{it["src"]}" style="transform:scale({it["scale"]})">')
        code=f' &nbsp;·&nbsp; code {it["code"]}' if it['code'] else ''
        S.append(f'''{head()}<body>{media}{chip}{cnt}
        <div class=info><div class="lab brand">{esc(it["brand"])}</div><h2>{esc(it["name"])}</h2>
        <div class=price><span class=was>{money(it["was"])}</span><span class=now>{money(it["now"])}</span><span class=off>{it["off"]}</span></div>
        <p class=note>{it["note"]}{code}</p></div></body>''')
    # the list
    rows=''.join(f'''<div class=row><div class=th><img src="{it["thumb"]}" class="{'pk' if it['kind']=='pack' else 'ph'}"></div>
      <div class=tx><div class="lab b">{esc(it["brand"])}</div><div class="ser nm">{esc(it["name"])}</div></div>
      <div class=pr><span class=w>{money(it["was"])}</span><span class="ser n">{money(it["now"])}</span></div></div>''' for it in items)
    S.append(f'''{head()}<style>
    .ttl{{position:absolute;left:72px;top:262px;font-size:92px;line-height:1}}
    .rows{{position:absolute;left:72px;right:72px;top:420px}}
    .row{{display:flex;align-items:center;gap:30px;padding:20px 0;border-top:1.5px solid var(--hair)}}
    .row:last-child{{border-bottom:1.5px solid var(--hair)}}
    .th{{width:150px;height:150px;flex:none;display:flex;align-items:center;justify-content:center}}
    .th img{{width:150px;height:150px}} .th .pk{{object-fit:contain;mix-blend-mode:multiply}} .th .ph{{object-fit:cover;object-position:50% 25%;border-radius:4px}}
    .tx{{flex:1}} .tx .b{{font-size:19px;color:var(--acc)}} .tx .nm{{font-size:42px;line-height:1.06;margin-top:6px}}
    .pr{{text-align:right;white-space:nowrap}} .pr .w{{display:block;font-size:28px;color:var(--muted);text-decoration:line-through}} .pr .n{{font-size:58px;line-height:1}}
    .save{{position:absolute;left:72px;right:72px;top:1372px;font-family:Newsreader;font-style:italic;font-size:34px;color:#3d3832;line-height:1.3}}
    </style><body><div class=top><img class=wm src="{WM}"><span class=lab>Save this one</span></div>
    <h2 class="ser ttl">{name}, <span class=it>{year}</span></h2><div class=rows>{rows}</div>
    <p class=save>Prices checked on each brand's site, Nov 26. Most of these end Dec 1.</p></body>''')
    # next
    if nxt:
        S.append(f'''{head()}<style>
        .nx{{position:absolute;left:72px;right:72px;top:300px}} .nx .t{{font-size:118px;line-height:.98;margin-top:18px}}
        .bagc{{position:absolute;left:60px;width:960px;top:760px;filter:drop-shadow(0 34px 30px rgba(60,40,20,.28))}}
        .f{{position:absolute;left:72px;right:150px;top:1370px;font-size:60px;line-height:1.08}}
        </style><body><div class=top><img class=wm src="{WM}"><span class=lab>The Grand Tour &nbsp;·&nbsp; N° {n} of {total}</span></div>
        <div class=nx><div class=lab style="color:var(--acc)">Next stop</div><div class="ser t">{nxt[0]}, <span class=it>{nxt[1]}</span></div></div>
        <img class=bagc src="{bag(nxt[2])}">
        <div class="ser f">Follow, or you'll find this one <span class=it>after</span> the sale ends.</div></body>''')
    else:
        S.append(f'''{head()}<style>
        .q{{position:absolute;left:72px;right:72px;top:290px;font-size:112px;line-height:.98}}
        .g{{position:absolute;left:60px;right:60px;top:640px;display:grid;grid-template-columns:1fr 1fr;gap:26px 30px}}
        .g div{{text-align:center}} .g img{{width:100%;filter:drop-shadow(0 16px 14px rgba(60,40,20,.25))}} .g .lab{{font-size:19px;margin-top:6px;color:var(--muted)}}
        .g div:last-child{{grid-column:1/3}} .g div:last-child img{{width:50%}}
        </style><body><div class=top><img class=wm src="{WM}"><span class=lab>The Grand Tour</span></div>
        <h2 class="ser q">Which city <span class=it>are you?</span></h2>
        <div class=g>{''.join(f'<div><img src="{bag(b)}"><div class=lab>{c}</div></div>' for b,c in [('havana','Havana, 1958'),('monaco','Monaco, 1964'),('nyc','New York, 1977'),('miami','Miami, 1959'),('tokyo','Tokyo, 1995')])}</div></body>''')
    for i,s in enumerate(S): open(f'{outdir}/slide-{i+1:02d}.html','w').write(s)
    subprocess.run(['node',B+'/shoot.js',outdir],check=True)
    return items
