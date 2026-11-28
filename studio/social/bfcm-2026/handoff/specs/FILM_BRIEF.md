# Brief: one TikTok video cut from brands' own product footage, MOMENTI brand-book look

Pily posts Black Friday sale videos. What works for her now: real moving footage from the brands' own product pages, MOMENTI brand-book typography over it, her voice on top. Her last message: "I'd love to highlight specific and cool pieces so people are actually getting cool information." So name real pieces, with real prices. It is about good sales and good pieces; never frame anything as "the cheapest".

Read and look at a finished example first:
- spec: /tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/roundup/film-jewelry.json
- frames: /tmp/claude-0/-home-user/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/film/strip-jewelry-film.jpg  (open with Read)

## Tools (all local and free)
```python
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad'); sys.path.insert(0,'/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/build')
import pick, vid
pick.host('Brand'); pick.rows(host); pick.best(host,min_off=30,n=40); pick.detail(host,handle); pick.share(host)   # catalog read Nov 26-27: price now (pr), original (ca), % off, sizes in stock (av of n), sheet rows with sale text / code / end date
vid.find(host,[handles]) ; vid.get(url,'name',sub='<your slug>') ; vid.sheet([paths],'name')   # product videos; ALWAYS look at the sheet
```
/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/roundup/allvideos.json lists which brands had product videos on their 10 top products (a start; use vid.find on more handles).
Render: `cd /tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad && PYTHONPATH=. python3 build/film.py roundup/<your-slug>.json` -> film/<slug>.mp4, then `cd /tmp/claude-0/-home-user/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/film && python3 strip.py <slug>` -> strip-<slug>.jpg. Open the strip with Read and fix what looks wrong. Then compress for phone: `ffmpeg -v error -y -i <slug>.mp4 -c:v libx264 -preset slow -b:v 7M -maxrate 9M -bufsize 14M -pix_fmt yuv420p -movflags +faststart <slug>-final.mp4`.

## Spec format (film.py)
```json
{"slug":"x","tag":"Black Friday","per":4.0,
 "hook":{"caps":"Three or four words.","per":9,"fact":"one small caps line, a fact","dry":"Six words or fewer.","dur":2.6,"clips":[{"f":"sub/a.mp4","ss":1.0}]},
 "brands":[
   {"brand":"Brand Name","facts":["Says 30% off sitewide","20% of the store is half off or more","Ends Dec 7"],"dry":"A fifth is half off.","clips":[{"f":"sub/b.mp4","ss":2},{"f":"sub/c.mp4","ss":1}]},
   {"brand":"Brand Name","piece":"The Gaze Choker.","facts":["Was $110 · now $44","60% off · final sale","Ends Dec 1"],"dry":"Gold, not shy.","clips":[...]}   // "piece" switches to piece mode: brand in the small label, piece name large in Bodoni; use <i>..</i> inside piece for an italic word
 ],
 "end":{"caps":"Which store next?","dry":"I’ll count it.","dur":2.6,"clips":[{"f":"sub/a.mp4","ss":3}]}}
```
Each clip plays from "ss" for (dur / number of clips) seconds: make sure ss + that length is shorter than the clip. Optional per clip: "x","y" 0..1 crop position (default 0.5), per brand "dur" seconds.

## Hard rules
- NO paid tools (no Apify, ElevenLabs, Runway, Canva, Windsor MCP tools), no AI image/video/audio generation, no git, post nothing. Network: only curl to the brands' own sites via vid/pick helpers.
- Never invent. Prices, % off and stock from pick (per-variant, already correct). Sale claim, code and end date from pick.share(host)['sheet'] / homepage phrases. Materials only from pick.detail. If you can't verify, leave it out.
- A piece shown in piece mode must be the product the video belongs to (vid.find gives the handle), in stock, and really marked down in pick.rows (or discounted by a sitewide code you can cite: then write "25% off with code X", no invented now-price).
- Footage: beautiful, calm, product clearly visible. Reject clips with baked-in captions/text, split screens, green screen, UGC talking heads, lingerie/swim close-ups, children. Vertical clips preferred; square is ok (it gets cropped to 9:16, so the subject must sit in the middle third).
- Brand book copy rules: ivory and ink only (the renderer handles it). Cover caps end with a full stop. ONE dry line per item, six words or fewer, dry with a wink, a true fact, never explains the joke. No exclamation marks, no emoji, no hype. Banned words: iconic, timeless, nostalgia, elevate, curated, luxury, heirloom, journey, discover, shop now, vibes, must-have, obsessed, magic, elegant, effortless, bespoke, cherish, limited, exclusive, cheap, cheapest, steal, perfect, stunning.
- Facts lines: max 3 per item, each <= 36 characters, the last one is the end date ("Ends Dec 1") or "Final sale · ends Dec 1".
- Length 25 to 40 seconds silent draft (her voice will stretch it).

## Deliver
1. film/<slug>-final.mp4 rendered and its strip checked by eye.
2. /tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/roundup/<slug>.script.json: {"say":["hook line", "one entry per item: what Pily says, first person, plain, 1-2 short sentences, includes 'good for ...' and the end date", "closing question"], "caption":"full caption listing every item with numbers, code and end date; ends with: Commissionable links in bio.", "recheck":["what she must confirm before posting"]}
Final message to me under 120 words: the item list with prices, and doubts. No file dumps.
