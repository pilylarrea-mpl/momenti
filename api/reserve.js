// Starts a waitlist place: creates a Stripe customer and a Checkout session in setup mode,
// which saves a card without charging it. Answers 503 when STRIPE_SECRET_KEY is not set,
// so the site falls back to a free waitlist sign-up.

const stripe = require('./_stripe');
const PRICES = { havana: 520, miami: 500, nyc: 560, tokyo: 580, monaco: 600 };   // keep in step with P in index.html

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });
  if (!process.env.STRIPE_SECRET_KEY) return res.status(503).json({ error: 'Stripe not set up', fallback: true });
  const o = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  const base = String(o.piece || '').split(':')[0];
  const price = PRICES[base];
  if (!price || !o.first || !o.last || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(o.email || '')) return res.status(400).json({ error: 'Missing or invalid fields' });

  const origin = `https://${req.headers['x-forwarded-host'] || req.headers.host}`;
  const a = o.attribution || {};
  const meta = {
    piece: String(o.piece).slice(0, 80), name: String(o.name || '').slice(0, 80), price: String(price),
    note: String(o.note || '').slice(0, 450), news: o.news ? 'yes' : 'no', from: String(o.from || '').slice(0, 80),
    utm_source: String(a.utm_source || '').slice(0, 100), utm_campaign: String(a.utm_campaign || '').slice(0, 100), utm_content: String(a.utm_content || '').slice(0, 100),
  };
  try {
    const customer = await stripe('POST', 'customers', { email: o.email, name: `${o.first} ${o.last}`, metadata: meta });
    const session = await stripe('POST', 'checkout/sessions', {
      mode: 'setup', currency: 'usd', customer: customer.id,
      success_url: `${origin}/?session_id={CHECKOUT_SESSION_ID}&piece=${encodeURIComponent(o.piece)}`,
      cancel_url: `${origin}/?waitlist=cancelled&piece=${encodeURIComponent(o.piece)}`,
      metadata: meta, setup_intent_data: { metadata: meta },
      custom_text: { submit: { message: `Nothing is charged today. You allow Momenti to charge $${price} to this card when your ${o.name || 'piece'} is ready to ship. We email at least 7 days before, and you can cancel any time before then.` } },
    });
    return res.status(200).json({ url: session.url });
  } catch (_) {
    return res.status(502).json({ error: 'Could not start the waitlist' });
  }
};
