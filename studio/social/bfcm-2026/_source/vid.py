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
    subprocess.run(['node',B+'/shoot.js',out],check=True)
    cs=sorted(f for f in os.listdir(out) if f.endswith('.jpg')); Sh=Image.new('RGB',(len(cs)*300,533))
    for i,f in enumerate(cs): Sh.paste(Image.open(out+'/'+f).resize((300,533)),(i*300,0))
    Sh.save(f'{SP}/out3/{slug}-cards.jpg',quality=85)
    json.dump([{k:v for k,v in b.items() if k!='items'}|{'items':[(t['name'],t['was'],t['now']) for t in b['items']]} for b in brands],open(f'{SP}/out3/{slug}.json','w'))
    print('ok',slug,sum(d for _,d in frames))
HM='heavenmayhem.com';AM='alexandramiro.com';AO='aliceandolivia.com';EP='emmeparsons.com';JS='jetsetcandy.com';PM='pastmidnight.com'
W=sys.argv[1:]
if 'best' in W: edition('best-deals','Best deals',"Seven sales where the discount is real. I checked the prices.",[
 dict(brand='Alexandra Miro',deal='Up to 70% off',items=[C(AM,'harper-dress-red-capri','Harper dress',1),C(AM,'sophia-dress-scarf-print','Sophia dress'),C(AM,'vienna-swimsuit-scarf-print','Vienna swimsuit'),C(AM,'clementine-gown-red-capri','Clementine gown',1)]),
 dict(brand='Intentionally Blank',deal='Up to 75% off',items=[U('1420/0110/files/prettyplease2.png','Pretty Please heel',198,89),U('1420/0110/files/LEFTY-IVF2-1405-CRM02.jpg','Lefty mule',158,63),U('1420/0110/files/COCKTAIL-ISF2-1554-CRM03.jpg','Cocktail slide',218,87),U('1420/0110/files/ECHO_LEO-2.jpg','Echo kitten heel',188,75)]),
 dict(brand='Heaven Mayhem',deal='Up to 60% off sitewide',items=[C(HM,'gaze-choker','Gaze choker'),C(HM,'alma-clip-on-earrings','Alma clip-ons',1),C(HM,'plaza-earrings','Plaza earrings'),C(HM,'the-icon-watch','Icon watch')]),
 dict(brand='Jenni Kayne',deal='Up to 60% off',items=[U('0565/1234/8333/files/Olivia-Coat_Black.jpg','Olivia coat',1025,513),U('0565/1234/8333/files/Jessica-Sweater-Coat_Chocolate.jpg','Sweater coat',625,250),U('0565/1234/8333/files/Mccall-Trench-Coat_BritishKhaki.jpg','McCall trench',795,397.50),U('0565/1234/8333/files/Long-Shearling-Yves-Shawl-Coat_Black-1.jpg','Shearling coat',1895,947.50)]),
 dict(brand='Emme Parsons',deal='40% off, private sale',items=[C(EP,'delicat-burnt-red-satin','Delicat, red satin'),C(EP,'isabel-black-calf','Isabel slingback'),C(EP,'salome-mary-jane-washed-gold-nappa','Salomé, gold'),C(EP,'stasera-marine-blue-nappa','Stasera, blue')]),
 dict(brand='alice + olivia',deal='Sale up to 60% off',items=[C(AO,'willa-silk-blouse-75','Willa silk blouse'),C(AO,'breann-embell-cutaway-blazer-off-white-gold','Breann blazer'),C(AO,'drew-oversized-wool-trench-coat','Drew wool coat'),C(AO,'alana-twist-strap-lace-godet-maxi-dress-black-almond','Alana lace dress')]),
 dict(brand='Past Midnight',deal='Only sale of the year',code='THESEASON',items=[C(PM,'the-flare-blue-gradient','The Flare, blue',now=109),C(PM,'the-flare-amber-gradient','The Flare, amber',now=109),C(PM,'the-frame-garnet','The Frame',now=101.25),C(PM,'the-flare-blue-gradient','The Flare, worn',1,now=109)]),
 ],'Travel')
