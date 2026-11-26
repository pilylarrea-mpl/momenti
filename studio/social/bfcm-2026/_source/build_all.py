import sys,json; sys.path.insert(0,'.')
from extra import *
P=lambda s:json.load(open(f'{SP}/picks/{s}.json'))
N=lambda t:f'{t}<br><span class=it>edition.</span>'
def fix(spec):
    for b in spec['brands']:
        if b['brand'] in('Odd Muse','Stripe & Stare','Beyond Nine'): b['cur']='£'
        if b['brand']=='Odd Muse': b['deal']='Up to 60% off, UK store'
    return spec
W=sys.argv[1:]
if 'jewelry' in W:
    J=fix(P('jewelry'))
    for br in J['brands']:
        if br['brand'] in('Bryan Anthonys','Sterling Forever'):
            for it in br['items']: it['img2']=-1; it['pos']='50% 35%'
    edition(J,nxt=N('Shoes'))
    bb=[b for b in J['brands'] if b['brand']=='BaubleBar'][0]; a=pick.A['baublebar.com']
    counted(dict(slug='counted-baublebar',brand='BaubleBar',claim='30% off',total=a['instock'],count=a['ge50'],what=f"pieces are half off or more. {a['ge60']} of them are 60% off or more.",host=bb['host'],items=bb['items'],next='The sale that<br><span class=it>overpromises.</span>'))
if 'workwear' in W: edition(fix(P('workwear')),nxt=N('Denim'))
if 'denim' in W: edition(fix(P('denim')),nxt=N('Jewelry'))
if 'shoes' in W: s=fix(P('shoes')); s['pos']='50% 78%'; edition(s,nxt=N('Pajamas'))
if 'pajamas' in W: edition(fix(P('pajamas')),nxt='Last call:<br><span class=it>what ends tonight.</span>')

def ends(slug,day,spec,nxt,hold=3.0):
    spec['slug']=slug; edition(spec,kick_r='Ends tonight',title_a=day,title_h='Ends<br><span class=it>tonight.</span>',nxt=nxt,hold=hold)
def brand(spec_name,name):
    return [x for x in fix(P(spec_name))['brands'] if x['brand']==name][0]
if 'ends' in W:
    a=fix(P('ends-nov29')); a['sub']='Three sales close at midnight. These are the pieces to check first.'
    ends('ends-nov29','Sunday Nov 29',a,'Tomorrow:<br><span class=it>four more close.</span>')
    b30=dict(title='Ends tonight',sub='Four sales close at midnight: denim, tailoring, pajamas and basics.',brands=[brand('ends-nov30','Pistola Denim'),brand('workwear','Odd Muse'),brand('pajamas','LAKE'),brand('ends-nov30','Harper Wilde')])
    ends('ends-nov30','Monday Nov 30',b30,'Tomorrow:<br><span class=it>the last call.</span>')
    c=fix(P('ends-dec1')); c['brands']=[x for x in c['brands'] if x['brand'] not in('Vicci Eyewear','LAKE')]
    for x in c['brands']:
        if x['brand']=='ANEMOS': x['code']=None
    c['sub']=f"About 100 sales end tonight. These {len(c['brands'])} have the deepest real markdowns I found."
    ends('ends-dec1','Tuesday Dec 1',c,"Still on tomorrow:<br><span class=it>the sales that didn't end.</span>",hold=2.6)
if 'spots' in W:
    S=[dict(brand='Intentionally Blank',host='intentionallyblank.us',handle='hiperson-leather-knee-high-boot',name='Hiperson Knee Boot',imgs=[0,1,2],reasons=['Leather knee boot at half price','15 of 16 sizes still in stock','A kitten heel you can walk in'],caveat='The glossy crinkle finish is a love-it-or-not.',ends_txt='Dec 1'),
       dict(brand='M.M.LaFleur',host='mmlafleur.com',handle='theodora-black',name='Theodora Eyelet Dress',imgs=[0,2,1],reasons=['$418 off. That is 79%.','All six sizes in stock','Black eyelet: office now, dinner later'],caveat='Final sale. And it is sleeveless.',ends_txt='soon: no end date posted'),
       dict(brand='Freja',host='frejanyc.com',handle='alma-bag-black-gloss',name='Alma Bag, Black Gloss',imgs=[0,2,1],reasons=['$358 bag for $168','A structured shoulder bag, no logo','Looks three times the price'],caveat='Final sale, and only one batch left.',ends_txt='Dec 1'),
       dict(brand='FRĒDA SALVADOR',host='fredasalvador.com',handle='laurel-leopard-mesh',name='Laurel Mesh Mary Jane',imgs=[0,1,3],reasons=['Half price: $298 down to $149','12 of 13 sizes in stock','Leopard mesh, the flat of the year'],caveat='Final sale. Mesh is not a snow shoe.',ends_txt='Dec 2'),
       dict(brand='Pistola Denim',host='pistoladenim.com',handle='karlee-chore-jacket',name='Karlee Chore Jacket',imgs=[0,1,2],reasons=['$258 jacket for $90','Every size in stock','A denim jacket that reads as a blazer'],caveat='Final sale. Ends Monday night.',ends_txt='Nov 30')]
    for i,sp in enumerate(S): spotlight(sp,f'one-thing-{i+1}-{sp["handle"][:18]}')
