import sys,json,os,shutil,subprocess; sys.path.insert(0,'.')
from vid2 import *
from PIL import Image
OUT=SP+'/out4'
def hd(): return f'<!doctype html><meta charset=utf-8><link rel=stylesheet href="{B}/base.css"><style>.top .lab{{font-size:21px;color:var(--muted)}}</style>'
TOP=lambda r:f'<div class=top><span class=lab style="color:var(--ink)">I read 376 sales</span><span class=lab>{r}</span></div>'
def shoot(slug,S):
    out=f'{OUT}/{slug}'; shutil.rmtree(out,ignore_errors=True); os.makedirs(out)
    for i,s in enumerate(S): open(f'{out}/slide-{i+1:02d}.html','w').write(s)
    subprocess.run(['node',B+'/shoot.js',out],check=True)
    fs=sorted(f for f in os.listdir(out) if f.endswith('.jpg')); Sh=Image.new('RGB',(len(fs)*300,533))
    for i,f in enumerate(fs): Sh.paste(Image.open(f'{out}/{f}').resize((300,533)),(i*300,0))
    Sh.save(f'{OUT}/{slug}-overview.jpg',quality=85); print('ok',slug,len(fs))
def thumb(host,handle,img=0):
    r={x['h']:x for x in pick.rows(host)}[handle]; assert r['av']>0; k,s=prep(r['img'][min(img,len(r['img'])-1)]); return k,s,r
# ---------- codes
C=[c for c in json.load(open(SP+'/picks/codes.json')) if c.get('seen_on_site')]
note={'LulaKate':None,'TWOPAGES Curtains':'28% off selected picks','ANEMOS':'20% off select styles','Lizzie Fortunato':'Up to 20% off','Vince':'25% off, 30% off sweaters','Algenist':'Sitewide','Past Midnight':'Extra 25% off, only sale of the year','Petal & Pup':'30% off','Chantecaille':'25% off sitewide + gifts','Social Threads':'25% off sitewide'}
rowsC=[]
for c in C:
    if c['brand'] in note and note[c['brand']] is None: continue
    d=note.get(c['brand']) or (c.get('sheet_discount') or '').replace('–',' to ')
    e=(c.get('end') or '')[5:].replace('-','/')
    if c['brand']=='Social Threads': e='12/04'
    rowsC.append((c['brand'],c['code'].upper(),d,e))
rowsC.sort(key=lambda r:(r[3],r[0].lower()))
CSS='''<style>.h{position:absolute;left:72px;right:72px;top:270px;font-size:124px;line-height:.96}.sub{position:absolute;left:72px;right:120px;top:700px;font-family:Newsreader;font-style:italic;font-size:46px;line-height:1.22;color:#3d3832}
.ttl{position:absolute;left:72px;top:250px;font-size:76px;line-height:1}.rw{position:absolute;left:72px;right:72px;top:370px}
.r{display:flex;align-items:center;gap:20px;padding:19px 0;border-top:1.5px solid var(--hair)}.r .b{flex:1;min-width:0}.r .b .n{font-family:'Bodoni Moda';font-size:44px;line-height:1.05}.r .b .d{font-family:Newsreader;font-size:27px;color:var(--muted)}
.r .c{font-family:'Inter Tight';font-weight:700;font-size:27px;letter-spacing:.1em;background:var(--ink);color:var(--ivory);padding:11px 18px 10px;border-radius:999px;white-space:nowrap}.r .e{font-family:'Inter Tight';font-weight:600;font-size:21px;letter-spacing:.08em;color:var(--acc);white-space:nowrap;width:120px;text-align:right}
.ft{position:absolute;left:72px;right:120px;top:1420px;font-family:Newsreader;font-style:italic;font-size:31px;color:#3d3832;line-height:1.3}</style>'''
S=[f'{hd()}{CSS}<body>{TOP(f"Kept {len(rowsC)}")}<h1 class="ser h">Every code<br>that <span class=it>actually works.</span></h1><p class=sub>Your feed is full of Black Friday codes. I checked each one against the brand\'s own site. {len(rowsC)} are real.</p><div class="lab" style="position:absolute;left:72px;top:1000px;color:var(--acc)">Swipe &rarr; and save it</div></body>']
per=6
for p in range(0,len(rowsC),per):
    rr=''.join(f'<div class=r><div class=b><div class=n>{esc(b)}</div><div class=d>{esc(d)}</div></div><div class=c>{esc(c)}</div><div class=e>ends {e}</div></div>' for b,c,d,e in rowsC[p:p+per])
    S.append(f'{hd()}{CSS}<body>{TOP("Save this one")}<h2 class="ser ttl">Codes, <span class=it>checked</span></h2><div class=rw>{rr}</div><p class=ft>Each code was seen on the brand\'s own site on Nov 26.</p></body>')
