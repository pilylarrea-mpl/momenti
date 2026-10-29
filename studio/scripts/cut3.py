import numpy as np
from PIL import Image, ImageDraw, ImageFilter
D='/tmp/claude-0/-home-user/7e31a87e-85e4-513b-957c-728f06c1313d/images/'
S={'paris':'6','miami':'7','miami-pink':'8','monaco':'9','nyc':'10'}
for n,f in S.items():
    im=Image.open(D+f+'.webp').convert('RGB'); a=np.asarray(im).astype(float); H,W,_=a.shape
    bg=np.concatenate([a[:,:10],a[:,-10:]],1).mean(1)
    d=np.sqrt(((a-bg[:,None,:])**2).sum(2)); sat=a.max(2)-a.min(2)
    m=(d>30)
    mi=Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))
    pad=Image.new('L',(W+2,H+2),0); pad.paste(mi,(1,1))
    for p in [(0,0),(W+1,0),(0,H+1),(W+1,H+1)]: ImageDraw.floodfill(pad,p,128)
    m=np.asarray(pad)[1:-1,1:-1]!=128
    # floor: find the bag's lowest row = last row where coverage spans >40% of max width, then cut
    rows=m.sum(1); mx=rows.max(); ys=np.nonzero(rows>mx*0.4)[0]; bottom=ys.max()
    m[bottom+2:]=0
    lum=a.mean(2)
    # bag bottom: the biggest dark-to-light jump going down, sampled across the middle columns
    ys=[]
    for x in range(int(W*.3),int(W*.7),12):
        col=np.convolve(lum[:,x],np.ones(5)/5,'same'); g=col[6:]-col[:-6]
        lo=int(H*.75); seg=g[lo:H-12]; idx=np.nonzero(seg>max(22,seg.max()*.45))[0]
        if len(idx): ys.append(lo+idx.max()+3)
    yb=int(np.median(ys))
    m[yb:]=False
    band=60; r0=yb-band
    xs=np.nonzero(m[r0])[0]; L,Rr=xs.min(),xs.max(); Wd=Rr-L
    for yy in range(r0,yb):
        t=(yy-r0)/band; k=int(Wd*0.035*t*t)
        m[yy,:L+k]=False; m[yy,Rr-k+1:]=False
    alpha=Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(.7))
    o=im.convert('RGBA'); o.putalpha(alpha); bb=alpha.getbbox(); o=o.crop(bb)
    w,h=o.size
    if w>1400: o=o.resize((1400,round(h*1400/w)),Image.LANCZOS)
    o.save(f'site/img/{n}-piece.webp',quality=88,method=6); print(n,im.size,bb,bottom)
s=Image.new('RGB',(1600,1650),(60,140,80))
for i,n in enumerate(S):
    p=Image.open(f'site/img/{n}-piece.webp'); p.thumbnail((780,520)); s.paste(p,((i%2)*800,(i//2)*550),p)
s.save('src/pieces2.png')
