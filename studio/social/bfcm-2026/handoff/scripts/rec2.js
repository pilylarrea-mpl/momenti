const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [,,url,name]=process.argv;const b=await chromium.launch();
const ctx=await b.newContext({viewport:{width:430,height:764},deviceScaleFactor:2,isMobile:true,hasTouch:true,userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',locale:'en-US',recordVideo:{dir:'v_'+name,size:{width:860,height:1528}}});
const p=await ctx.newPage();const t0=Date.now();const log=[];const mark=m=>log.push([m,(Date.now()-t0)/1000]);
await p.goto(url,{waitUntil:'domcontentloaded',timeout:45000});await p.waitForTimeout(2500);mark('loaded');
// wait for a sign-up popup and close it the way a person would
const closers=['[aria-label="Close dialog"]','[aria-label="Close form"]','button[aria-label*="lose" i]','.klaviyo-close-form','[class*="modal"] [class*="close"]','[class*="popup"] [class*="close"]','button:has-text("No thanks")','button:has-text("No, thanks")'];
for(let k=0;k<14;k++){let done=false;for(const s of closers){try{const e=p.locator(s).first();if(await e.isVisible({timeout:150})){await p.waitForTimeout(500);await e.click({timeout:1000});done=true;mark('closed');break;}}catch(e){}}if(done)break;await p.waitForTimeout(500);}
for(const s of ['button:has-text("Accept")','button:has-text("Got it")','button:has-text("Close")']){try{const e=p.locator(s).first();if(await e.isVisible({timeout:200})){await e.click({timeout:800});}}catch(e){}}
await p.waitForTimeout(900);mark('clean');
// find the price and bring it to the middle with a slow, human scroll
const y=await p.evaluate(()=>{const els=[...document.querySelectorAll('s,del,[class*="compare"],[class*="was"],[class*="price"]')].filter(e=>/\$\s?\d/.test(e.textContent)&&e.getBoundingClientRect().height>0&&e.getBoundingClientRect().top>60);return els.length?els[0].getBoundingClientRect().top+window.scrollY:600;});
const target=Math.max(0,y-380);let cur=0;while(cur<target-4){const d=Math.min(70,target-cur);await p.mouse.wheel(0,d);cur+=d;await p.waitForTimeout(120);}
mark('price');await p.waitForTimeout(3200);await p.screenshot({path:name+'.png'});mark('end');
for(let i=0;i<6;i++){await p.mouse.wheel(0,90);await p.waitForTimeout(160);}await p.waitForTimeout(900);
const v=await p.video().path();await ctx.close();await b.close();fs.writeFileSync(name+'.json',JSON.stringify({video:v,log}));console.log(name,JSON.stringify(log));})();
