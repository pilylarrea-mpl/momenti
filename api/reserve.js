// Reserve on the bag page: saves the visitor's card with Stripe and charges nothing.
// The card form lives inside the MOMENTI reserve sheet (Stripe's card fields, our page); nobody is sent to Stripe.
//   GET                                  -> { pk }           publishable key for the card fields
//   POST { piece, name, email, ads }     -> { clientSecret } Customer + SetupIntent for that bag
// After the browser confirms the card, it calls api/stripe-confirm with the SetupIntent ID (seti_...)
// and the usual reservation events go to Meta.
// Needs STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY in Vercel.
// Charge later in Stripe: Customers -> the buyer -> saved card -> Create payment.

const stripe = require('./_stripe');
const { PRICES, NAMES, slug } = require('./_catalog');

module.exports = async (req, res) => {
  if (req.method === 'GET') {
    const pk = process.env.STRIPE_PUBLISHABLE_KEY;
    return pk ? res.status(200).json({ pk }) : res.status(503).json({ error: 'Stripe not set up' });
  }
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });
  let o;
  try { o = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {}); } catch (_) { return res.status(400).json({ error: 'Bad JSON' }); }
  const piece = slug(o.piece);
  const name = String(o.name || '').trim().slice(0, 120), email = String(o.email || '').trim().slice(0, 200);
  if (!piece) return res.status(400).json({ error: 'Unknown piece' });
  if (!name) return res.status(400).json({ error: 'Please add your name.' });
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return res.status(400).json({ error: 'Please add a valid email.' });
  const meta = { piece, bag_price: PRICES[piece], ads: o.ads === 'no' ? 'no' : undefined };
  try {
    const c = await stripe('POST', 'customers', {
      email, name, metadata: meta,
      description: `Reserved ${NAMES[piece]} ($${PRICES[piece]}). Nothing charged; charge when the bag is ready.`,
    });
    if (!c) return res.status(503).json({ error: 'Stripe not set up' });
    const si = await stripe('POST', 'setup_intents', {
      customer: c.id, usage: 'off_session', payment_method_types: ['card'], metadata: meta,
      description: `${NAMES[piece]} reservation, $${PRICES[piece]}, nothing charged today`,
    });
    res.status(200).json({ clientSecret: si.client_secret });
  } catch (_) {
    res.status(502).json({ error: 'Something went wrong. Please try again in a moment.' });
  }
};
