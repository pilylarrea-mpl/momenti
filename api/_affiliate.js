// Turns a plain product link into one that pays you, through an affiliate network that has
// already signed up thousands of shops. No deal with each brand needed.
//
// Set one or more of these in Vercel → Settings → Environment Variables:
//   SOVRN_API_KEY      Sovrn Commerce (formerly VigLink). Covers ~50,000 shops: Nordstrom, Sephora, Shopbop...
//   SKIMLINKS_ID       Skimlinks site ID, e.g. 123456X789012. Similar coverage. Used if Sovrn is not set.
//   AMAZON_TAG         Amazon Associates tracking ID, e.g. pily-20. Sovrn and Skimlinks do not pay on Amazon.
//   LINK_SECRET        Any long random text. Signs the links made on /shop/new so nobody can reuse /go to send
//                      people to their own sites.
//   SHOP_PASSWORD      The password for /shop/new.

const crypto = require('crypto');

const isAmazon = host => /(^|\.)amazon\.(com|co\.uk|ca|de|fr|es|it|com\.mx|com\.au)$/.test(host);

function monetize(raw, ref, env = process.env) {
  let u;
  try { u = new URL(raw); } catch (_) { return null; }
  if (u.protocol !== 'https:' && u.protocol !== 'http:') return null;
  const tag = String(ref || '').replace(/[^A-Za-z0-9_-]/g, '').slice(0, 40);

  if (isAmazon(u.hostname)) {
    if (env.AMAZON_TAG) u.searchParams.set('tag', env.AMAZON_TAG);
    return { url: u.toString(), network: env.AMAZON_TAG ? 'amazon' : 'none' };
  }
  if (env.SOVRN_API_KEY) {
    const q = new URLSearchParams({ key: env.SOVRN_API_KEY, u: u.toString() });
    if (tag) q.set('cuid', tag);
    return { url: `https://redirect.viglink.com/?${q}`, network: 'sovrn' };
  }
  if (env.SKIMLINKS_ID) {
    const q = new URLSearchParams({ id: env.SKIMLINKS_ID, xs: '1', url: u.toString() });
    if (tag) q.set('xcust', tag);
    return { url: `https://go.skimresources.com/?${q}`, network: 'skimlinks' };
  }
  return { url: u.toString(), network: 'none' };
}

const sign = (url, secret) => crypto.createHmac('sha256', secret).update(url).digest('base64url').slice(0, 16);
const verify = (url, sig, secret) => {
  if (!secret || typeof sig !== 'string') return false;
  const want = Buffer.from(sign(url, secret)), got = Buffer.from(sig);
  return want.length === got.length && crypto.timingSafeEqual(want, got);
};

module.exports = { monetize, sign, verify, isAmazon };
