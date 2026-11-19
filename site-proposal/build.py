#!/usr/bin/env python3
"""MOMENTI website proposal: builds every page of the working site from one place.
Run:  python3 build.py   (writes the .html files next to this script)"""
import os, json
H = os.path.dirname(os.path.abspath(__file__))
I = 'assets/img/'
WM, WMI, O = 'assets/logo/momenti-wordmark-ink.svg', 'assets/logo/momenti-wordmark-ivory.svg', 'assets/logo/the-o-ink.svg'
EMAIL = 'hello@momenti.com'

def D(t): return ''  # customer pages carry no draft notes; open items are listed in notes.html
def lines(*ls): return ''.join(f'<span class="line"><span>{l}</span></span>' for l in ls)

# ------------------------------------------------------------------ the pieces (facts from the kit; drafts marked)
PIECES = [
 dict(slug='havana-1958', no='01', name='Havana 1958', title='Havana, 1958.', tl=('Havana,', '1958.'), feel='What you take with you.', price=520,
      photo='havana-photograph', reverse='havana-reverse', hero='havana-hero',
      cap1='The Prado, late morning.', cap2='On the balcony, smiling at someone below.', cap2l='Above the street',
      master='havana-1958_01-front_MASTER', cut='havana-1958', gallery=['havana-1958_06-car-closeup','havana-1958_07-fabric-closeup','havana-1958_05-open','havana-1958_08-chain'],
      moment='The Prado, Havana, in 1958. Late morning, a turquoise convertible at the kerb and the Capitol at the end of the street. The photograph is printed edge to edge, front and back, in its faded colours.',
      car='A 9 cm die-cast miniature of the turquoise convertible in the photograph sits on the clasp. Lift it, and the bag opens.',
      chain='A gold chain threaded with ivory leather, to wear it on the shoulder; unclip it to carry the bag in hand.',
      back='The same photograph on the back, with HAVANA, 1958. engraved into the gold frame.',
      arrive=dict(print=I+'havana-print.jpg', printW=2400, printH=1437, car=[0.155,0.575,0.475,0.82],
                  poly='polygon(0% 42%,22% 30%,30% 2%,62% 6%,78% 30%,100% 44%,100% 78%,64% 100%,4% 100%,0% 78%)', clasp=[0.398,0.205,0.602,0.31])),
 dict(slug='miami-1959', no='02', name='Miami 1959', title='Miami, 1959.', tl=('Miami,', '1959.'), feel='Starting over.', price=500,
      photo='miami-photograph', reverse='miami-reverse', hero='miami-hero',
      cap1='Ocean Drive, at noon.', cap2='Under the awning, ignoring the street.', cap2l='Across the street',
      master=None, gallery=['detail-miami-clasp','miami-reverse','miami-wall'],
      moment='Ocean Drive, Miami Beach, in 1959. Noon, from the kerb outside the Colony.',
      car='The pink convertible from the photograph sits on the clasp, in miniature. Lift it, and the bag opens.',
      chain='A detachable chain, to wear it on the shoulder or carry it in hand.', back='The same photograph on the back, with MIAMI, 1959. engraved into the gold frame.'),
 dict(slug='new-york-1977', no='05', name='New York 1977', title='New York, 1977.', tl=('New York,', '1977.'), feel='Going out anyway.', price=560,
      photo='new-york-photograph', reverse='new-york-reverse', hero='new-york-hero',
      cap1='Water Street, after the rain.', cap2='A dancer stretching in a loading-dock door.', cap2l='Next door',
      master='new-york-1977_01-front_MASTER', cut='new-york-1977', gallery=['new-york-1977_06-car-closeup','new-york-1977_02-three-quarter','new-york-1977_05-open','new-york-1977_08-chain'],
      moment='Water Street, Lower Manhattan, in 1977. A yellow cab at the kerb on wet cobbles, and the Manhattan Bridge at the end of the street.',
      car='A 9 cm die-cast miniature of the yellow taxi in the photograph sits on the clasp. Lift it, and the bag opens.',
      chain='A champagne-gold chain threaded with black leather, to wear it on the shoulder; unclip it to carry the bag in hand.',
      back='The same photograph on the back, with NEW YORK, 1977. engraved into the gold frame.',
      arrive=dict(print=I+'new-york-print.jpg', printW=2400, printH=874, car=[0.115,0.635,0.36,0.98],
                  poly='polygon(0% 40%,30% 30%,40% 4%,62% 4%,72% 28%,100% 40%,100% 82%,70% 100%,6% 100%,0% 80%)', clasp=[0.386,0.178,0.614,0.31])),
 dict(slug='tokyo-1995', no='06', name='Tokyo 1995', title='Tokyo, 1995.', tl=('Tokyo,', '1995.'), feel='A world of your own.', price=580,
      photo='tokyo-1995_print-file', reverse='tokyo-1995_04-back', hero='tokyo-1995_02-three-quarter',
      cap1='A side street, just after the rain.', cap2='The same street, with TOKYO, 1995. on the frame.', cap2l='On the back',
      master='tokyo-1995_01-front_MASTER', cut='tokyo-1995', gallery=['tokyo-1995_06-car-closeup','tokyo-1995_02-three-quarter','tokyo-1995_05-open','tokyo-1995_08-chain'],
      moment='A narrow side street in Tokyo, in 1995, just after the rain. Neon on the wet road, red lanterns outside a yakitori bar, and a purple coupé at the kerb.',
      car='A 9 cm die-cast miniature of the purple coupé in the photograph sits on the clasp. Lift it, and the bag opens.',
      chain='A champagne-gold chain threaded with black leather, to wear it on the shoulder; unclip it to carry the bag in hand.',
      back='The same photograph on the back, with TOKYO, 1995. engraved into the gold frame.'),
 dict(slug='monaco', no='07', name='Monaco 1964', title='Monaco, 1964.', tl=('Monaco,', '1964.'), cut='monaco-1964', feel='The long way round.', price=600,
      photo='monaco-photograph', reverse='monaco-reverse', hero='campaign-monaco-quay',
      cap1='The hairpin, race week.', cap2='The crowd leans to the race; she sits on the rail.', cap2l='On the balustrade',
      master='monaco-1964_01-front_MASTER', gallery=['monaco-1964_06-car-closeup','monaco-1964_02-three-quarter','monaco-1964_05-open','monaco-1964_08-chain'],
      moment='Monaco, 1964, race week: the hairpin, seen from the stone balustrade above it.',
      car='The red race car from the photograph sits on the clasp, in miniature. Lift it, and the bag opens.',
      chain='A detachable chain, to wear it on the shoulder or carry it in hand.', back='The same photograph on the back, with MONACO, 1964. engraved into the gold frame.'),
]
PIECES = [p for p in PIECES if p['slug'] != 'miami-1959']  # Miami returns when its final images are approved
BY = {p['slug']: p for p in PIECES}

# ------------------------------------------------------------------ shared parts
def head(title, desc='MOMENTI is a design house that makes objects from moments.', extra=''):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title><meta name="description" content="{desc}">
<meta name="theme-color" content="#F4F0E8"><link rel="icon" href="assets/logo/the-o-ink.svg">
<link rel="preload" href="assets/fonts/BodoniModa-Italic-VF.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="assets/site.css">
<script src="/js/attribution.js"></script>
<script>window.va=window.va||function(){{(window.vaq=window.vaq||[]).push(arguments)}}</script><script defer src="/_vercel/insights/script.js"></script>{extra}</head>'''

def nav(photo=False, reserve_here=False):
    res = '<a class="lab res" href="#reserve" data-reserve>Reserve</a>' if reserve_here else '<a class="lab res" href="the-grand-tour.html">Reserve</a>'
    return f'''<header class="nav{' on-photo' if photo else ''}">
  <nav class="l"><a class="lab hide-m" href="collections.html">Collections</a><a class="lab hide-m" href="the-house.html">Our Story</a><a class="lab menu-btn" href="#" data-menu>Menu</a></nav>
  <a href="index.html" aria-label="MOMENTI, home"><img class="wm wm-k" src="{WM}" alt="MOMENTI"><img class="wm wm-i" src="{WMI}" alt=""></a>
  <nav class="r"><a class="lab hide-m" href="questions.html">Questions</a><a class="lab hide-m" href="join.html">The House</a>{res}</nav>
