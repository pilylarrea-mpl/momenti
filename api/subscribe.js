// Adds someone to the House List: sends them to the Google Form in _gform.js, emails the studio
// when RESEND_API_KEY and ORDER_EMAIL are set, and adds them to a Resend audience if RESEND_AUDIENCE_ID is set.
// Optional: FROM_EMAIL. Answers ok only when the Google Form or the email really took it.

const toGoogle = require('./_gform');

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });
  const o = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  const email = String(o.email || '').trim();
  const topics = Array.isArray(o.topics) ? o.topics.map(String).slice(0, 5) : [];
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return res.status(400).json({ error: 'Invalid email' });
  const text = `HOUSE LIST · ${email}\nWants: ${topics.join(', ') || 'news'}\nReceived: ${new Date().toISOString()}`;

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
  res.status(200).json({ ok: true, google, email: sent });
};
