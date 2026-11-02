const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const source = fs.readFileSync('js/tracking.js', 'utf8');
function boot(consent, config = {metaPixelId:'123456789',tiktokPixelId:'TESTPIXEL'}) {
  const saved = new Map(consent ? [['momenti_ad_consent_v1',consent]] : []);
  const scripts = [];
  const context = {
    document: {readyState:'loading', addEventListener(){}, getElementById(){return null}, createElement(){return {}}, head:{appendChild(s){scripts.push(s.src)}}},
    localStorage: {getItem:k=>saved.get(k) || null,setItem:(k,v)=>saved.set(k,v)},
    MOMENTI_TRACKING:config,
  };
  context.window=context;
  vm.runInNewContext(source, context);
  return {context,scripts};
}
test('no advertising scripts or events before consent; do not replay past conversions', () => {
  const {context:c,scripts}=boot();
  c.momentiTrack('preorder_submit');
  assert.equal(scripts.length,0);
  c.momentiAdConsent.set('granted');
  assert.equal(scripts.length,2);
  assert.equal(c.fbq.queue.filter(a=>a[1]==='Lead').length,0);
  assert.equal(c.fbq.queue.filter(a=>a[1]==='PageView').length,1);
  c.momentiAdConsent.set('granted'); assert.equal(scripts.length,2);
});
test('blank IDs remain inactive even with consent', () => {
  const {context:c,scripts}=boot('granted',{});
  c.momentiTrack('preorder_submit'); assert.equal(scripts.length,0);
});
test('conversion mapping, duplicate guard and payload allowlist', () => {
  const {context:c}=boot('granted');
  const details={content_id:'paris',content_name:'Paris',email:'private@example.com',phone:'123',value:540};
  c.momentiTrack('preorder_submit',details,'order-1');
  c.momentiTrack('preorder_submit',details,'order-1');
  const leads=c.fbq.queue.filter(a=>a[1]==='Lead');
  assert.equal(leads.length,1); assert.equal(leads[0][0],'track');
  assert.equal(leads[0][2].email,undefined); assert.equal(leads[0][2].phone,undefined);
  assert.equal(leads[0][2].value,undefined);
  assert.equal(c.ttq.filter(a=>a[0]==='track'&&a[1]==='SubmitForm').length,1);
  c.momentiTrack('house_list_signup');
  assert.equal(c.fbq.queue.filter(a=>a[1]==='CompleteRegistration').length,1);
  c.momentiTrack('deposit_checkout',details);
  assert.equal(c.fbq.queue.find(a=>a[1]==='InitiateCheckout')[2].value,100);
  c.momentiTrack('purchase',details);
  assert.equal(c.fbq.queue.filter(a=>a[1]==='Purchase').length,0);
});
test('decline or withdrawal suppresses subsequent events', () => {
  const {context:c}=boot('granted'); c.momentiAdConsent.set('denied');
  const before=c.fbq.queue.length; c.momentiTrack('preorder_submit');
  assert.equal(c.fbq.queue.length,before);
  assert.equal(c.fbq.queue.at(-1)[1],'revoke');
  assert.equal(c.ttq.at(-1)[0],'revokeConsent');
  assert.equal(boot('denied').scripts.length,0);
});
test('consent can be granted again after withdrawal without reinitializing pixels', () => {
  const {context:c,scripts}=boot('granted');
  c.momentiAdConsent.set('denied');
  c.momentiAdConsent.set('granted');
  assert.equal(scripts.length,2);
  assert.equal(c.fbq.queue.at(-1)[1],'grant');
  assert.equal(c.ttq.at(-1)[0],'grantConsent');
  c.momentiTrack('preorder_submit',{},'after-regrant');
  assert.equal(c.fbq.queue.filter(a=>a[1]==='Lead').length,1);
});
for (const file of ['index.html','studio/source/momenti.html']) {
  test(file+': only successful House List submissions convert', async () => {
    const html=fs.readFileSync(file,'utf8');
    const start=html.indexOf('async function subscribe(email,topics){');
    const end=html.indexOf('const okEmail=',start);
    let calls=[];
    const c={fetch:async()=>({ok:false}),toGoogle:async()=>false,db:null,user:null,cameFrom:()=>({}),logStep(){},adTrack:(...args)=>calls.push(args)};
    vm.createContext(c); vm.runInContext(html.slice(start,end),c);
    assert.equal(await c.subscribe('test@example.com',[]),false); assert.equal(calls.length,0);
    c.fetch=async()=>({ok:true});
    assert.equal(await c.subscribe('test@example.com',[]),true);
    assert.equal(calls.length,1); assert.equal(calls[0][0],'house_list_signup');
    // Validate the actual success callback in each page independently of DOM rendering.
    const callbackStart=html.indexOf('const done=()=>{');
    const callbackEnd=html.indexOf('\n try{',callbackStart);
    const snippet=html.slice(callbackStart,callbackEnd);
    assert.match(snippet,/adTrack\('preorder_submit'/);
    if (file === 'index.html') assert.match(html,/if\(r.ok\)\{done\(\);return\}/);
    else assert.match(html,/if\(await toGoogle\(txt\)\)\{done\(\);return\}/);
    assert.match(html,/\/js\/tracking-config.js/);
  });
}
