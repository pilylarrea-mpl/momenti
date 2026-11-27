const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const dir=process.argv[2];const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.html')).sort()){await p.goto('file://'+path.join(dir,f));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(80);
await p.screenshot({path:path.join(dir,f.replace('.html','.png')),omitBackground:true});}
await b.close();})();
