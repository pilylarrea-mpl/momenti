import subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont
V='/tmp/claude-0/-home-user/7e31a87e-85e4-513b-957c-728f06c1313d/scratchpad/momenti/gen/tA.mp4'
OUT='/home/user/momenti-tiktok.mp4'
SW,SH=1920,1080; OW,OH=1080,1920; FPS=24
TOP=np.array([241,231,219]);BOT=np.array([250,242,233])
grad=np.zeros((OH,OW,3),np.uint8)
for y in range(OH): grad[y,:]=(TOP+(BOT-TOP)*y/OH).astype(np.uint8)
def ease(t): return t*t*(3-2*t)
def lerp(a,b,t): return a+(b-a)*t
def seg(t,a,b): return min(1,max(0,(t-a)/(b-a)))
def window(t):
    # 9:16 window that follows the car, then eases out to show the whole clutch
    cx=lerp(520,900,ease(seg(t,2.0,3.4)))
    cx=lerp(cx,960,ease(seg(t,3.4,4.3)))
    w=lerp(SH*9/16,1560,ease(seg(t,4.2,6.2)))
    return cx,540,w
dec=subprocess.Popen(['ffmpeg','-v','error','-i',V,'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{OW}x{OH}','-r',str(FPS),'-i','-',
  '-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-profile:v','high','-movflags','+faststart',OUT],stdin=subprocess.PIPE)
def place(fr,t):
    cx,cy,w=window(t); s=OW/w; h=w*16/9
    canvas=Image.fromarray(grad.copy())
    img=Image.fromarray(fr).resize((round(SW*s),round(SH*s)),Image.LANCZOS)
    # feather the frame's edges into the backdrop so no rectangle shows as it pulls back
    k=ease(seg(t,4.2,5.0))
    if k<=0: canvas.paste(img,(round(OW/2-cx*s),round(OH/2-cy*s))); return canvas
    a=np.ones((img.height,img.width),np.float32); f=max(2,int(img.height*0.09*k))
    ramp=np.linspace(0,1,f,dtype=np.float32)
    a[:f]*=ramp[:,None];a[-f:]*=ramp[::-1][:,None];fx=max(2,int(img.width*0.05*k));a[:,:fx]*=ramp[np.linspace(0,f-1,fx).astype(int)][None,:];a[:,-fx:]*=ramp[np.linspace(0,f-1,fx).astype(int)][::-1][None,:]
    canvas.paste(img,(round(OW/2-cx*s),round(OH/2-cy*s)),Image.fromarray((a*255).astype(np.uint8)))
    return canvas
n=0;last=None
while True:
    b=dec.stdout.read(SW*SH*3)
    if len(b)<SW*SH*3: break
    fr=np.frombuffer(b,np.uint8).reshape(SH,SW,3); last=place(fr,n/FPS); enc.stdin.write(last.tobytes()); n+=1
# hold on the parked car, then the end card
for i in range(int(FPS*1.0)): enc.stdin.write(last.tobytes())
logo=Image.open('/home/user/momenti/img/momenti-logo.png').convert('RGBA'); lw=760; logo=logo.resize((lw,round(logo.height*lw/logo.width)),Image.LANCZOS)
card=Image.fromarray(grad.copy()).convert('RGBA'); card.alpha_composite(logo,((OW-lw)//2,820))
d=ImageDraw.Draw(card)
try:
    f1=ImageFont.truetype('/tmp/claude-0/-home-user-momenti/7e31a87e-85e4-513b-957c-728f06c1313d/scratchpad/fonts/Jost-500.ttf',30)
except Exception: f1=None
def spaced(txt,y,size,col):
    font=ImageFont.truetype(FONT,size)
    chars=list(txt); tr=size*0.32
    widths=[d.textlength(c,font=font) for c in chars]; tw=sum(widths)+tr*(len(chars)-1); x=(OW-tw)/2
    for c,wd in zip(chars,widths): d.text((x,y),c,font=font,fill=col); x+=wd+tr
import glob
FONT=glob.glob('/usr/share/fonts/**/DejaVuSans.ttf',recursive=True)[0]
card=card.convert('RGB'); d=ImageDraw.Draw(card)
spaced('OBJECTS OF A MOMENT',1000,28,(74,63,53))
spaced('HOUSEOFMOMENTI.COM',1640,26,(142,131,120))
cardnp=np.asarray(card); lastnp=np.asarray(last).astype(float)
for i in range(int(FPS*0.8)):
    k=(i+1)/(FPS*0.8); enc.stdin.write((lastnp*(1-k)+cardnp*k).astype(np.uint8).tobytes())
for i in range(int(FPS*2.6)): enc.stdin.write(cardnp.tobytes())
enc.stdin.close(); enc.wait(); print('frames',n)
