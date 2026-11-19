// Adds someone to the House List: sends them to the Google Form in _gform.js, emails the studio
// when RESEND_API_KEY and ORDER_EMAIL are set, and adds them to a Resend audience if RESEND_AUDIENCE_ID is set.
// Optional: FROM_EMAIL. Answers ok only when the Google Form or the email really took it.

const toGoogle = require('./_gform');
const acquisition = require('./_attribution');

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });
  const o = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  const email = String(o.email || '').trim();
  const topics = Array.isArray(o.topics) ? o.topics.map(String).slice(0, 5) : [];
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return res.status(400).json({ error: 'Invalid email' });
  const details = o.details && typeof o.details === 'object' ? Object.entries(o.details).slice(0, 10).map(([k, v]) => `${String(k).slice(0, 40)}: ${String(v).slice(0, 600)}`) : [];
  const firstName = o.details && o.details['First name'] ? String(o.details['First name']).slice(0, 60) : '';
  const list = topics.includes('the house') ? 'THE HOUSE' : 'THE LETTER';
  const from = String(o.from || 'direct').slice(0, 40), ref = String(o.ref || '').slice(0, 80), landed = String(o.landed || '').slice(0, 4096);
  const text = `${list} · ${firstName ? firstName + ' · ' : ''}${email}\nWants: ${topics.join(', ') || 'news'}\n${details.length ? details.join('\n') + '\n' : ''}Came from: ${from}${ref ? ` (referrer ${ref})` : ''}\nLanded on: ${landed}\n${acquisition(o.attribution)}\nReceived: ${new Date().toISOString()}`;

  const { RESEND_API_KEY, ORDER_EMAIL, RESEND_AUDIENCE_ID, FROM_EMAIL } = process.env;
  const h = { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' };
  const byEmail = async () => {
    if (!RESEND_API_KEY || !ORDER_EMAIL) return false;
    if (RESEND_AUDIENCE_ID) {
      await fetch(`https://api.resend.com/audiences/${RESEND_AUDIENCE_ID}/contacts`, { method: 'POST', headers: h, body: JSON.stringify(firstName ? { email, first_name: firstName, unsubscribed: false } : { email, unsubscribed: false }) }).catch(() => null);
    }
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST', headers: h,
      body: JSON.stringify({ from: FROM_EMAIL || 'Momenti <onboarding@resend.dev>', to: [ORDER_EMAIL], subject: `${list === 'THE HOUSE' ? 'The House' : 'The Letter'}: ${firstName ? firstName + ' · ' : ''}${email}`, text }),
    }).catch(() => null);
    if (r && !r.ok) console.error('Resend refused the email:', r.status, await r.text());
    return !!(r && r.ok);
  };

  const [google, sent] = await Promise.all([toGoogle(text), byEmail()]);
  if (!google && !sent) return res.status(502).json({ error: 'Could not add' });
  res.status(200).json({ ok: true, google, email: sent });
};
