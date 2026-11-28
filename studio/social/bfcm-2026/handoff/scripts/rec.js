const {chromium}=require('playwright');
(async()=>{const [,,url,name,scroll]=process.argv;const b=await chromium.launch();
const ctx=await b.newContext({viewport:{width:430,height:764},deviceScaleFactor:2,isMobile:true,hasTouch:true,userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',locale:'en-US',recordVideo:{dir:'vid_'+name,size:{width:860,height:1528}}});
const p=await ctx.newPage();const r=await p.goto(url,{waitUntil:'domcontentloaded',timeout:45000});await p.waitForTimeout(4500);
// close popups politely
for(const s of ['button[aria-label*="lose" i]','[class*="popup"] button[class*="close"]','button:has-text("No thanks")','button:has-text("Accept")','.klaviyo-close-form','[aria-label="Close dialog"]','[aria-label="Close form"]']){try{const e=p.locator(s).first();if(await e.isVisible({timeout:400})){await e.click({timeout:800});await p.waitForTimeout(400);}}catch(e){}}
await p.keyboard.press('Escape').catch(()=>{});await p.waitForTimeout(800);
await p.screenshot({path:name+'_0.png'});
const n=parseInt(scroll||'5');for(let i=0;i<n;i++){await p.mouse.wheel(0,260);await p.waitForTimeout(650);}
await p.screenshot({path:name+'_1.png'});await p.waitForTimeout(600);
const t=await p.evaluate(()=>document.body.innerText.slice(0,1500));console.log(name,'status',r&&r.status(),t.replace(/\s+/g,' ').slice(0,400));
await ctx.close();await b.close();})();
