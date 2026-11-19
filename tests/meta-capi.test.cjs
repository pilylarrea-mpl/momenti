// Meta pixel + Conversions API: browser/server pairing, Stripe-confirmed reservations, dedup IDs.
const {test, beforeEach} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {Readable} = require('node:stream');
const root = path.join(__dirname, '..');
const req = m => require(path.join(root, 'api', m));
const sha = v => crypto.createHash('sha256').update(v).digest('hex');

// ---- fake HTTP helpers ----
function fakeRes() { const r = {code: 200, body: null, status(c) { r.code = c; return r; }, json(b) { r.body = b; return r; }}; return r; }
function fakeReq(body, headers = {}) { return {method: 'POST', body, headers: Object.assign({'user-agent': 'UA-test', 'x-forwarded-for': '203.0.113.9, 10.0.0.1'}, headers)}; }
let calls;
function mockFetch(routes) {
  calls = [];
  globalThis.fetch = async (url, opts = {}) => {
    calls.push({url: String(url), opts});
    for (const [re, fn] of routes) if (re.test(String(url))) return fn(url, opts);
    return {ok: true, status: 200, json: async () => ({}), text: async () => ''};
  };
}
const metaCalls = () => calls.filter(c => /graph\.facebook\.com/.test(c.url)).map(c => JSON.parse(c.opts.body));
beforeEach(() => { process.env.META_CAPI_TOKEN = 'TOKEN'; delete process.env.META_TEST_EVENT_CODE; process.env.STRIPE_SECRET_KEY = 'sk_test_x'; process.env.STRIPE_WEBHOOK_SECRET = 'whsec_test'; });

const setupSession = (over = {}) => Object.assign({
  id: 'cs_test_abc123', object: 'checkout.session', mode: 'setup', status: 'complete', amount_total: 0, currency: 'usd',
  client_reference_id: 'havana-1958', setup_intent: {status: 'succeeded'}, customer: 'cus_1',
  customer_details: {email: ' Ana@Example.com ', name: 'Ana Maria Ruiz', phone: '+1 (787) 555-0100', address: {country: 'US', postal_code: '00901', city: 'San Juan', state: 'PR'}},
}, over);

// ---- _meta ----
test('_meta: hashes personal data the way Meta asks, keeps fbp/fbc/IP/UA, no-op without token', async () => {
  const meta = req('_meta.js');
  const u = meta.userData({em: ' Ana@Example.com ', ph: '+1 (787) 555-0100', fbp: 'fb.1.1700000000000.123', fbc: 'fb.1.1700000000000.AbC-_1', client_ip_address: '1.2.3.4', client_user_agent: 'UA'});
  assert.deepEqual(u.em, [sha('ana@example.com')]);
  assert.deepEqual(u.ph, [sha('17875550100')]);
  assert.equal(u.fbp, 'fb.1.1700000000000.123'); assert.equal(u.fbc, 'fb.1.1700000000000.AbC-_1');
  assert.equal(meta.userData({fbp: 'evil'}).fbp, undefined);
  delete process.env.META_CAPI_TOKEN; mockFetch([]);
  assert.equal(await meta.send({event_name: 'Lead', event_id: 'x'}), false); assert.equal(calls.length, 0);
  process.env.META_CAPI_TOKEN = 'TOKEN'; process.env.META_TEST_EVENT_CODE = 'TEST123'; mockFetch([]);
  assert.equal(await meta.send({event_name: 'Lead', event_id: 'abc12345'}), true);
  assert.match(calls[0].url, /graph\.facebook\.com\/v\d+\.\d+\/1518737959611932\/events\?access_token=TOKEN/);
  const b = metaCalls()[0]; assert.equal(b.test_event_code, 'TEST123'); assert.equal(b.data[0].action_source, 'website');
  assert.deepEqual(meta.fromRequest(fakeReq({})), {client_ip_address: '203.0.113.9', client_user_agent: 'UA-test'});
});

