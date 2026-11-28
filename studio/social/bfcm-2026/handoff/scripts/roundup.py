"""Brand roundup video in a native TikTok look: one brand every ~4s, big plain text, product tiles popping in. Silent draft; recut to voice later.
usage: python3 roundup.py <spec.json>"""
import sys,os,json,shutil,subprocess,html
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import pick,fast
from PIL import Image
SP='/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad'
NS='/tmp/claude-0/-home-user/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/roundup'
B=SP+'/build'; PW,PH=1080,1920; e=html.escape
CSS='''<style>
@font-face{font-family:'TT';src:url('%s/fonts/TikTokSans.woff2');font-weight:300 900}
*{margin:0;padding:0;box-sizing:border-box} html,body{width:1080px;height:1920px;background:transparent;font-family:'TT',sans-serif;overflow:hidden}
.t{position:absolute;left:50px;right:130px;text-align:center;color:#fff;text-shadow:0 0 22px rgba(0,0,0,.7),0 3px 8px rgba(0,0,0,.75),0 0 3px #000,0 0 3px #000}
.nm{top:850px;font-weight:800;font-size:92px;line-height:1.02;letter-spacing:-.01em}
.cl{top:966px;font-weight:600;font-size:46px;white-space:nowrap}
.st{position:absolute;left:50px;right:130px;top:1048px;text-align:center}
.st span{display:inline-block;background:#fff;color:#111;font-weight:700;font-size:40px;line-height:1.15;padding:12px 22px 14px;border-radius:14px;max-width:860px}
.tile{position:absolute;background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,.35)}
.tile img{width:100%%;height:100%%;object-fit:cover}
.a{left:56px;top:270px;width:420px;height:540px}.b{left:500px;top:270px;width:420px;height:540px}.c{left:278px;top:1160px;width:420px;height:410px}
.hw{position:absolute;left:50px;right:130px;top:560px;display:flex;flex-direction:column;align-items:center;gap:26px;text-align:center}
.hk{position:static!important;font-weight:800;font-size:100px;line-height:1.05;letter-spacing:-.015em;text-wrap:balance}
.hs{text-align:center}.hs span{display:inline-block;background:#fff;color:#111;font-weight:700;font-size:38px;padding:12px 22px 14px;border-radius:14px;max-width:820px;line-height:1.2}
.shade{position:absolute;inset:0;background:rgba(0,0,0,SH)}
</style>'''%SP
def cover(url,out,W=1296,H=2304,yb=0.3):
    im=Image.open(fast.fetch(url,1600)).convert('RGB'); r=max(W/im.width,H/im.height); im=im.resize((round(im.width*r)+1,round(im.height*r)+1),Image.LANCZOS)
    x=(im.width-W)//2; y=int((im.height-H)*yb); im.crop((x,y,x+W,y+H)).save(out,quality=92)
def tile(url,out):
    im=Image.open(pick._get(url,900)).convert('RGB'); im.thumbnail((900,1100)); im.save(out,quality=90)
def img(host,ref):
    r={x['h']:x for x in pick.rows(host)}[ref['handle']]; return r['img'][min(ref.get('img',0),len(r['img'])-1)]
