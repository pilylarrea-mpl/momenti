# Brief: one Black Friday BRAND ROUNDUP video (TikTok, creator voice)

Pily's first video (boots, item by item, magazine styling) flopped. The format that works for deal creators is a BRAND ROUNDUP: "Black Friday sales worth your attention: Abercrombie, 25 to 50% off, but a lot of items really are 50, I already ordered. Staud, 30% sitewide..." One brand every 3 to 5 seconds, each with its discount and ONE honest opinion, product photos popping in. It is about GOOD SALES and good pieces. Never frame anything as "the cheapest" — she hates that.

What Pily has that other creators don't: we crawled every store's full catalog, so she can say how much of the store is REALLY marked down ("the banner says up to 60%, and 54% of the store really is 40% off or more" / "only 4% is").

## Tools (local, free)
```python
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad'); import pick
pick.host('Daze Denim'); pick.share(host)   # instock, marked, ge40, ge50, pct40, pct50, the store's sheet rows (sale text, dates, code, disc) and homepage sale phrases
pick.best(host,min_off=30,n=40)             # best marked-down in-stock items
pick.rows(host); pick.detail(host,handle); pick.info(host); pick.currency(host)
pick.sheet(host,[handles],'name')           # contact sheet jpg -> open it with Read and LOOK
```
Read pick.py's docstring. Catalog data was read Nov 26-27, 2026. Today is Fri Nov 27; the video posts Sat Nov 28.

## Hard rules
- NO paid tools (no Apify, ElevenLabs, Runway, Canva, Windsor MCP tools), no AI image/video/audio generation, no git, post nothing. Network only for pick.sheet photo downloads and, optionally, `curl -sL -A 'Mozilla/5.0' https://<host>/` to re-read a store's homepage banner today.
- Never invent. Every number comes from code you ran. A brand's "claim" must be its own words from the sheet row or homepage phrases; if you have neither, say "sale" without a number.
- Stores where the catalog shows 0% marked down may discount by code or at checkout (e.g. Margaux, Jennifer Behr, Rails, Tatcha): do not say "nothing is on sale". Use the sheet/homepage claim and say "sitewide with code" only if the data says so.
- Drop non-$ stores (pick.currency) and anything whose sale has ended by Nov 28 per the sheet.
- Prefer brands a 25-40 year old woman on TikTok might know or want. 7 to 9 brands per video.
- For each brand choose 4 product photos that look great at phone size: 1 background photo (a model/lifestyle shot, vertical, product clearly visible) + 3 tiles (clean product shots, different items, all really in the sale and in stock). LOOK at them with pick.sheet. Give host, handle and image index (index into pick.rows(host)[i]['img']).
- Writing style: how a real person talks to camera. Short. Specific. Lowercase brand vibe is fine. No "it's not X, it's Y". No triple adjectives. Banned words: elevate, effortless, timeless, staple, obsessed, game-changer, stunning, perfect, must-have, cheapest, cheap, steal, delve, seamless, robust. Honest negatives welcome.

## Deliver
Write `/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/roundup/<slug>.json`:
```json
{"slug":"", "hook":["line 1","line 2"],            // on-screen opening text, max 2 short lines, lowercase ok, like a TikTok caption
 "hook_say":"what she says in the first 4 seconds; a take or a promise, not a greeting",
 "sub":"one small line under the hook, the proof (e.g. 'i counted what's really marked down at 199 stores')",
 "brands":[{"brand":"exact name","host":"","claim":"up to 60% off",   // their words, short
            "stat":"54% of the store is 40% off or more",              // our count, short, <= 44 chars; or a factual note like 'their only sale of the year'
            "say":"one or two spoken sentences: the discount, our count, and one opinion or tip",
            "bg":{"handle":"","img":0}, "tiles":[{"handle":"","img":0},{"handle":"","img":0},{"handle":"","img":0}],
            "code":"", "ends":"2026-12-01", "numbers":{"instock":0,"ge40":0,"ge50":0}}],
 "close_say":"last line + a question that gets comments", "end_text":["2 short lines for the end card"],
 "caption":"2 sentences + question. Must end with: Commissionable links in bio.", "pinned_comment":"",
 "recheck":["what Pily must confirm before posting"], "dropped":["brand: reason"]}
```
Order brands so the strongest is first and the second strongest is last. Validate with `python3 -m json.tool`. Final message to me under 120 words: the hook, the brand list with each stat, doubts.
