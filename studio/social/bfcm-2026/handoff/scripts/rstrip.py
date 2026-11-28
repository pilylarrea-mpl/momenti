import json,subprocess,sys
from PIL import Image
NS='/tmp/claude-0/-home-user/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/roundup'
for slug in sys.argv[1:]:
    b=json.load(open(f'{NS}/{slug}/build.json')); ts=[1.5]+[t+3.6 for n,t in b['marks'][1:-1]]+[b['marks'][-1][1]+1]; fs=[]
    for k,t in enumerate(ts):
        f=f'{NS}/{slug}/f{k:02d}.jpg'; subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',f'{NS}/roundup-{slug}.mp4','-frames:v','1','-vf','scale=300:534',f]); fs.append(f)
    cols=6; rows=(len(fs)+cols-1)//cols; S=Image.new('RGB',(cols*300,rows*534),'white')
    for k,f in enumerate(fs): S.paste(Image.open(f),((k%cols)*300,(k//cols)*534))
    S.save(f'{NS}/strip-{slug}.jpg',quality=85); print(slug,b['duration'])
