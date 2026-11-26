import sys,os,json,hashlib,subprocess,html
import numpy as np
from PIL import Image
SP='/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad'
sys.path.insert(0,SP)
import an
os.chdir(SP+'/data')
REPO='/home/user/momenti'
A=SP+'/build/assets'; os.makedirs(A,exist_ok=True)
_cat={}
def prod(host,handle):
    if host not in _cat: _cat[host]={r['h']:r for r in an.rows(host)}
    return _cat[host][handle]
def fetch(url,w=1500):
    u=url.split('?')[0]+f'?width={w}' if '/cdn/shop/' in url or 'cdn.shopify.com' in url else url
    fn=A+'/'+hashlib.md5(u.encode()).hexdigest()
    if not os.path.exists(fn) or os.path.getsize(fn)<500:
        subprocess.run(['curl','-sL','-m','60','-A','Mozilla/5.0','-o',fn,u],check=True)
    return fn
def photo(url):
    """lifestyle photo -> jpg path"""
    src=fetch(url); out=src+'.jpg'
    if not os.path.exists(out): Image.open(src).convert('RGB').save(out,quality=92)
    return out
def packshot(url,trim=True):
    """product on flat light background -> background pushed to pure white (for multiply blend), trimmed"""
    src=fetch(url); out=src+'.pack.png'
    if os.path.exists(out): return out
    im=Image.open(src).convert('RGB'); a=np.asarray(im).astype(float)
    b=6; edge=np.concatenate([a[:b].reshape(-1,3),a[-b:].reshape(-1,3),a[:,:b].reshape(-1,3),a[:,-b:].reshape(-1,3)])
    bg=np.median(edge,0)
    o=np.clip(a/bg*255*1.012,0,255)
    if trim:
        m=(255-o.min(2))>14; ys=np.nonzero(m.any(1))[0]; xs=np.nonzero(m.any(0))[0]
        if len(ys) and len(xs):
            pad=int(0.04*max(a.shape[:2])); y0=max(0,ys[0]-pad); y1=min(a.shape[0],ys[-1]+pad); x0=max(0,xs[0]-pad); x1=min(a.shape[1],xs[-1]+pad)
            o=o[y0:y1,x0:x1]
    Image.fromarray(o.astype(np.uint8)).save(out); return out
def bag(name):
    out=A+f'/bag-{name}.png'
    if not os.path.exists(out): Image.open(f'{REPO}/img/{name}-piece.webp').convert('RGBA').save(out)
    return out
def money(x):
    x=float(x); return f'${x:,.0f}' if abs(x-round(x))<.005 else f'${x:,.2f}'
esc=html.escape
