"""Picker page per category from tomorrow/<slug>/pick/items.json, using the boots page as the template."""
import sys,json,html,re
NS='/tmp/claude-0/-home-user/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/tomorrow'
T=open('/tmp/claude-0/-home-user/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/bootpick/index.html').read()
def run(spec):
    S=json.load(open(spec)); slug=S['slug']; C=json.load(open(f'{NS}/{slug}/pick/items.json')); e=html.escape
    head=T[:T.index('<div class="w">')]; tail=T[T.index('<div class="bar">'):]
    m=lambda x:f'${x:,.0f}' if abs(x-round(x))<.005 else f'${x:,.2f}'
    cards=''
    for c in sorted(C,key=lambda c:(not c['pick'],c['now'])):
        im=c['imgs']+c['imgs'][:1]
        cards+=f'<label class="card" for="c{c["id"]}"><input type="checkbox" id="c{c["id"]}" {"checked" if c["pick"] else ""} data-name="{e(c["brand"])} — {e(c["name"])}" data-h="{e(c["handle"])}"><div class="ph"><img loading="lazy" alt="{e(c["name"])}" src="{im[0]}"><img loading="lazy" alt="" src="{im[1]}"></div><div class="tx"><div class="br">{e(c["brand"])}</div><div class="nm">{e(c["name"])}</div><div class="pr"><b>{m(c["now"])}</b> <s>{m(c["was"])}</s> <span>{c["off"]}% off</span></div><div class="st">{c["av"]} of {c["n"]} sizes or colors in stock{" · my default pick" if c["pick"] else ""}</div></div><span class="tick" aria-hidden="true">✓</span></label>'
    body=f'<div class="w">\n<div class="lab">Black Friday · {e(S["label"])}</div>\n<h1>Pick the {e(S["noun"])} you like</h1>\n<p>{e(S["finding"])} These {len(C)} passed a photo check out of {S["items_total"]} at {S["threshold"]}% off or more. The eight ticked ones are in the draft video. Untick what you don’t like, tick what you do, then tap Copy and paste the list to me in chat.</p>\n<div class="g">{cards}</div>\n</div>\n'
    page=(head+body+tail).replace('<title>Boot Picks</title>',f'<title>{e(S["label"])} Picks</title>').replace("'bootpicks'",f"'picks-{slug}-v1'").replace('My boot picks:',f'My {S["label"].lower()} picks:')
    # default ticks must survive first load: only restore saved state when there is one
    page=page.replace("try{(JSON.parse(localStorage.getItem('picks-%s-v1')||'[]')).forEach(id=>{const el=document.getElementById(id);if(el)el.checked=true})}catch(e){}"%slug,
      "try{const s=localStorage.getItem('picks-%s-v1');if(s){const k=JSON.parse(s);document.querySelectorAll('.card input').forEach(x=>x.checked=k.includes(x.id))}}catch(e){}"%slug)
    open(f'{NS}/{slug}/pick/index.html','w').write(page); print(f'{NS}/{slug}/pick/index.html',len(C))
if __name__=='__main__': run(sys.argv[1])
