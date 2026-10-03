/* Uses an isolated Chrome context and public teaching fixtures only. */
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright-core');
const hosted = path.resolve(process.argv[2]);
const config = JSON.parse(fs.readFileSync(path.join(hosted, 'deanza/mirrors/deanza46601/config.json')));
const mime = {'.html':'text/html', '.js':'text/javascript', '.json':'application/json', '.css':'text/css', '.svg':'image/svg+xml', '.png':'image/png', '.jpg':'image/jpeg', '.txt':'text/plain'};
let changed = false;
const errors = [];
const forbidden = [];
async function main() {
  const browser = await chromium.launch({executablePath: process.env.BROWSER_EXECUTABLE || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:true});
  const context = await browser.newContext({viewport:{width:1280,height:900}, acceptDownloads:true});
  await context.route('**/*', async route => {
    const request = route.request();
    const url = new URL(request.url());
    if (request.headers()['authorization'] || /instructure\.com|ssoshib\.fhda\.edu|canvas-progress-lti/.test(url.hostname)) {
      forbidden.push(url.hostname); await route.abort(); return;
    }
    if (url.origin !== 'https://profsathya.github.io') { await route.abort(); return; }
    const relative = decodeURIComponent(url.pathname.replace(/^\/Common-Curriculum\//, ''));
    const target = path.resolve(hosted, relative.endsWith('/') ? relative+'index.html' : relative);
    if (!target.startsWith(hosted+path.sep) || !fs.existsSync(target) || !fs.statSync(target).isFile()) { await route.fulfill({status:404,body:'Missing fixture'}); return; }
    let body = fs.readFileSync(target);
    if (changed && relative === 'deanza/course1/assignments/problem-frame-is-it-worth-pursuing.html') body = Buffer.from(body.toString().replace('</body>', '<p id="mirror-live-proof">Updated shared source after adapter build</p></body>'));
    await route.fulfill({status:200,contentType:mime[path.extname(target)] || 'application/octet-stream',body});
  });
  const page = await context.newPage();
  page.on('pageerror', error => errors.push(error.message));
  const results = [];
  const entry = (value, mode='canvas') => config.mirrorBaseUrl+'?'+new URLSearchParams({page:value,context:mode});
  for (const value of config.pages) {
    await page.goto(entry(value), {waitUntil:'domcontentloaded'});
    await page.waitForSelector('[data-course-mirror-source]', {timeout:10000});
    const data = await page.evaluate(() => ({title:document.title,source:document.body.dataset.courseMirrorSource,destination:document.body.dataset.courseMirrorDestination,links:[...document.querySelectorAll('a[href]')].map(a=>a.href),textareaCount:document.querySelectorAll('textarea').length}));
    assert.equal(data.source, config.sharedBaseUrl+value);
    assert.equal(data.destination, config.destinationCanvasUrl);
    assert.ok(data.links.every(url => !url.includes('cti-courses.instructure.com')));
    results.push({page:value,title:data.title,links:data.links.length,textareaCount:data.textareaCount});
  }
  await page.goto(entry('home.html'));
  await page.waitForSelector('[data-course-mirror-source]');
  assert.equal(await page.locator('#sprint-action').getAttribute('href'), config.destinationCanvasUrl+'/modules/532930');
  await page.locator('[data-module-toggle][data-module-title="Sprint 1: Find the problem worth solving"]').click();
  assert.ok(await page.locator('[data-module-key="1"] [data-activity-link]').first().getAttribute('href').then(v=>v.startsWith(config.destinationCanvasUrl+'/modules/items/')));
  await page.goto(entry('home.html','web'));
  await page.waitForSelector('[data-course-mirror-source]');
  await page.locator('#sprint-action').click();
  await page.waitForSelector('[data-course-mirror-source]');
  assert.equal(new URL(page.url()).searchParams.get('page'), 'sprint-6.html');
  await page.goto(entry('assignments/problem-frame-is-it-worth-pursuing.html'));
  await page.waitForSelector('[data-course-mirror-source]');
  assert.ok((await page.locator('body').innerText()).includes('Step 1. What fixing this would ask of people'));
  await page.evaluate(() => {const a=document.createElement('a');a.id='mirror-fragment-test';a.href='#guided-response-area';a.textContent='QA fragment';document.body.appendChild(a);});
  await page.locator('#mirror-fragment-test').click();
  assert.equal(new URL(page.url()).searchParams.get('page'), 'assignments/problem-frame-is-it-worth-pursuing.html');
  await page.locator('textarea').first().fill('Synthetic mirror QA response');
  changed = true;
  await page.reload();
  await page.waitForSelector('#mirror-live-proof');
  assert.equal(await page.locator('textarea').first().inputValue(), 'Synthetic mirror QA response');
  await page.goto(entry('../course2/home.html'));
  await page.waitForSelector('[role="alert"]');
  assert.equal(forbidden.length, 0, JSON.stringify(forbidden));
  assert.equal(errors.length, 0, JSON.stringify(errors));
  console.log(JSON.stringify({passed:true,pages:results.length,live_upstream_change_seen:true,draft_retained:true,native_home_links:true,web_context_retained:true,unknown_page_blocked:true,forbidden_requests:forbidden,script_errors:errors,results},null,2));
  await browser.close();
}
main().catch(error => {console.error(error);process.exit(1);});