</header>
<div class="menu" aria-hidden="true">
  <div class="top"><a class="lab" href="#" data-menu>Close</a><img src="{WM}" alt="MOMENTI"><span></span></div>
  <ul>
    <li><a href="collections.html" data-pic="a"><span class="line"><span>Collections</span><small class="lab">The bags</small></span></a></li>
    <li><a href="the-house.html" data-pic="b"><span class="line"><span>Our Story</span><small class="lab">Pily and Havana</small></span></a></li>
    <li><a href="join.html" data-pic="c"><span class="line"><span>The House</span><small class="lab">Open to anyone</small></span></a></li>
    <li><a href="questions.html" data-pic="d"><span class="line"><span>Questions</span><small class="lab">Client care</small></span></a></li>
  </ul>
  <div class="pic"><img class="on" data-k="a" src="{I}havana-photograph.jpg" alt=""><img data-k="b" src="{I}havana-reverse.jpg" alt=""><img data-k="c" src="{I}monaco-hero.jpg" alt=""><img data-k="d" src="{I}making-carving.jpg" alt=""></div>
  <div class="foot-l"><span class="it">{EMAIL}</span><span class="lab">Instagram · TikTok · @houseofmomenti</span></div>
</div>'''

def join(cls='', btn='Join', done='You’re on the list.'):
    return f'<form class="join {cls}" novalidate><input type="email" placeholder="Your email" aria-label="Your email"><button type="submit">{btn}</button><span class="done">{done}</span></form>'

FOOT = f'''<footer class="foot">
  <div class="cols">
    <div><h5>The Letter</h5><p class="ser" style="font-size:30px;line-height:1.15;max-width:460px">Letters from the house: <span class="it">new moments, first.</span></p>{join(btn='Sign up')}</div>
    <div><h5>MOMENTI</h5><ul><li><a href="collections.html">Collections</a></li><li><a href="the-house.html">Our Story</a></li><li><a href="join.html">The House</a></li><li><a href="owners-circle.html">The Owners’ Circle</a></li></ul></div>
    <div><h5>Client care</h5><ul><li><a href="questions.html">Questions</a></li><li><a href="legal.html#reserving">Reserving</a></li><li><a href="legal.html#shipping">Shipping</a></li><li><a href="legal.html#returns">Returns</a></li><li><a href="legal.html#care">Care</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
    <div><h5>Follow</h5><ul><li><a href="https://www.instagram.com/houseofmomenti">Instagram</a></li><li><a href="https://www.tiktok.com/@houseofmomenti">TikTok</a></li></ul><h5 style="margin-top:34px">Legal</h5><ul><li><a href="legal.html#terms">Terms of sale</a></li><li><a href="legal.html#reserving">Reservation terms</a></li><li><a href="legal.html#privacy">Privacy</a></li></ul></div>
  </div>
  <img class="wmbig" src="{WMI}" alt="MOMENTI">
  <div class="base lab"><span>© 2026 MOMENTI</span><span>Images show the finished piece; the first pieces are in the making.</span><span>USD · Worldwide</span></div>
</footer>'''

def page(fname, title, body_cls, content, piece=None, extra_head='', foot=True, arrive=None):
    data = f' data-piece="{piece}"' if piece else ''
    ar = f'<script>window.ARRIVE={json.dumps(arrive)};</script>' if arrive else ''
    html = head(title, extra=extra_head) + f'<body class="{body_cls}"{data}><div class="curtain"></div>' + content + (FOOT if foot else '') + ar + '<script src="assets/site.js"></script></body></html>'
    open(os.path.join(H, fname), 'w').write(html)

def card(p, extra_cls=''):
    bag = f'<img class="bag" src="{I}{p["master"]}.jpg" alt="" loading="lazy">' if p['master'] else f'<img class="alt" src="{I}{p["reverse"]}.jpg" alt="" loading="lazy">'
    dr = ' ' + D('proposed') if p.get('feel_draft') else ''
    return f'''<a class="card {extra_cls}" href="{p['slug']}.html" data-arrive="{p['slug']}" draggable="false">
<div class="ph rv-img"><img class="main" src="{I}{p['photo']}.jpg" alt="{p['title']} The photograph." loading="lazy" draggable="false">{bag}</div>
<div class="meta"><span class="cap">{p['title']}</span></div>
<div class="feel"><span class="it">{p['feel']}{dr}</span><span class="go link">See the moment</span></div>
<span class="price">${p['price']}</span></a>'''

FL = 'assets/img/cut/'
def flt(p, tag='a', k=0):
    """A bag, cut out, floating on ivory. No approved bag yet: a hairline silhouette and 'Coming soon.'"""
    ph = [-1.2, -4.6, -2.8, -6.1, -0.4][k % 5]; du = [7.2, 8.6, 6.4, 8.1, 7.6][k % 5]
    st = f' style="--ph:{ph}s;--du:{du}s"'
    href = f' href="{p["slug"]}.html" data-arrive="{p["slug"]}" draggable="false"' if tag == 'a' else ''
    if p.get('cut'):
        bag = f'<img src="{FL}{p["cut"]}_cut.webp" alt="{p["name"]}, frame clutch, with its car on the clasp" loading="lazy" draggable="false">'
        txt = f'<span class="it">{p["feel"]}</span>'
        cls = 'flt'
    else:
        bag = f'<img class="ghost" src="{FL}silhouette.svg" alt="" loading="lazy" draggable="false">'
        txt = '<span class="it">Coming soon.</span>'
        cls = 'flt soon'
    return (f'<{tag} class="{cls} c-{p["slug"]}"{href}{st}><div class="stage"><div class="lift"><div class="bob">{bag}</div></div>'
            f'<div class="sh-w"><i class="sh"></i></div></div><div class="fcap"><span class="cap">{p["title"]}</span>{txt}</div></{tag}>')

# ================================================================== HOME
hv = BY['havana-1958']
home = nav() + f'''
<div class="opening"><img src="{WM}" alt=""></div>
<section class="hero hero-c" data-nav-photo>
  <div class="film" aria-hidden="true"><video muted playsinline preload="none"></video></div>
  <div class="frame"><img src="{I}havana-hero.jpg" alt="Havana, 1958: asleep in the back seat of a turquoise convertible on the Prado" fetchpriority="high"></div>
  <div class="shade"></div>
  <div class="title"><span class="lab kick">Collection I</span><h1 class="ser rv-lines">{lines('The Grand Tour')}</h1>
    <div class="side"><span class="it">Moments are the only luxury you can’t buy.</span><a class="link lt" href="collections.html">Discover the collection</a></div></div>
</section>
<section class="tour">
  <div class="head"><h2 class="cap rv-lines">{lines('The Grand Tour.')}</h2><a class="link rv" href="the-grand-tour.html">See the collection</a></div>
  <div class="track-wrap flo"><div class="track">{''.join(flt(p, k=k) for k, p in enumerate(PIECES))}</div></div>
  <div class="drag-bar"><span class="lab">Drag</span><div class="bar"><i></i></div><span class="lab mut count">01 / {len(PIECES):02d}</span></div>
</section>
<a class="spread" href="new-york-1977.html" data-arrive="new-york-1977" data-nav-photo>
  <img class="bgimg" data-par="-0.12" src="{I}new-york-hero.jpg" alt="New York, 1977: dawn, asleep on the roof of the cab" loading="lazy">
  <div class="shade"></div>
  <div class="t"><h2 class="cap rv-lines">{lines('New York,', '1977.')}</h2><div style="text-align:right" class="rv d2"><span class="it" style="display:block;margin-bottom:22px">Going out anyway.</span><span class="link">See the moment</span></div></div>
