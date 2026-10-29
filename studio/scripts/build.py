# Turns studio/source/momenti.html into the site's index.html.
# Run from the repo root: python3 studio/scripts/build.py index.html
import sys
src=open(__import__('os').path.join(__import__('os').path.dirname(__file__),'..','source','momenti.html')).read()
body=src[src.index('</title>')+len('</title>'):].replace('<meta name="claude:viewport-fit-sides" content="cover">\n','',1)
head='''<!doctype html>
<html lang="en" data-paths="1">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Momenti</title>
<meta name="description" content="Momenti. Collection I: frame clutches printed with a moment, with one thing from the photograph made small enough to hold. Editions of 25, by pre-order.">
<meta property="og:title" content="Momenti">
<meta property="og:description" content="We welcome you to our first collection.">
<meta property="og:image" content="/img/og.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F2E8DD">
<link rel="icon" href="/img/favicon.png">
<link rel="preload" as="image" href="img/havana-street.jpg">
<style>:root{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
'''
html=head+body
html=html.replace('<header class="nav"','</head>\n<body>\n<header class="nav"',1)+'\n</body>\n</html>\n'
a="try{if(!db||!user)throw 0;const uid=await user.id();if(!uid)throw 0;const ref=db.collection('preorders')"
assert html.count(a)==1
html=html.replace(a,"try{const r=await fetch('/api/preorder',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(en)});if(r.ok){done();return}}catch(_){}\n "+a)
html=html.replace('href="#house"','href="/house"').replace('href="#top"','href="/"')
open(sys.argv[1],'w').write(html)
