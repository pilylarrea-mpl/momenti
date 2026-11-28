"""Brand roundup, Momenti look per Pily's picks: full-screen photo, bold caps in ivory, rust count box, Newsreader italic claim, photo cards popping in. No ivory backgrounds.
usage: python3 roundup_m.py <spec.json>"""
import sys,os,json,shutil,subprocess,html
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import roundup as R
from roundup import cover,tile,img,NS,B,PW,PH
e=html.escape; F='/home/user/momenti/assets/fonts'
CSS=f'''<style>
@font-face{{font-family:'IT';src:url('{F}/InterTight-VF.ttf');font-weight:100 900}}
@font-face{{font-family:'BM';src:url('{F}/BodoniModa-Italic-VF.ttf');font-weight:400 900;font-style:italic}}
@font-face{{font-family:'BM';src:url('{F}/BodoniModa-VF.ttf');font-weight:400 900;font-style:normal}}
.pc{{font-family:'BM';font-weight:400;font-size:104px;line-height:.98;letter-spacing:-.02em;margin:16px 0 20px -2px}}.pc i{{font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}} html,body{{width:1080px;height:1920px;background:transparent;font-family:'IT';overflow:hidden}}
:root{{--iv:#F4F0E8;--ink:#1C1A18}}
/* brand book: ivory and ink only, cover caps huge with a full stop, one dry line in Bodoni italic, labels in tracked caps, a soft scrim and never a shape */
.sh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(28,26,24,.50),rgba(28,26,24,.22) 24%,rgba(28,26,24,0) 40%,rgba(28,26,24,0) 60%,rgba(28,26,24,.42) 80%,rgba(28,26,24,.58))}}
.top{{position:absolute;left:60px;right:140px;top:262px;color:var(--iv);text-shadow:0 2px 26px rgba(28,26,24,.35)}}
.lb{{font-weight:700;font-size:28px;letter-spacing:.08em;text-transform:uppercase}}
.nm{{font-weight:800;line-height:.88;letter-spacing:-.035em;text-transform:uppercase;margin:14px 0 18px -4px}}
.ft{{font-weight:700;letter-spacing:.08em;text-transform:uppercase;line-height:1.3}}
.dry{{position:absolute;left:60px;right:140px;bottom:388px;color:var(--iv);font-family:'BM';font-style:italic;font-weight:500;font-size:86px;line-height:1.02;letter-spacing:-.01em;text-shadow:0 2px 24px rgba(28,26,24,.45)}}
.tile{{position:absolute;top:1010px;width:281px;height:368px;overflow:hidden;background:var(--iv)}}
.tile img{{width:100%;height:100%;object-fit:cover}}
.bn{{font-weight:800;font-size:54px;letter-spacing:-.01em;text-transform:uppercase;margin-top:10px}}
.key{{font-weight:800;line-height:.86;letter-spacing:-.04em;text-transform:uppercase;margin:6px 0 16px -5px}}
.flag{{display:inline-block;background:var(--iv);color:var(--ink);font-weight:800;font-size:40px;letter-spacing:.04em;text-transform:uppercase;padding:12px 18px 10px;text-shadow:none}}
.sm{{font-weight:700;font-size:28px;letter-spacing:.08em;text-transform:uppercase;margin-top:14px}}
.a{{left:60px}}.b{{left:349px}}.c{{left:638px}}
.hsh{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(28,26,24,.66),rgba(28,26,24,.34) 34%,rgba(28,26,24,.10) 55%,rgba(28,26,24,.60))}}
</style>'''
def caps(text,maxfs=176,width=880,per=10):
    w=text.upper().split(); lines=[]
    for x in w:
        if lines and len(lines[-1])+1+len(x)<=per: lines[-1]+=' '+x
        else: lines.append(x)
    lines=lines[:4]; m=max(len(l) for l in lines); fs=min(maxfs,int(width/(0.585*m)))
    return f'<div class=nm style="font-size:{fs}px">'+'<br>'.join(e(l) for l in lines)+'</div>'
