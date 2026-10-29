// Adds someone to the House List: emails the studio, and adds them to a Resend audience if one is set.
// Environment variables: RESEND_API_KEY, ORDER_EMAIL, optional RESEND_AUDIENCE_ID and FROM_EMAIL.

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });
  const o = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  const email = String(o.email || '').trim();
  const topics = Array.isArray(o.topics) ? o.topics.map(String).slice(0, 5) : [];
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return res.status(400).json({ error: 'Invalid email' });

  const { RESEND_API_KEY, ORDER_EMAIL, RESEND_AUDIENCE_ID, FROM_EMAIL } = process.env;
  if (!RESEND_API_KEY || !ORDER_EMAIL) return res.status(503).json({ error: 'The list is not connected yet' });
  const h = { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' };

  if (RESEND_AUDIENCE_ID) {
    await fetch(`https://api.resend.com/audiences/${RESEND_AUDIENCE_ID}/contacts`, { method: 'POST', headers: h, body: JSON.stringify({ email, unsubscribed: false }) });
  }
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST', headers: h,
    body: JSON.stringify({ from: FROM_EMAIL || 'Momenti <onboarding@resend.dev>', to: [ORDER_EMAIL], subject: `House List: ${email}`, text: `${email}\nWants: ${topics.join(', ') || 'news'}\n${new Date().toISOString()}` }),
  });
  if (!r.ok) return res.status(502).json({ error: 'Could not add', detail: await r.text() });
  res.status(200).json({ ok: true });
};
