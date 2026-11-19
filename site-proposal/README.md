# MOMENTI website proposal (18 Nov 2026)

A working version of the proposed new site, to open and click through. **Status: for Pily's review. Not live, not deployed** (listed in `.vercelignore`).

- Open: http://localhost:8123/site-proposal/ (or `index.html` in a browser).
- Hidden notes page (not linked from the site): `notes.html`, with the three decisions, the opening-film storyboard and the copy deck.
- Pages: `index.html` (home), `collections.html` (Collection I · The Grand Tour, Collection II coming), `the-grand-tour.html` (the bags cut out and floating on ivory), one page per piece (`havana-1958.html`, `miami-1959.html`, `new-york-1977.html`, `tokyo-1979.html`, `monaco.html`), `the-house.html` (Our Story), `join.html` (The House: the community, with Conversations), `owners-circle.html` (The Owners’ Circle), `questions.html`, `legal.html`.
- Edit words or pieces in `build.py`, then run `python3 build.py`. Styles: `assets/site.css`. Motion: `assets/site.js` (the film slot and the Stripe links are at the top).
- Images come only from `2 Product/MOMENTI-clutch/images/` and `1 Brand/kit/assets/Photography/`, resized into `assets/img/` (bag images cropped to remove the "Render" mark; the footer carries one line instead).
- Floating bags: transparent cut-outs of the approved masters (Havana, New York, Monaco 1964) in `assets/img/cut/` (made with macOS Vision's foreground mask, then edge-cleaned). Miami and Tokyo show a hairline outline from the spec drawing and "Coming soon." until their bags are approved.

## Waiting on Pily
1. The opening film storyboard (yes/no), to be made on Runway.
2. The House page: founder story, her quote, AS SHE PLEASES. as the last line.
3. The launch line-up: five moments, live once the Miami, Tokyo and Monaco bag images are approved; Rome and London off until confirmed.

Also open (marked "draft" in grey on the pages): returns window, lead time, the maker's materials and country, how early owners see new moments, the Monaco year and car, the Tokyo car, the Stripe links, and the email domain (the site uses hello@momenti.com; the site is houseofmomenti.com).
