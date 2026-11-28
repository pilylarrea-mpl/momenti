import sys,json; sys.path.insert(0,'.')
from extra import *
F=lambda s:json.load(open(f'{SP}/final/{s}.json'))
T=lambda p:json.load(open(f'{SP}/talk/{p}.json')) if os.path.exists(f'{SP}/talk/{p}.json') else None
N=lambda t:f'{t}<br><span class=it>edition.</span>'
ED=[('best-deals','Travel'),('travel','Home'),('home','Beauty'),('makeup','Workwear'),('workwear','Denim'),('denim','Jewelry'),('jewelry','Shoes'),('shoes','Pajamas'),('pajamas',None)]
W=sys.argv[1:] or ['ed','ends','count','spots']
if 'ed' in W:
    for s,nx in ED: edition(F(s),nxt=N(nx) if nx else 'Last call:<br><span class=it>what ends tonight.</span>')
if 'ends' in W:
    for s,day,nx in [('ends-nov29','Sunday Nov 29','Tomorrow:<br><span class=it>four more close.</span>'),('ends-nov30','Monday Nov 30','Tomorrow:<br><span class=it>the last call.</span>'),('ends-dec1','Tuesday Dec 1',"Still on tomorrow:<br><span class=it>the sales that didn't end.</span>")]:
        edition(F(s),kick_r='Ends tonight',title_a=day,title_h=True,title_words=[('Ends',False),('tonight.',True)],nxt=nx,hold=2.6 if s=='ends-dec1' else 3.0)
if 'count' in W:
    J=F('jewelry'); bb=[b for b in J['brands'] if b['brand']=='BaubleBar'][0]; a=pick.A['baublebar.com']
    counted(dict(slug='i-counted-baublebar',brand='BaubleBar',claim='30% off',total=a['instock'],count=a['ge50'],what=f"pieces are half off or more. {a['ge60']} of them are 60% off or more.",host=bb['host'],items=bb['items'],next='The sale that<br><span class=it>overpromises.</span>'))
if 'spots' in W:
    DEF={'one-thing-boots':(['Leather knee boot at half price','15 of 16 sizes still in stock','A kitten heel you can walk in'],'The glossy crinkle finish is a love-it-or-not.'),'one-thing-eyelet-dress':(['$418 off. That is 79%.','All six sizes in stock','Black eyelet: office now, dinner later'],'Final sale. And it is sleeveless.'),'one-thing-alma-bag':(['$358 bag for $168','A structured shoulder bag, no logo','In stock today'],'Final sale, and only one batch left.'),'one-thing-mary-jane':(['Half price: $298 down to $149','12 of 13 sizes in stock','Leopard mesh Mary Jane'],'Final sale. Mesh is not a snow shoe.'),'one-thing-chore-jacket':(['$258 jacket for $90','Every size in stock','Denim chore jacket'],'Final sale. Ends Monday night.')}
    for sp in F('spotlights'):
        t=T(sp['slug']); r,c=(t['reasons'],t['caveat']) if t else DEF[sp['slug']]
        spotlight(dict(sp,reasons=r,caveat=c),sp['slug'])
