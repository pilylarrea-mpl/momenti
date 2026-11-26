import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from creator import *
CDN='https://cdn.shopify.com/s/files/1/'
FOOT='Prices checked on each brand\'s site, Nov 26.'
W=sys.argv[1:]
if 'once' in W: post('once-a-year','Kept 5',"Five brands<br>that go on sale <span class=it>once a year.</span>","It's this week. Each one says so on its own site.",[
 I('pastmidnight.com','the-flare-blue-gradient',1,'photo','Past Midnight','The Flare, Blue Gradient','Marked to $145, then 25% more with the code.',now=109,off='60% off',code='THESEASON',pos='50% 20%',tag='&ldquo;Our only sale of the year&rdquo;'),
 I('margauxny.com','the-demi-merlot-suede',0,'pack','Margaux','The Demi, Merlot Suede','20% off everything, in every size they make.',was=290,now=232,scale=1.1,tag='&ldquo;Our only sitewide sale of the year&rdquo;'),
 M(CDN+'0412/1296/9117/files/Set1-DaniSummerEssentials_23668031-119d-4c0c-b741-a8dcb9654494.jpg','photo','MERIT','The Intro Set','20% off, or 25% once your order passes $150. A free bag comes with every order.',119,95.20,pos='50% 50%',tag='&ldquo;Our only sale of the year&rdquo;'),
 I('jenniferbehr.com','abbie-barrette-crystal',0,'pack','Jennifer Behr','Abbie Barrette, Crystal','25% comes off at checkout on orders over $150.',was=228,now=171,scale=.85,tag='&ldquo;The biggest sale of the year&rdquo;'),
 M(CDN+'0949/3328/7221/files/KissuLipMaskMaple-pdp-FullSize-MainImage-1200x1200.jpg','pack','Tatcha','Kissu Lip Mask, Maple Red','25% off sitewide with the code.',29,21.75,code='CYBER26',scale=.9,tag='&ldquo;Our best offer of the year&rdquo;'),
 ],None,'Once a year,<br><span class=it>this week</span>',FOOT+' The quotes are from each brand\'s homepage.',("Next: under $50.","I'm going through all 376 sales. <span class=it>Follow for the next cut.</span>"))
if 'under50' in W: post('under-50','Kept 7',"Seven things<br>under $50 that <span class=it>look like $200.</span>","Cheapest first. The first one is $13.",[
 M(CDN+'1131/0390/files/1-MAKE_PDP_Lipstick_CapOff_Flourescense_NewBeautyAwards2024.jpg','pack','MAKE Beauty','Cream Supreme Lipstick','Refillable, and half off.',26,13,scale=.9),
 M(CDN+'0949/3328/7221/files/TheKissuLipMask-pdp-Aug26-Omi-FullSize-MainImage-1200x1200.jpg','pack','Tatcha','The Kissu Lip Mask','25% off sitewide with the code.',29,21.75,code='CYBER26',scale=.9),
 I('jetsetcandy.com','new-york-jfk-charm-silver-mini',0,'pack','Jet Set Candy','JFK Luggage Tag Charm','Sterling silver. They make one for most airports.',scale=.7),
 I('heavenmayhem.com','luna-statement-bangle',0,'pack','Heaven Mayhem','Luna Bangle','60% off, all three sizes in stock.',scale=.9),
 I('heavenmayhem.com','plaza-earrings',0,'pack','Heaven Mayhem','Plaza Earrings','60% off. Final sale.',scale=.75),
 I('heavenmayhem.com','edith-earrings',0,'pack','Heaven Mayhem','Edith Earrings','60% off. Final sale.',scale=.85),
 M(CDN+'0032/3423/4479/files/Beis_Ecom_NorthSouthTote_Black_Product_2035_f63a8ccb-ba95-447d-9ea0-523fe3d9de82.jpg','pack','BÉIS','North To South Tote','Half off, no code.',98,49,scale=.95),
 ],lambda k,it:f'Under ${[15,25,25,30,45,50,50][k]}','Under $50','All seven together: under $225. '+FOOT,("Next: the biggest dollar drops.","I'm going through all 376 sales. <span class=it>Follow for the next cut.</span>"))
if 'drops' in W:
    its=[
 I('aliceandolivia.com','jackie-embellished-bomber-jacket-1',0,'photo','alice + olivia','Jackie Embellished Bomber','40% off. Four of five sizes left.',pos='50% 20%'),
 I('aliceandolivia.com','shanti-embr-cmbo-btn-ft-tiered-dress',0,'photo','alice + olivia','Shanti Tiered Dress','60% off, all eight sizes in.',pos='50% 15%'),
 M(CDN+'0565/1234/8333/files/Olivia-Coat_Black.jpg','photo','Jenni Kayne','Olivia Coat, Black','Half off. Final sale.',1025,513,pos='50% 20%'),
 I('aliceandolivia.com','drew-oversized-wool-trench-coat',0,'photo','alice + olivia','Drew Wool Coat, Red','40% off. Four of five sizes left.',pos='50% 15%'),
 I('aliceandolivia.com','alana-twist-strap-lace-godet-maxi-dress-black-almond',0,'photo','alice + olivia','Alana Lace Maxi Dress','40% off, all eight sizes in.',pos='50% 12%'),
 I('alexandramiro.com','sophia-dress-scarf-print',0,'photo','Alexandra Miro','Sophia Dress, Scarf Print','60% off, every size in. Final sale.',pos='50% 25%'),
 I('emmeparsons.com','isabel-black-calf',0,'pack','Emme Parsons','Isabel Slingback, Black','40% off. Eight of 13 sizes left.',scale=1.25)]
    its.sort(key=lambda i:-(i['was']-i['now']))
    post('dollar-drops','Kept 7',"Seven pieces,<br>ranked by <span class=it>dollars off.</span>","A 60% tag can mean $39 saved. The first one here saves $718.",its,
      lambda k,it:f'{money(it["was"]-it["now"])} off','Ranked by<br><span class=it>dollars off</span>',FOOT,("Next: a full outfit, all on sale.","I'm going through all 376 sales. <span class=it>Follow for the next cut.</span>"))
if 'outfit' in W: post('red-outfit','Kept 5',"One holiday outfit. <span class=it>Every piece</span> is on sale.","Dress, shoes, earrings, bag, sunglasses. Built from five different sales.",[
 I('alexandramiro.com','harper-dress-red-capri',1,'photo','Alexandra Miro','Harper Dress, Red Capri','60% off, all five sizes in. Final sale.',pos='50% 18%'),
 I('emmeparsons.com','delicat-burnt-red-satin',0,'pack','Emme Parsons','Delicat Sandal, Red Satin','40% off. Nine of 13 sizes left.',scale=1.25),
 I('heavenmayhem.com','alma-clip-on-earrings',1,'pack','Heaven Mayhem','Alma Clip-On Earrings','60% off. Clip-ons, so no piercing needed.',scale=.8),
 M(CDN+'0245/9844/6140/files/lin-capp-front_0294d7f4-cfdd-48bd-8350-7cce70168ccb.png','pack','Freja','Slim Clutch, Burgundy','25% off everything, no code.',228,171,scale=.95),
 I('pastmidnight.com','the-flare-amber-gradient',1,'photo','Past Midnight','The Flare, Amber Gradient','Their only sale of the year.',now=109,off='60% off',code='THESEASON',pos='50% 20%'),
 ],lambda k,it:['The dress','The shoes','The earrings','The bag','The sunglasses'][k],'The whole look',FOOT,("Want one in black?","Comment <span class=it>black</span> and I'll build it from the same 376 sales."),total=True)
