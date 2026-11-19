// Called by the page when a visitor comes back from Stripe with ?session_id=cs_...
// Asks Stripe whether that Checkout Session really completed (card saved or paid). Only then it
// sends the reservation events to Meta from the server, with the visitor's IP, browser, _fbp/_fbc
// and hashed email, and answers the page with the same event IDs so the pixel copy is deduplicated.
// Needs STRIPE_SECRET_KEY (and META_CAPI_TOKEN for the server events).

const stripe = require('./_stripe');
const meta = require('./_meta');
const r = require('./_reservation');

// A card saved in the reserve sheet (api/reserve.js) is a SetupIntent, not a Checkout Session.
// Shape it like a completed setup-mode session so the same reservation events come out.
function fromSetupIntent(si) {
  if (!si) return si;
  const c = si.customer && typeof si.customer === 'object' ? si.customer : null;
  return {
    object: 'checkout.session', id: si.id, mode: 'setup', status: si.status === 'succeeded' ? 'complete' : 'open',
    setup_intent: si, metadata: si.metadata || {}, customer: c || si.customer, amount_total: 0, currency: 'usd',
    customer_details: { email: c && c.email, name: c && c.name },
  };
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });
  let o;
  try { o = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {}); } catch (_) { return res.status(400).json({ error: 'Bad JSON' }); }
  const id = String(o.session_id || '');
  if (!/^(cs|seti)_[A-Za-z0-9_]+$/.test(id)) return res.status(400).json({ error: 'Invalid session' });
  let s;
  try { s = id.startsWith('seti_') ? fromSetupIntent(await stripe('GET', `setup_intents/${id}?expand[]=customer`)) : await stripe('GET', `checkout/sessions/${id}?expand[]=setup_intent`); } catch (_) { return res.status(502).json({ error: 'Stripe unreachable' }); }
  if (!s) return res.status(503).json({ error: 'Stripe not set up' });
  if (!r.isComplete(s)) return res.status(409).json({ error: 'Not completed' });

  const m = o.meta && typeof o.meta === 'object' ? o.meta : null;
  const url = m && typeof m.url === 'string' && /^https:\/\/(www\.)?houseofmomenti\.com\//.test(m.url) ? m.url.split('?')[0] : undefined;
  const out = r.events(s, { event_source_url: url, user: Object.assign(meta.fromRequest(req), m ? { fbp: m.fbp, fbc: m.fbc } : {}) });
  // Visitor declined ad tracking (in the page, or marked on the session): no server events.
  const tracked = !!m && !r.optedOut(s);
  if (tracked) await meta.send(out.events);
  res.status(200).json({
    ok: true, piece: out.piece, name: out.name, price: out.price, charged: out.charged,
    events: tracked ? out.events.map(e => ({ name: e.event_name, id: e.event_id, data: e.custom_data })) : [],
  });
};
