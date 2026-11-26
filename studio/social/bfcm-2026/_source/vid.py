import sys,os,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from lib import *
import numpy as np
from PIL import Image
B=SP+'/build'; CDN='https://cdn.shopify.com/s/files/1/'
def auto(url):
    src=fetch(url); a=np.asarray(Image.open(src).convert('RGB').resize((200,200))).astype(float)
    e=np.concatenate([a[:4].reshape(-1,3),a[-4:].reshape(-1,3),a[:,:4].reshape(-1,3),a[:,-4:].reshape(-1,3)])
    if e.mean()>222 and e.std()<14: return 'pack',packshot(url)
    return 'photo',photo(url)
def U(path,name,was,now,pos='50% 25%'):
    k,s=auto(CDN+path if not path.startswith('http') else path); return dict(kind=k,src=s,name=name,was=was,now=now,pos=pos)
def C(host,handle,name,img=0,now=None,was=None,pos='50% 20%'):
    p=prod(host,handle); k,s=auto(p['img'][img]); return dict(kind=k,src=s,name=name,was=was or p['ca'] or p['pr'],now=now if now is not None else p['pr'],pos=pos)
CSS='''<style>
.kick{position:absolute;left:72px;top:168px;right:72px;display:flex;justify-content:space-between}
.kick .lab{font-size:22px;color:var(--muted)} .kick .lab:first-child{color:var(--ink)}
.tiles{position:absolute;left:60px;right:60px;display:grid;grid-template-columns:1fr 1fr;gap:20px}
.t1{top:230px}.t2{top:1150px}
.tile{background:var(--paper);border-radius:10px;overflow:hidden;position:relative;opacity:0}
.t1 .tile{height:560px}.t2 .tile{height:400px}
.tile.on{opacity:1}
.tile img{position:absolute;left:0;top:0;width:100%;height:calc(100% - 78px)}
.tile.k-pack img{left:7%;top:4%;width:86%;height:calc(92% - 78px);object-fit:contain;mix-blend-mode:multiply}
.tile.k-photo img{object-fit:cover}
.tag{position:absolute;left:0;right:0;bottom:0;height:78px;background:var(--paper);display:flex;align-items:center;justify-content:space-between;padding:0 20px;gap:10px}
.tag .n{font-family:'Inter Tight';font-weight:600;font-size:21px;letter-spacing:.04em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#3d3832}
.tag .p{white-space:nowrap;font-family:'Bodoni Moda';font-size:40px} .tag .p s{font-family:Newsreader;font-size:24px;color:var(--muted);margin-right:8px}
.mid{position:absolute;left:60px;right:60px;top:812px;height:320px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.mid .num{font-family:'Bodoni Moda';font-style:italic;font-size:44px;color:var(--acc)}
.mid .b{font-family:'Bodoni Moda';font-size:BSpx;line-height:1;letter-spacing:-.015em;margin:2px 0 14px;white-space:nowrap}
.mid .d{font-family:'Inter Tight';font-weight:700;font-size:34px;letter-spacing:.14em;text-transform:uppercase}
.mid .c{margin-top:14px;font-family:'Inter Tight';font-weight:700;font-size:28px;letter-spacing:.12em;text-transform:uppercase;background:var(--ink);color:var(--ivory);padding:10px 22px 9px;border-radius:999px}
.mid .c.no{background:none;color:var(--muted);padding:0;font-weight:600;font-size:24px}
.ti{position:absolute;left:72px;right:72px;top:470px}
.ti .a{font-family:'Inter Tight';font-weight:700;font-size:40px;letter-spacing:.2em;text-transform:uppercase;color:var(--acc)}
.ti .h{font-family:'Bodoni Moda';font-size:168px;line-height:.92;letter-spacing:-.02em;margin:22px 0 40px}
.ti .s{font-family:Newsreader;font-style:italic;font-size:52px;line-height:1.2;color:#3d3832;max-width:860px}
</style>'''
def head(bs=104): return f'<!doctype html><meta charset=utf-8><link rel=stylesheet href="{B}/base.css">'+CSS.replace('BS',str(bs))
def tile(it,on): 
    return f'<div class="tile k-{it["kind"]} {"on" if on else ""}"><img src="{it["src"]}" style="object-position:{it["pos"]}"><div class=tag><span class=n>{esc(it["name"])}</span><span class=p><s>{money(it["was"])}</s>{money(it["now"])}</span></div></div>'