if 'travel' in W: edition('travel','Travel',"Bags, cases, sunglasses and swim. Six sales worth packing for.",[
 dict(brand='BÉIS',deal='25% off, up to 50% select',items=[U('0032/3423/4479/files/Beis_Ecom_NorthSouthTote_Black_Product_2035_f63a8ccb-ba95-447d-9ea0-523fe3d9de82.jpg','North to South tote',98,49),U('0032/3423/4479/files/BEIS323434-Overnighter-Black-Front-4284.jpg','Commuter duffle',158,79),U('0032/3423/4479/files/BEIS322162-TheJewelryCase-Black-Product.jpg','Jewelry case',48,33.60),U('0032/3423/4479/files/BEIS154802-TheCosmeticCase-Black-Product0332.jpg','Cosmetic case',78,54.60)]),
 dict(brand='Heaven Mayhem',deal='30% off travel cases',items=[C(HM,'vintage-jewelry-travel-case','Vintage jewelry case'),C(HM,'jewelry-travel-case','Jewelry travel case'),C(HM,'zebra-jewelry-case','Jewelry case'),C(HM,'fashion-sunglasses-vittoria','Vittoria glasses')]),
 dict(brand='Past Midnight',deal='Only sale of the year',code='THESEASON',items=[C(PM,'the-flare-blue-gradient','The Flare, blue',now=109),C(PM,'the-flare-amber-gradient','The Flare, amber',1,now=109),C(PM,'the-frame-garnet','The Frame',now=101.25),C(PM,'the-scene-black','The Scene',now=93.75)]),
 dict(brand='Jet Set Candy',deal='Up to 50% off',items=[C(JS,'new-york-jfk-charm-silver-mini','JFK tag charm'),C(JS,'silver-trunk-suitcase-charm-stickers','Suitcase charm'),C(JS,'paris-france-cdg-charm-silver-mini','Paris CDG charm'),C(JS,'gold-enamel-poker-chips-charm','Poker chips charm')]),
 dict(brand="Rothy's",deal='Up to 40% off',items=[U('0877/4986/files/444_TheAlmondBallet_MetallicGoldLattice_PrimaryOverhead_2188.jpg','Almond ballet flat',155,129),U('0877/4986/files/322_ThePointIII_ReVelvetCobalt_PrimaryOverhead_2100.jpg','The Point III',165,119),U('0877/4986/files/093_TheWristlet_MetallicBlackLattice_Front_5445_1x1_shop.jpg','The wristlet',120,110)]),
 dict(brand='Alexandra Miro',deal='Swim up to 60% off',items=[C(AM,'vienna-swimsuit-scarf-print','Vienna swimsuit'),C(AM,'willow-swimsuit-scarf-print','Willow swimsuit'),C(AM,'whitney-swimsuit-capri','Whitney swimsuit'),C(AM,'carlotta-bikini-top-fluid-marble','Carlotta bikini top')]),
 ],'Home')
if 'home' in W: edition('home','Home',"Linen, robes, the table. Seven sales for the house.",[
 dict(brand='Piglet in Bed',deal='25 to 40% off',items=[U('2151/7379/files/Pine_Green_Pembroke_Gingham_Linen_Blend_Duvet_Cover_1.jpg','Gingham duvet, king',349,209),U('2151/7379/files/Berry_Heritage_Gingham_100_Linen.jpg','Linen pillowcases',109,65),U('2151/7379/files/5063469049862.jpg','Rhubarb duvet, king',349,244)]),
 dict(brand='Parachute',deal='20% off, up to 40% select',items=[U('0396/8269/files/cotton-drift-comforter_bone_main_01_1.jpg','Drift comforter',279,167.40),U('0396/8269/files/organic-plush-robe_warm-grey_main_1712.jpg','Plush robe',159,111.30),U('0396/8269/files/plaid-wool-alpaca-throw-natural-plaid_01_f38f307a-863f-4a4d-ac31-efc148db0541.jpg','Alpaca throw',329,230.30),U('0396/8269/files/linen-tencel-sheet-set-bone-_f-q_k-ck__01.jpg','Linen sheet set',329,246.75)]),
 dict(brand='Brooklinen',deal='25% off sitewide',items=[U('0951/7126/files/BKL_26-08_Bedding_Throws_Super-Fluff_Cream_1x_PDP_WOgrey.jpg','Super Fluff throw',129,75),U('0951/7126/files/BKL_23-09_Bath_Robe_White_Flat_1x_c16809ff-2055-4153-bbef-c918024fc2b2.jpg','Super-Plush robe',139,104.25)]),
 dict(brand='Hudson Grace',deal='20% off everything',items=[U('0257/7127/8418/files/harrington-crystal-decanter.png','Crystal decanter',148,118.40),U('0257/7127/8418/files/stella-ceramic-scallop-serving-platter.jpg','Scallop platter',148,118.40),U('0257/7127/8418/files/cherry-red-bistro-5-piece-flatware-set.webp','Red bistro flatware',128,102.40),U('0257/7127/8418/files/red-and-green-candy-cane-stripe-linen-tablecloth.jpg','Stripe tablecloth',298,238.40)]),
 dict(brand='Dear Annabelle',deal='Up to 32% off',items=[U('0061/9924/6959/files/DA_CocktailNapkins_Loopy-Black_7dea6350-6930-42ef-934c-12f447802113.jpg','Cocktail napkins',95,65),U('0061/9924/6959/files/Swan_White_R1_970b63c8-afc9-46a5-96a3-bc8bce421d6e.jpg','Swan place cards',60,46),U('0061/9924/6959/files/DA_Sayingspads_Lace_R1.jpg','Lace notepad set',65,46),U('0061/9924/6959/files/All_Tied_Up_Notecard_Envelope_R1.jpg','Notecards',85,60)]),
 dict(brand='LAKE Pajamas',deal='25% off at checkout',items=[U('0505/6125/files/LAKE_Webcrop_Holiday1_2026_Kimono3Pc_BurgundyPencilStripe_1200x1800_e5892a2e-cf75-42c5-a070-f8c7e029c583.jpg','Kimono 3-piece set',168,126),U('0505/6125/files/LAKE_Webcrop_Holiday1_2026_LL_DarkSeaVoyagerStripe_1200x1800_16df5a91-5129-4849-9c8b-761915d9ce46.jpg','Pima long set',128,96),U('0505/6125/products/hydrangea_robe_new.jpg','Pima robe',134,100.50)]),
 dict(brand='Society Social',deal='20% off sitewide',code='EVERYTHING20',items=[U('0093/1772/files/BettyStool.png','Betty stool',595,476),U('0093/1772/files/LightBlueWickerLampshade.jpg','Wicker lampshade',258,206.40)]),
 ],'Makeup')
