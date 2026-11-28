import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tour import *
OUT=SP+'/out'
which=sys.argv[1:] 
T={}
T['havana']=dict(city=('Havana','1958','havana'),n=1,nxt=('Monaco','1964','monaco'),
 hook='I sorted Black Friday by <span class=it>city.</span>',sub="Five things on sale right now that look like they left the house with this bag.",
 items=lambda:[
  I('alexandramiro.com','harper-dress-red-capri',1,'photo','Alexandra Miro','Harper Dress, Red Capri','Final sale, and all five sizes are still in stock.',pos='50% 18%'),
  I('emmeparsons.com','delicat-burnt-red-satin',0,'pack','Emme Parsons','Delicat Sandal, Red Satin','40% off in her private sale. 9 of 13 sizes left.',scale=1.25),
  I('heavenmayhem.com','alma-clip-on-earrings',1,'pack','Heaven Mayhem','Alma Clip-On Earrings','Clip-ons, the way they wore them in 1958. No piercing needed.',scale=.8),
  I('jetsetcandy.com','silver-domino-charm',0,'pack','Jet Set Candy','Domino Charm, Sterling','Dominoes is the game on every Havana corner.',scale=.9),
  I('pastmidnight.com','the-flare-amber-gradient',1,'photo','Past Midnight','The Flare, Amber Gradient','Their only sale of the year. Marked to $145, then 25% more.',now=109,off='60% off',code='THESEASON',pos='50% 20%'),
 ])
T['monaco']=dict(city=('Monaco','1964','monaco'),n=2,nxt=('New York','1977','nyc'),
 hook='Black Friday, sorted by <span class=it>city.</span>',sub="Race weekend, the casino after. Six things on sale that belong at both.",
 items=lambda:[
  I('heavenmayhem.com','gaze-choker',1,'photo','Heaven Mayhem','Gaze Choker','The deepest real markdown I found on their whole site.',pos='50% 60%'),
  I('jetsetcandy.com','gold-enamel-poker-chips-charm',0,'pack','Jet Set Candy','Poker Chips Charm, Gold','Half off. One of 58 pieces on their site that really are.',scale=.8),
  I('emmeparsons.com','isabel-black-calf',0,'pack','Emme Parsons','Isabel Slingback, Black','40% off in her private sale. 8 of 13 sizes left.',scale=1.25),
  I('heavenmayhem.com','the-icon-watch',0,'pack','Heaven Mayhem','The Icon Watch','A rectangular dress watch for under $200.',scale=.85),
  I('jenniferbehr.com','sofia-hair-pin-crystal',1,'photo','Jennifer Behr','Sofia Hair Pin, Crystal','25% comes off at checkout on orders over $150. Her biggest sale of the year.',was=368,now=276,pos='50% 40%'),
  I('margauxny.com','the-demi-tomato-suede',0,'pack','Margaux','The Demi, Tomato Suede','Racing red. Their only sitewide sale of the year.',was=290,now=232,scale=1.1),
 ])
T['nyc']=dict(city=('New York','1977','nyc'),n=3,nxt=('Miami','1959','miami'),
 hook='Black Friday, sorted by <span class=it>city.</span>',sub="Pinstripes downtown, sequins after midnight. Six on sale now.",
 items=lambda:[
  I('aliceandolivia.com','breann-embell-cutaway-blazer-off-white-gold',0,'photo','alice + olivia','Breann Pinstripe Blazer','The matching wide-leg trouser is 40% off too. All eight sizes in stock.',pos='50% 12%'),
  I('aliceandolivia.com','jackie-embellished-bomber-jacket-1',0,'photo','alice + olivia','Jackie Embellished Bomber','$718 off. The splurge of the whole list.',pos='50% 20%'),
  I('aliceandolivia.com','drew-oversized-wool-trench-coat',0,'photo','alice + olivia','Drew Wool Coat, Red','Wool, floor-length, $478 off. Four of five sizes left.',pos='50% 15%'),
  I('heavenmayhem.com','plaza-earrings',0,'pack','Heaven Mayhem','Plaza Earrings','60% off, and under $50.',scale=.75),
  I('heavenmayhem.com','fashion-sunglasses-vittoria',0,'pack','Heaven Mayhem','Vittoria Glasses','A seventies shield frame, $120 off.',scale=1.05),
  I('jetsetcandy.com','new-york-jfk-charm-silver-mini',0,'pack','Jet Set Candy','JFK Luggage Tag Charm','$22. The cheapest thing on this whole tour.',scale=.7),
 ])
T['miami']=dict(city=('Miami','1959','miami'),n=4,nxt=('Tokyo','1995','tokyo'),
 hook='Black Friday, sorted by <span class=it>city.</span>',sub="Ocean Drive, pink Cadillac, pool by noon. Five on sale now.",
 items=lambda:[
  I('alexandramiro.com','vienna-swimsuit-scarf-print',0,'photo','Alexandra Miro','Vienna Swimsuit, Scarf Print','60% off, final sale, every size still in.',pos='50% 25%'),
  I('alexandramiro.com','sophia-dress-scarf-print',0,'photo','Alexandra Miro','Sophia Dress, Scarf Print','The cover-up that goes to dinner. $288 off.',pos='50% 25%'),
  I('emmeparsons.com','delicat-gold-nappa',0,'pack','Emme Parsons','Delicat Sandal, Gold','40% off in her private sale. 10 of 13 sizes left.',scale=1.25),
  I('pastmidnight.com','the-flare-blue-gradient',1,'photo','Past Midnight','The Flare, Blue Gradient','Their only sale of the year. Marked to $145, then 25% more.',now=109,off='60% off',code='THESEASON',pos='50% 20%'),
  I('jetsetcandy.com','mia-miami-luggage-tag-mini-charm-silver',0,'pack','Jet Set Candy','MIA Luggage Tag Charm','$22, sterling.',scale=.7),
 ])
T['tokyo']=dict(city=('Tokyo','1995','tokyo'),n=5,nxt=None,
 hook='Black Friday, sorted by <span class=it>city.</span>',sub="Neon, rain on the street, a midnight-purple coupe. Five on sale now.",
 items=lambda:[
  I('aliceandolivia.com','alana-twist-strap-lace-godet-maxi-dress-black-almond',0,'photo','alice + olivia','Alana Lace Maxi Dress','$398 off, all eight sizes in stock.',pos='50% 12%'),
  I('emmeparsons.com','delicat-bordeaux-kidskin',0,'pack','Emme Parsons','Delicat Sandal, Bordeaux','The same deep purple as the clasp on the bag.',scale=1.25),
  I('jenniferbehr.com','meena-hairpin-malachite',0,'pack','Jennifer Behr','Meena Hairpin, Malachite','A hair stick, the way a kanzashi is worn. 25% off at checkout over $150, so pair it.',was=198,now=148.50,scale=.9),
  I('margauxny.com','the-fonteyn-petrol-velvet',0,'pack','Margaux','The Fonteyn, Petrol Velvet','Velvet flats. Their only sitewide sale of the year.',was=325,now=260,scale=1.1),
  I('jetsetcandy.com','tokyo-japan-luggage-tag-charm-silver-mini',0,'pack','Jet Set Candy','NRT Luggage Tag Charm','$22, sterling.',scale=.7),
 ])
for k in which:
    t=T[k]; render(t['city'],t['items'](),t['n'],5,t['nxt'],f'{OUT}/tour-{t["n"]}-{k}',t['hook'],t['sub'])
    print('ok',k)
