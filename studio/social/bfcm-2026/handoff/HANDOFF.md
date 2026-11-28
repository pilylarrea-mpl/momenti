# Handoff: Pily's Black Friday TikTok (as of Sat Nov 28, 2026)

Read this whole file before doing anything. It is the state of a long cloud session, written so a new session on Pily's Mac can continue without redoing work.

## Who and what

- **Pily** runs MOMENTI (a handbag house; brand book in this repo and on her Mac). She is posting on TikTok as a **creator**, not as MOMENTI: videos about Black Friday / Cyber Monday sales. The posts never mention her own bags.
- **Goal: followers and TikTok presence.** Affiliate sales are a bonus. She has **no ShopMy account**. The sheet of sales (376 rows, `data/bfcm.csv`) is her **sister's** ShopMy sheet. Captions must not say "commissionable links in bio" unless her sister's links are actually in her bio; then the line is "Links in bio are affiliate links."
- Sales mostly end **Dec 1**. Today is Nov 28. Time matters.
- She just had wisdom teeth removed: **no on-camera for now**. Voice memos are fine.

## What has been posted and how it did

| Video | Views | Avg watch | Note |
|---|---|---|---|
| Boots (dark countdown opening, item by item) | 320 | 4.4s | most left at 0:01 |
| Sales worth opening, short (brand footage + caps title, her voice) | 82 | 2.3s | most left at 0:01 |
| Ends tonight (full-screen photos + big italic number) | 100 | 1.5s | most left at 0:01, 0% finished |
| Jewelry punchy (34s, her voice sped 20%) | sent to her Nov 28; unknown if posted | | same kind of opening |

98% of views come from For You, 100% non-followers. Audience on the latest: 82% women, 52% aged 25–34.

**Conclusion (firm): any video that opens on a brand photo or brand footage with a headline over it dies in the first second. It reads as an ad. Do not make another one in that style, however pretty.** Many hours went into restyling that format (Momenti type, tags, colours, "cover" look); none of it changed the result.

## What she has told us she wants (her words, paraphrased closely)

- Fast. "People have short attention spans." "Nobody likes to watch while it's boring."
- Useful and specific: real pieces, real prices, codes and end dates in the caption.
- Three things she cares about: (1) great deals on things she'd love, (2) cool products she didn't know she needed, (3) **being deinfluenced** ("everyone supposedly loves Rhode, I think that's just marketing").
- It has to be **more niche than "great deals."** This is the open decision (below).
- She must **approve the pieces before a video is built** ("I don't want to show ugly dresses"). She rejected all 12 Marea/Wild Rose prairie-floral dresses with "none". Her earlier boot picks were sleek and bold (patent heeled boot, red kitten-heel boot, suede knee boots).
- Visual taste: MOMENTI brand book. She disliked boxes, tags, product-tile grids, ivory backgrounds ("looks like a PDF"). She said the big-italic-number look ("E") "isn't bad". She asked for "cool and aesthetically pleasing" and has not yet reacted to three concept sketches (`sheets/three.jpg`: 1 contact sheet with red pencil, 2 the pair, 3 the ticket).
- Make her part tiny and put it in front of her: one numbered image, "reply with numbers." She gets lost when several things are open at once. One ask per message.
- Sound: no synthetic or generated sound effects, ever. Music is added in TikTok (she has been using a "Nicole Kidman instrumental"). Her voice: do not process it beyond trimming pauses, levelling, and a mild speed-up she okayed ("you can put it in fast forward"); earlier heavy processing made it "wack".
- She said: "you can cut out. It's not like you have to say everything I say." Cut her memos down to the punchy parts.

## Hard rules

