import json,glob,re,html,os,collections,sys
D='/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/data/'
B=json.load(open(D+'brands.json'))
def rows(h):
    R=[]
    for f in sorted(glob.glob(f'{D}crawl/{h}.[0-9].json')+glob.glob(f'{D}crawl/{h}.x*.json')):
        try: P=json.load(open(f)).get('products',[])
        except: continue
        for p in P:
            vs=p.get('variants') or []
            if not vs: continue
            av=sum(1 for v in vs if v.get('available'))
            pool=[v for v in vs if v.get('available')] or vs
            v0=min(pool,key=lambda v:float(v['price']))
            pr=float(v0['price']); ca=float(v0.get('compare_at_price') or 0)
            off=round(100*(1-pr/ca)) if ca>pr>0 else 0
            t=p['title']; ty=p.get('product_type') or ''
            if pr<=0 or re.search(r'gift card|e-gift|insurance|shipping protection|route|sample',t+ty,re.I): continue
            R.append(dict(t=t,h=p['handle'],type=ty,pr=pr,ca=ca,off=off,av=av,n=len(vs),img=[i['src'] for i in p.get('images',[])[:2]],tags=p.get('tags') if isinstance(p.get('tags'),list) else [],pub=(p.get('published_at') or '')[:10]))
    return R
def home(h):
    f=f'{D}crawl/{h}.home.html'
    if not os.path.exists(f): return dict(ok=False)
    raw=open(f,errors='ignore').read()
    t=re.sub(r'<script.*?</script>|<style.*?</style>',' ',raw,flags=re.S); t=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\s+',' ',t)
    ph=[];seen=set()
    for m in re.finditer(r'[^.!|•]{0,70}(\d\d ?% off|% OFF|Black Friday|BLACK FRIDAY|Cyber|code:? [A-Z0-9]{4,}|CODE:? [A-Z0-9]{4,}|sale of the year|offer of the year|once a year|only sale|ONLY SALE|biggest sale|BIGGEST SALE|Private Sale|ends? (Mon|Sun|Tue|tonight|soon|[0-9/]+)|final sale|FINAL SALE|free gift|FREE GIFT)[^.!|•]{0,80}',t):
        s=m.group(0).strip(); k=re.sub(r'\W','',s.lower())[:40]
        if k in seen: continue
        seen.add(k); ph.append(s[:170])
        if len(ph)>=7: break
    vids=len(set(re.findall(r'[^"\' ]+\.mp4',raw)))
    tk=re.findall(r'tiktok\.com/@([A-Za-z0-9_.]+)',raw); ig=re.findall(r'instagram\.com/([A-Za-z0-9_.]+)',raw)
    once=bool(re.search(r'only (sitewide )?sale of the year|once a year|only sale|one annual sale|once in a blue moon',t,re.I))
    big=bool(re.search(r'biggest (sale|offer|discount|savings)|best offer of the year',t,re.I))
    return dict(ok=len(raw)>3000,size=len(raw),phrases=ph,videos=vids,tiktok=tk[0] if tk else '',ig=next((x for x in ig if x not in('p','reel','explore')),''),once=once,biggest=big)
OUT={}
for h,b in B.items():
    R=rows(h); live=[r for r in R if r['av']]
    a=dict(b); a['home']=home(h); a['shopify']=bool(R)
    if R:
        offs=sorted(r['off'] for r in live if r['off'])
        c=lambda lo:sum(1 for r in live if r['off']>=lo)
        a.update(n=len(R),instock=len(live),marked=len(offs),median=offs[len(offs)//2] if offs else 0,max=max(offs) if offs else 0,ge30=c(30),ge40=c(40),ge50=c(50),ge60=c(60),
                 mode=collections.Counter(offs).most_common(1)[0][0] if offs else 0,
                 promo_tags=sorted({t for r in live for t in r['tags'] if re.search(r'bfcm|black|cyber|sale|promo|\d\d%|final',t,re.I)})[:12])
        good=[r for r in live if r['off']>=30 and r['av']>=max(1,0.5*r['n'])]
        a['top_dollar']=[dict(t=r['t'][:70],h=r['h'],was=r['ca'],now=r['pr'],off=r['off'],av=f"{r['av']}/{r['n']}",img=r['img'][:1]) for r in sorted(good,key=lambda r:-(r['ca']-r['pr']))[:10]]
        a['top_pct']=[dict(t=r['t'][:70],h=r['h'],was=r['ca'],now=r['pr'],off=r['off'],av=f"{r['av']}/{r['n']}",img=r['img'][:1]) for r in sorted([g for g in good if g['ca']>=40],key=lambda r:(-r['off'],-r['ca']))[:8]]
        cheap=[r for r in good if r['pr']<=50 and r['ca']>=40]
        a['under50']=[dict(t=r['t'][:70],h=r['h'],was=r['ca'],now=r['pr'],off=r['off'],img=r['img'][:1]) for r in sorted(cheap,key=lambda r:-(r['ca']-r['pr']))[:5]]
    OUT[h]=a
json.dump(OUT,open(D+'audit.json','w'))
sh=[a for a in OUT.values() if a['shopify']]
print('brands',len(OUT),'catalog read',len(sh),'home ok',sum(1 for a in OUT.values() if a['home'].get('ok')))
