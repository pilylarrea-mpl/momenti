import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from lib import *
B=SP+'/build'
def head(): return f'<!doctype html><meta charset=utf-8><link rel=stylesheet href="{B}/base.css"><style>.top .lab{{font-size:21px;color:var(--muted)}} .chip{{padding:16px 26px}} .chip .lab{{font-size:20px}}</style>'
TOP=lambda r:f'<div class=top><span class=lab style="color:var(--ink)">I read 376 sales</span><span class=lab>{r}</span></div>'
def I(host,handle,img,kind,brand,name,note,was=None,now=None,off=None,pos='50% 30%',code=None,scale=1,tag=None):
    p=prod(host,handle); was=was or p['ca'] or p['pr']; now=now if now is not None else p['pr']
    f=photo if kind=='photo' else packshot
    return dict(src=f(p['img'][img]),thumb=f(p['img'][img]),kind=kind,brand=brand,name=name,note=note,was=was,now=now,off=off or f'{round(100*(1-now/was))}% off',pos=pos,code=code,scale=scale,tag=tag)
def M(url,kind,brand,name,note,was,now,off=None,code=None,scale=1,pos='50% 30%',tag=None):
    f=photo if kind=='photo' else packshot
    return dict(src=f(url),thumb=f(url),kind=kind,brand=brand,name=name,note=note,was=was,now=now,off=off or f'{round(100*(1-now/was))}% off',code=code,scale=scale,pos=pos,tag=tag)
def thumbs(items,n=4):
    return ''.join(f'<div class="c k{it["kind"]}"><img src="{it["thumb"]}" style="object-position:{it["pos"]}"></div>' for it in items[:n])
def post(slug,label,hook,sub,items,chip,list_title,foot,end,big=None,total=False):
    out=SP+'/out2/'+slug; os.makedirs(out,exist_ok=True)
    for f in os.listdir(out): os.remove(out+'/'+f)
    S=[]
    S.append(f'''{head()}<style>.col{{position:absolute;left:72px;right:72px;top:270px}}
    .h{{font-size:124px;line-height:.96}}
    .sub{{font-family:Newsreader;font-style:italic;font-size:46px;line-height:1.22;color:#3d3832;margin:36px 48px 56px 0}}
    .gr{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
    .gr .c{{height:{'330' if hook.count('<br>')>=2 else '390'}px;background:var(--paper);border-radius:6px;overflow:hidden;position:relative}}
    .gr img{{position:absolute;inset:0;width:100%;height:100%}} .gr .kpack img{{inset:8%;width:84%;height:84%;object-fit:contain;mix-blend-mode:multiply}} .gr .kphoto img{{object-fit:cover}}
    .sw{{margin-top:34px;color:var(--acc)}}</style><body>{TOP(label)}
    <div class=col><h1 class="ser h">{hook}</h1><p class=sub>{sub}</p><div class=gr>{thumbs(items)}</div><div class="lab sw">Swipe &rarr;</div></div></body>''')
    for k,it in enumerate(items):
        ch=it['tag'] or (chip(k,it) if callable(chip) else chip)
        media=(f'<img class=shot src="{it["src"]}" style="object-position:{it["pos"]}"><div class=shade></div>' if it['kind']=='photo' else f'<img class=pack src="{it["src"]}" style="transform:scale({it["scale"]})">')
        code=f' &nbsp;·&nbsp; code {it["code"]}' if it['code'] else ''
        S.append(f'''{head()}<body>{media}<div class=chip><span class=lab>{ch}</span></div>
        <div class="lab count" style="color:{'#fff' if it['kind']=='photo' else 'var(--muted)'}">{k+1} / {len(items)}</div>
        <div class=info><div class="lab brand">{esc(it["brand"])}</div><h2>{esc(it["name"])}</h2>
        <div class=price><span class=was>{money(it["was"])}</span><span class=now>{money(it["now"])}</span><span class=off>{it["off"]}</span></div>
        <p class=note>{it["note"]}{code}</p></div></body>''')
    rows=''.join(f'''<div class=row><div class=th><img src="{it["thumb"]}" class="{'pk' if it['kind']=='pack' else 'ph'}"></div>
      <div class=tx><div class="lab b">{esc(it["brand"])}</div><div class="ser nm">{esc(it["name"])}</div></div>
      <div class=pr><span class=w>{money(it["was"])}</span><span class="ser n">{money(it["now"])}</span></div></div>''' for it in items)
    tw=sum(i['was'] for i in items); tn=sum(i['now'] for i in items)
    tot=f'<div class=tot><span class=lab>The whole look</span><span><s>{money(tw)}</s><span class=ser>{money(tn)}</span></span></div>' if total else ''
    rh=118 if len(items)>6 else 150
    S.append(f'''{head()}<style>.ttl{{position:absolute;left:72px;right:72px;top:250px;font-size:84px;line-height:1}}
    .rows{{position:absolute;left:72px;right:72px;top:{'470' if '<br>' in list_title else '390'}px}}
    .row{{display:flex;align-items:center;gap:28px;padding:{12 if len(items)>6 else 18}px 0;border-top:1.5px solid var(--hair)}}
    .th{{width:{rh}px;height:{rh}px;flex:none}} .th img{{width:{rh}px;height:{rh}px}} .th .pk{{object-fit:contain;mix-blend-mode:multiply}} .th .ph{{object-fit:cover;object-position:50% 20%;border-radius:4px}}
    .tx{{flex:1}} .tx .b{{font-size:18px;color:var(--acc)}} .tx .nm{{font-size:{36 if len(items)>6 else 40}px;line-height:1.06;margin-top:4px}}
    .pr{{text-align:right;white-space:nowrap}} .pr .w{{display:block;font-size:26px;color:var(--muted);text-decoration:line-through}} .pr .n{{font-size:{50 if len(items)>6 else 56}px;line-height:1}}
    .tot{{border-top:3px solid var(--ink);padding-top:20px;margin-top:4px;display:flex;justify-content:space-between;align-items:baseline}} .tot .ser{{font-size:84px}} .tot s{{font-family:Newsreader;font-size:40px;color:var(--muted);margin-right:18px}}
    .save{{font-family:Newsreader;font-style:italic;font-size:32px;color:#3d3832;line-height:1.3;margin-top:22px;border-top:1.5px solid var(--hair);padding-top:20px}}</style>
    <body>{TOP('Save this one')}<h2 class="ser ttl">{list_title}</h2><div class=rows>{rows}{tot}<p class=save>{foot}</p></div></body>''')
    S.append(f'''{head()}<style>.e{{position:absolute;left:72px;right:72px;top:420px;font-size:124px;line-height:.98}}
    .p{{position:absolute;left:72px;right:140px;top:1010px;font-size:64px;line-height:1.1}}</style><body>{TOP(label)}
    <h2 class="ser e">{end[0]}</h2><div class="ser p">{end[1]}</div></body>''')
    for i,s in enumerate(S): open(f'{out}/slide-{i+1:02d}.html','w').write(s)
    subprocess.run(['node',B+'/shoot.js',out],check=True)
    from PIL import Image; import glob
    fs=sorted(glob.glob(out+'/*.jpg')); Sh=Image.new('RGB',(len(fs)*300,533))
    for i,f in enumerate(fs): Sh.paste(Image.open(f).resize((300,533)),(i*300,0))
    Sh.save(SP+f'/out2/{slug}-overview.jpg',quality=85); print('ok',slug,len(fs))