// ---- reservations from Stripe ----
test('_reservation: card saved ($0) = AddPaymentInfo + CompleteRegistration value 0, never Purchase', () => {
  const r = req('_reservation.js');
  const s = setupSession();
  assert.equal(r.isComplete(s), true);
  const out = r.events(s);
  assert.deepEqual(out.events.map(e => e.event_name), ['AddPaymentInfo', 'CompleteRegistration']);
  out.events.forEach(e => { assert.equal(e.event_id, 'cs_test_abc123'); assert.equal(e.custom_data.value, 0); assert.deepEqual(e.custom_data.content_ids, ['havana-1958']); assert.equal(e.custom_data.bag_price, 520); });
  assert.equal(out.events[0].user.em, ' Ana@Example.com '); assert.equal(out.events[0].user.fn, 'Ana'); assert.equal(out.events[0].user.ln, 'Ruiz');
  assert.equal(r.isComplete(setupSession({status: 'open'})), false);
  assert.equal(r.isComplete(setupSession({setup_intent: {status: 'requires_payment_method'}})), false);
  assert.equal(r.optedOut(setupSession({client_reference_id: 'havana-1958--optout'})), true);
  assert.equal(r.events(setupSession({client_reference_id: 'havana-1958--optout'})).piece, 'havana-1958');
  assert.equal(r.events(setupSession({client_reference_id: null, metadata: {piece: 'nyc'}})).piece, 'new-york-1977');
});
test('_reservation: money really charged adds Purchase with the amount charged; unpaid is not complete', () => {
  const r = req('_reservation.js');
  const s = setupSession({mode: 'payment', setup_intent: null, payment_status: 'paid', amount_total: 10000});
  const out = r.events(s);
  const p = out.events.find(e => e.event_name === 'Purchase');
  assert.equal(p.custom_data.value, 100); assert.equal(p.custom_data.currency, 'USD'); assert.equal(p.event_id, s.id);
  assert.equal(r.isComplete(Object.assign({}, s, {payment_status: 'unpaid'})), false);
});

// ---- stripe-confirm ----
test('stripe-confirm: checks with Stripe, sends server events with IP/UA/fbp and returns the same IDs', async () => {
  const handler = req('stripe-confirm.js');
  mockFetch([[/api\.stripe\.com/, () => ({ok: true, json: async () => setupSession()})]]);
  const res = fakeRes();
  await handler(fakeReq({session_id: 'cs_test_abc123', meta: {fbp: 'fb.1.1700000000000.42', url: 'https://www.houseofmomenti.com/?x=1'}}), res);
  assert.equal(res.code, 200); assert.equal(res.body.piece, 'havana-1958');
  assert.match(calls[0].url, /checkout\/sessions\/cs_test_abc123/);
  assert.equal(calls[0].opts.headers.Authorization, 'Bearer sk_test_x');
  const sent = metaCalls()[0].data;
  assert.deepEqual(sent.map(e => e.event_name), ['AddPaymentInfo', 'CompleteRegistration']);
  assert.equal(sent[0].event_id, 'cs_test_abc123'); assert.equal(sent[0].user_data.fbp, 'fb.1.1700000000000.42');
  assert.equal(sent[0].user_data.client_ip_address, '203.0.113.9'); assert.deepEqual(sent[0].user_data.em, [sha('ana@example.com')]);
  assert.equal(sent[0].event_source_url, 'https://www.houseofmomenti.com/');
  assert.deepEqual(res.body.events.map(e => [e.name, e.id]), [['AddPaymentInfo', 'cs_test_abc123'], ['CompleteRegistration', 'cs_test_abc123']]);
});
test('stripe-confirm: incomplete session, bad id, or a visitor who declined send nothing to Meta', async () => {
  const handler = req('stripe-confirm.js');
  mockFetch([[/api\.stripe\.com/, () => ({ok: true, json: async () => setupSession({status: 'open'})})]]);
  let res = fakeRes(); await handler(fakeReq({session_id: 'cs_test_abc123', meta: {}}), res);
  assert.equal(res.code, 409); assert.equal(metaCalls().length, 0);
  res = fakeRes(); await handler(fakeReq({session_id: 'nope'}), res); assert.equal(res.code, 400);
  mockFetch([[/api\.stripe\.com/, () => ({ok: true, json: async () => setupSession()})]]);
  res = fakeRes(); await handler(fakeReq({session_id: 'cs_test_abc123'}), res);   // no meta = declined in the page
  assert.equal(res.code, 200); assert.equal(metaCalls().length, 0); assert.deepEqual(res.body.events, []);
  delete process.env.STRIPE_SECRET_KEY; mockFetch([]);
  res = fakeRes(); await handler(fakeReq({session_id: 'cs_test_abc123', meta: {}}), res); assert.equal(res.code, 503);
});