def run(spec,per=4.4):
    S=json.load(open(spec)); slug=S['slug']; OUT=f'{NS}/{slug}'; shutil.rmtree(OUT,ignore_errors=True)
    for d in ('ov','seg','im'): os.makedirs(f'{OUT}/{d}')
    BR=S['brands']; css=CSS.replace('SH','.26')
    for i,b in enumerate(BR):
        cover(img(b['host'],b['bg']),f'{OUT}/im/bg{i}.jpg')
        for j,t in enumerate(b['tiles'][:3]): tile(img(b['host'],t),f'{OUT}/im/t{i}_{j}.jpg')
        nm=b['brand'].lower(); fs=92 if len(nm)<=15 else (76 if len(nm)<=19 else 62)
        base=f'<div class=shade></div><div class="t nm" style="font-size:{fs}px">{i+1}. {e(nm)}</div><div class="t cl" style="font-size:{46 if len(b.get("claim") or "")<=32 else 38}px">{e(b.get("claim") or "")}</div><div class=st><span style="font-size:{40 if len(b["stat"])<=40 else (33 if len(b["stat"])<=50 else 28)}px;white-space:nowrap">{e(b["stat"])}</span></div>'
        for k in range(4):
            tiles=''.join(f'<div class="tile {"abc"[j]}"><img src="{OUT}/im/t{i}_{j}.jpg"></div>' for j in range(min(k,len(b['tiles']))))
            open(f'{OUT}/ov/b{i}_{k}.html','w').write(f'{css}<body>{base}{tiles}</body>')
    hk=''.join(f'{e(l)}<br>' for l in S['hook']); n=len(S['hook'])
    open(f'{OUT}/ov/hook.html','w').write(CSS.replace('SH','.38').replace('HSpx',f'{660+n*112+30}px')+f'<body><div class=shade></div><div class=hw><div class="t hk">{e(" ".join(S["hook"]))}</div><div class=hs><span>{e(S.get("sub") or "")}</span></div></div></body>')
    et=''.join(f'{e(l)}<br>' for l in S.get('end_text') or ['which sale are you shopping?'])
    open(f'{OUT}/ov/end.html','w').write(CSS.replace('SH','.38').replace('HSpx','0px')+f'<body><div class=shade></div><div class=hw><div class="t hk">{e(S.get("end_q") or "which store should i count next?")}</div></div></body>')
    subprocess.run(['node',B+'/shootpng.js',OUT+'/ov'],check=True)
    segs=[]; marks=[]; t=0
    def seg(bg,ovs,dur,zin=True):
        # ovs: list of (png, start_time); each stays until the next one starts
        f=f'{OUT}/seg/{len(segs):03d}.mp4'; fr=max(2,round(dur*30)); z=f"'1+0.04*on/{fr}'" if zin else f"'1.04-0.04*on/{fr}'"
        cmd=['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-t',str(dur+0.5),'-i',bg]
        for p,_ in ovs: cmd+=['-loop','1','-framerate','30','-t',str(dur+0.5),'-i',p]
        fc=f"[0]scale=iw*3:ih*3:flags=bicubic,zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={PW}x{PH}:fps=30[v0]"
        for k,(p,st) in enumerate(ovs):
            en=ovs[k+1][1] if k+1<len(ovs) else dur+1
            fc+=f";[v{k}][{k+1}]overlay=0:0:enable='between(t,{st},{en-0.001})'[v{k+1}]"
        fc+=f";[v{len(ovs)}]format=yuv420p[o]"
        subprocess.run(cmd+['-filter_complex',fc,'-map','[o]','-frames:v',str(fr),'-r','30','-c:v','libx264','-crf','18',f],check=True); segs.append(f); return fr/30
    marks.append(('hook',0)); each=S.get('hook_dur',3.2)/len(BR)
    for i in range(len(BR)): t+=seg(f'{OUT}/im/bg{i}.jpg',[(f'{OUT}/ov/hook.png',0)],each,i%2==0)
    for i,b in enumerate(BR):
        marks.append((b['brand'],round(t,2)))
        t+=seg(f'{OUT}/im/bg{i}.jpg',[(f'{OUT}/ov/b{i}_0.png',0),(f'{OUT}/ov/b{i}_1.png',0.9),(f'{OUT}/ov/b{i}_2.png',1.5),(f'{OUT}/ov/b{i}_3.png',2.1)],per,i%2==0)
    marks.append(('end',round(t,2))); t+=seg(f'{OUT}/im/bg0.jpg',[(f'{OUT}/ov/end.png',0)],2.6,True)
    open(OUT+'/list.txt','w').write(''.join(f"file '{s}'\n" for s in segs)); final=f'{NS}/roundup-{slug}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',OUT+'/list.txt','-c:v','libx264','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',final],check=True)
    json.dump(dict(marks=marks,duration=round(t,2)),open(f'{OUT}/build.json','w')); print(final,round(t,2),marks); return final
if __name__=='__main__': run(sys.argv[1])
