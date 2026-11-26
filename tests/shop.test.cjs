const {test} = require('node:test');
const assert = require('node:assert/strict');
const {monetize, sign, verify} = require('../api/_affiliate');
const go = require('../api/go');

test('Sovrn wraps any shop and tags the click with the pick id', () => {
  const o = monetize('https://www.nordstrom.com/s/bag', 'pick-1', {SOVRN_API_KEY: 'K'});
  const u = new URL(o.url);
  assert.equal(o.network, 'sovrn');
  assert.equal(u.hostname, 'redirect.viglink.com');
  assert.equal(u.searchParams.get('u'), 'https://www.nordstrom.com/s/bag');
  assert.equal(u.searchParams.get('cuid'), 'pick-1');
});
test('Skimlinks is used when Sovrn is not set', () => {
  const o = monetize('https://www.sephora.com/x', 'a', {SKIMLINKS_ID: '123X456'});
  assert.equal(o.network, 'skimlinks');
  assert.equal(new URL(o.url).searchParams.get('url'), 'https://www.sephora.com/x');
});
test('Amazon gets the Associates tag, not the network', () => {
  const o = monetize('https://www.amazon.com/dp/B01?tag=someoneelse-20', 'a', {AMAZON_TAG: 'pily-20', SOVRN_API_KEY: 'K'});
  assert.equal(o.network, 'amazon');
  assert.equal(new URL(o.url).searchParams.get('tag'), 'pily-20');
});
test('rejects non-web links', () => {
  assert.equal(monetize('javascript:alert(1)'), null);
  assert.equal(monetize('not a url'), null);
});
test('signed links verify; tampered ones do not', () => {
  const s = sign('https://a.com/x', 'secret');
  assert.ok(verify('https://a.com/x', s, 'secret'));
  assert.ok(!verify('https://evil.com/x', s, 'secret'));
  assert.ok(!verify('https://a.com/x', s, ''));
});
function run(query) {
  const res = {headers: {}, setHeader(k, v) { this.headers[k] = v; }, end() {}};
  go({query, headers: {}}, res);
  return res;
}
test('/go/<id> redirects a known pick; unknown ids and unsigned links go back to /shop', () => {
  const log = console.log; console.log = () => {};
  try {
    assert.equal(run({id: 'example-1'}).headers.Location, 'https://www.nordstrom.com/');
    assert.equal(run({id: 'nope'}).headers.Location, '/shop');
    assert.equal(run({u: 'https://evil.com', s: 'x'}).headers.Location, '/shop');
  } finally { console.log = log; }
});
