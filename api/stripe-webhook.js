// Stripe webhook: checkout.session.completed (and async_payment_succeeded).
// Sends the reservation events to Meta from the server even if the visitor closes the tab
// before coming back to the site. Same event names and IDs as api/stripe-confirm, so Meta
// counts each reservation once. Needs STRIPE_WEBHOOK_SECRET (from the webhook endpoint in Stripe)
// and META_CAPI_TOKEN. Endpoint: https://www.houseofmomenti.com/api/stripe-webhook

const stripe = require('./_stripe');
const meta = require('./_meta');
const r = require('./_reservation');

function rawBody(req) {
  if (typeof req.rawBody === 'string' || Buffer.isBuffer(req.rawBody)) return Promise.resolve(String(req.rawBody));
  return new Promise((resolve) => {
    const chunks = [];
    req.on('data', c => chunks.push(Buffer.from(c)));
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', () => resolve(''));
  });
}

const handler = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });
  const secret = process.env.STRIPE_WEBHOOK_SECRET;
  if (!secret) return res.status(503).json({ error: 'Webhook secret not set' });
  const raw = await rawBody(req);
  if (!stripe.verify(raw, req.headers['stripe-signature'], secret)) return res.status(400).json({ error: 'Bad signature' });
  let evt;
  try { evt = JSON.parse(raw); } catch (_) { return res.status(400).json({ error: 'Bad JSON' }); }
  const ok = ['checkout.session.completed', 'checkout.session.async_payment_succeeded'].includes(evt.type);
  const s = ok && evt.data && evt.data.object;
  if (!s || !r.isComplete(s) || r.optedOut(s)) return res.status(200).json({ received: true, tracked: false });
  const out = r.events(s);
  const sent = await meta.send(out.events);
  res.status(200).json({ received: true, tracked: sent });
};

module.exports = handler;
// Keep the body raw so the Stripe signature can be checked.
module.exports.config = { api: { bodyParser: false } };