def edition(slug,title,sub,brands,nxt):
    out=SP+'/out3/'+slug; os.makedirs(out,exist_ok=True)
    import shutil; shutil.rmtree(out); os.makedirs(out)
    frames=[]  # (html, seconds)
    kick=f'<div class=kick><span class=lab>Black Friday</span><span class=lab>{title} edition</span></div>'
    frames.append((f'{head()}<body>{kick}<div class=ti><div class=a>Black Friday</div><div class="ser h">{title}<br><span class=it>edition.</span></div><div class=s>{sub}</div></div></body>',2.4))
    for i,b in enumerate(brands):
        its=b['items']; n=len(its); top=its[:2]; bot=its[2:4]
        bs=104 if len(b['brand'])<=14 else (84 if len(b['brand'])<=19 else 70)
        code=f'<div class=c>Code {b["code"]}</div>' if b.get('code') else '<div class="c no">No code needed</div>'
        for st in range(n+1):
            h=f'''{head(bs)}<body>{kick}<div class="tiles t1">{''.join(tile(t,k<st) for k,t in enumerate(top))}</div>
            <div class=mid><div class=num>{i+1} of {len(brands)}</div><div class=b>{esc(b["brand"])}</div><div class=d>{b["deal"]}</div>{code}</div>
            <div class="tiles t2">{''.join(tile(t,k+2<st) for k,t in enumerate(bot))}</div></body>'''
            frames.append((h,0.45 if st==0 else (0.32 if st<n else b.get('hold',3.4))))
        open(out+f'/card-{i+1:02d}.html','w').write(h)
    frames.append((f'{head()}<body>{kick}<div class=ti><div class=a>Next</div><div class="ser h" style="font-size:150px">{nxt}<br><span class=it>edition.</span></div><div class=s>Follow so it finds you before the sales end.</div></div></body>',2.6))
    fd=out+'/f'; os.makedirs(fd,exist_ok=True)
    for k,(h,_) in enumerate(frames): open(f'{fd}/{k:03d}.html','w').write(h)
    subprocess.run(['node',B+'/shoot.js',fd],check=True)
    lst=''.join(f"file '{fd}/{k:03d}.jpg'\nduration {d}\n" for k,(_,d) in enumerate(frames))+f"file '{fd}/{len(frames)-1:03d}.jpg'\n"
    open(fd+'/list.txt','w').write(lst)
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',fd+'/list.txt','-vf','fps=30,format=yuv420p','-c:v','libx264','-crf','19',f'{SP}/out3/{slug}.mp4'],check=True)
    # sound effects: a soft pop when each photo lands, a whoosh on each new brand
    t=0; pops=[]; whoosh=[]; prev=None
    for k,(h,d) in enumerate(frames):
        on=h.count('class="tile k-pack on"')+h.count('class="tile k-photo on"'); isc='class=mid' in h
        if k>0 and (not isc or on==0): whoosh.append(t)
        elif isc and on>0: pops.append((t,on))
        t+=d
    total=t; ins=[]; fl=[]; n=0
    for (tt,on) in pops:
        f0=520+90*on
        ins+=['-f','lavfi','-t','0.16','-i',f"aevalsrc=0.55*sin(2*PI*({f0}+900*exp(-45*t))*t)*exp(-30*t):s=44100"]
        fl.append(f'[{n}]adelay={int(tt*1000)}:all=1[a{n}]'); n+=1
    for tt in whoosh:
        ins+=['-f','lavfi','-t','0.34','-i','anoisesrc=c=pink:r=44100:a=0.5']
        fl.append(f"[{n}]highpass=f=500,lowpass=f=3500,afade=t=in:d=0.2,afade=t=out:st=0.22:d=0.12,adelay={max(0,int((tt-0.24)*1000))}:all=1[a{n}]"); n+=1
    fc=';'.join(fl)+';'+''.join(f'[a{i}]' for i in range(n))+f'amix=inputs={n}:normalize=0,apad,atrim=0:{total}[out]'
    subprocess.run(['ffmpeg','-v','error','-y']+ins+['-filter_complex',fc,'-map','[out]','-ar','44100',f'{SP}/out3/{slug}.wav'],check=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',f'{SP}/out3/{slug}.mp4','-i',f'{SP}/out3/{slug}.wav','-c:v','copy','-c:a','aac','-b:a','160k','-shortest',f'{SP}/out3/{slug}-sfx.mp4'],check=True)
    subprocess.run(['node',B+'/shoot.js',out],check=True)
    cs=sorted(f for f in os.listdir(out) if f.endswith('.jpg')); Sh=Image.new('RGB',(len(cs)*300,533))
    for i,f in enumerate(cs): Sh.paste(Image.open(out+'/'+f).resize((300,533)),(i*300,0))
    Sh.save(f'{SP}/out3/{slug}-cards.jpg',quality=85)
    json.dump([{k:v for k,v in b.items() if k!='items'}|{'items':[(t['name'],t['was'],t['now']) for t in b['items']]} for b in brands],open(f'{SP}/out3/{slug}.json','w'))
    print('ok',slug,sum(d for _,d in frames))
HM='heavenmayhem.com';AM='alexandramiro.com';AO='aliceandolivia.com';EP='emmeparsons.com';JS='jetsetcandy.com';PM='pastmidnight.com'
W=sys.argv[1:]
def Cq(host,handle,name,pct,img=0,pos='50% 20%'):
    p=prod(host,handle); k,s=auto(p['img'][img]); return dict(kind=k,src=s,name=name,was=p['pr'],now=round(p['pr']*(1-pct),2),pos=pos)
if 'best' in W: edition('best-deals','Best deals',"Seven sales where the discount is real. I went through each one.",[
 dict(brand='Alexandra Miro',deal='Up to 70% off',items=[C(AM,'harper-dress-red-capri','Harper dress',1),C(AM,'sophia-dress-scarf-print','Sophia dress'),C(AM,'vienna-swimsuit-scarf-print','Vienna swimsuit'),C(AM,'clementine-gown-red-capri','Clementine gown',1)]),
 dict(brand='Intentionally Blank',deal='Boots half off',items=[C('intentionallyblank.us','hiperson-leather-knee-high-boot','Hiperson knee boot'),C('intentionallyblank.us','filmore-suede-knee-boot','Filmore suede boot'),C('intentionallyblank.us','taffy-patent-leather-heeled-boot','Taffy patent boot'),C('intentionallyblank.us','florence-curved-heel-leather-ankle-boot','Florence ankle boot')]),
 dict(brand='Heaven Mayhem',deal='Up to 60% off sitewide',items=[C(HM,'alma-clip-on-earrings','Alma clip-ons',1),C(HM,'edith-earrings','Edith earrings'),C(HM,'plaza-earrings','Plaza earrings'),C(HM,'fashion-sunglasses-vittoria','Vittoria glasses')]),
 dict(brand='Jenni Kayne',deal='Coats 50 to 60% off',items=[U('0565/1234/8333/files/Olivia-Coat_Black.jpg','Olivia coat',1025,512.50),U('0565/1234/8333/files/Jessica-Sweater-Coat_Chocolate.jpg','Sweater coat',625,250),U('0565/1234/8333/files/Mccall-Trench-Coat_BritishKhaki.jpg','McCall trench',795,397.50)]),
 dict(brand='Emme Parsons',deal='40% off, private sale',items=[C(EP,'delicat-burnt-red-satin','Delicat, red satin'),C(EP,'isabel-black-calf','Isabel slingback'),C(EP,'salome-mary-jane-washed-gold-nappa','Salomé, gold'),C(EP,'stasera-marine-blue-nappa','Stasera, blue')]),
 dict(brand='alice + olivia',deal='Sale up to 60% off',items=[C(AO,'willa-silk-blouse-75','Willa silk blouse'),C(AO,'breann-embell-cutaway-blazer-off-white-gold','Breann blazer'),C(AO,'drew-oversized-wool-trench-coat','Drew wool coat'),C(AO,'alana-twist-strap-lace-godet-maxi-dress-black-almond','Alana lace dress')]),
 dict(brand='Past Midnight',deal='Only sale of the year',code='THESEASON',items=[C(PM,'the-flare-blue-gradient','The Flare, blue',now=109),C(PM,'the-flare-amber-gradient','The Flare, amber',now=109),C(PM,'the-frame-garnet','The Frame',now=101.25),C(PM,'the-flare-blue-gradient','The Flare, worn',1,now=109)]),
 ],'Travel')
if 'travel' in W: edition('travel','Travel',"Weekenders, flats, sunglasses and swim. Six sales worth packing for.",[
 dict(brand='BÉIS',deal='25% off sitewide',items=[Cq('beistravel.com','the-weekender-in-black','The Weekender',.25),Cq('beistravel.com','the-mini-weekender-in-midnight','Mini Weekender',.25),Cq('beistravel.com','the-weekender-in-beige','Weekender, beige',.25),Cq('beistravel.com','the-catchall-tote-in-black','Catchall tote',.25)]),
 dict(brand="Rothy's",deal='Up to 45% off',items=[C('rothys.com','the-almond-loafer-black','Almond loafer',1,pos='50% 80%'),C('rothys.com','the-lightweight-tote','Lightweight tote'),C('rothys.com','womens-double-bit-driver-sesame','Double Bit driver'),C('rothys.com','womens-apres-clog-revelvet-dove','Après clog')]),
 dict(brand='Heaven Mayhem',deal='30% off travel cases',items=[C(HM,'vintage-jewelry-travel-case','Vintage jewelry case'),C(HM,'jewelry-travel-case','Jewelry travel case'),C(HM,'zebra-jewelry-case','Jewelry case'),C(HM,'fashion-sunglasses-vittoria','Vittoria glasses')]),
 dict(brand='Past Midnight',deal='Only sale of the year',code='THESEASON',items=[C(PM,'the-flare-blue-gradient','The Flare, blue',now=109),C(PM,'the-flare-amber-gradient','The Flare, amber',1,now=109),C(PM,'the-frame-garnet','The Frame',now=101.25),C(PM,'the-scene-black','The Scene',now=93.75)]),
 dict(brand='Jet Set Candy',deal='Up to 50% off',items=[C(JS,'new-york-jfk-charm-silver-mini','JFK tag charm'),C(JS,'silver-trunk-suitcase-charm-stickers','Suitcase charm'),C(JS,'paris-france-cdg-charm-silver-mini','Paris CDG charm'),C(JS,'gold-enamel-poker-chips-charm','Poker chips charm')]),
 dict(brand='Alexandra Miro',deal='Swim 60% off',items=[C(AM,'vienna-swimsuit-scarf-print','Vienna swimsuit'),C(AM,'willow-swimsuit-scarf-print','Willow swimsuit'),C(AM,'carlotta-bikini-top-fluid-marble','Carlotta bikini top'),C(AM,'sophia-dress-scarf-print','Sophia cover-up')]),
 ],'Home')
if 'home' in W: edition('home','Home',"Linen, robes and pajamas. Four sales with real markdowns.",[
 dict(brand='Piglet in Bed',deal='Linen up to 60% off',items=[C('us.pigletinbed.com','pine-green-pembroke-gingham-linen-blend-duvet-cover','Gingham duvet, twin',1),C('us.pigletinbed.com','berry-heritage-gingham-100-linen-duvet-cover','Berry duvet, queen',1),C('us.pigletinbed.com','elderberry-gingham-linen-duvet-cover','Elderberry, twin',1),C('us.pigletinbed.com','sage-green-linen-duvet-cover','Sage duvet, twin',1)]),
 dict(brand='Brooklinen',deal='40% off last call',items=[C('brooklinen.com','luxe-core-sheet-set-last-call','Luxe sateen sheets',1),C('brooklinen.com','super-plush-robe-last-call','Super-Plush robe'),C('brooklinen.com','bigtime-robe-last-call','Bigtime robe'),C('brooklinen.com','weekend-wash-throw-blanket-last-call','Weekend throw')]),
 dict(brand='Parachute',deal='Up to 60% off, final sale',items=[C('parachutehome.com','organic-cloud-cotton-duvet-cover-set-white','Cloud cotton duvet set',1),C('parachutehome.com','classic-knit-alpaca-throw-charcoal','Alpaca throw',1),C('parachutehome.com','soft-spun-cotton-throw-natural','Cotton throw',1),C('parachutehome.com','organic-cloud-cotton-quilt-pebble','Cloud cotton quilt',1)]),
 dict(brand='LAKE Pajamas',deal='Up to 50% off',items=[C('lakepajamas.com','vintage-skis-crew-long-long-set','Vintage Skis pajamas',1),C('lakepajamas.com','night-before-christmas-long-long-set','Christmas pajamas',1),C('lakepajamas.com','tart-coupe-pant-set','Coupe pant set',1),C('lakepajamas.com','black-eyelet-cafe-dress','Eyelet cafe dress',1)]),
 ],'Makeup')
if 'makeup' in W: edition('makeup','Makeup',"Four beauty sales. One is half off everything, one only happens once a year.",[
 dict(brand='MAKE Beauty',deal='50% off almost everything',items=[C('makebeauty.com','cream-supreme','Cream Supreme lipstick'),C('makebeauty.com','heat-stroke','Heat Stroke blush stick'),C('makebeauty.com','skin-mimetic-microsuede-blush','Microsuede blush'),C('makebeauty.com','lash-prototype-volumizing-mascara','Lash Prototype')]),
 dict(brand='MERIT',deal='Only sale of the year',items=[C('meritbeauty.com','the-signature-lip-trio','Erdem lip trio'),C('meritbeauty.com','signature-lip','Signature lipstick'),C('meritbeauty.com','signature-lip-liner','Lip liner'),C('meritbeauty.com','the-great-skin-trio','Great Skin trio')]),
 dict(brand='Chantecaille',deal='Archive 40% off',code='CYBER',items=[C('chantecaille.com','radiance-elixir','Radiance Elixir'),C('chantecaille.com','cheek-light-blush-eclat-cristalline','Cheek Light blush'),C('chantecaille.com','flamingo-lip-chic-guava','Flamingo Lip Chic'),C('chantecaille.com','lip-chic-wild-rose-1','Lip Chic, Wild Rose')]),
 dict(brand='Tatcha',deal='Sets up to 32% off',code='CYBER26',items=[C('tatcha.com','the-starter-ritual-firming-and-smoothing-set','Starter Ritual set'),C('tatcha.com','am-pm-moisture-duo-gift-set','AM/PM Moisture duo'),C('tatcha.com','dewy-glow-protect-set','Dewy Glow set'),C('tatcha.com','dewy-bright-glossy-set','Dewy Bright set')]),
 ],'Jewelry')
