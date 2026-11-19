// Adds someone to the House List: sends them to the Google Form in _gform.js, emails the studio
// when RESEND_API_KEY and ORDER_EMAIL are set, and adds them to a Resend audience if RESEND_AUDIENCE_ID is set.
// Optional: FROM_EMAIL. Answers ok only when the Google Form or the email really took it.

const toGoogle = require('./_gform');
const acquisition = require('./_attribution');
const meta = require('./_meta');

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });
  const o = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  const email = String(o.email || '').trim();
  const topics = Array.isArray(o.topics) ? o.topics.map(String).slice(0, 5) : [];
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return res.status(400).json({ error: 'Invalid email' });
  const from = String(o.from || 'direct').slice(0, 40), ref = String(o.ref || '').slice(0, 80), landed = String(o.landed || '').slice(0, 4096);
  const text = `HOUSE LIST · ${email}\nWants: ${topics.join(', ') || 'news'}\nCame from: ${from}${ref ? ` (referrer ${ref})` : ''}\nLanded on: ${landed}\n${acquisition(o.attribution)}\nReceived: ${new Date().toISOString()}`;

  const { RESEND_API_KEY, ORDER_EMAIL, RESEND_AUDIENCE_ID, FROM_EMAIL } = process.env;
  const h = { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' };
  const byEmail = async () => {
    if (!RESEND_API_KEY || !ORDER_EMAIL) return false;
    if (RESEND_AUDIENCE_ID) {
      await fetch(`https://api.resend.com/audiences/${RESEND_AUDIENCE_ID}/contacts`, { method: 'POST', headers: h, body: JSON.stringify({ email, unsubscribed: false }) }).catch(() => null);
    }
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST', headers: h,
      body: JSON.stringify({ from: FROM_EMAIL || 'Momenti <onboarding@resend.dev>', to: [ORDER_EMAIL], subject: `House List: ${email}`, text }),
    }).catch(() => null);
    if (r && !r.ok) console.error('Resend refused the email:', r.status, await r.text());
    return !!(r && r.ok);
  };

  const [google, sent] = await Promise.all([toGoogle(text), byEmail()]);
  if (!google && !sent) return res.status(502).json({ error: 'Could not add' });
  // Server copy of the browser's Lead (same event_id), only when the page says ad tracking is allowed.
  const m = o.meta && typeof o.meta === 'object' ? o.meta : null;
  if (m && /^[A-Za-z0-9_.:-]{8,120}$/.test(String(m.event_id || ''))) {
    const url = typeof m.url === 'string' && /^https:\/\/(www\.)?houseofmomenti\.com\//.test(m.url) ? m.url.split('?')[0] : undefined;
    const back = topics.find(t => /^back: /.test(t));
    await meta.send({ event_name: 'Lead', event_id: m.event_id, event_source_url: url,
      user: Object.assign(meta.fromRequest(req), { em: email, fbp: m.fbp, fbc: m.fbc }),
      custom_data: { content_category: back ? 'back_in_stock' : String(topics[0] || 'the letter').replace(/\s+/g, '_').slice(0, 40), content_ids: back ? [back.slice(6).trim().slice(0, 40)] : undefined } });
  }
  res.status(200).json({ ok: true, google, email: sent });
};
