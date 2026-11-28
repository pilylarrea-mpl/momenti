import json,subprocess,sys
from PIL import Image
s=sys.argv[1]; b=json.load(open(f'{s}/build.json')); ts=[0.1,1.6]
for n,t in b['marks'][1:-1]: ts+=[t+0.5,t+2.8]
ts.append(b['marks'][-1][1]+1.2); fs=[]
for k,t in enumerate(ts):
    f=f'{s}/f{k:02d}.jpg'; subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',f'{s}.mp4','-frames:v','1','-vf','scale=270:480',f]); fs.append(f)
cols=7; S=Image.new('RGB',(cols*270,((len(fs)+cols-1)//cols)*480),'white')
for k,f in enumerate(fs): S.paste(Image.open(f),((k%cols)*270,(k//cols)*480))
S.save(f'strip-{s}.jpg',quality=85); print(S.size,b['duration'])
