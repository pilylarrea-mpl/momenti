# Brief: one Black Friday category video (curation + script)

You are curating ONE category for a TikTok creator (Pily). She read ~376 Black Friday sales (her affiliate sheet); we crawled the full catalogs of the stores. Her video format, which finally worked for boots:
"I read almost 400 sales. Only 3 stores have boots 40% off. 34 boots qualify. My 8 favorites." -> each pick full-screen with price, was-price, % off, and a stock note -> end card with a question.
The value to the viewer is NEW information that is hard to find: how few stores really discount this category, and which specific pieces are worth it (or not). She does hot takes. Nothing cheesy.

## Tools (all local, free)
```python
import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad'); import pick
items,per_store = pick.category(include_regex, exclude_regex, min_off=40, min_price=15)   # every qualifying in-stock item in all core stores
pick.currency(host)      # DROP any store that is not '$'
pick.sheet(host,[handles],'name')   # writes a contact sheet jpg (2 photos per item) -> you MUST open it with the Read tool and look
pick.detail(host,handle) # description, materials, options, per-variant price/original/in-stock
pick.info(host)          # sheet row (sale name, dates, code) + homepage phrases
pick.rows(host)          # full catalog rows: t,h,type,pr,ca,off,av,n,vname,img[],tags,pub
```
Read the docstring at the top of pick.py. Catalog data was read Nov 26-27, 2026.

## Hard rules
- NO paid tools: do not call any Apify, ElevenLabs, Runway, Canva, Windsor MCP tools. No AI image/video/audio generation. No git. Post/send nothing.
- Only network allowed: pick.sheet's photo downloads, and optionally `curl -sL -A 'Mozilla/5.0' https://<host>/products/<handle>.js` to confirm today's price/stock for your final 8 (if it fails, note "not rechecked").
- Never invent facts. Every number in the spec must come from code you ran. Materials/claims only from pick.detail's description.
- Discount = cheapest in-stock variant vs ITS OWN compare_at (pick already does this). Watch for fake anchors (everything in the store "was" the same inflated price, or compare_at on items that never sold at it): drop suspicious stores and say so.
- Your regex will catch junk (e.g. "dress shirt", "bag charm", "earring case", men's, kids). Clean the list by reading titles; fix the regex; report the honest final counts.
- LOOK at photos. Reject bad photos (tiny, cluttered, text-on-image, flat-lay you can't read at phone size), ugly or dated items, and anything you would not tell a friend to buy. Pick things a stylish 25-40 woman would actually want.
- Picks: 8 items, from at least 3 different stores if the category allows, max 3 from one store. Price spread is good (one cheap, one splurge). Each needs >= 2 good photos; give the two best image indexes (index into pick.rows(...)['img'], which holds up to 4).
- Stock note per pick from pick.detail variants, factual and short (<= 28 chars): "Every size in stock", "Only S and M left", "Gold is sold out", "Final sale" (only if the store says so).
- Writing style for all text: plain, specific, how a person talks. No "it's not X, it's Y". No lists of three adjectives. No words like: elevate, effortless, timeless, staple, obsessed, game-changer, stunning, perfect, must-have, delve, seamless, robust. Short sentences. Honest negatives welcome ("runs small", "the silver one is the ugly one").

## What to deliver
Write `/tmp/claude-0/-home-user-momenti/f8db058d-6b86-53e9-be25-77324683de3f/scratchpad/tomorrow/<slug>.json`:
```json
{
 "slug": "coats", "label": "Coats",                  // label is shown as "Black Friday · Coats"
 "noun": "coats",                                    // used in "N stores have <noun> 40% off"
 "threshold": 40,                                    // the % bar you used (40 or 50; choose the one that makes the sharper honest finding)
 "include": "...", "exclude": "...",                 // final regexes
 "stores_total": 12, "items_total": 96,              // after cleaning + dropping non-$ and suspicious stores
 "per_store": {"Marcella": 22, "...": 0},            // cleaned counts
 "finding": "one sentence: the hard-to-find fact, with numbers (e.g. 'Half of all the coats at 50% off sit in two stores.')",
 "hook_lines": [["Only 12 stores",true],["have coats",false],["40% off.",false]],   // 2-3 short lines for the opening card, true = highlighted line
 "keep_stores": ["A","B","C"],                       // 3 to 5 store names (exact brand names from pick.B) to show as "the stores that had them" - the ones your picks come from first
 "candidates": [ {"host":"","handle":"","brand":"","name":"short name <=30 chars","imgs":[0,1]} ],   // 24 to 36 items that passed your photo review, for the mosaic and for Pily's picker page. Include the 8 picks.
 "picks": [ {"host":"","handle":"","brand":"","name":"<=26 chars","imgs":[0,2],"now":0,"was":0,"off":0,"chip":"Every size in stock",
             "say":"what Pily says over this item, one or two spoken sentences, a real reason or a hot take",
             "why":"", "for_who":"", "skip_if":"", "live":"rechecked 2026-11-27 ok | not rechecked"} ],   // exactly 8, ordered for the video (strong first, best last)
 "script": {"open":"3 spoken sentences max: I read almost 400 Black Friday sales + the finding + 'my eight favorites'", "close":"one line + a question for comments", "tease":"what category she might do next"},
 "hooks_alt": ["2 alternative first lines"],
 "caption": "2 sentences + a question. Must end with: Commissionable links in bio.",
 "pinned_comment": "", 
 "recheck": ["things Pily must confirm before posting"],
 "dropped": ["store or item: reason"]
}
```
Validate with `python3 -m json.tool`. Prices as numbers. Before finishing, make one final contact sheet of your 8 picks (`pick.sheet` per store is fine) and look at it once more: would this make someone stop scrolling and send it to a friend? If not, swap picks.

Your final message to me: under 150 words. The finding, the 8 picks (brand, name, price, % off), and anything I must know (dropped stores, doubts). No file dumps.
