// Used by /shop/new: paste any product link, get back a short link that pays you.
const { monetize, sign } = require('./_affiliate');

module.exports = (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });
  let o;
  try { o = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {}); } catch (_) { return res.status(400).json({ error: 'Bad JSON' }); }
  const { SHOP_PASSWORD, LINK_SECRET } = process.env;
  if (!SHOP_PASSWORD || !LINK_SECRET) return res.status(503).json({ error: 'Set SHOP_PASSWORD and LINK_SECRET in Vercel first.' });
  if (String(o.password || '') !== SHOP_PASSWORD) return res.status(401).json({ error: 'Wrong password' });

  const url = String(o.url || '').trim();
  const out = monetize(url, o.ref);
  if (!out) return res.status(400).json({ error: 'That is not a web link' });
  const ref = String(o.ref || '').replace(/[^A-Za-z0-9_-]/g, '').slice(0, 40) || 'link';
  const host = `https://${req.headers.host}`;
  const q = new URLSearchParams({ u: url, s: sign(url, LINK_SECRET), r: ref });
  res.status(200).json({ link: `${host}/go?${q}`, network: out.network });
};
