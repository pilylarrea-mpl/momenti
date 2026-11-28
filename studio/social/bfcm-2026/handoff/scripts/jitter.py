import subprocess,sys,numpy as np
def frames(f,t0,n=40,w=270,h=480):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(t0),'-i',f,'-frames:v',str(n),'-vf',f'crop=iw:ih*0.5:0:ih*0.08,scale={w}:{h}','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.uint8).reshape(-1,h,w).astype(float)
def shift(a,b):
    A=np.fft.fft2(a);Bf=np.fft.fft2(b);R=A*np.conj(Bf);R/=np.abs(R)+1e-9;c=np.abs(np.fft.ifft2(R));y,x=np.unravel_index(c.argmax(),c.shape)
    # sub-pixel by parabola
    def sp(v,i,n):
        l,m,r=v[(i-1)%n],v[i],v[(i+1)%n];d=(l-r)/(2*(l-2*m+r)+1e-9);p=i+d;return p-n if p>n/2 else p
    return sp(c[y,:],x,c.shape[1]),sp(c[:,x],y,c.shape[0])
def report(f,t0):
    F=frames(f,t0); S=np.array([shift(F[i],F[i+1]) for i in range(len(F)-1)])*4   # back to full-res pixels
    d=np.diff(S,axis=0); print(f'{f.split("/")[-1]} @{t0}s  frame-to-frame move: mean {np.abs(S).mean():.2f}px, jerk (change between steps): max {np.abs(d).max():.2f}px, rms {np.sqrt((d**2).mean()):.2f}px')
if __name__=='__main__':
    for t in sys.argv[2:]: report(sys.argv[1],float(t))
