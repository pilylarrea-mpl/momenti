import numpy as np
from PIL import Image, ImageFilter, ImageDraw
def shift(m,dx,dy):
    r=np.zeros_like(m); h,w=m.shape
    r[max(dy,0):h+min(dy,0), max(dx,0):w+min(dx,0)] = m[max(-dy,0):h+min(-dy,0), max(-dx,0):w+min(-dx,0)]
    return r
for n in ['tokyo','havana','rome','havana-blue']:
    im=Image.open(f'out/{n}-bag.jpg'); a=np.asarray(im).astype(float)
    # bloom: keep bright saturated highlights, blur
    lum=a.mean(2); hi=np.clip((lum-150)/90,0,1)[...,None]
    b=Image.fromarray((a*hi).clip(0,255).astype(np.uint8)).resize((768,512)).filter(ImageFilter.GaussianBlur(10))
    b.save(f'out/{n}-bloom.jpg',quality=80)
    # silhouette mask (bag body + frame), from diff vs per-row edge background
    bg=np.concatenate([a[:,:12],a[:,-12:]],1).mean(1)
    d=np.sqrt(((a-bg[:,None,:])**2).sum(2))
    m=d>28
    mi=Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(7))
    pad=Image.new('L',(mi.width+2,mi.height+2),0); pad.paste(mi,(1,1)); ImageDraw.floodfill(pad,(0,0),128)
    p=np.asarray(pad)[1:-1,1:-1]; m=p!=128
    ys,xs=np.nonzero(m); print(n,'silhouette bbox',xs.min(),ys.min(),xs.max(),ys.max())
    out=Image.new('RGBA',im.size,(0,0,0,0)); out.putalpha(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5)))
    out.resize((768,512)).save(f'out/{n}-mask.png')
