// Receives a pre-order from the site and emails it to the studio.
// Needs two environment variables in Vercel: RESEND_API_KEY and ORDER_EMAIL.
// Optional: FROM_EMAIL (a sender on a domain verified in Resend).

const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });
  const o = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  const a = o.address || {};
  const missing = ['first', 'last', 'email', 'phone'].filter(k => !o[k]).concat(['line1', 'city', 'country'].filter(k => !a[k]));
  if (missing.length || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(o.email)) return res.status(400).json({ error: 'Missing or invalid fields', missing });

  const { RESEND_API_KEY, ORDER_EMAIL, FROM_EMAIL } = process.env;
  if (!RESEND_API_KEY || !ORDER_EMAIL) return res.status(503).json({ error: 'Pre-orders are not connected yet' });

  const kind = o.mode === 'first-batch-deposit' ? `First batch · $${o.deposit} deposit` : 'Pre-order';
  const rows = [
    ['Piece', `${o.name} (${o.piece})`], ['Type', kind], ['Price', `$${o.price}`],
    ['Name', `${o.first} ${o.last}`], ['Email', o.email], ['Phone', o.phone],
    ['Address', [a.line1, a.line2, a.city, a.region, a.postal, a.country].filter(Boolean).join(', ')],
    ['Edition number', o.number || 'Any'], ['Note', o.note || ''], ['News', o.news ? 'Yes' : 'No'], ['Received', new Date().toISOString()],
  ];
  const html = `<h2>${esc(kind)}: ${esc(o.name)}</h2><table cellpadding="6">${rows.map(([k, v]) => `<tr><td><b>${esc(k)}</b></td><td>${esc(v)}</td></tr>`).join('')}</table>`;

  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: FROM_EMAIL || 'Momenti <onboarding@resend.dev>', to: [ORDER_EMAIL], reply_to: o.email, subject: `${kind}: ${o.name} · ${o.first} ${o.last}`, html }),
  });
  if (!r.ok) return res.status(502).json({ error: 'Could not send', detail: await r.text() });
  res.status(200).json({ ok: true });
};
