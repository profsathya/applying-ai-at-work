const fs=require('fs');
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const base=process.argv[2] || 'http://127.0.0.1:8765/deanza/course1/';
const label=process.argv[3] || 'local';
const dir=process.env.EVIDENCE_DIR + '/';
const modules=JSON.parse(fs.readFileSync(dir+'modules-before.json'));
const assignments=JSON.parse(fs.readFileSync(dir+'assignments-before.json'));
const wrapper=JSON.parse(fs.readFileSync(dir+'front-before.json')).body;
fs.writeFileSync(process.env.WRAPPER_DIR+'/wrapper.html',wrapper.replace(/src="[^"]+"/,`src="${base}home.html?context=canvas"`));
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const results=[];
 for(const width of [1440,390]) for(const framed of [false,true]) {
  const context=await browser.newContext({viewport:{width,height:900}});
  const page=await context.newPage(); const errors=[]; page.on('pageerror',e=>errors.push(e.message));
  // Intercept only the destination UI after the click; native target existence is verified via authenticated API reads.
  await context.route('https://cti-courses.instructure.com/courses/180/**',r=>r.fulfill({contentType:'text/html',body:'<h1>Native Canvas navigation reached</h1>'}));
  const src=base+'home.html?context=canvas';
  const load=async()=>{ await page.goto(framed?'http://127.0.0.1:8766/wrapper.html':src,{waitUntil:'domcontentloaded'}); const doc=framed?page.frameLocator('iframe'):page; await doc.locator('[data-sprint="1"] a.module-title').waitFor();return doc; };
  let doc=await load();
  assert.equal(await doc.locator('[data-activity-link]').count(),39);
  for(let i=0;i<modules.length;i++){
   const key=i?String(i):'orientation'; const expected=modules[i].items.filter(x=>x.published);
   const links=doc.locator(`#module-items-${key} [data-activity-link]`);
   const actual=await links.evaluateAll(xs=>xs.map(x=>({title:x.querySelector('.activity-title').textContent,meta:x.querySelector('.activity-meta').textContent,href:x.href,target:x.target})));
   assert.deepEqual(actual.map(x=>x.title),expected.map(x=>x.title));
   assert.deepEqual(actual.map(x=>Number(x.href.split('/').pop())),expected.map(x=>x.id));
   actual.forEach((x,j)=>{assert.equal(x.target,'_top'); if(expected[j].type==='Assignment'){const a=assignments.find(a=>a.id===expected[j].content_id); assert.ok(x.meta.includes(`${a.points_possible} points`),x.title+' points');}});
   const native=`https://cti-courses.instructure.com/courses/180/modules/${modules[i].id}`;
   const link=i?doc.locator(`[data-sprint="${i}"] a.module-title`):doc.locator('#sprint-action');
   assert.equal(await link.getAttribute('href'),native); assert.equal(await link.getAttribute('target'),'_top');
   await link.click(); await page.waitForURL(native); assert.equal(page.url(),native);
   results.push({width,framed,key,href:native,topLevelClick:true}); doc=await load();
  }
  await doc.locator('[data-sprint="5"] button').click();
  assert.equal(await doc.locator('#module-items-5 [data-activity-link]').count(),1);
  await page.screenshot({path:dir+`${label}-${width}-${framed?'iframe':'direct'}.png`,fullPage:true});
  assert.deepEqual(errors,[]); await context.close();
 }
 // Web URLs stay portable; hosted destinations remain intentionally available here.
 const p=await browser.newPage(); await p.goto(base+'home.html?context=web');
 assert.equal(new URL(await p.locator('[data-sprint="1"] a').first().getAttribute('href')).pathname,new URL(base+'sprint-14.html').pathname);
 assert.equal(await p.locator('[data-sprint="1"] a').first().getAttribute('target'),null);
 // Featured cards use the same module mapping as the list.
 for(const [date,id] of [['2026-10-06T12:00:00Z',2079],['2026-12-01T12:00:00Z',2076]]){
  await p.clock.install({time:new Date(date)}); await p.goto(base+'home.html?context=canvas');
  assert.equal(await p.locator('#sprint-action').getAttribute('href'),`https://cti-courses.instructure.com/courses/180/modules/${id}`);
 }
 await browser.close(); fs.writeFileSync(dir+label+'-browser.json',JSON.stringify({passed:true,publishedActivities:39,results},null,2));console.log('PASS',label,results.length,'native clicks; 39 titles/order/points; web and featured S1/S5');
})().catch(e=>{console.error(e);process.exit(1)});
