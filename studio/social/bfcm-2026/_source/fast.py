"""Fast-cut product video: full-bleed photos, three quick cuts per item, bold sticker labels, push-in on every cut."""
import sys,os,json,shutil,subprocess,urllib.request
sys.path.insert(0,'.')
from vid2 import SP,B,pick,fetch,esc
from PIL import Image
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
def live(host,handle):
    r=subprocess.run(['curl','-sL','-m','40','-A',UA['User-Agent'],f'https://{host}/products/{handle}.js'],capture_output=True,text=True).stdout
    try: p=json.loads(r)
    except Exception:
        row={x['h']:x for x in pick.rows(host)}[handle]; print('  (live check refused for',host,'- using the catalog read on Nov 26)')
        return dict(now=row['pr'],was=row['ca'],av=row['av'],n=row['n'],imgs=row['img'],stale=True)
    a=[v for v in p['variants'] if v['available']]
    return dict(now=min(v['price'] for v in a)/100,was=max((v.get('compare_at_price') or 0) for v in p['variants'])/100,av=len(a),n=len(p['variants']),imgs=['https:'+i if i.startswith('//') else i for i in p['images']])
def plate(url,out):
    im=Image.open(fetch(url,1600)).convert('RGB'); W,H=1296,2304; r=max(W/im.width,H/im.height)
    im=im.resize((round(im.width*r)+1,round(im.height*r)+1),Image.LANCZOS); x=(im.width-W)//2; y=(im.height-H)//2
    im.crop((x,y,x+W,y+H)).save(out,quality=93)
CSS='''<style>
@font-face{font-family:'IT';src:url('/home/user/momenti/assets/fonts/InterTight-VF.ttf');font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box} html,body{width:1080px;height:1920px;background:transparent;font-family:'IT';overflow:hidden}
.rank{position:absolute;left:60px;top:270px;background:#111;color:#fff;font-weight:800;font-size:44px;padding:10px 22px;border-radius:14px;letter-spacing:.02em}
.rank b{color:#ffd84a;font-weight:800}
.lab{position:absolute;left:60px;right:140px;bottom:370px}
.br{display:inline-block;background:#fff;color:#111;font-weight:800;font-size:34px;letter-spacing:.08em;text-transform:uppercase;padding:8px 16px;border-radius:10px}
.nm{display:inline-block;margin-top:10px;background:#111;color:#fff;font-weight:800;font-size:58px;line-height:1.05;padding:8px 18px 10px;border-radius:14px}
.pr{display:flex;align-items:center;gap:18px;margin-top:16px}
.now{background:#ffd84a;color:#111;font-weight:900;font-size:150px;line-height:1;padding:6px 26px 10px;border-radius:22px;letter-spacing:-.03em}
.was{display:inline-block;background:#fff;color:#111;font-weight:800;font-size:50px;padding:2px 12px;border-radius:10px;text-decoration:line-through;text-decoration-thickness:5px;margin-bottom:8px}
.off{background:#e5352b;color:#fff;font-weight:900;font-size:46px;padding:8px 16px;border-radius:12px}
.why{display:inline-block;margin-top:16px;background:#111;color:#fff;font-weight:700;font-size:40px;line-height:1.15;padding:10px 18px;border-radius:12px;max-width:860px}
.hook{position:absolute;left:60px;right:60px;top:560px;text-align:left}
.hook div{display:inline-block;background:#111;color:#fff;font-weight:900;font-size:HKpx;line-height:1.02;padding:6px 24px 12px;border-radius:20px;margin-bottom:14px;letter-spacing:-.02em}
.hook div.y{background:#ffd84a;color:#111}
.hook p{display:inline-block;background:#fff;color:#111;font-weight:800;font-size:44px;line-height:1.2;max-width:900px;padding:10px 20px;border-radius:14px;margin-top:10px}
.series{position:absolute;left:60px;top:270px;background:#fff;color:#111;font-weight:800;font-size:34px;letter-spacing:.06em;text-transform:uppercase;padding:10px 18px;border-radius:12px}
</style>'''
def build(slug,series,hook_lines,hook_sub,items,end_lines,end_sub,cut=0.6,per=3,hk=128):
    global CSS; CSS=CSS.replace('HKpx',f'{hk}px')
    out=f'{SP}/out6/{slug}'; shutil.rmtree(out,ignore_errors=True); os.makedirs(out+'/ov'); os.makedirs(out+'/pl'); os.makedirs(out+'/seg')
    L=[]
    for it in items:
        lv=live(it['host'],it['handle']); assert lv['av']>0 and lv['was']>lv['now'],it['handle']
        it.update(now=lv['now'],was=lv['was'],av=lv['av'],n=lv['n'],off=round(100*(1-lv['now']/lv['was'])))
        it['pl']=[]
        for j,ix in enumerate(it['imgs']):
            f=f"{out}/pl/{len(L):02d}_{j}.jpg"; plate(lv['imgs'][ix],f); it['pl'].append(f)
        L.append(it); print(f"{it['brand']:20} {it['name']:26} ${it['was']:.0f}->${it['now']:.0f} {it['off']}% {it['av']}/{it['n']}")
    money=lambda x:f'${x:,.0f}' if abs(x-round(x))<.005 else f'${x:,.2f}'
    hookh=''.join(f'<div class="{c}">{esc(t)}</div><br>' for t,c in hook_lines)
    O={'hook':f'{CSS}<body><div class=series>{esc(series)}</div><div class=hook>{hookh}<p>{esc(hook_sub)}</p></div></body>',
       'end':f'{CSS}<body><div class=series>{esc(series)}</div><div class=hook>'+''.join(f'<div class="{c}">{esc(t)}</div><br>' for t,c in end_lines)+f'<p>{esc(end_sub)}</p></div></body>'}
    for i,it in enumerate(L):
        base=f'<div class=rank><b>{i+1}</b> / {len(L)}</div><div class=lab><span class=br>{esc(it["brand"])}</span><br><span class=nm>{esc(it["name"])}</span><div class=pr><span class=now>{money(it["now"])}</span><div><div class=was>{money(it["was"])}</div><div class=off>-{it["off"]}%</div></div></div>'
        O[f'i{i:02d}a']=f'{CSS}<body>{base}</div></body>'
        O[f'i{i:02d}b']=f'{CSS}<body>{base}<span class=why>{esc(it["why"])}</span></div></body>'
    for k,h in O.items(): open(f'{out}/ov/{k}.html','w').write(h)
    subprocess.run(['node',B+'/shootpng.js',out+'/ov'],check=True)
    segs=[]
    def seg(img,ov,dur,zin=True,name=None):
        n=name or f'{len(segs):03d}'; f=f'{out}/seg/{n}.mp4'; fr=max(2,round(dur*30))
        z=f"'1+0.07*on/{fr}'" if zin else f"'1.07-0.07*on/{fr}'"
        subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-t',str(dur+0.2),'-i',img,'-i',ov,'-filter_complex',f"[0]zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30[b];[b][1]overlay=0:0,format=yuv420p",'-frames:v',str(fr),'-r','30','-c:v','libx264','-crf','18',f],check=True); segs.append(f)
    for i,it in enumerate(L): seg(it['pl'][1 if len(it['pl'])>1 else 0],f'{out}/ov/hook.png',2.6/len(L),i%2==0)   # hook montage
    for i,it in enumerate(L):
        for j,p in enumerate(it['pl'][:per]): seg(p,f"{out}/ov/i{i:02d}{'a' if j==0 else 'b'}.png",cut if j<per-1 else cut+0.25,j%2==0)
    dark=f'{out}/pl/end.jpg'; Image.open(L[-1]['pl'][1]).point(lambda v:int(v*0.45)).save(dark,quality=90); seg(dark,f'{out}/ov/end.png',2.4,True)
    open(out+'/list.txt','w').write(''.join(f"file '{s}'\n" for s in segs))
    final=f'{SP}/out6/{slug}.mp4'; subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',out+'/list.txt','-c','copy',final],check=True)
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',final],capture_output=True,text=True).stdout)
    subprocess.run(['ffmpeg','-v','error','-y','-i',final,'-vf',f"fps={12/d},scale=270:-1,tile=12x1",'-frames:v','1',f'{SP}/out6/{slug}-strip.jpg'],check=True)
    json.dump(L,open(f'{SP}/out6/{slug}.json','w'),indent=1,default=str); print('ok',slug,round(d,1),'s')
