// /go/<id>        a pick from shop/picks.json, sent on through the affiliate network.
// /go?u=...&s=... a link made on /shop/new (signed, so /go can't be used to send people anywhere else).

const { monetize, verify } = require('./_affiliate');
const shop = require('../shop/picks.json');

module.exports = (req, res) => {
  const q = req.query || {};
  let target = null, ref = '';

  if (q.id) {
    const pick = shop.picks.find(p => p.id === String(q.id));
    if (pick) { target = pick.url; ref = pick.id; }
  } else if (q.u && verify(String(q.u), q.s, process.env.LINK_SECRET)) {
    target = String(q.u); ref = String(q.r || 'link');
  }

  const out = target && monetize(target, ref);
  if (!out) { res.statusCode = 302; res.setHeader('Location', '/shop'); return res.end(); }
  // Shows in Vercel → Logs, so you can count clicks per link.
  console.log(JSON.stringify({ click: ref, network: out.network, to: new URL(target).hostname, from: req.headers.referer || '' }));
  res.statusCode = 302;
  res.setHeader('Location', out.url);
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Referrer-Policy', 'no-referrer-when-downgrade');
  res.end();
};