// ---- stripe-webhook ----
function signed(obj, secret = 'whsec_test', t = Math.floor(Date.now() / 1000)) {
  const raw = JSON.stringify(obj);
  const sig = crypto.createHmac('sha256', secret).update(`${t}.${raw}`).digest('hex');
  const r = Readable.from([Buffer.from(raw)]);
  r.method = 'POST'; r.headers = {'stripe-signature': `t=${t},v1=${sig}`};
  return r;
}
test('stripe-webhook: verified checkout.session.completed sends the same events and IDs; forgeries are refused', async () => {
  const handler = req('stripe-webhook.js');
  assert.deepEqual(handler.config, {api: {bodyParser: false}});
  mockFetch([]);
  let res = fakeRes();
  await handler(signed({type: 'checkout.session.completed', data: {object: setupSession()}}), res);
  assert.equal(res.code, 200); assert.equal(res.body.tracked, true);
  const sent = metaCalls()[0].data;
  assert.deepEqual(sent.map(e => [e.event_name, e.event_id]), [['AddPaymentInfo', 'cs_test_abc123'], ['CompleteRegistration', 'cs_test_abc123']]);
  mockFetch([]); res = fakeRes();
  await handler(signed({type: 'checkout.session.completed', data: {object: setupSession()}}, 'whsec_wrong'), res);
  assert.equal(res.code, 400); assert.equal(metaCalls().length, 0);
  mockFetch([]); res = fakeRes();
  await handler(signed({type: 'checkout.session.completed', data: {object: setupSession({client_reference_id: 'monaco--optout'})}}), res);
  assert.equal(res.body.tracked, false); assert.equal(metaCalls().length, 0);
  mockFetch([]); res = fakeRes();
  await handler(signed({type: 'checkout.session.completed', data: {object: setupSession()}}, 'whsec_test', Math.floor(Date.now() / 1000) - 3600), res);
  assert.equal(res.code, 400, 'old signatures are refused');
});

// ---- track relay ----
test('api/track: relays browser events with server prices; refuses conversions', async () => {
  const handler = req('track.js');
  mockFetch([]);
  let res = fakeRes();
  await handler(fakeReq(JSON.stringify({event_name: 'InitiateCheckout', event_id: 'evt-12345678', data: {content_ids: ['tokyo-1995'], value: 1}, fbp: 'fb.1.1700000000000.7', url: 'https://www.houseofmomenti.com/tokyo-1995'})), res);
  assert.equal(res.code, 200);
  const e = metaCalls()[0].data[0];
  assert.equal(e.event_id, 'evt-12345678'); assert.equal(e.custom_data.value, 580, 'value from our price list, not the browser');
  assert.equal(e.user_data.client_user_agent, 'UA-test'); assert.equal(e.event_source_url, 'https://www.houseofmomenti.com/tokyo-1995');
  for (const name of ['Lead', 'CompleteRegistration', 'AddPaymentInfo', 'Purchase']) {
    mockFetch([]); res = fakeRes();
    await handler(fakeReq({event_name: name, event_id: 'evt-12345678'}), res);
    assert.equal(res.code, 400); assert.equal(metaCalls().length, 0);
  }
});