S.append(f'{hd()}{CSS}<body>{TOP("Updated codes")}<h2 class="ser ttl">Codes going round<br>that <span class=it>changed</span></h2><div class=rw style="top:480px">'+''.join(f'<div class=r><div class=b><div class=n>{b}</div><div class=d>{d}</div></div><div class=c>{c}</div></div>' for b,d,c in [('Nette','The site now gives 30%, not 25%','NETTE30'),('Bonheur','30% off, double the old code','BLCKFDAY30'),('Boll &amp; Branch','25% off orders over $200','CYBER25'),('Kyrgies','25% off, one-time code','BISHKEK25')])+'</div><p class=ft>Follow. I recheck these every morning until the sales end.</p></body>')
shoot('codes',S)
# ---------- gifts under $25
G=json.load(open(SP+'/picks/gifts25.json'))['items']
ICSS='''<style>.pack{position:absolute;left:90px;top:270px;width:900px;height:880px;object-fit:contain;mix-blend-mode:multiply}.shot{position:absolute;left:0;top:0;width:1080px;height:1190px;object-fit:cover;object-position:50% 30%}
.chipx{position:absolute;left:60px;top:150px;background:var(--ivory);border-radius:999px;padding:16px 26px;z-index:6;box-shadow:0 6px 22px rgba(0,0,0,.16)}</style>'''
its=[]
for g in G:
    try: k,s,r=thumb(g['host'],g['handle'],g.get('img',0))
    except Exception as e: print('skip',g['brand'],g['handle'],e); continue
    its.append(dict(g,kind=k,src=s,was=r['ca'],now=r['pr']))
its.sort(key=lambda x:x['now'])
S=[f'{hd()}{CSS}<body>{TOP(f"Kept {len(its)}")}<h1 class="ser h">Gifts under $25<br>that were <span class=it>never $25.</span></h1><p class=sub>All {len(its)} are at least half off, and all were $40 or more last week. Cheapest first.</p><div class="lab" style="position:absolute;left:72px;top:1000px;color:var(--acc)">Swipe &rarr;</div></body>']
for i,g in enumerate(its):
    media=f'<img class=shot src="{g["src"]}">' if g['kind']=='photo' else f'<img class=pack src="{g["src"]}">'
    S.append(f'''{hd()}{ICSS}<body>{media}<div class=chipx><span class=lab style="font-size:20px">For {esc(g["for"])}</span></div><div class="lab count" style="color:{'#fff' if g['kind']=='photo' else 'var(--muted)'}">{i+1} / {len(its)}</div>
    <div class=info><div class="lab brand">{esc(g["brand"])}</div><h2>{esc(g["name"])}</h2><div class=price><span class=was>{money(g["was"])}</span><span class=now>{money(g["now"])}</span><span class=off>{round(100*(1-g["now"]/g["was"]))}% off</span></div></div></body>''')
shoot('gifts-under-25',S)
# ---------- I counted, corrected
A=pick.A
def st(h): a=A[h]; return a['instock'],a['ge50'],a['ge60']
D=[('BaubleBar says','30% off',st('baublebar.com')[1],st('baublebar.com')[0],'pieces are half off or more. The headline undersells it.',('baublebar.com','eliana-necklace-clear-gold',0)),
   ('Daze Denim says','25% off',st('dazedenim.com')[1],st('dazedenim.com')[0],'styles are half off or more. That is half the store.',None),
   ('alice + olivia says','25% off',st('aliceandolivia.com')[2],st('aliceandolivia.com')[0],'pieces are 60% off. The sale section is the real sale.',('aliceandolivia.com','willa-silk-blouse-75',0)),
   ('Jet Set Candy says','Up to 50% off',st('jetsetcandy.com')[1],st('jetsetcandy.com')[0],'pieces are 50% off. The usual markdown is 25%.',('jetsetcandy.com','gold-enamel-poker-chips-charm',0)),
   ('Heaven Mayhem says','Up to 60% off sitewide',st('heavenmayhem.com')[2],st('heavenmayhem.com')[0],'pieces are 60% off or more. The usual markdown is 30%.',('heavenmayhem.com','alma-clip-on-earrings',1))]