</a>
<section class="m2b">
  <div class="m2b-head rv"><span class="lab mut">How it begins</span><h2 class="ser">From a moment, <span class="it">a bag.</span></h2></div>
  <div class="m2b-pair">
    <figure class="rv-img"><img src="{I}havana-photograph.jpg" alt="Havana, 1958: the Prado, late morning" loading="lazy"><figcaption class="lab">The moment · Havana, 1958</figcaption></figure>
    <figure class="m2b-bag rv"><img src="assets/img/cut/havana-1958_cut.webp" alt="The Havana 1958 bag, its car on the clasp" loading="lazy"><figcaption class="lab">The bag · Havana, 1958</figcaption></figure>
  </div>
  <div class="m2b-txt rv"><p class="body-l">Every bag begins with one moment, and carries a piece of it with you. Ours began in Havana, with my grandparents.</p><p style="margin-top:28px"><a class="link" href="the-house.html">Our story</a></p></div>
</section>
<section class="hinv" data-nav-photo>
  <img class="bgimg" data-par="-0.08" src="{I}campaign-monaco-quay.jpg" alt="Monaco: in a white suit and hat, standing on a red race car on the quay" loading="lazy">
  <div class="shade"></div>
  <div class="t">
    <span class="lab rv">Free to join</span>
    <h2 class="cap rv-lines">{lines('The House.')}</h2>
    <p class="it rv d2">Bring a moment.</p>
    <p class="sm rv d2">Conversations with women who have a moment worth telling, evenings when there are some, and the first look at every new piece. Every so often, a member’s moment becomes a bag.</p>
    <a class="btn lt rv d3" href="join.html"><span>Inside the House</span></a>
  </div>
</section>
<section class="letterband"><span class="lab mut rv">The Letter</span><p class="ser rv">Letters from the house: <span class="it">new moments, first.</span></p><div class="rv d2">{join(btn='Sign up')}</div></section>'''
page('index.html', 'MOMENTI', 'home pre', home)

# ================================================================== THE GRAND TOUR
tour = nav() + f'''
<section class="lu-top"><nav class="crumb lab rv" aria-label="Breadcrumb"><a href="collections.html">Collections</a><span>/</span><span class="mut">The Grand Tour</span></nav>
  <h1 class="cap rv-lines">{lines('The Grand', 'Tour.')}</h1>
  <div class="meta rv d3"><span class="lab">Collection I</span><span class="it">Our first collection. Each bag carries one photograph of a city in one year, with the car from that street on the clasp.</span></div></section>
<section class="lineup-f"><div class="track-wrap flo"><div class="track">{''.join(flt(p, k=k) for k, p in enumerate(PIECES))}</div></div>
  <div class="drag-bar"><span class="lab">Drag</span><div class="bar"><i></i></div><span class="lab mut count">01 / {len(PIECES):02d}</span></div></section>
<section class="lu-note"><p class="rv">Every bag is sold out for now. <span class="it">Reserve yours</span> and pay nothing until it’s ready.</p></section>'''
page('the-grand-tour.html', 'The Grand Tour · MOMENTI', 'tour', tour)

# ================================================================== COLLECTIONS
hero_bags = [p for p in PIECES if p.get('cut')]
cols = nav() + f'''
<section class="co-top"><span class="lab mut rv">The bags</span><h1 class="cap rv-lines">{lines('Collections.')}</h1>
  <p class="it rv d2">Each collection is a set of moments. Each bag carries one of them.</p></section>
<a class="co-one" href="the-grand-tour.html">
  <div class="co-bags">{''.join(flt(p, tag='div', k=k) for k, p in enumerate(hero_bags))}</div>
  <div class="co-t"><span class="lab">Collection I</span><h2 class="cap rv-lines">{lines('The Grand Tour.')}</h2>
    <p class="it rv">Our first collection: a city in one year, for each bag, with the car from its photograph on the clasp.</p>
    <span class="link rv">See the collection</span></div>
</a>
<section class="co-two rv"><span class="lab">Collection II</span><span class="it">Coming.</span><a class="link" href="join.html">Hear first</a></section>'''
page('collections.html', 'Collections · MOMENTI', 'collections', cols)

# ================================================================== PIECE PAGES
def piece_page(p):
    k = PIECES.index(p)
    has_bag = bool(p['master'])
    first = f'{I}{p["master"]}.jpg' if has_bag else f'{I}{p["photo"]}.jpg'
    g = p['gallery']
    if has_bag:
        gal = f'''<div class="a"><img src="{first}" alt="{p['name']}, front" fetchpriority="high"></div>
<div class="row"><div><img src="{I}{g[0]}.jpg" alt="The car on the clasp" loading="lazy"></div><div><img src="{I}{g[1]}.jpg" alt="" loading="lazy"></div></div>
<div class="b"><img src="{I}{g[2]}.jpg" alt="Open, the ivory lining" loading="lazy"></div><div class="b chain"><img src="{I}{g[3]}.jpg" alt="With its chain" loading="lazy" style="object-position:50% 100%"></div>'''
        n_dots = 5; note = ''
    else:
        gal = f'''<div class="a tall"><img src="{first}" alt="{p['title']} The photograph." fetchpriority="high"></div>
<div class="b tall"><img src="{I}{g[0]}.jpg" alt="The car" loading="lazy"></div><div class="row"><div><img src="{I}{g[1]}.jpg" alt="" loading="lazy"></div><div><img src="{I}{g[2]}.jpg" alt="" loading="lazy"></div></div>'''
        n_dots = 4; note = ''
    dots = '<div class="dots">' + ''.join(f'<i{" class=on" if i==0 else ""}></i>' for i in range(n_dots)) + '</div>'
    spec = [
      ('The moment', p['moment']), ('The car', p['car']),
      ('Dimensions', '33 × 16 cm (13 × 6¼ in); 19 cm (7½ in) tall with the car; 7 cm deep at its fullest.'),
      ('Materials', 'A champagne-gold frame, with soft ivory suede inside and a slot for a card. ' + p['chain']),
      ('The back', p['back']),
      ('Made', 'In small runs, never everywhere. Each bag is made for the person who reserved it.'),
      ('In the box', 'A card telling the true story behind the moment, with a line for your name. The photograph itself, in an ivory envelope. A dust bag. And a ticket: your place in the Owners’ Circle.'),
      ('Care', 'Keep it in its dust bag, away from sun and damp. Wipe the frame with a soft, dry cloth. Hold it by its body, not by the car.'),
      ('Delivery', 'When your bag is ready, we’ll email you, and you’ll have a week to change your mind before anything is charged. It arrives tracked and insured; shipping and any duties are shown before you pay.'),
      ('Returns', f'If anything isn’t right, write to {EMAIL} and a person will reply within one working day.'),
    ]
    spec_html = ''.join(f'<div class="r rv"><span class="lab">{a}</span><p>{b}</p></div>' for a, b in spec)
    acc_rows = [('The moment', p['moment']), ('The car', p['car']), ('Details and dimensions', spec[2][1] + ' ' + spec[3][1]),
                ('What comes with it', spec[6][1]), ('Care', spec[7][1]), ('Delivery and returns', spec[8][1] + ' ' + spec[9][1])]
    acc = ''.join(f'<div class="row{" open" if i==0 else ""}"><button class="h" aria-expanded="{"true" if i==0 else "false"}"><span class="lab">{a}</span><i></i></button><div class="c"><div><p>{b}</p></div></div></div>' for i, (a, b) in enumerate(acc_rows))
    dr = ' ' + D('proposed') if p.get('feel_draft') else ''
    others = [q for q in PIECES if q is not p]
    if p['slug'] == 'havana-1958':
        why = f'''<section class="why"><div class="img rv-img"><img src="{I}havana-print.jpg" style="object-position:22% 70%" alt="" loading="lazy"></div>
<div class="t rv"><span class="lab mut">Why Havana is first</span><p class="ser">Pily’s grandparents had to leave Cuba. <span class="it">The first piece is Havana, 1958.</span></p><a class="link" href="the-house.html">Our story</a></div></section>'''
    else:
        why = f'''<section class="why"><div class="img rv-img"><img src="{I}{p['hero']}.jpg" alt="" loading="lazy"></div>