// ---- subscribe: server Lead ----
test('api/subscribe: a stored sign-up sends Lead with hashed email and the browser event ID; none without consent', async () => {
  const handler = req('subscribe.js');
  process.env.RESEND_API_KEY = ''; process.env.ORDER_EMAIL = '';
  mockFetch([[/docs\.google\.com/, () => ({ok: true, status: 200})]]);
  let res = fakeRes();
  await handler(fakeReq({email: 'Ana@Example.com', topics: ['back: monaco'], meta: {event_id: 'lead-12345678', fbp: 'fb.1.1700000000000.1'}}), res);
  assert.equal(res.code, 200);
  const e = metaCalls()[0].data[0];
  assert.equal(e.event_name, 'Lead'); assert.equal(e.event_id, 'lead-12345678');
  assert.deepEqual(e.user_data.em, [sha('ana@example.com')]); assert.equal(e.custom_data.content_category, 'back_in_stock');
  mockFetch([[/docs\.google\.com/, () => ({ok: true, status: 200})]]); res = fakeRes();
  await handler(fakeReq({email: 'ana@example.com', topics: ['the letter']}), res);
  assert.equal(metaCalls().length, 0);
  mockFetch([[/docs\.google\.com/, () => ({ok: false, status: 401})]]); res = fakeRes();
  await handler(fakeReq({email: 'ana@example.com', topics: ['the letter'], meta: {event_id: 'lead-12345678'}}), res);
  assert.equal(res.code, 502); assert.equal(metaCalls().length, 0, 'a failed sign-up is never a Lead');
});

// ---- browser: pixel and server share event IDs ----
function bootBrowser(consent) {
  const saved = new Map(consent ? [['momenti_ad_consent_v1', consent]] : []), beacons = [];
  const c = {MOMENTI_CONSENT_MODE: 'opt-out', MOMENTI_TRACKING: {metaPixelId: '1518737959611932', tiktokPixelId: ''},
    document: {readyState: 'loading', cookie: '_fbp=fb.1.1700000000000.99', addEventListener() {}, getElementById() { return null; }, createElement() { return {}; }, head: {appendChild() {}}},
    location: {search: '?fbclid=AbC', origin: 'https://www.houseofmomenti.com', pathname: '/havana-1958'},
    navigator: {sendBeacon: (u, b) => { beacons.push({u, b}); return true; }}, Blob: class { constructor(p) { this.text = p.join(''); } }, URLSearchParams,
    localStorage: {getItem: k => saved.get(k) || null, setItem: (k, v) => saved.set(k, v)}};
  c.window = c; vm.runInNewContext(fs.readFileSync(path.join(root, 'js/tracking.js'), 'utf8'), c);
  return {c, beacons: () => beacons.map(b => JSON.parse(b.b.text))};
}
test('browser: PageView/ViewContent/InitiateCheckout go to pixel and server with one shared event ID', () => {
  const {c, beacons} = bootBrowser();
  const pv = c.fbq.queue.find(a => a[1] === 'PageView');
  assert.equal(beacons()[0].event_name, 'PageView'); assert.equal(beacons()[0].event_id, pv[3].eventID);
  const id = c.momentiTrack('product_view', {content_id: 'havana-1958', value: 520, currency: 'USD', content_name: 'Havana 1958'}, 'havana-1958');
  const vc = c.fbq.queue.find(a => a[1] === 'ViewContent');
  assert.equal(JSON.stringify(vc[2].content_ids), '["havana-1958"]'); assert.equal(vc[2].value, 520); assert.equal(vc[2].currency, 'USD'); assert.equal(vc[3].eventID, id);
  const b = beacons().find(x => x.event_name === 'ViewContent');
  assert.equal(b.event_id, id); assert.equal(b.fbp, 'fb.1.1700000000000.99'); assert.match(b.fbc, /^fb\.1\.\d+\.AbC$/);
  assert.equal(b.url, 'https://www.houseofmomenti.com/havana-1958');
  c.momentiTrack('checkout_start', {content_id: 'havana-1958', value: 520});
  assert.equal(c.fbq.queue.find(a => a[1] === 'InitiateCheckout')[2].value, 520);
  assert.ok(beacons().find(x => x.event_name === 'InitiateCheckout'));
  c.momentiTrack('checkout_cancel', {content_id: 'havana-1958'}, 'cancel');
  assert.equal(c.fbq.queue.find(a => a[1] === 'CheckoutCancel')[0], 'trackCustom');
});
test('browser: Stripe events need a Checkout Session ID; Lead is not relayed (the server sends its own)', () => {
  const {c, beacons} = bootBrowser();
  assert.equal(c.momentiTrack('card_saved', {content_id: 'havana-1958'}), null);
  assert.equal(c.momentiTrack('purchase', {value: 520}), null);
  assert.equal(c.fbq.queue.filter(a => a[1] === 'AddPaymentInfo' || a[1] === 'Purchase').length, 0);
  c.momentiTrack('card_saved', {content_id: 'havana-1958', value: 0, event_id: 'cs_test_abc123'}, 'cs_test_abc123');
  c.momentiTrack('reservation_complete', {content_id: 'havana-1958', value: 0, event_id: 'cs_test_abc123'}, 'cs_test_abc123');
  assert.equal(c.fbq.queue.find(a => a[1] === 'AddPaymentInfo')[3].eventID, 'cs_test_abc123');
  assert.equal(c.fbq.queue.find(a => a[1] === 'CompleteRegistration')[3].eventID, 'cs_test_abc123');
  c.momentiTrack('lead', {content_category: 'the_letter', event_id: 'lead-12345678', value: 99}, 'a@b.co');
  const lead = c.fbq.queue.find(a => a[1] === 'Lead');
  assert.equal(lead[3].eventID, 'lead-12345678'); assert.equal(lead[2].value, undefined);
  assert.equal(beacons().filter(x => ['Lead', 'AddPaymentInfo', 'CompleteRegistration'].includes(x.event_name)).length, 0);
  assert.equal(c.momentiMeta('e1').event_id, 'e1');
});
test('browser: after a decline nothing is sent, and the server is told not to track', () => {
  const {c, beacons} = bootBrowser('denied');
  assert.equal(c.momentiTrack('product_view', {content_id: 'monaco'}), null);
  assert.equal(beacons().length, 0); assert.equal(c.momentiMeta('x'), null);
});

