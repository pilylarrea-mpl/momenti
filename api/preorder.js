// Receives a pre-order from the site and delivers it to the studio:
// to the Google Form in _gform.js, and by email when RESEND_API_KEY and ORDER_EMAIL are set in Vercel.
// Optional: FROM_EMAIL (a sender on a domain verified in Resend). Once it is set, the client also gets a confirmation email.
// Answers ok only when at least one of the two really took it, so the site never confirms an order we lost.

const toGoogle = require('./_gform');
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });
  const o = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  const a = o.address || {};
  // Priority II needs only a name and email; phone and address are asked for before the piece is made.
  const deposit = o.mode === 'first-batch-deposit';
  const missing = ['first', 'last', 'email'].concat(deposit ? ['phone'] : []).filter(k => !o[k]).concat((deposit ? ['line1', 'city', 'country'] : []).filter(k => !a[k]));
  if (missing.length || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(o.email)) return res.status(400).json({ error: 'Missing or invalid fields', missing });

  const kind = deposit ? `Priority I · $${o.deposit} deposit` : 'Priority II';
  const rows = [
    ['Piece', `${o.name} (${o.piece})`], ['Type', kind], ['Price', `$${o.price}`],
    ['Name', `${o.first} ${o.last}`], ['Email', o.email], ['Phone', o.phone],
    ['Address', [a.line1, a.line2, a.city, a.region, a.postal, a.country].filter(Boolean).join(', ')],
    ['Edition number', o.number || 'Any'], ['Note', o.note || ''], ['News', o.news ? 'Yes' : 'No'],
    ['Came from', o.from || 'direct'], ['Referrer', o.ref || ''], ['Landed on', o.landed || ''], ['Received', new Date().toISOString()],
  ];
  const text = `${kind.toUpperCase()} · ${o.name}\n` + rows.map(([k, v]) => `${k}: ${v}`).join('\n');
  const html = `<h2>${esc(kind)}: ${esc(o.name)}</h2><table cellpadding="6">${rows.map(([k, v]) => `<tr><td><b>${esc(k)}</b></td><td>${esc(v)}</td></tr>`).join('')}</table>`;

  const { RESEND_API_KEY, ORDER_EMAIL, FROM_EMAIL } = process.env;
  const byEmail = async () => {
    if (!RESEND_API_KEY || !ORDER_EMAIL) return false;
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: FROM_EMAIL || 'Momenti <onboarding@resend.dev>', to: [ORDER_EMAIL], reply_to: o.email, subject: `${kind}: ${o.name} · ${o.first} ${o.last}`, html }),
    }).catch(() => null);
    if (r && !r.ok) console.error('Resend refused the email:', r.status, await r.text());
    return !!(r && r.ok);
  };

  const [google, email] = await Promise.all([toGoogle(text), byEmail()]);
  if (!google && !email) return res.status(502).json({ error: 'Could not deliver the pre-order' });

  // Confirmation to the client: only from a verified sender, since Resend's test sender can't reach other inboxes.
  if (RESEND_API_KEY && FROM_EMAIL) {
    const body = deposit
      ? `<p>Dear ${esc(o.first)},</p><p>Your Priority I place for <b>${esc(o.name)}</b> is held. If you haven't paid the $${esc(o.deposit)} deposit yet, a secure link follows within a day.</p><p>Before your piece is made, we write to you with its delivery window and the balance.</p><p>The House of Momenti</p>`
      : `<p>Dear ${esc(o.first)},</p><p>Your pre-order for <b>${esc(o.name)}</b> is received. Nothing is due today.</p><p>Before your piece is made, we write to you with its delivery window and payment, and ask for your shipping address.</p><p>The House of Momenti</p>`;
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from: FROM_EMAIL, to: [o.email], reply_to: ORDER_EMAIL || undefined, subject: `Your Momenti pre-order: ${o.name}`, html: body }),
    }).catch(() => null);
    if (r && !r.ok) console.error('Client confirmation refused:', r.status, await r.text());
  }
  res.status(200).json({ ok: true, google, email });
};
