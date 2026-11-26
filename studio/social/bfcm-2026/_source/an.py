import json,glob,sys,collections
def load(h):
    out=[]
    for f in sorted(glob.glob(f'cat/{h}.*.json')):
        try: out+=json.load(open(f)).get('products',[])
        except Exception as e: pass
    return out
def rows(h):
    R=[]
    for p in load(h):
        vs=p['variants']; 
        if not vs: continue
        av=sum(1 for v in vs if v['available'])
        pool=[v for v in vs if v['available']] or vs
        v0=min(pool,key=lambda v:float(v['price']))   # cheapest in-stock variant, with ITS OWN compare-at
        pr=float(v0['price']); ca=float(v0['compare_at_price'] or 0); vname=v0.get('title','')
        off=round(100*(1-pr/ca)) if ca>pr else 0
        R.append(dict(vname=vname,t=p['title'],h=p['handle'],type=p['product_type'],pr=pr,ca=ca,off=off,av=av,n=len(vs),img=[i['src'] for i in p['images'][:3]],tags=p['tags'],pub=p['published_at'][:10]))
    return R
if __name__=='__main__':
    for h in sys.argv[1:]:
        R=rows(h); 
        print('\n==',h,len(R),'products;','marked down:',sum(1 for r in R if r['off']>0),'in stock:',sum(1 for r in R if r['av']))
        print(' types:',collections.Counter(r['type'] for r in R).most_common(12))
        S=sorted([r for r in R if r['av'] and r['off']>0],key=lambda r:(-r['off'],-r['ca']))
        for r in S[:28]: print(f"  {r['off']}% ${r['ca']:.0f}->${r['pr']:.0f} av{r['av']}/{r['n']} [{r['type']}] {r['t']} | {r['h']}")
