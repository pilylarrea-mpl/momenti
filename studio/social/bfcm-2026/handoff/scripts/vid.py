"""Footage helpers (free, plain curl). 
  import vid
  vid.find(host, [handles])        -> [{handle,url,w,h,dur}] product videos on those product pages
  vid.get(url, 'name')             -> downloads to film/<sub>/name.mp4, returns the path relative to film/ (use it as "f" in a film spec)
  vid.sheet([relpaths], 'name', n=3)-> contact sheet jpg of n frames per clip; open it with Read and LOOK
"""
import json,subprocess,os
FD='/tmp/claude-0/-home-user/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/film'
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36'
def find(host,handles):
    out=[]
    for hd in handles:
        r=subprocess.run(['curl','-sL','-m','20','-A',UA,f'https://{host}/products/{hd}.js'],capture_output=True,text=True).stdout
        try: p=json.loads(r)
        except Exception: continue
        for m in p.get('media') or []:
            if m.get('media_type')=='video':
                s=sorted([x for x in m.get('sources',[]) if x.get('format')=='mp4'],key=lambda x:-(x.get('height') or 0))
                if s: out.append(dict(handle=hd,url=s[0]['url'],w=s[0].get('width'),h=s[0].get('height'),dur=(m.get('duration') or 0)/1000))
    return out
def get(url,name,sub='ag'):
    os.makedirs(f'{FD}/{sub}',exist_ok=True); f=f'{FD}/{sub}/{name}.mp4'; u='https:'+url if url.startswith('//') else url
    if not os.path.exists(f) or os.path.getsize(f)<50000: subprocess.run(['curl','-sL','-m','180','-A',UA,'-o',f,u])
    return f'{sub}/{name}.mp4'
def dur(rel): 
    try: return float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{FD}/{rel}'],capture_output=True,text=True).stdout)
    except Exception: return 0
def sheet(rels,name,n=3):
    from PIL import Image,ImageDraw
    tiles=[]
    for r in rels:
        d=dur(r)
        for j in range(n):
            t=max(0.2,d*(0.1+0.8*j/max(1,n-1))); o=f'{FD}/_sh_{os.getpid()}_{len(tiles)}.jpg'
            subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',f'{FD}/{r}','-frames:v','1','-vf','scale=-2:300',o])
            if os.path.exists(o):
                im=Image.open(o); c=Image.new('RGB',(230,334),'white'); im.thumbnail((230,300)); c.paste(im,((230-im.width)//2,0)); ImageDraw.Draw(c).text((3,303),f'{os.path.basename(r)[:30]}\n@{t:.1f}s of {d:.0f}s',fill='black'); tiles.append(c); os.remove(o)
    cols=9; S=Image.new('RGB',(cols*230,max(1,(len(tiles)+cols-1)//cols)*334),'white')
    for k,t in enumerate(tiles): S.paste(t,((k%cols)*230,(k//cols)*334))
    out=f'{FD}/sheet-{name}.jpg'; S.save(out,quality=82); print(out); return out
