import numpy as np
from PIL import Image, ImageDraw, ImageFilter
D='/tmp/claude-0/-home-user/7e31a87e-85e4-513b-957c-728f06c1313d/images/'
# name: (file, clasp box x0,y0,x1,y1 incl. pedestal, frame top y)
S={'tokyo':('1',(606,46,948,168)),'havana':('2',(618,138,926,241)),
   'rome':('3',(644,52,898,172)),'havana-blue':('4',(590,96,940,212))}
def shift(m,dx,dy):
    r=np.zeros_like(m); h,w=m.shape
    r[max(dy,0):h+min(dy,0), max(dx,0):w+min(dx,0)] = m[max(-dy,0):h+min(-dy,0), max(-dx,0):w+min(-dx,0)]
    return r
def dil(m,k=1):
    o=m.copy()
    for dx in range(-k,k+1):
        for dy in range(-k,k+1): o|=shift(m,dx,dy)
    return o
def ero(m,k=1):
    o=m.copy()
    for dx in range(-k,k+1):
        for dy in range(-k,k+1): o&=shift(m,dx,dy)
    return o
for name,(f,(x0,y0,x1,y1)) in S.items():
    im=Image.open(D+f+'.webp').convert('RGB'); a=np.asarray(im).astype(float)
    # background model per row: linear interp between strips left and right of the box
    L=a[:, x0-30:x0-6].mean(1); R=a[:, x1+6:x1+30].mean(1)
    t=(np.arange(x0,x1)-x0)/(x1-x0)
    bg=L[:,None,:]*(1-t[None,:,None])+R[:,None,:]*t[None,:,None]   # H x w x 3
    reg=a[y0:y1, x0:x1]; bgr=bg[y0:y1]
    d=np.sqrt(((reg-bgr)**2).sum(2))
    m=d>18
    m=ero(dil(m,2),2)               # close small gaps
    # fill holes: flood background from border
    mi=Image.fromarray((m*255).astype(np.uint8)); pad=Image.new('L',(mi.width+2,mi.height+2),0); pad.paste(mi,(1,1))
    ImageDraw.floodfill(pad,(0,0),128)
    p=np.asarray(pad)[1:-1,1:-1]; m=p!=128
    m=ero(m,1); m=dil(m,0)
    # keep only the largest-ish content: drop tiny specks via opening
    m=dil(ero(m,2),2)
    alpha=Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    rgba=im.crop((x0,y0,x1,y1)).convert('RGBA'); rgba.putalpha(alpha)
    ys,xs=np.nonzero(m); bb=(xs.min(),ys.min(),xs.max()+1,ys.max()+1)
    rgba=rgba.crop(bb)
    # upscale 2x for crispness when flying large
    rgba=rgba.resize((rgba.width*2,rgba.height*2),Image.LANCZOS)
    rgba.save(f'out/{name}-clasp.png')
    cx0,cy0=x0+bb[0],y0+bb[1]; cw,ch=bb[2]-bb[0],bb[3]-bb[1]
    # clean bag: paint background into the masked clasp pixels (dilated)
    md=dil(m,3)
    clean=a.copy(); sub=clean[y0:y1,x0:x1]; sub[md]=bgr[md]; clean[y0:y1,x0:x1]=sub
    ci=Image.fromarray(clean.clip(0,255).astype(np.uint8))
    ci.save(f'out/{name}-bag.jpg',quality=86)
    im.save(f'out/{name}-orig.jpg',quality=86)
    print(name, 'clasp at', cx0,cy0,cw,ch)
