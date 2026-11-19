// Server copy (Meta Conversions API) of browser events that have no server step of their own:
// bag views, opening the reserve sheet, going to Stripe, returning without finishing,
// email and social clicks. The page sends the same event_id the pixel used, so Meta counts
// each action once. Conversions (reservations, sign-ups) are NOT accepted here: those are only
// sent by the server after Stripe or the sign-up really succeeded.

const meta = require('./_meta');
const { PRICES, NAMES, slug } = require('./_catalog');
const ALLOWED = new Set(['PageView', 'ViewContent', 'PreorderStart', 'InitiateCheckout', 'CheckoutCancel', 'Contact', 'SocialClick']);

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });
  let o;
  try { o = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {}); } catch (_) { return res.status(400).json({ error: 'Bad JSON' }); }
  const name = String(o.event_name || ''), id = String(o.event_id || '');
  if (!ALLOWED.has(name) || !/^[A-Za-z0-9_.:-]{8,120}$/.test(id)) return res.status(400).json({ error: 'Not accepted' });
  const url = typeof o.url === 'string' && /^https:\/\/(www\.)?houseofmomenti\.com\//.test(o.url) ? o.url.split('?')[0].slice(0, 500) : undefined;
  const d = o.data && typeof o.data === 'object' ? o.data : {};
  const cd = {};
  const p = slug(Array.isArray(d.content_ids) ? d.content_ids[0] : d.content_id);
  if (p) { cd.content_ids = [p]; cd.content_name = NAMES[p]; cd.content_type = 'product'; }
  // Values come from our own price list, never from the browser.
  if (p && (name === 'ViewContent' || name === 'InitiateCheckout' || name === 'PreorderStart')) { cd.value = PRICES[p]; cd.currency = 'USD'; }
  ['destination', 'source', 'content_category'].forEach(k => { if (typeof d[k] === 'string') cd[k] = d[k].slice(0, 60); });
  const sent = await meta.send({ event_name: name, event_id: id, event_source_url: url,
    user: Object.assign(meta.fromRequest(req), { fbp: o.fbp, fbc: o.fbc }), custom_data: cd });
  res.status(200).json({ ok: true, sent });
};