<div class="t rv"><span class="lab mut">{p['title']}</span><p class="ser">{p['feel']}</p><a class="link" href="the-grand-tour.html">The Grand Tour</a></div></section>'''
    thumb = f'{I}{p["master"]}.jpg' if has_bag else f'{I}{p["photo"]}.jpg'
    content = nav(reserve_here=True) + f'''
<section class="pp">
  <div><div class="gal">{gal}</div>{dots}{note}</div>
  <aside class="info"><div class="stick">
    <span class="lab mut rv">Collection I · The Grand Tour</span>
    <h1 class="cap t rv-lines" style="margin-top:22px">{lines(*p['tl'])}</h1>
    <span class="it feel rv d2">{p['feel']}{dr}</span>
    <div class="name rv d3"><span class="ser">{p['name']}, <span class="it">frame clutch</span></span><span class="price">${p['price']}</span></div>
    <p class="state rv d3">Sold out for now.</p>
    <a class="btn rv d4" href="#reserve" data-reserve><span>Reserve yours</span></a>
    <p class="reass rv d4">Pay nothing today. When yours is ready, you’ll have a week to change your mind.</p>
    <div class="acc rv d4">{acc}</div>
  </div></aside>
</section>
<section class="moment">
  <figure class="rv-img"><img src="{I}{p['photo']}.jpg" alt="" loading="lazy"><span class="lab over">The moment</span><figcaption><span class="lab">The photograph on the bag</span><span class="it">{p['cap1']}</span></figcaption></figure>
  <figure class="rv-img"><img src="{I}{p['reverse']}.jpg" alt="" loading="lazy"><figcaption><span class="lab">{p['cap2l']}</span><span class="it">{p['cap2']}</span></figcaption></figure>
</section>
<section class="details"><h2 class="cap rv-lines">{lines('The details.')}</h2>
  <p class="intro rv">Everything about the piece, in one place. If something isn’t here, write to {EMAIL}. A person reads it.</p>
  <div class="spec">{spec_html}</div></section>
{why}
<section class="more"><div class="head"><span class="cap">The Grand Tour.</span><a class="link" href="the-grand-tour.html">The collection</a></div>
<div class="grid">{''.join(card(q) for q in others)}</div></section>
<div class="veil"></div>
<aside class="sheet" aria-label="Reserve">
  <span class="handle"></span>
  <div class="x"><span class="lab">Reserve</span><button class="lab" data-close>Close</button></div>
  <div class="form-state">
  <h2 class="ser">Reserve <span class="it">yours.</span></h2>
  <div class="pc"><div class="t"><img src="{thumb}" alt=""></div><div><span class="ser" style="font-size:21px;display:block">{p['name']}</span><span class="it mut" style="font-size:16px">frame clutch</span></div><span>${p['price']}</span></div>
  <p class="r-body">Pay nothing today. We’ll tell you the moment yours is ready, and you’ll have a week to change your mind before anything is charged.</p>
  <a class="btn" href="#" data-hold><span>Reserve mine</span></a>
  <p class="fine">Secure checkout. Nothing is charged until your bag is ready.</p>
  </div>
  <div class="done-state">
    <h2 class="ser">Reserved. <span class="it">{p['name']} has your name on it.</span></h2>
    <p style="font-size:17px">We’ve sent you an email with everything you need, and we’ll be in touch the moment yours is ready.</p>
  </div>
  <div class="alt"><span class="tell-txt" style="display:flex;justify-content:space-between;align-items:center;width:100%;gap:16px"><span class="it" style="font-size:18px">Not ready? Hear when it’s back.</span><a class="link tell" href="#" data-tell>Tell me</a></span>
  <form class="tell-in join" novalidate style="border-color:var(--hair);margin:0;max-width:none;width:100%"><input type="email" placeholder="Your email" style="color:var(--ink)"><button type="submit">Tell me</button></form></div>
</aside>'''
    ar = dict(p['arrive'], master=I + p['master'] + '.jpg') if p.get('arrive') else None
    page(f"{p['slug']}.html", f"{p['name']} · MOMENTI", 'piece', content, piece=p['slug'], arrive=ar)
for p in PIECES: piece_page(p)

# ================================================================== THE HOUSE (the community, free): join.html
# Not to be confused with the-house.html, which is Our Story (About). The Letter (newsletter) is separate: footer + home.
# CONVERSATIONS: the interview series. Placeholders until the first ones are done. Fill name, city and quote and the
# "Coming soon" state disappears. The images are stand-ins from the kit until the real portraits are taken.
CONVOS = [
 dict(img='campaign-new-york-1977', pos='50% 35%', no='01', name='', city='Madrid', quote=''),
 dict(img='new-york-reverse', pos='50% 30%', no='02', name='', city='', quote=''),
 dict(img='havana-reverse', pos='50% 62%', no='03', name='', city='', quote=''),
 dict(img='tokyo-reverse', pos='60% 60%', no='04', name='', city='', quote=''),
]
def convo(c, lead=False):
    soon = not c['name']
    who = (f'<span class="ser nm">{c["name"]}{", " + c["city"] if c["city"] else ""}</span>' if not soon
           else f'<span class="ser nm">Coming soon{"<span class=it>, " + c["city"] + "</span>" if c["city"] else ""}</span>')
    q = (f'<p class="q it">“{c["quote"]}”</p>' if c['quote'] else
         (f'<p class="q it">The first conversation is being written.</p>' if lead else ''))
    return (f'<article class="cv{" lead" if lead else ""}{" soon" if soon else ""} rv">'
            f'<figure class="ph rv-img"><img src="{I}{c["img"]}.jpg" alt="" loading="lazy" style="object-position:{c["pos"]}">'
            f'{"<span class=\"lab tag\">Coming soon</span>" if soon else ""}</figure>'
            f'<div class="tx"><span class="lab mut">Conversation No. {c["no"]}</span>{who}{q}</div></article>')

def hx(img, alt, pos, lab, h, body, cls='', extra='', anchor=''):
    """One part of the House: a photograph and a short line, set like a magazine spread."""
    aid = f' id="{anchor}"' if anchor else ''
    return f'''<section class="hx {cls}"{aid}>
  <figure class="ph rv-img"><img src="{I}{img}.jpg" alt="{alt}" loading="lazy" style="object-position:{pos}"></figure>
  <div class="tx rv"><span class="lab mut">{lab}</span><h2 class="ser">{h}</h2><p>{body}</p>{extra}</div>
</section>'''

moment_form = '''<form class="nom" novalidate>
  <label class="f"><span class="lab">City</span><input type="text" placeholder="Havana"></label>
  <label class="f"><span class="lab">Year</span><input type="text" inputmode="numeric" placeholder="1958"></label>
  <label class="f wide"><span class="lab">What happened</span><textarea rows="3" placeholder="Where you were, who was there"></textarea></label>
  <label class="f wide file"><span class="lab">A photograph, if you have one</span><input type="file" accept="image/*"><span class="fake it">Choose a photograph</span></label>
  <label class="f wide"><span class="lab">Your email</span><input type="email" placeholder="So we can write back"></label>
  <button class="btn" type="submit"><span>Send your moment</span></button>
  <p class="done ser">Received. <span class="it">It’s with the house now.</span></p>
</form>'''

join_form = '''<form class="nom jn" novalidate>
  <label class="f wide"><span class="lab">Your email</span><input type="email" placeholder="you@example.com"></label>
  <label class="f wide"><span class="lab">Your moment <span class="opt">(if you like)</span></span><textarea rows="2" placeholder="A city, a year, what happened"></textarea></label>
  <button class="btn" type="submit"><span>Join the House</span></button>
  <p class="done ser">You’re in. <span class="it">Welcome to the House.</span></p>
</form>'''

community = nav(photo=True) + f'''
<section class="hh" data-nav-photo>
  <img class="bgimg" data-par="-0.1" src="{I}monaco-hero.jpg" alt="Monaco, race week: sitting on the nose of a red race car at the harbour hairpin" fetchpriority="high">
  <div class="shade"></div>
  <span class="lab where">Monaco, race week.</span>
  <div class="t">
    <span class="lab rv">Free to join</span>
    <h1 class="cap rv-lines">{lines('The', 'House.')}</h1>
    <div class="side rv d2"><p class="it">Bring a moment.</p><a class="btn lt" href="#join"><span>Join the House</span></a></div>
  </div>
