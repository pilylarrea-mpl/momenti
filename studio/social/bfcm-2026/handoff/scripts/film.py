"""Roundup cut from the brands' own moving footage, brand-book overlays (ivory caps with a full stop, facts in tracked caps, one dry line in Bodoni italic), soft grain.
usage: python3 film.py <spec.json>"""
import sys,os,json,shutil,subprocess,html
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import roundup_m as M
e=html.escape; FD='/tmp/claude-0/-home-user/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/film'; B=M.B
def run(spec):
    S=json.load(open(spec)); OUT=f'{FD}/{S["slug"]}'; shutil.rmtree(OUT,ignore_errors=True)
    for d in ('ov','seg'): os.makedirs(f'{OUT}/{d}')
    tag=S.get('tag','Black Friday'); BR=S['brands']
    def page(top,dry): return f'{M.CSS}<body><div class=sh></div><div class=top>{top}</div><div class=dry>{e(dry or "")}</div></body>'
    for i,b in enumerate(BR):
        facts='<br>'.join(e(x) for x in b['facts']); fs=34 if max(len(x) for x in b['facts'])<=36 else 30
        # piece mode: the brand goes in the label, the piece name is set in Bodoni like a bag name in the brand book
        if b.get('big'):
            # cover look: the deal is the headline in Bodoni italic, brand small on top, deadline in bold caps under a thin rule
            n,u=b['big']; nfs=400 if len(n)<=2 else (330 if len(n)<=3 else 250)
            ECSS=M.CSS+'''<style>.lbx{position:absolute;left:60px;top:262px;font-weight:800;font-size:58px;letter-spacing:.02em;text-transform:uppercase;color:#F4F0E8;text-shadow:0 1px 14px rgba(0,0,0,.45)}
.blk{position:absolute;left:60px;right:140px;bottom:388px;color:#F4F0E8;text-shadow:0 2px 30px rgba(28,26,24,.5)}
.num{font-family:'BM';font-style:italic;line-height:.8;letter-spacing:-.04em;margin-left:-14px;white-space:nowrap}
.rule{height:2px;background:#F4F0E8;margin:20px 0 18px;box-shadow:0 1px 10px rgba(0,0,0,.3)}
.cp{font-weight:700;font-size:31px;letter-spacing:.18em;text-transform:uppercase}
.dl{font-weight:800;font-size:46px;letter-spacing:.1em;text-transform:uppercase;margin-top:10px}
.shx{position:absolute;inset:0;background:linear-gradient(180deg,rgba(28,26,24,.36),rgba(28,26,24,0) 24%,rgba(28,26,24,0) 48%,rgba(28,26,24,.66) 84%)}</style>'''
            def pg(show): return ECSS+f'<body><div class=shx></div><div class=lbx>{e(b["brand"])}</div><div class=blk><div class=num style="font-size:{nfs}px">{e(n)}<span style="font-size:{int(nfs*0.38)}px;letter-spacing:-.02em">{e(u)}</span></div><div class=rule></div><div class=cp>{e(b.get("what",""))}</div><div class=dl style="visibility:{"visible" if show else "hidden"}">{e(b.get("deadline",""))}</div></div></body>'
            open(f'{OUT}/ov/b{i}_0.html','w').write(pg(False)); open(f'{OUT}/ov/b{i}_1.html','w').write(pg(True)); continue
        if b.get('piece'):
            pn=b['piece']; pfs=104 if len(pn)<=18 else (88 if len(pn)<=26 else 72)
            top=f'<div class=lb>{e(b["brand"])} · {i+1:02d} / {len(BR):02d}</div><div class=pc style="font-size:{pfs}px">{pn}</div><div class=ft style="font-size:{fs}px">{facts}</div>'
        else:
            top=f'<div class=lb>{e(tag)} · {i+1:02d} / {len(BR):02d}</div>{M.caps(b["brand"]+".")}<div class=ft style="font-size:{fs}px">{facts}</div>'
        open(f'{OUT}/ov/b{i}_0.html','w').write(page(top,'')); open(f'{OUT}/ov/b{i}_1.html','w').write(page(top,b.get('dry')))
    hk=S['hook']; top=f'<div class=lb>{e(tag)}</div>{M.caps(hk["caps"],per=hk.get("per",9))}<div class=ft style="font-size:32px">{e(hk.get("fact",""))}</div>'
    open(f'{OUT}/ov/hook.html','w').write(page(top,hk.get('dry')))
    en=S['end']; top=f'<div class=lb>{e(tag)}</div>{M.caps(en["caps"],per=9)}'
    open(f'{OUT}/ov/end.html','w').write(page(top,en.get('dry')))
    subprocess.run(['node',B+'/shootpng.js',OUT+'/ov'],check=True)
    segs=[]; marks=[]; t=0
    def seg(clip,ss,dur,ovs,speed=1.0,xpos=0.5,ypos=0.5):
        f=f'{OUT}/seg/{len(segs):03d}.mp4'; fr=round(dur*30)
        cmd=['ffmpeg','-v','error','-y','-ss',str(ss),'-i',f'{FD}/{clip}']
        for p,_ in ovs: cmd+=['-loop','1','-framerate','30','-t',str(dur+0.5),'-i',p]
        fc=(f"[0]setpts={1/speed}*PTS,fps=30,scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop=1080:1920:(iw-1080)*{xpos}:(ih-1920)*{ypos},eq=saturation=1.04,noise=alls=6:allf=t,setsar=1[v0]")
        for k,(p,st) in enumerate(ovs):
            en2=ovs[k+1][1] if k+1<len(ovs) else dur+1
            fc+=f";[v{k}][{k+1}]overlay=0:0:enable='between(t,{st},{en2-0.001})'[v{k+1}]"
        fc+=f";[v{len(ovs)}]format=yuv420p[o]"
        subprocess.run(cmd+['-filter_complex',fc,'-map','[o]','-frames:v',str(fr),'-r','30','-an','-c:v','libx264','-crf','18',f],check=True); segs.append(f); return fr/30
    def shots(clips,total,ov_first,ov_rest_fn):
        nonlocal t
        each=total/len(clips)
        for j,c in enumerate(clips):
            ovs=ov_first if j==0 else ov_rest_fn()
            t+=seg(c['f'],c.get('ss',0.4),each,ovs,c.get('speed',1.0),c.get('x',0.5),c.get('y',0.5))
    marks.append(('hook',0)); H=f'{OUT}/ov/hook.png'
    if hk.get('dur',2.6)>=0.3: shots(hk['clips'],hk.get('dur',2.6),[(H,0)],lambda:[(H,0)])
    for i,b in enumerate(BR):
        marks.append((b['brand'],round(t,2))); d=b.get('dur',S.get('per',3.8)); a,c=f'{OUT}/ov/b{i}_0.png',f'{OUT}/ov/b{i}_1.png'
        shots(b['clips'],d,[(a,0),(c,0.6 if b.get('big') else min(1.0,d/len(b['clips'])-0.1))] if (len(b['clips'])==1 or b.get('big')) else [(a,0)],lambda:[(c,0)])
    marks.append(('end',round(t,2))); E_=f'{OUT}/ov/end.png'; shots(en['clips'],en.get('dur',2.6),[(E_,0)],lambda:[(E_,0)])
    open(OUT+'/list.txt','w').write(''.join(f"file '{s}'\n" for s in segs)); final=f'{FD}/{S["slug"]}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',OUT+'/list.txt','-c:v','libx264','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',final],check=True)
    json.dump(dict(marks=marks,duration=round(t,2)),open(f'{OUT}/build.json','w')); print(final,round(t,2),marks); return final
if __name__=='__main__': run(sys.argv[1])
