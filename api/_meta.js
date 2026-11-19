// Meta Conversions API (server-side events). Needs META_CAPI_TOKEN in Vercel
// (Events Manager > the MOMENTI pixel > Settings > Conversions API > Generate access token).
// Optional: META_TEST_EVENT_CODE to see server events under Test Events while checking.
// Without a token every call is a quiet no-op, so the site works the same.
// Browser and server copies of one action carry the same event_id, so Meta counts it once.

const { createHash } = require('node:crypto');
const PIXEL_ID = process.env.META_PIXEL_ID || '1518737959611932';
const API = 'https://graph.facebook.com/v21.0';

const sha = v => createHash('sha256').update(v).digest('hex');
const norm = {
  em: v => String(v).trim().toLowerCase(),
  ph: v => String(v).replace(/\D/g, ''),
  fn: v => String(v).trim().toLowerCase(),
  ln: v => String(v).trim().toLowerCase(),
  ct: v => String(v).toLowerCase().replace(/[^a-z]/g, ''),
  st: v => String(v).toLowerCase().replace(/[^a-z]/g, ''),
  zp: v => String(v).toLowerCase().replace(/\s/g, '').split('-')[0],
  country: v => String(v).trim().toLowerCase().slice(0, 2),
  external_id: v => String(v).trim(),
};

// Personal fields are hashed (SHA-256, normalised as Meta asks); fbp/fbc/IP/user agent are sent as is.
function userData(u = {}) {
  const out = {};
  for (const k of Object.keys(norm)) {
    if (u[k] === undefined || u[k] === null || u[k] === '') continue;
    const v = norm[k](u[k]);
    if (v) out[k] = [sha(v)];
  }
  if (out.em && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(norm.em(u.em))) delete out.em;
  if (typeof u.fbp === 'string' && /^fb\.\d\.\d+\.\d+$/.test(u.fbp)) out.fbp = u.fbp;
  if (typeof u.fbc === 'string' && /^fb\.\d\.\d+\..{1,500}$/.test(u.fbc)) out.fbc = u.fbc;
  if (u.client_ip_address) out.client_ip_address = String(u.client_ip_address);
  if (u.client_user_agent) out.client_user_agent = String(u.client_user_agent).slice(0, 512);
  return out;
}

// IP and user agent of the visitor, from the request Vercel received.
function fromRequest(req) {
  const h = (req && req.headers) || {};
  const ip = String(h['x-real-ip'] || h['x-forwarded-for'] || '').split(',')[0].trim();
  return { client_ip_address: ip || undefined, client_user_agent: h['user-agent'] || undefined };
}

// One event: {event_name, event_id, event_source_url, custom_data, user}
function build(e) {
  return {
    event_name: e.event_name,
    event_time: Math.floor((e.event_time || Date.now()) / 1000),
    event_id: String(e.event_id || '').slice(0, 200) || undefined,
    action_source: 'website',
    event_source_url: e.event_source_url || 'https://www.houseofmomenti.com/',
    user_data: userData(e.user),
    custom_data: e.custom_data && Object.keys(e.custom_data).length ? e.custom_data : undefined,
  };
}

async function send(events) {
  const token = process.env.META_CAPI_TOKEN;
  const list = (Array.isArray(events) ? events : [events]).filter(Boolean);
  if (!token || !list.length) return false;
  const body = { data: list.map(build) };
  if (process.env.META_TEST_EVENT_CODE) body.test_event_code = process.env.META_TEST_EVENT_CODE;
  try {
    const r = await fetch(`${API}/${PIXEL_ID}/events?access_token=${encodeURIComponent(token)}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
    });
    if (!r.ok) console.error('Meta CAPI refused:', r.status, (await r.text()).slice(0, 300));
    return r.ok;
  } catch (err) {
    console.error('Meta CAPI unreachable:', err && err.message);
    return false;
  }
}

module.exports = { send, build, userData, fromRequest, PIXEL_ID };
