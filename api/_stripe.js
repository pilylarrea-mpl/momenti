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
