import json,os,shutil,html
SP='/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/roundup/'; NS='/tmp/claude-0/-home-user/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/roundup/'
site=NS+'site'; shutil.rmtree(site,ignore_errors=True); os.makedirs(site+'/v'); e=html.escape
plan=[('actually-good','Sat 9 am','Sales that are really good'),('lost-the-plot','Sat 12 pm','“Up to” sales, counted'),('shoe-sales','Sat 3 pm','Shoe sales'),('once-a-year','Sat 6 pm','Brands that rarely go on sale'),('jewelry-sales','Sat 9 pm','Jewelry sales'),('denim-sales','Sun 11 am','Denim sales'),('home-sales','Sun 7 pm','Home and bedding sales')]
secs='';nav=''
for slug,when,label in plan:
    S=json.load(open(SP+slug+'.json')); Bd=json.load(open(NS+slug+'/build.json')); shutil.copy(NS+f'roundup-{slug}.mp4',site+f'/v/{slug}.mp4')
    rows=''.join(f'<li><b>{e(b["brand"])}</b> <span class=pr>{e(b.get("claim") or "")} · {e(b["stat"])}{" · code "+e(b["code"]) if b.get("code") else ""}</span><p>{e(b["say"])}</p></li>' for b in S['brands'])
    rc=''.join(f'<li>{e(x)}</li>' for x in S.get('recheck',[]))
    nav+=f'<a href="#{slug}">{e(when)} · {e(label)}</a>'
    secs+=f'''<section id="{slug}"><div class=lab>{e(when)} · {e(label)}</div><h2>{e(" ".join(S["hook"]))}</h2>
<div class=two><div><video controls playsinline preload="metadata" src="v/{slug}.mp4"></video><p class=note>{Bd["duration"]:.0f} seconds, {len(S["brands"])} brands, silent draft.</p></div>
<div><h3>Say this</h3><p class=say>{e(S["hook_say"])}</p><ol>{rows}</ol><p class=say>{e(S["close_say"])}</p>
<h3>Caption</h3><p class=cap>{e(S["caption"])}</p><h3>Pin this comment</h3><p class=cap>{e(S.get("pinned_comment") or "")}</p>
<details><summary>Check before posting ({len(S.get("recheck",[]))})</summary><ul>{rc}</ul></details></div></div></section>'''
css=open('/tmp/claude-0/-home-user/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/tomorrow/site/index.html').read(); css=css[css.index('<style>'):css.index('</style>')+8]
page=f'''<title>Sale Roundups</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;1,6..96,400&family=Inter+Tight:wght@500;700&family=Newsreader:ital,opsz@0,6..72;1,6..72&display=swap">
{css}
<div class="w">
<div class="lab">New direction after the boots video</div>
<h1>Seven brand roundups</h1>
<p class="lede">The boots video went item by item, slowly, in magazine styling. The two creator videos you sent do the opposite: one brand every few seconds, the discount, one opinion, plain TikTok text, product photos popping in. These seven follow that format. Each brand shows the store’s own claim and then your count of how much of the store is really marked down, which no other creator has.</p>
<p class="lede">How to finish one: read the lines under “Say this” into a voice memo and send it to me, and I cut the video to your voice. Stronger still: film yourself saying it to camera, the way both of those creators do, and I put the brand names and product photos around you.</p>
<p class="lede">Counts come from each store’s full catalog, read November 26 and 27. Stores blocked a fresh read of their homepages today, so open each sale before you post and confirm the banner still says what the video says.</p>
<nav>{nav}</nav>
{secs}
</div>'''
open(site+'/index.html','w').write(page); print(sum(len(f) for _,_,f in os.walk(site)),'files')
