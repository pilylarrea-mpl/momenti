// Minimal Stripe REST client: no SDK, form-encoded requests with STRIPE_SECRET_KEY from Vercel.
// Returns null when no key is set, so the site falls back to a free waitlist sign-up.

function encode(obj, prefix, out = []) {
  for (const [k, v] of Object.entries(obj)) {
    if (v === undefined || v === null || v === '') continue;
    const key = prefix ? `${prefix}[${k}]` : k;
    if (typeof v === 'object') encode(v, key, out);
    else out.push(encodeURIComponent(key) + '=' + encodeURIComponent(String(v)));
  }
  return out.join('&');
}

module.exports = async function stripe(method, path, params) {
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) return null;
  const r = await fetch('https://api.stripe.com/v1/' + path, {
    method,
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/x-www-form-urlencoded' },
    body: method === 'GET' ? undefined : encode(params || {}),
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) { console.error('Stripe refused', path, r.status, j && j.error && j.error.message); throw new Error('stripe'); }
  return j;
};
module.exports.encode = encode;

// Checks a Stripe webhook signature (Stripe-Signature header) with STRIPE_WEBHOOK_SECRET.
// raw must be the exact request body as received. Rejects anything older than 5 minutes.
module.exports.verify = function verify(raw, header, secret, now = Date.now()) {
  const { createHmac, timingSafeEqual } = require('node:crypto');
  if (!raw || !header || !secret) return false;
  const parts = String(header).split(',').map(p => p.split('='));
  const t = (parts.find(p => p[0] === 't') || [])[1];
  const sigs = parts.filter(p => p[0] === 'v1').map(p => p[1]);
  if (!t || !sigs.length || Math.abs(now / 1000 - Number(t)) > 300) return false;
  const want = Buffer.from(createHmac('sha256', secret).update(`${t}.${raw}`).digest('hex'));
  return sigs.some(s => { const b = Buffer.from(String(s)); return b.length === want.length && timingSafeEqual(b, want); });
};
