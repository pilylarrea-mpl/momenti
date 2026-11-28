import sys,json,subprocess,os; sys.path.insert(0,'/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad'); import pick
from concurrent.futures import ThreadPoolExecutor
OUTF=pick.SP+'/roundup/allvideos.json'
def one(a):
    h,hd=a
    r=subprocess.run(['curl','-sL','-m','20','-A','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36',f'https://{h}/products/{hd}.js'],capture_output=True,text=True).stdout
    try: p=json.loads(r)
    except Exception: return (h,hd,None)
    vs=[]
    for m in p.get('media') or []:
        if m.get('media_type')=='video':
            s=sorted([x for x in m.get('sources',[]) if x.get('format')=='mp4'],key=lambda x:-(x.get('height') or 0))
            if s: vs.append(dict(url=s[0]['url'],w=s[0].get('width'),h=s[0].get('height'),dur=(m.get('duration') or 0)/1000))
    return (h,hd,vs)
jobs=[]
for h,b in pick.B.items():
    if b['industry'] in pick.CORE_SKIP or pick.currency(h)!='$': continue
    R=[r for r in pick.rows(h) if r['av']>0]
    if len(R)<20: continue
    R=sorted(R,key=lambda r:(-(r['off']>=30),-(r['off']>0),-r['ca'],-r['pr']))[:10]
    jobs+=[(h,r['h']) for r in R]
print(len(jobs),'requests',flush=True); out={}
with ThreadPoolExecutor(16) as ex:
    for h,hd,vs in ex.map(one,jobs):
        d=out.setdefault(h,dict(brand=pick.B[h]['brand'],industry=pick.B[h]['industry'],ok=0,fail=0,vids=[]))
        if vs is None: d['fail']+=1
        else:
            d['ok']+=1
            for v in vs: d['vids'].append(dict(v,handle=hd))
json.dump(out,open(OUTF,'w'),indent=1)
for h,d in sorted(out.items(),key=lambda x:-len(x[1]['vids'])):
    if d['vids']: print(f"{d['brand']:24} {d['industry'][:18]:18} videos {len(d['vids']):2} of {d['ok']} products; vertical {sum(1 for v in d['vids'] if (v['h'] or 0)>(v['w'] or 0))}")