if 'makeup' in W: edition('makeup','Makeup',"Six beauty sales, three with codes. One only happens once a year.",[
 dict(brand='MERIT',deal='20% off, 25% over $150',items=[U('0412/1296/9117/files/Set1-DaniSummerEssentials_23668031-119d-4c0c-b741-a8dcb9654494.jpg','The Intro Set',119,95.20,'50% 50%'),U('0412/1296/9117/files/MERIT-SignatureLipSatin-Ginger-PDP_6af6e518-8eae-47a7-b0b3-23a81d2092b1.jpg','Signature lipstick',28,22.40,'50% 50%'),U('0412/1296/9117/files/FiveMinuteMorning_fcd646c2-fb81-4caa-9a4b-31fb6f0772cc.jpg','Five Minute Morning',177,132.75,'50% 50%')]),
 dict(brand='MAKE Beauty',deal='Up to 50% off',items=[U('1131/0390/files/1-MAKE_PDP_Lipstick_CapOff_Flourescense_NewBeautyAwards2024.jpg','Cream Supreme lipstick',26,13),U('1131/0390/products/PDP_SerumBalmIntense_Hero_NudeNova.jpg','Serum Balm Intense',26,13)]),
 dict(brand='Chantecaille',deal='25% off sitewide',code='CYBER',items=[U('1951/2637/files/3022076-hero.jpg','Lip Cristal',55,41.25),U('1951/2637/files/656509168279_01.jpg','Rose de Mai set',275,206.25),U('1951/2637/files/ROSE-HARVEST-DUO_1.jpg','Rose Harvest duo',198,148.50),U('1951/2637/files/656509163106-1_1.jpg','Cushion foundation',76,57)]),
 dict(brand='Tatcha',deal='25% off sitewide',code='CYBER26',items=[U('0949/3328/7221/files/KissuLipMaskMaple-pdp-FullSize-MainImage-1200x1200.jpg','Kissu, maple red',29,21.75),U('0949/3328/7221/files/TheKissuLipMask-pdp-Aug26-Omi-FullSize-MainImage-1200x1200.jpg','Kissu lip mask',29,21.75)]),
 dict(brand='MALIN+GOETZ',deal='20% off, 25% over $125',items=[U('0643/1398/3073/files/leather-edp-p1_1.jpg','Leather eau de parfum',105,84),U('0643/1398/3073/files/image_214.jpg','Dark rum perfume oil',40,32),U('0643/1398/3073/files/braindead-leather-perfumeoil-1.jpg','Leather perfume oil',40,32)]),
 dict(brand='Retrouvé',deal='25% off sitewide',items=[U('0835/4260/6126/files/01_Radiance_Reverie_pdp.jpg','Radiance Reverie set',245,183),U('0835/4260/6126/files/Bazaar_lip_gray_2048_e9391d82-4a39-4948-85e7-21ed1fcff704.jpg','Hydrating lip serum',55,41.25)]),
 ],'Jewelry')