if __name__=='__main__':
    IB='intentionallyblank.us'; b=lambda h,n,w,im,host=IB,brand='Intentionally Blank':dict(host=host,handle=h,brand=brand,name=n,why=w,imgs=im)
    build('boots-fast','Black Friday · Boots',[('ONLY 3 STORES','y'),('HAVE BOOTS','') ,('40% OFF','')],'I checked 199 Black Friday sales. These are the 10 best pairs.',[
      b('marlowe-black','Marlowe platform','Vegan, every size in',[0,1,3]),
      b('go-to-lace-lug-boot-black','Go-To lug boot','Water-resistant suede. Final sale',[0,1,3],'nisolo.com','Nisolo'),
      b('taffy-patent-leather-heeled-boot','Taffy patent boot','Olive patent leather',[0,1,2]),
      b('camille-boots-lilac-purple','Camille kitten boot','Lilac suede, every size in',[0,1,2],'marcellanyc.com','Marcella'),
      b('florence-curved-heel-leather-ankle-boot','Florence Chelsea','Leather, every size in',[0,2,3]),
      b('rancher-suede-mid-boot','Rancher western','Suede, every size in',[0,1,3]),
      b('scorpio-heeled-ankle-boot','Scorpio ankle boot','Block heel, 15 of 16 sizes',[0,1,3]),
      b('lindstrom-patent-mid-boot','Lindstrom buckle boot','Three buckles, patent',[0,1,3]),
      b('filmore-suede-knee-boot','Filmore knee boot','Suede, every size in',[0,1,3]),
      b('hiperson-leather-knee-high-boot','Hiperson knee boot','Leather, black in every size',[0,1,3])],
      [('TOMORROW','y'),('JEWELRY','')],'From $26. Follow so you see it.',hk=112)
