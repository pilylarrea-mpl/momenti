// Called when a visitor returns from Stripe. Confirms with Stripe that the card was really saved,
// records the waitlist place (Google Form + email), and tells the page so it can show the
// confirmation and send the Purchase event. Only a completed, succeeded setup counts.

const stripe = require('./_stripe');
const toGoogle = require('./_gform');
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Use POST' });
  const o = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  const id = String(o.session_id || '');
  if (!/^cs_[A-Za-z0-9_]+$/.test(id)) return res.status(400).json({ error: 'Invalid session' });
  let s;
  try { s = await stripe('GET', `checkout/sessions/${id}?expand[]=setup_intent&expand[]=customer`); } catch (_) { return res.status(502).json({ error: 'Stripe unreachable' }); }
  if (!s) return res.status(503).json({ error: 'Stripe not set up' });
  const ok = s.mode === 'setup' && s.status === 'complete' && s.setup_intent && s.setup_intent.status === 'succeeded';
  if (!ok) return res.status(409).json({ error: 'Card not saved' });

  const m = s.metadata || {}, c = s.customer || {};
  const price = Number(m.price) || 0;
  const rows = [['Piece', `${m.name} (${m.piece})`], ['Type', 'Waitlist · card saved, $0 charged'], ['Price', `$${price}`], ['Name', c.name || ''], ['Email', c.email || ''],
    ['Stripe customer', c.id || ''], ['Note', m.note || ''], ['News', m.news || ''], ['Came from', m.from || ''], ['UTM', [m.utm_source, m.utm_campaign, m.utm_content].filter(Boolean).join(' / ')], ['Session', id], ['Received', new Date().toISOString()]];

  // Record once per session: the Stripe customer remembers that it was recorded.
  if (!(c.metadata && c.metadata['recorded_' + id.slice(-12)])) {
    const text = `WAITLIST (CARD SAVED) · ${m.name}\n` + rows.map(([k, v]) => `${k}: ${v}`).join('\n');
    const html = `<h2>Waitlist, card saved: ${esc(m.name)}</h2><table cellpadding="6">${rows.map(([k, v]) => `<tr><td><b>${esc(k)}</b></td><td>${esc(v)}</td></tr>`).join('')}</table>`;
    const { RESEND_API_KEY, ORDER_EMAIL, FROM_EMAIL } = process.env;
    const send = (to, subject, body, key) => fetch('https://api.resend.com/emails', {
      method: 'POST', headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json', 'Idempotency-Key': key },
      body: JSON.stringify({ from: FROM_EMAIL || 'Momenti <onboarding@resend.dev>', to: [to], reply_to: to === ORDER_EMAIL ? c.email : ORDER_EMAIL || undefined, subject, html: body }),
    }).catch(() => null);
    await Promise.all([
      toGoogle(text),
      RESEND_API_KEY && ORDER_EMAIL ? send(ORDER_EMAIL, `Waitlist, card saved: ${m.name} · ${c.name}`, html, 'wl-studio-' + id) : null,
      RESEND_API_KEY && FROM_EMAIL && c.email ? send(c.email, `Your ${m.name}`, `<p>Dear ${esc(String(c.name || '').split(' ')[0])},</p><p>You're on the waitlist for the ${esc(m.name)}. Nothing has been charged.</p><p>When your piece is made, we'll write at least a week before your card is charged, with your delivery window. To leave the waitlist, reply to this email. That's all it takes.</p><p>Pily<br>Momenti</p>`, 'wl-client-' + id) : null,
    ]);
    try { await stripe('POST', `customers/${c.id}`, { metadata: { ['recorded_' + id.slice(-12)]: 'yes' } }); } catch (_) {}
  }
  res.status(200).json({ ok: true, piece: m.piece, name: m.name, price });
};