def run(spec,per=4.0):
    S=json.load(open(spec)); slug=S['slug']+'-m'; OUT=f'{NS}/{slug}'; shutil.rmtree(OUT,ignore_errors=True)
    for d in ('ov','seg','im'): os.makedirs(f'{OUT}/{d}')
    BR=S['brands']; tag=S.get('tag') or 'Black Friday'
    for i,b in enumerate(BR):
        cover(img(b['host'],b['bg']),f'{OUT}/im/bg{i}.jpg')
        nt=min(3,len(b['tiles']),b.get('ntiles',3))
        for j,t in enumerate(b['tiles'][:nt]): tile(img(b['host'],t),f'{OUT}/im/t{i}_{j}.jpg')
        st=b['stat']; sfs=34 if len(st)<=36 else 30
        cl=('Says '+b['claim']) if b.get('claim') else ''
        if b.get('key'):
            # emphasis layout: the deal is the biggest thing on screen, the deadline sits in a solid ivory tag
            kl=b['key'].upper().split('|'); m=max(len(x) for x in kl); kfs=min(230,int(880/(0.60*m)))
            base=f'<div class=sh></div><div class=top><div class=lb>{e(tag)} · {i+1:02d} / {len(BR):02d}</div><div class=bn>{e(b["brand"])}</div><div class=key style="font-size:{kfs}px">'+'<br>'.join(e(x) for x in kl)+f'</div>'+(f'<div class=flag>{e(b["flag"])}</div>' if b.get('flag') else '')+(f'<div class=sm>{e(b["small"])}</div>' if b.get('small') else '')+'</div>'
            for k in range(4):
                tiles=''.join(f'<div class="tile {"abc"[j]}" style="top:1090px"><img src="{OUT}/im/t{i}_{j}.jpg"></div>' for j in range(min(k,nt)))
                open(f'{OUT}/ov/b{i}_{k}.html','w').write(f'{CSS}<body>{base}{tiles}</body>')
            continue
        base=f'<div class=sh></div><div class=top><div class=lb>{e(tag)} · {i+1:02d} / {len(BR):02d}</div>{caps(b["brand"].rstrip(".")+".")}<div class=ft style="font-size:{sfs}px">{e(cl)}<br>{e(st)}</div></div><div class=dry>{e(b.get("dry") or "")}</div>'
        for k in range(4):
            tiles=''.join(f'<div class="tile {"abc"[j]}"><img src="{OUT}/im/t{i}_{j}.jpg"></div>' for j in range(min(k,nt)))
            open(f'{OUT}/ov/b{i}_{k}.html','w').write(f'{CSS}<body>{base}{tiles}</body>')
    hk=S.get('hook_caps') or ' '.join(S['hook'])
    open(f'{OUT}/ov/hook.html','w').write(f'{CSS}<body><div class=hsh></div><div class=top><div class=lb>{e(tag)}</div>{caps(hk,per=S.get("hook_per",9))}<div class=ft style="font-size:32px">{e(S.get("hook_fact") or "")}</div></div><div class=dry>{e(S.get("hook_dry") or "")}</div></body>')
    open(f'{OUT}/ov/end.html','w').write(f'{CSS}<body><div class=hsh></div><div class=top><div class=lb>{e(tag)}</div>{caps(S.get("end_caps") or "Which store next?",per=9)}</div><div class=dry>{e(S.get("end_dry") or "")}</div></body>')
    subprocess.run(['node',B+'/shootpng.js',OUT+'/ov'],check=True)
    segs=[]; marks=[]; t=0
    def seg(bg,ovs,dur,zin=True):
        f=f'{OUT}/seg/{len(segs):03d}.mp4'; fr=max(2,round(dur*30)); z=f"'1+0.04*on/{fr}'" if zin else f"'1.04-0.04*on/{fr}'"
        cmd=['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-t',str(dur+0.5),'-i',bg]
        for p,_ in ovs: cmd+=['-loop','1','-framerate','30','-t',str(dur+0.5),'-i',p]
        fc=f"[0]scale=iw*3:ih*3:flags=bicubic,zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={PW}x{PH}:fps=30[v0]"
        for k,(p,st) in enumerate(ovs):
            en=ovs[k+1][1] if k+1<len(ovs) else dur+1
            fc+=f";[v{k}][{k+1}]overlay=0:0:enable='between(t,{st},{en-0.001})'[v{k+1}]"
        fc+=f";[v{len(ovs)}]format=yuv420p[o]"
        subprocess.run(cmd+['-filter_complex',fc,'-map','[o]','-frames:v',str(fr),'-r','30','-c:v','libx264','-crf','18',f],check=True); segs.append(f); return fr/30
    D=S.get('durs') or {}
    marks.append(('hook',0)); hd=D.get('hook',2.2); n=min(len(BR),4)
    for i in range(n): t+=seg(f'{OUT}/im/bg{i}.jpg',[(f'{OUT}/ov/hook.png',0)],hd/n,i%2==0)
    for i,b in enumerate(BR):
        marks.append((b['brand'],round(t,2))); d=D.get(b['brand'],per); s1=min(0.8,d*0.2); gap=min(0.55,d*0.14)
        t+=seg(f'{OUT}/im/bg{i}.jpg',[(f'{OUT}/ov/b{i}_0.png',0),(f'{OUT}/ov/b{i}_1.png',s1),(f'{OUT}/ov/b{i}_2.png',s1+gap),(f'{OUT}/ov/b{i}_3.png',s1+2*gap)],d,i%2==0)
    marks.append(('end',round(t,2))); t+=seg(f'{OUT}/im/bg0.jpg',[(f'{OUT}/ov/end.png',0)],D.get('end',2.4),True)
    open(OUT+'/list.txt','w').write(''.join(f"file '{s}'\n" for s in segs)); final=f'{NS}/{slug}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',OUT+'/list.txt','-c:v','libx264','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',final],check=True)
    json.dump(dict(marks=marks,duration=round(t,2)),open(f'{OUT}/build.json','w')); print(final,round(t,2)); return final
if __name__=='__main__': run(sys.argv[1])
