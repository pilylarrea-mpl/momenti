const {test}=require('node:test');
const assert=require('node:assert/strict');
const vm=require('node:vm');
const fs=require('node:fs');
const source=fs.readFileSync('js/attribution.js','utf8');
const sanitize=require('../api/_attribution');
function visit(search,store={},referrer='',ua='') {
 const context={URL,URLSearchParams,Date,location:{search},document:{referrer},navigator:{userAgent:ua},sessionStorage:{getItem:k=>store[k],setItem:(k,v)=>store[k]=v},window:{}};
 vm.runInNewContext(source,context);
 return JSON.parse(JSON.stringify(context.window.momentiAttribution()));
}
test('all four paid identifiers survive navigation and a direct revisit in session',()=>{
 const store={};
 visit('?utm_source=instagram&utm_medium=paid_social&utm_campaign=havana&campaign_id=123&adset_id=456&ad_id=789&utm_content=cafe',store);
 const a=visit('',store);
 assert.equal(a.first.ad_id,'789');assert.equal(a.last.adset_id,'456');assert.equal(a.last.channel,'paid_social');
});
test('organic tagged link is distinct; first and last touches are retained',()=>{
 const store={};visit('?utm_source=instagram&utm_medium=organic_social&utm_content=bio',store);
 const a=visit('?utm_source=instagram&utm_medium=paid_social&ad_id=789',store);
 assert.equal(a.first.channel,'organic_social');assert.equal(a.last.channel,'paid_social');
});
test('fbclid and Instagram browser never imply paid or organic',()=>{
 assert.equal(visit('?fbclid=abc',{},'','Instagram').last.channel,'unknown');
 assert.equal(visit('',{},'https://instagram.com/').last.channel,'unknown');
 assert.equal(visit('',{},'','Instagram').last.channel,'unknown');
});
test('blocked storage still returns acquisition evidence',()=>{
 const a=visit('?utm_source=instagram&utm_medium=paid_social&ad_id=789',Object.freeze({}));assert.equal(a.last.ad_id,'789');
});
test('server recalculates classification rather than trusting declared channel',()=>{
 const a=JSON.parse(sanitize({version:1,last:{channel:'paid_social',social_click:true}}).split('Acquisition evidence: ')[1]);assert.equal(a.last.channel,'unknown');
 assert.equal(sanitize(null),'Acquisition: unknown (legacy submission)');
});