dz=json.load(open(SP+'/picks/denim.json')); dzh=[x for b in dz['brands'] if b['brand']=='Daze Denim' for x in b['items'] if x.get('hero')][0]
D[1]=D[1][:5]+(('dazedenim.com',dzh['handle'],dzh.get('img',0)),)
XC='''<style>.claim{position:absolute;left:72px;right:72px;top:250px}.claim .q{font-size:66px;line-height:1.05;margin-top:12px}.big{position:absolute;left:72px;top:470px;font-size:220px;line-height:.9;letter-spacing:-.03em}.big small{font-size:70px}
.what{position:absolute;left:72px;right:72px;top:700px;font-family:Newsreader;font-size:40px;line-height:1.2;color:#3d3832}.dots{position:absolute;left:72px;top:820px;width:936px;display:flex;flex-wrap:wrap;gap:7px}.dots i{width:24.4px;height:24.4px;border-radius:50%;border:2px solid rgba(28,26,24,.3)}.dots i.on{background:var(--acc);border-color:var(--acc)}
.pk{position:absolute;left:72px;right:72px;top:1250px;display:flex;gap:26px;align-items:center;border-top:1.5px solid var(--hair);padding-top:20px}.pk img{width:210px;height:210px;object-fit:contain;mix-blend-mode:multiply}.pk img.ph{object-fit:cover;object-position:50% 20%;mix-blend-mode:normal;border-radius:4px}.pk .nm{font-size:46px;line-height:1.05;margin:6px 0}.pk .p{font-family:Newsreader;font-size:36px}.pk s{color:var(--muted)}</style>'''
tot=sum(d[3] for d in D)
S=[f'{hd()}{CSS}<body>{TOP("I counted")}<h1 class="it h" style="font-size:150px">&ldquo;25% off.&rdquo;</h1><p class=sub style="top:640px;font-style:normal;font-family:\'Bodoni Moda\';font-size:70px;line-height:1.05;color:var(--ink)">I counted what the stores are actually doing.</p><p class=sub style="top:900px">Five stores, {tot:,} in-stock pieces, read one by one. Three are better than they say. Two are not.</p></body>']
for i,(who,claim,num,den,what,pk) in enumerate(D):
    unit=max(1,round(den/460)); nd=round(den/unit); dots=''.join(f'<i class="{"on" if j<round(num/unit) else ""}"></i>' for j in range(nd))
    k,s,r=thumb(*pk)
    S.append(f'''{hd()}{XC}<body>{TOP(f"{i+1} / {len(D)}")}<div class=claim><div class=lab style="color:var(--acc)">{who}</div><div class="it q">&ldquo;{claim}&rdquo;</div></div><div class="ser big">{num:,}<small> of {den:,}</small></div><div class=what>{what}{f" Each dot is {unit} pieces." if unit>1 else ""}</div><div class=dots>{dots}</div>
    <div class=pk><img class="{'ph' if k=='photo' else ''}" src="{s}"><div><div class=lab style="font-size:20px;color:var(--acc)">One worth it</div><div class="ser nm">{esc(r['t'].split(' - ')[0].title()[:30])}</div><div class=p><s>{money(r['ca'])}</s> &nbsp;{money(r['pr'])} &nbsp;·&nbsp; {r['off']}% off</div></div></div></body>''')
S.append(f'{hd()}{CSS}<body>{TOP("Save this one")}<h2 class="ser h" style="font-size:104px;top:300px">Tell me a store.<br><span class=it>I\'ll count it.</span></h2><p class=sub style="top:760px">I have the full catalog of 199 stores. Comment a name and it is tomorrow\'s post.</p></body>')
shoot('i-counted-v2',S)
