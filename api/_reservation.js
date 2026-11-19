// Turns a completed Stripe Checkout Session into the Meta events for a reservation.
// Used by api/stripe-confirm (visitor comes back from Stripe) and api/stripe-webhook (Stripe tells us).
// Both send the same event names with event_id = the Checkout Session ID, so Meta counts each once,
// and the browser pixel uses the same IDs too.
//
// Card saved, nothing charged (setup mode or a $0 total): AddPaymentInfo + CompleteRegistration, value 0.
// Money actually charged: Purchase with the amount charged, plus AddPaymentInfo + CompleteRegistration.
// The bag's list price travels as bag_price so reports can show reserved demand without faking revenue.

const { PRICES, NAMES, slug } = require('./_catalog');

function isComplete(s) {
  if (!s || s.object !== 'checkout.session' || s.status !== 'complete') return false;
  if (s.mode === 'setup') return !s.setup_intent || typeof s.setup_intent === 'string' || s.setup_intent.status === 'succeeded';
  return s.payment_status === 'paid' || s.payment_status === 'no_payment_required';
}

function piece(s) {
  const m = s.metadata || {};
  return slug(s.client_reference_id) || slug(m.piece) || null;
}

function optedOut(s) { return /--optout$/.test(String(s.client_reference_id || '')) || (s.metadata || {}).ads === 'no'; }

function events(s, extra = {}) {
  const p = piece(s), price = p ? PRICES[p] : 0;
  const cd = s.customer_details || {}, addr = cd.address || {};
  const cust = s.customer && typeof s.customer === 'object' ? s.customer : null;
  const name = String(cd.name || (cust && cust.name) || '').trim().split(/\s+/);
  const charged = (s.amount_total || 0) / 100, currency = String(s.currency || 'usd').toUpperCase();
  const user = Object.assign({
    em: cd.email || (cust && cust.email) || s.customer_email,
    ph: cd.phone, fn: name.length > 1 ? name[0] : undefined, ln: name.length > 1 ? name[name.length - 1] : undefined,
    ct: addr.city, st: addr.state, zp: addr.postal_code, country: addr.country,
    external_id: typeof s.customer === 'string' ? s.customer : cust && cust.id,
  }, extra.user || {});
  const base = { content_ids: p ? [p] : undefined, content_name: p ? NAMES[p] : undefined, content_type: 'product', bag_price: price || undefined };
  const url = extra.event_source_url || (p ? `https://www.houseofmomenti.com/${p}` : 'https://www.houseofmomenti.com/');
  const list = [
    { event_name: 'AddPaymentInfo', custom_data: Object.assign({}, base, { value: 0, currency: 'USD' }) },
    { event_name: 'CompleteRegistration', custom_data: Object.assign({}, base, { value: 0, currency: 'USD', content_category: 'reservation', status: charged > 0 ? 'paid' : 'card_saved' }) },
  ];
  if (charged > 0) list.push({ event_name: 'Purchase', custom_data: Object.assign({}, base, { value: charged, currency }) });
  return {
    piece: p, name: p ? NAMES[p] : '', price, charged,
    events: list.map(e => Object.assign(e, { event_id: s.id, event_source_url: url, user })),
  };
}

module.exports = { isComplete, piece, optedOut, events };