</section>
<section class="hi"><p class="ser rv">Every bag begins with someone’s moment. The House is where people bring theirs: <span class="it">a city, a year, and what happened there.</span></p></section>
<section class="cvs" id="conversations">
  <div class="cvs-head"><span class="lab mut rv">The House · An interview series</span><h2 class="cap rv-lines">{lines('Conversations.')}</h2>
    <p class="it rv d2">We sit down with women who have a moment worth telling, and share part of it.</p></div>
  <div class="cvs-grid">{convo(CONVOS[0], lead=True)}<div class="more3">{''.join(convo(c) for c in CONVOS[1:])}</div></div>
</section>
{hx('miami-hero', 'Miami, 1959: the car wash, top down, still in the car', '50% 50%', 'Tell us your moment', 'Tell us <span class="it">your moment.</span>',
    'A city, a year, what happened, and a photograph if you have one. The best are told in Conversations. And every so often, one becomes a bag, made with the person who lived it and named after their moment.', 'c', moment_form, 'your-moment')}
<section class="hx-full" data-nav-photo>
  <img class="bgimg" data-par="-0.1" src="{I}worn-opera-steps.jpg" alt="Opera steps at night: a black slip dress, long gloves, the clutch in her hand" loading="lazy">
  <div class="shade"></div>
  <div class="t rv"><span class="lab">Evenings</span><h2 class="ser">Evenings, <span class="it">when there are some.</span></h2>
  <p>One moment for one night, city by city: a Havana, 1958, say, with the music of that year. Members hear first.</p></div>
</section>
{hx('monaco-reverse', 'Monaco, race week: the crowd leans to the race; she sits on the rail, elsewhere', '50% 60%', 'First look', 'First look, <span class="it">before anyone.</span>',
    'Each new moment reaches the House before it reaches anyone else.', 'b')}
<section class="hj" id="join" data-nav-photo>
  <img class="bgimg" data-par="-0.1" src="{I}new-york-hero.jpg" alt="New York, 1977: dawn, asleep on the roof of the cab" loading="lazy" style="object-position:50% 40%">
  <div class="shade"></div>
  <div class="t"><div><h2 class="cap rv-lines">{lines('Come in.')}</h2><p class="it rv d2">Joining takes your email and, if you like, your moment.</p></div>
  <div class="card rv d2">{join_form}</div></div>
</section>
<a class="up" href="owners-circle.html">
  <span class="lab">Own a piece?</span>
  <span class="ser">There’s a room <span class="it">upstairs.</span></span>
  <span class="link">The Owners’ Circle</span>
</a>'''
page('join.html', 'The House · MOMENTI', 'community', community)

# ================================================================== THE OWNERS' CIRCLE (owners only): owners-circle.html
# Says little on purpose. Pily: keep the surprises; never name what's in it beyond these lines.
OWN = [
 ('Kept by.', 'Your name on your piece’s card.'),
 ('First to reserve.', 'Each new piece, yours to reserve before anyone else.'),
 ('Owners’ evenings.', 'When there are some.'),
]
own_rows = ''.join(f'<div class="r rv"><h3 class="ser">{a}</h3><p>{b}</p></div>' for k, (a, b) in enumerate(OWN))
circle = nav(photo=True) + f'''
<section class="oc-top" data-nav-photo>
  <div class="t"><span class="lab rv">For owners only</span>
    <h1 class="ser rv">The Owners’ <span class="it">Circle.</span></h1>
    <p class="rv d2">Every piece arrives with a ticket. The ticket is your place here.</p></div>
  <figure class="box rv-img"><img src="{I}box-contents.jpg" alt="What comes with each bag: the box, the dust bag, the record card, the photograph and the ticket" fetchpriority="high"></figure>
</section>
<section class="oc-kept" data-nav-photo>
  <div class="ticket rv">
    <span class="lab">The Owners’ Circle</span>
    <span class="ser pc">New York, 1977.</span>
    <span class="kb"><span class="lab">Kept by</span><span class="it nm">your name</span></span>
    <img class="o" src="assets/logo/the-o-ink.svg" alt="">
  </div>
</section>
<section class="oc-list" data-nav-photo>
  <div class="l rv"><span class="lab">What owners have</span></div>
  <div class="rows">{own_rows}<p class="last ser rv">And a few things <span class="it">we’d rather not tell you yet.</span></p></div>
</section>
<section class="oc-room" data-nav-photo>
  <img class="bgimg" data-par="-0.08" src="{I}escape-monaco-room.jpg" alt="Monaco: an empty drawing room, a red race car, and her in black and long gloves" loading="lazy">
  <div class="shade"></div>
  <div class="t rv"><h2 class="ser">Already own a piece? <span class="it">Register it.</span></h2>
    <p>Send the code on your ticket, and your name goes on the list of owners.</p>
    <a class="btn lt" href="mailto:{EMAIL}?subject=Register%20my%20piece"><span>Register</span></a></div>
</section>
<section class="oc-out">
  <p class="ser rv">Not an owner yet? <span class="it">The House is free to join.</span></p>
  <div class="rv d2"><a class="link" href="join.html">The House</a><a class="link" href="the-grand-tour.html">See the collection</a></div>