// ---- the page script is wired to all of it ----
test('assets/site.js: reserve flow, Stripe return, sign-ups and both copies of site.js', () => {
  const js = fs.readFileSync(path.join(root, 'assets/site.js'), 'utf8');
  assert.equal(js, fs.readFileSync(path.join(root, 'site-proposal/assets/site.js'), 'utf8'));
  assert.match(js, /adTrack\('product_view', bag\(\), PIECE\)/);
  assert.match(js, /adTrack\('preorder_start', bag\(\{ mode: 'reserve' \}\)/);
  assert.match(js, /adTrack\('checkout_start', bag\(\{ mode: 'reserve' \}\)\)/);
  assert.match(js, /client_reference_id=/); assert.match(js, /--optout/);
  assert.match(js, /\/api\/stripe-confirm/); assert.match(js, /adTrack\('checkout_cancel'/);
  assert.match(js, /form\.join:not\(\.tell-in\)/, 'the "tell me" form must not also post as a newsletter sign-up');
  assert.doesNotMatch(js, /adTrack\('preorder_submit'/, 'a click on Reserve mine is not a Lead');
  for (const f of ['havana-1958.html', 'new-york-1977.html', 'tokyo-1995.html', 'monaco.html']) {
    const html = fs.readFileSync(path.join(root, f), 'utf8');
    const slug = html.match(/data-piece="([^"]+)"/)[1];
    const price = Number(html.match(/class="name[^"]*">[\s\S]*?class="price">\$(\d+)/)[1]);
    assert.equal(req('_catalog.js').PRICES[slug], price, f + ' price matches api/_catalog.js');
  }
});
