import numpy as np, json
from PIL import Image, ImageDraw, ImageFilter
D='/tmp/claude-0/-home-user/7e31a87e-85e4-513b-957c-728f06c1313d/images/'
S={'tokyo':('1',(606,46,948,168),(712,149,834,178),[(685,135),(872,135)],25),
   'havana':('2',(618,138,926,241),(710,229,834,252),[(689,220),(856,220)],21.5),
   'rome':('3',(644,52,898,172),(718,158,814,182),[(692,150),(842,150)],22.5),
   'havana-blue':('4',(590,96,940,212),(712,192,814,216),[(665,185),(857,185)],25)}
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
meta={}
for name,(f,(x0,y0,x1,y1),ped,wheels,wr) in S.items():
    im=Image.open(D+f+'.webp').convert('RGB'); a=np.asarray(im).astype(float)
    L=a[:, x0-30:x0-6].mean(1); R=a[:, x1+6:x1+30].mean(1)
    t=(np.arange(x0,x1)-x0)/(x1-x0)
    bg=L[:,None,:]*(1-t[None,:,None])+R[:,None,:]*t[None,:,None]
    reg=a[y0:y1,x0:x1]; bgr=bg[y0:y1]
    m=np.sqrt(((reg-bgr)**2).sum(2))>18
    m=ero(dil(m,2),2)
    mi=Image.fromarray((m*255).astype(np.uint8)); pad=Image.new('L',(mi.width+2,mi.height+2),0); pad.paste(mi,(1,1))
    ImageDraw.floodfill(pad,(0,0),128); m=np.asarray(pad)[1:-1,1:-1]!=128
    m=dil(ero(m,2),2)
    full=m.copy()
    # take the mount out of the car
    pr=np.zeros_like(m); pr[ped[1]-y0:ped[3]-y0, ped[0]-x0:ped[2]-x0]=True
    car=m&~pr
    car=dil(ero(car,1),1)
    alpha=Image.fromarray((car*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(.8))
    rgba=im.crop((x0,y0,x1,y1)).convert('RGBA'); rgba.putalpha(alpha)
    ys,xs=np.nonzero(car); bb=(xs.min(),ys.min(),xs.max()+1,ys.max()+1)
    rgba=rgba.crop(bb).resize(((bb[2]-bb[0])*2,(bb[3]-bb[1])*2),Image.LANCZOS)
    rgba.save(f'site/img/{name}-car.png')
    ox,oy=x0+bb[0],y0+bb[1]
    # clean bag: paint out the car but keep the mount
    md=dil(car,3)&~pr
    clean=a.copy(); sub=clean[y0:y1,x0:x1]; sub[md]=bgr[md]; clean[y0:y1,x0:x1]=sub
    ci=Image.fromarray(clean.clip(0,255).astype(np.uint8)); ci.save(f'site/img/{name}-bag.jpg',quality=86)
    # silhouette of the clean bag incl. mount
    bgrow=np.concatenate([clean[:,:12],clean[:,-12:]],1).mean(1)
    sil=np.sqrt(((clean-bgrow[:,None,:])**2).sum(2))>28
    si=Image.fromarray((sil*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(7))
    pad=Image.new('L',(si.width+2,si.height+2),0); pad.paste(si,(1,1)); ImageDraw.floodfill(pad,(0,0),128)
    sil=np.asarray(pad)[1:-1,1:-1]!=128
    cov=sil[:,300:1200].mean(1); cut=next(y for y in range(600,1024) if cov[y]<0.97); sil[cut:]=0
    ys2,xs2=np.nonzero(sil)
    mk=Image.new('RGBA',ci.size,(0,0,0,0)); mk.putalpha(Image.fromarray((sil*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)))
    mk.resize((1536,1024)).save(f'site/img/{name}-mask.png')
    meta[name]={'car':[int(ox),int(oy),int(bb[2]-bb[0]),int(bb[3]-bb[1])],'wheels':[[float(w[0]-ox),float(w[1]-oy)] for w in wheels],'wr':wr,
                'bag':[int(xs2.min()),int(ys2.min()),int(xs2.max()-xs2.min()),int(cut-ys2.min())]}
    # check sheet: car with wheel circles
    chk=Image.open(f'site/img/{name}-car.png').copy(); d=ImageDraw.Draw(chk)
    for (wx,wy) in wheels: d.ellipse([((wx-ox)-wr)*2,((wy-oy)-wr)*2,((wx-ox)+wr)*2,((wy-oy)+wr)*2],outline=(255,0,0,255),width=2)
    bgc=Image.new('RGBA',chk.size,(40,140,70,255)); bgc.alpha_composite(chk); bgc.convert('RGB').save(f'src/chk-{name}.png')
print(json.dumps(meta))
json.dump(meta,open('src/meta.json','w'))