</section>'''
page('owners-circle.html', 'The Owners’ Circle · MOMENTI', 'circlepg', circle)

# ================================================================== THE HOUSE (ABOUT): a family archive
# Pily's black-and-white family photographs go in assets/img/family-1.jpg, family-2.jpg, family-3.jpg.
# Until a file exists, its slot shows an ivory frame marked "Family photograph". Captions are in FAMILY below.
FAMILY = [
 ('family-1', 'My grandmother.', 'Cuba, before they left.'),
 ('family-2', 'My grandfather.', 'He lived through the 1950s in Cuba.'),
 ('family-3', 'What they took with them.', 'Photographs like this one, and the stories behind them.'),
]
def fam(slot, cls=''):
    f, t, c = slot
    if not os.path.exists(os.path.join(H, I, f + '.jpg')): return ''  # hidden until Pily's photo is saved
    return f"""<figure class="fam {cls} rv">
  <div class="fr"><span class="ph-l lab">Family photograph</span><img src="{I}{f}.jpg" alt="{t}" onerror="this.remove()"></div>
  <figcaption><span class="ser">{t}</span> <span class="it">{c}</span></figcaption></figure>"""
house = nav() + f"""
<section class="ab-top"><span class="lab mut rv">Our story</span>
  <h1 class="ser rv">Moments are the only luxury <span class="it">you can’t buy.</span></h1></section>
<section class="archive">
  {fam(FAMILY[0], 'big')}
</section>
<section class="letter">
  <div class="l rv"><span class="lab mut">From Pily</span></div>
  <div class="r rv">
    <p class="ser open">I named MOMENTI after <span class="it">my grandparents’ story.</span></p>
    <p>They had to leave Cuba. The moments they lived there became part of history, and part of us, and I wanted a way to carry them with me.</p>
    <p>So the first bag I made is Havana, 1958: a street in Havana printed on the bag, and on the clasp a small turquoise car from that street.</p>
    <blockquote><p>“So much hurt and pain behind it, but also memories. I felt proud.”</p></blockquote>
    <p class="sig it">Pily</p>
  </div>
</section>
<section class="archive pair">
  {fam(FAMILY[1], 'a')}
  {fam(FAMILY[2], 'b')}
</section>
<section class="ab-img">
  <div class="a rv-img"><img src="{I}havana-1958_01-front_MASTER.jpg" alt="Havana 1958, the first MOMENTI bag" loading="lazy"></div>
  <div class="t rv"><span class="lab mut">MOMENTI</span><p class="body-l" style="margin-top:16px">A design house that turns real moments into bags you carry. Each one begins with a single photograph of a place, in a year, and keeps its feeling.</p><p style="margin-top:26px"><a class="link" href="havana-1958.html" data-arrive="havana-1958">See Havana, 1958</a></p></div>
</section>
<section class="ways">
  <div class="head"><span class="cap">From a moment to a piece.</span><span class="lab mut">How each bag is made</span></div>
  <div class="grid">
    <div class="rv"><div class="ph rv-img"><img src="{I}new-york-print.jpg" style="object-position:28% 50%" alt="" loading="lazy"></div><h3 class="ser">The moment.</h3><p>Every bag begins with one moment: one place, in one year. It is printed edge to edge, front and back.</p></div>
    <div class="rv d1"><div class="ph rv-img"><img src="{I}making-painting.jpg" alt="" loading="lazy"></div><h3 class="ser">The car.</h3><p>One detail from it, a car from that street, is sculpted in miniature and painted to match. It sits on the clasp, and lifting it opens the bag.</p></div>
    <div class="rv d2"><div class="ph rv-img"><img src="{I}record-card-daylight.jpg" alt="" loading="lazy"></div><h3 class="ser">The story.</h3><p>Each bag comes with a card telling the true story behind its moment, with a line for your name.</p></div>
  </div>
</section>
<section class="closer" data-nav-photo><img class="bgimg" data-par="-0.1" src="{I}miami-reverse.jpg" alt="" loading="lazy"><div class="shade"></div><h2 class="cap rv-lines">{lines('As she', 'pleases.')}</h2></section>"""
import re as _re
house = _re.sub(r'<section class="archive[^"]*">\s*</section>\n?', '', house)  # no empty photo slots
page('the-house.html', 'Our story · MOMENTI', 'house', house)

# ================================================================== QUESTIONS
QS = [
 ('Reserving', [
  ('How does reserving work?', 'You pay nothing today; your card simply saves your place. When your bag is ready, we’ll email you, and you have a week to change your mind. If you keep it, we charge the price shown and send it to you.'),
  ('What does it cost?', 'The price on each piece’s page, in US dollars. Shipping, and any duties for your country, are shown before you are charged.'),
  ('Can I change my mind?', f'Yes, any time before the charge. Reply to any email from us, or write to {EMAIL}. Nothing is charged.'),
  ('When will mine be ready?', 'Each bag is made after it’s reserved. We’ll email you the moment yours is ready, with the date it ships.')]),
 ('The piece', [
  ('Does the car open?', 'Yes. It has to.'),
  ('What comes with it?', 'A card with the true story behind the moment, the photograph itself, a dust bag, and a ticket: your place in the Owners’ Circle.'),
  ('Are the pictures of the finished bag?', 'They show the finished piece. The first pieces are in the making.'),
  ('Is it a limited edition?', 'Each design is made in small runs, never everywhere.'),
  ('How should I care for it?', 'Keep it in its dust bag, away from sun and damp. Wipe the frame with a soft, dry cloth. Hold it by its body, not by the car.')]),
 ('About MOMENTI', [
  ('Who is behind it?', 'Pily, our founder. She named MOMENTI after her grandparents’ story.'),
  ('What is the House?', 'Our community: Conversations with women who have a moment worth telling, a place to share your own, evenings when there are some, and the first look at each new piece. Anyone can join, and it’s free.'),
  ('And the Letter?', 'Letters from the house, with new moments first. Just your email.'),
  ('And the Owners’ Circle?', 'For people who own a piece. Your ticket comes in the box.'),
  ('Where do you ship?', 'Worldwide, tracked and insured. Any duties are shown before you pay.')]),
]
qh = ''
for gname, items in QS:
    rows = ''.join(f'<div class="row{" open" if (gname=="Reserving" and i==0) else ""}"><button class="h"><span>{q}</span><i></i></button><div class="c"><div><p>{a}</p></div></div></div>' for i, (q, a) in enumerate(items))
    qh += f'<div class="grp lab mut">{gname}</div><div class="acc">{rows}</div>'
qpage = nav() + f'''
<section class="qa">
  <div class="l"><div class="stk"><h1 class="cap rv-lines">{lines('Questions.')}</h1><p class="rv">Write to <a href="mailto:{EMAIL}" style="border-bottom:1px solid">{EMAIL}</a>. A person reads it, and replies within one working day.</p>
  <div class="img rv-img"><img src="{I}making-carving.jpg" alt=""></div></div></div>
  <div class="r rv">{qh}</div>
