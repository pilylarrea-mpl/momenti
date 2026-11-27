"""Curation toolkit. All data is local: no network needed except product photos (plain curl, free).
  import pick
  pick.host('BaubleBar')                 -> 'baublebar.com'
  R = pick.rows('baublebar.com')         -> list of dicts for every product:
        t title, h handle, type, pr price now, ca original price (0 if none), off % off,
        av sizes in stock, n sizes total, vname cheapest in-stock variant, img [urls], tags, pub date
  pick.best(host, min_off=30, n=40)      -> in-stock, >=half sizes available, sorted by dollars saved
  pick.sheet(host, [handles], 'name')    -> writes sheets/name.jpg, a labelled photo contact sheet (2 photos per item). Read it to look.
  pick.info(host)                        -> sheet rows for the brand (sale name, dates, code, claimed discount) + homepage sale phrases
"""
import json,glob,re,os,subprocess,hashlib
from PIL import Image,ImageDraw
SP='/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad'
D=SP+'/data/'
B=json.load(open(D+'brands.json')); A=json.load(open(D+'audit.json'))
def host(brand):
    for h,b in B.items():
        if b['brand'].lower()==brand.lower(): return h
    raise KeyError(brand)
_c={}
def rows(h):
    if h in _c: return _c[h]
    R=[]
    for f in sorted(glob.glob(f'{D}crawl/{h}.[0-9].json')+glob.glob(f'{D}crawl/{h}.x*.json')):
        try: P=json.load(open(f)).get('products',[])
        except Exception: continue
        for p in P:
            vs=p.get('variants') or []
            if not vs: continue
            av=sum(1 for v in vs if v.get('available')); pool=[v for v in vs if v.get('available')] or vs
            v0=min(pool,key=lambda v:float(v['price'])); pr=float(v0['price']); ca=float(v0.get('compare_at_price') or 0)
            if pr<=0: continue
            R.append(dict(t=p['title'],h=p['handle'],type=p.get('product_type') or '',pr=pr,ca=ca,off=round(100*(1-pr/ca)) if ca>pr else 0,av=av,n=len(vs),vname=v0.get('title',''),
                          img=[i['src'] for i in p.get('images',[])[:4]],tags=p.get('tags') if isinstance(p.get('tags'),list) else [],pub=(p.get('published_at') or '')[:10]))
    _c[h]=R; return R
def best(h,min_off=30,n=40,kw=None,max_price=None):
    R=[r for r in rows(h) if r['av']>=max(1,0.5*r['n']) and r['off']>=min_off]
    if kw: R=[r for r in R if re.search(kw,r['t']+' '+r['type'],re.I)]
    if max_price: R=[r for r in R if r['pr']<=max_price]
    return sorted(R,key=lambda r:-(r['ca']-r['pr']))[:n]
def info(h): return dict(sheet=B[h],home=A[h].get('home',{}),stats={k:A[h].get(k) for k in ('instock','marked','median','max','ge30','ge50','ge60')})
def _get(url,w=600):
    os.makedirs(SP+'/imgc',exist_ok=True)
    u=url.split('?')[0]+f'?width={w}'; fn=SP+'/imgc/'+hashlib.md5(u.encode()).hexdigest()+'.img'
    if not os.path.exists(fn) or os.path.getsize(fn)<500: subprocess.run(['curl','-sL','-m','40','-A','Mozilla/5.0','-o',fn,u])
    return fn
def sheet(h,handles,name,nimg=2,cell=280):
    R={r['h']:r for r in rows(h)}; tiles=[]
    for x in handles:
        r=R.get(x)
        if not r: print('missing',x); continue
        for i,src in enumerate(r['img'][:nimg]):
            try: im=Image.open(_get(src)).convert('RGB'); im.thumbnail((cell,cell))
            except Exception: im=Image.new('RGB',(cell,cell),'red')
            t=Image.new('RGB',(cell,cell+34),'white'); t.paste(im,((cell-im.width)//2,0))
            ImageDraw.Draw(t).text((4,cell+2),f"{x[:42]}\nimg{i} ${r['ca']:.0f}->${r['pr']:.0f} {r['off']}% av{r['av']}/{r['n']}",fill='black'); tiles.append(t)
    cols=6; S=Image.new('RGB',(cols*cell,max(1,(len(tiles)+cols-1)//cols)*(cell+34)),'white')
    for k,t in enumerate(tiles): S.paste(t,((k%cols)*cell,(k//cols)*(cell+34)))
    out=f'{SP}/sheets/{name}.jpg'; S.save(out,quality=80); print(out,len(tiles)); return out

def detail(host,handle):
    """Full product record: title, type, vendor, tags, description text, options, per-variant (name, price, original, in stock)."""
    import html
    for f in glob.glob(f'{D}crawl/{host}.*.json'):
        try: P=json.load(open(f)).get('products',[])
        except Exception: continue
        for p in P:
            if p['handle']==handle:
                t=html.unescape(re.sub(r'<[^>]+>',' ',p.get('body_html') or '')); t=re.sub(r'\s+',' ',t).strip()
                return dict(title=p['title'],type=p.get('product_type'),vendor=p.get('vendor'),tags=p.get('tags'),description=t[:2500],options=[(o['name'],o['values'][:16]) for o in p.get('options',[])],variants=[(v['title'],v['price'],v.get('compare_at_price'),v['available']) for v in p['variants'][:60]])

CORE_SKIP={'Baby & Kids','Cannabis','Pets','Health & Wellness','Food & Beverage','Sports & Fitness'}
def category(include,exclude=None,min_off=40,min_price=0,max_price=10**6,min_imgs=2):
    """Every in-stock item across all core stores whose title/type matches `include` (regex) and not `exclude`,
    at >= min_off % off its own original price, with at least half its sizes in stock.
    Returns (items, per_store) where items = list of dicts (brand, host, + pick.rows fields) and per_store = {brand: count}."""
    import collections
    out=[]; per=collections.Counter()
    for h,b in B.items():
        if b['industry'] in CORE_SKIP: continue
        for r in rows(h):
            t=r['t']+' '+r['type']
            if not re.search(include,t,re.I): continue
            if exclude and re.search(exclude,t,re.I): continue
            if re.search(r"(?<!wo)men's|(?<!wo)mens\b|\bmen\b|\bkids?\b|\bbaby\b|toddler|\bboys?\b|\bgirls?\b|mystery|advent|gift card",t,re.I): continue
            if r['off']>=min_off and r['av']>=max(1,0.5*r['n']) and len(r['img'])>=min_imgs and min_price<=r['pr']<=max_price:
                out.append(dict(r,brand=b['brand'],host=h)); per[b['brand']]+=1
    return out,dict(per)
def currency(host):
    """'$' unless the store's catalog is known to be priced in another currency."""
    return {'oddmuse.co.uk':'£','stripeandstare.com':'£','beyondnine.co.uk':'£','pigletinbed.com':'£','pe-nation.com':'A$','dissh.com':'A$','soleilsoleil.com.au':'A$','withconsideration.com.au':'A$','antipodeanlabel.com':'A$'}.get(host,'$')