- **Never spend paid credits** (Apify, ElevenLabs, Runway, Canva generation, etc.) without describing it, quoting the cost and getting her yes. No AI-generated footage or voices.
- **Nothing is posted, sent or bought without her.** She posts herself.
- **Never invent a fact.** Every price, percent, code and end date must come from the catalog data or from the live store page, and be re-checked on the live page the day it posts.
- **Check the live sites yourself**; do not ask her to. On Nov 27 the sheet was wrong on 3 of 6 stores (alice + olivia was 30% "today only", not 25%; Rothy's clog deal ended that night, not Saturday; Social Threads showed no sale).
- Never frame anything as "the cheapest". It is about good sales and good pieces.
- Writing style for anything she reads or says: plain, specific, no "it's not X, it's Y", no lists of three adjectives, no hype words. MOMENTI's banned words apply to on-screen copy: iconic, timeless, elevate, curated, luxury, must-have, obsessed, effortless, elegant, exclusive, limited, etc.
- Git: work on branch `claude/brave-johnson-4hmud5`. No pull request unless she asks. No model names in commits.

## The open decision: the niche

Three options were put to her; she has not answered:

- **A · The sale auditor**: "I count what's really on sale." Banner versus reality, with counts.
- **B · Accessories only**: bags, shoes, jewelry worth owning, and the ones that aren't. Builds MOMENTI's future audience.
- **C · Brands you haven't heard of.**

Recommendation given: **B done A's way** (accessories only, with receipts). Get her answer first; everything else follows from it.

## The format to test next: "Price check" (screen recording)

The one format not yet posted. A test exists: `videos/screenrec-dresses.mp4` (15s).

- A Playwright recording of the **real product page** on a phone-sized viewport (430×764), closing pop-ups the way a person would, scrolling to the price, then a zoom into the crossed-out price. Script: `scripts/rec2.js` (note: the recorded file only fills the top-left quarter; crop `iw/2:ih/2:0:0` before scaling).
- Plain TikTok-style captions (TikTok Sans, `fonts/TikTokSans.woff2`), first frame is a price: "this dress was $328. it's $68 right now."
- Her voice from the first frame, one line per piece, 15–20 seconds, three pieces.
- Recording the page also re-verifies price and stock that hour. It caught: the $68 Marea dress had only XL left and an extra code JOY30; Alexandra Miro showed VAT-inclusive prices to a non-US IP (do not quote those from a cloud machine; on her Mac in Puerto Rico the US prices should show).

**Decision rule agreed with her:** post two in this format. If average watch time is above ~5s, run the set. If still ~2s, the next test is her on camera once she has healed (both reference creators she sent open on their face, talking).

On her Mac there is a better version of this available: she can screen-record her own phone, or the Mac session can drive her real browser.

## Planned set (rewrite once the niche is chosen)

Three video types from her three cares: **Worth it** (deals on things she loves), **Found it** (things she didn't know she needed), **Skip it** (deinfluencing, with the counts). Suggested first: a "Skip it", because an opinion in the first second stops people and it gets comments.

Receipts ready for "Skip it" (catalog read Nov 26–27; re-check live): BK Beauty says up to 40%, 2 of 78 products are; Jet Set Candy up to 50%, 74 of 1,920; Rothy's up to 40%, 70 of 643; Heaven Mayhem up to 60%, 24 of 184 (but 98% marked at ~30%); Organic Basics up to 60%, 273 of 1,950; Jenni Kayne up to 60%, ~2% of the store marked at all (catalog may be incomplete); and the generous ones: Daze Denim says 25%, 78 of 156 at 50%+; Alexandra Miro says 20–50%, 63 of 126 at 50%+; LAKE says 25%, 44% of store at 40%+.

She was asked to label 20 known brands `love / overrated / never tried` and has not answered. Rhode is not in the sheet: no numbers on it.

## Waiting on Pily

1. **Niche: A, B, C, or "B done A's way".**
2. **Pieces:** numbers from `sheets/taste-1.jpg` and `taste-2.jpg` (24 sleeker pieces; data in `specs/taste-numbered.json`).
3. Stats screenshot for the jewelry video if she posted it.
4. Whether she will set up her sister's ShopMy links (she said she cares more about growth; fine either way).

## What is in this folder

- `data/bfcm.csv` — the sister's sheet (brand, URL, ShopMy link, sale, dates, code, discount).
- `data/brands.json` — host → brand, industry, sheet rows. `data/audit.json` — per-store counts and homepage phrases.
- `data/catalog-rows.json.gz` — compact catalog for 199 stores, 91,869 products: per product `t` title, `h` handle, `type`, `pr` price now, `ca` original, `off` %, `av` variants in stock, `n` variants, `img` up to 4 URLs. Discount is the cheapest in-stock variant against its own compare-at price. Read Nov 26–27; it goes stale fast.
- `scripts/pick.py` — catalog toolkit (`host`, `rows`, `best`, `category`, `share`, `detail`, `sheet`, `currency`). **Its paths point at the cloud scratchpad**; repoint `SP`/`D` and make `rows()` read `catalog-rows.json.gz` (the raw crawl, 854 MB, was not committed). `detail()` needs the raw crawl; use the live `/products/<handle>.js` instead.
- `scripts/vid.py` — finds and downloads brands' own product videos (`/products/<handle>.js` → `media`).
- `scripts/film.py`, `roundup_m.py`, `roundup.py`, `voicecut.py`, `funnel.py` — the renderers for the styles that failed. Keep for reference; `voicecut.py` (cuts a video to her voice memo using faster-whisper word timestamps, trims pauses, keeps chosen ranges) is still useful.
- `scripts/rec2.js` — the screen-recording recorder.
- `specs/` — every video spec and script, the brief files given to sub-agents, `allvideos.json` (which stores have product video), `taste-numbered.json`, `dress-numbered.json`.
- `sheets/` — the numbered pick sheets and the look sketches.
- `videos/` — the screen-recording test and the three most recent finished videos.
- Earlier work in `../` (`roundups/`, `film/`, `saturday-nov28/`, `videos/`, carousels): all in the failed style.

Other stores priced in £ or A$ in the data (drop or convert): Odd Muse, Stripe & Stare, Beyond Nine, Piglet in Bed, P.E Nation, DISSH, Soleil Soleil, With Consideration, Antipodean Label. The Silk Road is priced in euros. Marcella refuses automated `.js` price checks and is on sale most of the year.

Artifacts from the cloud session (may not open from the Mac session; rebuild if needed): to-do desk https://claude.ai/artifact/MuLicDC8EKzCiQtzZuHqx7

## What the Mac has that the cloud did not

Her content engine lives at `~/Documents/Hospitality/Momenti/momenti - claude`: the momenti-motion Remotion library, `public/sfx` (her real 18-sound kit), `_house/BRAND.md` and `CRAFT.md`, `render.py`, `capcut.py`, and CapCut itself. Her Notion has a Content Playbook, a CapCut pipeline guide and inboxes of effects and sounds to use. Read `_house/` and those Notion pages before making anything; she was annoyed in the cloud session that they were ignored. Use her real sound kit, never synthesized sounds.