</section>'''
page('questions.html', 'Questions · MOMENTI', 'questions', qpage)

# ================================================================== LEGAL
LEGAL = [
 ('reserving', 'Reservation terms.', [
  ('What a reservation is', 'A reservation saves your place for a bag that is sold out. Your card is saved securely by Stripe, and nothing is charged when you reserve.'),
  ('When you are charged', 'When your bag is ready, we email you. You have seven days from that email to change your mind. If you keep it, the price shown when you reserved is charged to the card you saved, and your bag is sent.'),
  ('Cancelling', f'You can cancel at any time before the charge, by replying to any email from us or writing to {EMAIL}. Nothing is charged.'),
  ('Your card', 'Payments are handled securely by our payment provider, Stripe. We never see or store your card number.')]),
 ('terms', 'Terms of sale.', [('Prices', 'Prices are shown in US dollars. Shipping, and any duties or taxes for your country, are shown before you pay.'), ('Questions', f'Write to {EMAIL}. A person reads every email.')]),
 ('shipping', 'Shipping.', [
  ('When', 'Each bag is made after it’s reserved. You’ll receive an email with tracking on the day it’s sent.'),
  ('How', 'Tracked and insured, with a signature on delivery. The parcel is plain: nothing on the outside says what’s inside.'),
  ('Duties and taxes', 'Shown to you before you are charged.'),
  ('If it’s late', 'We’ll tell you before you have to ask.')]),
 ('returns', 'Returns.', [
  ('If it isn’t right', f'Write to {EMAIL} with your order number, and we’ll take care of it.'),
  ('If it arrived damaged', f'That isn’t a return. Write to {EMAIL} with photos, and we’ll put it right.')]),
 ('care', 'Care.', [
  ('The car', 'It’s small, and it opens the bag. Lift it with a fingertip, not a nail, and never carry the bag by it.'),
  ('The frame', 'Wipe it with a soft, dry cloth. Close it gently: the frame clicks shut by itself.'),
  ('The print', 'Keep perfume, hand cream and sunscreen off it until they’ve dried on your skin. Keep it out of strong sun for long stretches.'),
  ('Storing it', 'In its dust bag, lying flat with the car facing up. Never in plastic, and never in a hot car in summer.')]),
 ('privacy', 'Privacy.', [
  ('What we keep', 'Your email if you join the House, the moment you send if you nominate one, and your name, address and email if you reserve. Card details stay with Stripe.'),
  ('Cookies', 'Where the law asks us to, we ask before using any cookies, and “No thanks” is always as easy as “Accept”.'),
  ('Leaving the list', 'Every letter has a link to leave, in one click.')]),
]
side = ''.join(f'<a href="#{k}"{" class=on" if i==0 else ""}>{t[:-1]}</a>' for i, (k, t, _) in enumerate(LEGAL))
docs = ''.join(f'<section id="{k}"><h2 class="cap">{t}</h2>' + ('<span class="stamp">Last updated 18 November 2026.</span>' if i==0 else '') + ''.join(f'<h3>{a}</h3><p>{b}</p>' for a, b in rows) + '</section>' for i, (k, t, rows) in enumerate(LEGAL))
legal = nav() + f'''<section class="lg"><div class="side"><nav><span class="lab mut" style="margin-bottom:8px">Client care</span>{side}</nav></div><article class="doc">{docs}</article></section>
<script>(function(){{var a=[].slice.call(document.querySelectorAll('.lg .side a'));var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting){{a.forEach(function(x){{x.classList.toggle('on',x.getAttribute('href')==='#'+e.target.id)}})}}}})}},{{rootMargin:'-30% 0px -60% 0px'}});document.querySelectorAll('.lg .doc section').forEach(function(s){{io.observe(s)}});}})();</script>'''
page('legal.html', 'Client services · MOMENTI', 'legal', legal)

print('built', 6 + len(PIECES) + 3, 'pages')

# ================================================================== NOTES (hidden: not linked from the site)
def sb(style): return f'<div class="sbf" style="{style}"></div>'
frames = [
 (sb(f"background-image:url({I}havana-print.jpg)"), '0.0–2.0 s', 'The photograph.', 'The Prado print, full frame, perfectly still. Only the light moves: a cloud’s shadow crosses the street.'),
 (sb(f"background-image:url({I}havana-print.jpg);background-size:230%;background-position:20% 82%"), '2.0–3.8 s', 'The push.', 'A slow, real dolly-in toward the turquoise convertible at the kerb. No zoom snap, no shake.'),
 (sb(f"background-image:url({I}havana-print.jpg);background-size:420%;background-position:16% 84%"), '3.8–4.6 s', 'Closer.', 'The car fills the frame. The street behind it softens.'),
 (sb(f"background-image:url({I}havana-1958_06-car-closeup.jpg)"), '4.6–6.5 s', 'The same car.', 'A match cut: the same convertible, now die-cast, sitting on the gold rail. Same angle, same place in frame.'),
 (sb(f"background-image:url({I}havana-1958_01-front_MASTER.jpg);background-size:190%;background-position:50% 30%"), '6.5–8.0 s', 'The pull-back.', 'The camera pulls back: the street was the print on the bag all along.'),
 (sb(f"background-image:url({I}havana-1958_01-front_MASTER.jpg)"), '8.0–10 s', 'Still.', 'The camera rests on the exact composition of the home page. The film dissolves into the live page: title, italic, Reserve.'),
]
sbh = ''.join(f'<figure><div class="fw">{a}</div><figcaption><span class="lab">{c}</span><span class="lab mut">{b}</span></figcaption><p>{d}</p></figure>' for a, b, c, d in frames)
dec = [
 ('The opening film', 'Approve the storyboard below: the Prado photograph, a push-in on the car, a match cut to the same car on the clasp, a pull-back to the bag, still. If yes, it is made on Runway from the approved Havana images and dropped into the slot (one line in assets/site.js). Until then the site opens with the still fallback you see now.'),
 ('Our story, in your words', 'Send 2–3 black-and-white family photos (your grandmother on the boat, for example) and approve or rewrite the captions, the short letter from you and your quote “So much hurt and pain behind it, but also memories. I felt proud.” AS SHE PLEASES. stays as the page’s last line.'),
 ('The line-up at launch', 'Launch with five moments (Havana, Miami, New York, Tokyo, Monaco, with Monaco’s “The long way round”), going live once the Miami, Tokyo and Monaco bag images are approved. Rome ($460) and London ($540) stay off until you confirm them.'),
]
dech = ''.join(f'<div class="dec"><span class="n">{["i","ii","iii"][k]}.</span><h3 class="ser">{a}</h3><p>{b}</p></div>' for k, (a, b) in enumerate(dec))
COPY = [
 ('Everywhere', [('Menu', 'Collections · Our Story · MOMENTI · Questions · The House · Reserve. Phone: Menu · MOMENTI · Reserve.'), ('Footer', 'THE LETTER: Letters from the house: <i>new moments, first.</i> SIGN UP · You’re on the list. · MOMENTI: Collections · Our Story · The House · The Owners’ Circle · Client care · © 2026 MOMENTI · Images show the finished piece; the first pieces are in the making.')]),
 ('Home', [('Hero', 'Collection I · The Grand Tour · <i>The Prado, late morning.</i> HAVANA, 1958. <i>What you take with you.</i> RESERVE YOURS · Sold out for now. Pay nothing today.'), ('Line-up', 'THE GRAND TOUR. · See the collection'), ('Spread', 'NEW YORK, 1977. <i>Going out anyway.</i> See the moment'), ('Belief', 'Moments are the only luxury <i>you can’t buy.</i> MOMENTI is a design house that turns real moments into bags you carry. Each one begins with a single photograph. · Our story'), ('The House', 'Free to join. THE HOUSE. <i>Bring a moment.</i> Conversations with women who have a moment worth telling, evenings when there are some, and the first look at every new piece. Every so often, a member’s moment becomes a bag. INSIDE THE HOUSE'), ('The Letter', 'The Letter · Letters from the house: <i>new moments, first.</i> SIGN UP · You’re on the list.')]),
 ('Collections', [('Title', 'The bags · COLLECTIONS. <i>Each collection is a set of moments. Each bag carries one of them.</i>'), ('Collection I', 'THE GRAND TOUR. <i>Our first collection: a city in one year, for each bag, with the car from its photograph on the clasp.</i> See the collection'), ('Collection II', '<i>Coming.</i> Hear first')]),
 ('The Grand Tour', [('Title', 'Collections / The Grand Tour · THE GRAND TOUR. Collection I. <i>Our first collection. Each bag carries one photograph of a city in one year, with the car from that street on the clasp.</i>')] + [(p['name'], f"{p['title'].upper()} <i>{p['feel']}</i> ${p['price']}" if p.get('cut') else f"{p['title'].upper()} <i>Coming soon.</i> (a hairline outline of the bag)") for p in PIECES] + [('Closing', 'Every bag is sold out for now. <i>Reserve yours</i> and pay nothing until it’s ready.')]),
 ('A piece', [('Top', 'Collection I · The Grand Tour · HAVANA, 1958. <i>What you take with you.</i> Havana 1958, <i>frame clutch</i> · $520 · Sold out for now. · RESERVE YOURS · Pay nothing today. When yours is ready, you’ll have a week to change your mind.'), ('Details', 'The moment · The car · Dimensions · Materials · The back · Made · In the box · Care · Delivery · Returns'), ('Reserve', 'Reserve <i>yours.</i> Pay nothing today. We’ll tell you the moment yours is ready, and you’ll have a week to change your mind before anything is charged. · RESERVE MINE · Secure checkout. Nothing is charged until your bag is ready.'), ('After', 'Reserved. <i>Havana 1958 has your name on it.</i> We’ve sent you an email with everything you need, and we’ll be in touch the moment yours is ready.')]),
 ('The House (join.html)', [('Hero', 'Free to join. THE HOUSE. <i>Bring a moment.</i> JOIN THE HOUSE'), ('Opening', 'Every bag begins with someone’s moment. The House is where people bring theirs: <i>a city, a year, and what happened there.</i>'), ('Conversations', 'The House · An interview series. CONVERSATIONS. <i>We sit down with women who have a moment worth telling, and share part of it.</i> PLACEHOLDERS: four slots (No. 01 lead, Madrid; 02–04), each showing “Coming soon” until Pily fills name, city and pull-quote in CONVOS in build.py. The portraits are stand-ins from the kit (campaign-new-york-1977, tokyo-hero, havana-reverse, tokyo-reverse) until the real portraits are taken. No real people or quotes are invented.'), ('Tell us your moment', 'Tell us <i>your moment.</i> A city, a year, what happened, and a photograph if you have one. The best are told in Conversations. And every so often, one becomes a bag, made with the person who lived it and named after their moment. Form: city · year · what happened · a photograph · your email · SEND YOUR MOMENT · Received. <i>It’s with the house now.</i>'), ('Evenings', 'Evenings, <i>when there are some.</i> One moment for one night, city by city: a Havana, 1958, say, with the music of that year. Members hear first.'), ('First look', 'First look, <i>before anyone.</i> Each new moment reaches the House before it reaches anyone else.'), ('Join', 'COME IN. <i>Joining takes your email and, if you like, your moment.</i> JOIN THE HOUSE · You’re in. <i>Welcome to the House.</i>'), ('Upstairs', 'Own a piece? There’s a room <i>upstairs.</i> The Owners’ Circle')]),
 ('The Owners’ Circle (owners-circle.html)', [('Top', 'For owners only. The Owners’ <i>Circle.</i> Every piece arrives with a ticket. The ticket is your place here.'), ('Kept by', 'The ticket: The Owners’ Circle · New York, 1977. · KEPT BY <i>your name</i>'), ('What owners have', 'i. Kept by. Your name on your piece’s card. · ii. First to reserve. Each new piece, yours to reserve before anyone else. · iii. Owners’ evenings. When there are some. · And a few things <i>we’d rather not tell you yet.</i> (Kept short on purpose: no surprises spelled out.)'), ('Register', 'Already own a piece? <i>Register it.</i> Send the code on your ticket, and your name goes on the list of owners. REGISTER'), ('Out', 'Not an owner yet? <i>The House is free to join.</i> The House · See the collection')]),
 ('Our story (About)', [('Opening', 'Moments are the only luxury <i>you can’t buy.</i>'), ('Archive', 'Three black-and-white family photographs, captioned in Pily’s voice: “My grandmother. <i>Cuba, before they left.</i>” · “My grandfather. <i>He lived through the 1950s in Cuba.</i>” · “What they took with them. <i>Photographs like this one, and the stories behind them.</i>”'), ('Letter', 'From Pily: I named MOMENTI after <i>my grandparents’ story.</i> They had to leave Cuba. The moments they lived there became part of history, and part of us, and I wanted a way to carry them with me. So the first bag I made is Havana, 1958… “So much hurt and pain behind it, but also memories. I felt proud.” Pily'), ('How it’s made', 'The photograph. · The car. · The story.'), ('Last line', 'AS SHE PLEASES.')]),
]
OPEN = [
 ('Family photographs', 'Pily sends 2–3 black-and-white photos. Save them as assets/img/family-1.jpg, family-2.jpg, family-3.jpg and they replace the placeholders automatically (shown in black and white).'),
 ('Captions and letter', 'The three captions and the “From Pily” letter are written from facts in the brand core, in her voice. She rewrites or approves them, and approves the quote.'),
 ('Returns policy', 'The window and who pays postage (with a lawyer). Until then the site says: write to us and we’ll take care of it.'),
 ('Lead time and couriers', 'Shown nowhere yet; the site promises only tracked, insured, signed for, worldwide.'),
 ('Materials and workshop', 'The outer material and where the bag is made. The site lists only confirmed parts: frame, lining, chain, car.'),
 ('Three things, now separate', 'The Letter (the newsletter: footer and one band on home, email only). The House (join.html: the community, free; Conversations, your moment, evenings, first look). The Owners’ Circle (owners-circle.html: owners only, says little on purpose). Our Story stays at the-house.html. The kit’s “House List” becomes The Letter; voice.md and the microcopy need the same change if you approve.'),
 ('Conversations placeholders', 'Four slots show “Coming soon” (the lead says “The first conversation is being written”). Fill name, city and quote in CONVOS at the top of the House section in build.py; the images are kit stand-ins until real portraits are shot.'),
 ('Still to decide', 'How often the Letter goes out (the site names no cadence). How early owners reserve before anyone else. Whether there will be evenings (both pages say “when there are some”). How a member’s moment becomes a bag (the site says only “every so often”). Where nominated moments and photos are sent (the forms are simulated).'),
 ('Monaco and Tokyo', 'Monaco’s year, car and its line “The long way round” (proposed). Tokyo’s car. Bag images for Miami, Tokyo and Monaco.'),
 ('Stripe', 'The payment links per bag (top of assets/site.js). Until then “Reserve mine” shows the reserved state.'),
 ('Email address', 'The site uses hello@momenti.com; the site lives at houseofmomenti.com.'),
]
copyh = ''.join(f'<div class="cg"><h3 class="cap">{g}.</h3>' + ''.join(f'<div class="r"><span class="lab">{a}</span><p>{b}</p></div>' for a, b in rows) + '</div>' for g, rows in COPY)
notes_css = '''<style>
.nt{padding:120px var(--m) 120px;max-width:1360px;margin:0 auto}
.nt h1{font-size:clamp(60px,9vw,130px)}
.nt h2{font-size:52px;margin:110px 0 30px;border-top:1px solid var(--ink);padding-top:26px}
.nt .lead{font-size:21px;max-width:760px;margin-top:26px}
.decs{display:grid;grid-template-columns:repeat(3,1fr);gap:40px}
.dec .n{font-family:var(--serif);font-style:italic;font-size:24px}.dec h3{font-size:34px;margin:6px 0 12px}.dec p{font-size:17px}
.sbg{display:grid;grid-template-columns:repeat(3,1fr);gap:40px 28px}
.sbg .fw{aspect-ratio:16/9;overflow:hidden;background:#e9dccb}.sbf{width:100%;height:100%;background-size:cover;background-position:center}
.sbg figcaption{display:flex;justify-content:space-between;margin-top:12px}.sbg p{font-size:15.5px;margin-top:6px}
.cgs{display:grid;grid-template-columns:1fr 1fr;gap:50px 60px}
.cg h3{font-size:28px;letter-spacing:-.03em;margin-bottom:12px}
.cg .r{display:grid;grid-template-columns:140px 1fr;gap:18px;padding:11px 0;border-bottom:1px solid var(--hair)}
.cg .r p{font-size:15.5px}
.spec2 .r{display:grid;grid-template-columns:200px 1fr;gap:20px;padding:12px 0;border-bottom:1px solid var(--hair)}
@media(max-width:760px){.decs,.sbg,.cgs{grid-template-columns:1fr}.cg .r,.spec2 .r{grid-template-columns:1fr;gap:4px}.nt h2{font-size:36px}}
</style>'''
notes = nav() + notes_css + f'''<main class="nt">
<span class="lab mut">For Pily · not linked from the site</span>
<h1 class="cap" style="margin-top:20px">Notes.</h1>
<p class="lead">The proposal in one line: <span class="it">first the moment, then the piece.</span> Every page opens on a place and a year, the bag arrives second, and only the car ever crosses a frame. Below: the three decisions, the film, and every word on the site.</p>
<h2 class="ser">Three decisions.</h2><div class="decs">{dech}</div>
<h2 class="ser">The opening film, <span class="it">storyboard.</span></h2>
<p style="max-width:760px;margin-bottom:34px">10 seconds, silent, once per visit, skippable after one second. 16:9 for desktop and a separate 9:16 cut for phones. Its last frame is the home page’s first view, so the film never “ends”: the page wakes up around it. Made on Runway with the print file as the first frame and the master front as the last; every clip frame-checked for fake physics before you see it. Frames below are composed from the approved images as a guide. The piece pages already use this same idea when you open a bag from the line-up.</p>
<div class="sbg">{sbh}</div>
<h2 class="ser">Motion, <span class="it">in short.</span></h2>
<div class="spec2">
<div class="r"><span class="lab">The curve</span><p>“The slow car”, cubic-bezier(.22,.61,.12,1): fast to leave, long to settle. 240 ms for small things, 700–900 ms for reveals, 1.2–1.4 s for photographs settling, about 3 s for the signature.</p></div>
<div class="r"><span class="lab">What moves</span><p>The car (opening a piece: push-in, match cut, pull-back). Photographs settling as they arrive. Headlines rising line by line. The reserve sheet. The menu. The line-up, which drifts like a crowd when dragged.</p></div>
<div class="r"><span class="lab">What never moves</span><p>The wordmark, prices, buttons (no bounce), body text once landed. Nothing loops or autoplays sideways; no cursor followers. Reduced-motion settings get 200 ms crossfades and no film.</p></div>
<div class="r"><span class="lab">To try</span><p>Open a bag from The Grand Tour (Havana or New York show the signature). Hover the line-up. Drag the line on the home page. Press Reserve the next one. Open the menu. The opening plays once per visit: open a new tab to see it again.</p></div>
<div class="r"><span class="lab">What is simulated</span><p>“Reserve mine” shows the “Reserved” state instead of opening Stripe (the links go in one line of assets/site.js). Email fields show their success state but send nothing. Register a piece opens an email.</p></div>
</div>
<h2 class="ser">Open items, <span class="it">hidden from customers.</span></h2><div class="spec2">{"".join(f"<div class=\"r\"><span class=\"lab\">{a}</span><p>{b}</p></div>" for a,b in OPEN)}</div>
<h2 class="ser">The copy deck.</h2><div class="cgs">{copyh}</div>
</main>'''
page('notes.html', 'Notes · MOMENTI website proposal', 'notes', notes)
print('notes built')
