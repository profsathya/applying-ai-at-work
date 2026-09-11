/* Browser evidence for preview_module.py. Uses fresh contexts, never the user's browser. */
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');

async function run() {
  const [directory, baseURL, ...args] = process.argv.slice(2);
  const option = name => { const i = args.indexOf(name); return i < 0 ? undefined : args[i + 1]; };
  const {chromium} = require(option('--playwright-module') || process.env.PLAYWRIGHT_MODULE || 'playwright');
  const preview = JSON.parse(fs.readFileSync(path.join(directory, 'preview.json')));
  const browser = await chromium.launch({headless: true, executablePath: option('--browser-executable')});
  const results = [];
  const comparison = {screenshots: [], errors: []};
  fs.mkdirSync(path.join(directory, 'screenshots'), {recursive: true});
  try {
    for (let index = 0; index < preview.pages.length; index++) {
      const item = preview.pages[index];
      const result = {id: item.id, title: item.title, checks: [], skipped: [], errors: []};
      results.push(result);
      if (!item.after) { result.skipped.push(item.skipped); continue; }
      const context = await browser.newContext({permissions: ['clipboard-read', 'clipboard-write']});
      const page = await context.newPage();
      page.setDefaultTimeout(10000);
      page.on('pageerror', error => result.errors.push(error.message));
      // No requests to Canvas, AI services, or other external sites during automated QA.
      await context.route('**/*', route => {
        const request = route.request();
        if (new URL(request.url()).origin === new URL(baseURL).origin && ['GET', 'HEAD'].includes(request.method())) return route.continue();
        return route.abort();
      });
      const taskField = (attribute, value) => page.locator(`[${attribute}="${value.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"]`);
      const config = async () => await page.locator('#guided-config').count() ? JSON.parse(await page.locator('#guided-config').textContent()) : null;
      const recordCheck = name => result.checks.push(name);
      try {
        await page.setViewportSize({width: 1280, height: 900});
        let previous = null;
        if (item.before) {
          await page.goto(new URL(item.before, baseURL).href);
          previous = await config();
          if (previous) for (const task of previous.tasks) {
            if (task.kind === 'response') await taskField('data-answer', task.id).fill(`Baseline QA: ${task.id}`);
            else await taskField('name', task.id).first().check();
          }
        }
        await page.goto(new URL(item.after, baseURL).href);
        const current = await config();
        if (previous && current) {
          let comparable = 0;
          for (const task of previous.tasks) {
            if (!current.tasks.some(t => t.id === task.id && t.kind === task.kind)) continue;
            if (task.kind === 'response') assert.equal(await taskField('data-answer', task.id).inputValue(), `Baseline QA: ${task.id}`);
            else assert(await taskField('name', task.id).first().isChecked());
            comparable++;
          }
          if (comparable) recordCheck(`baseline drafts restored for ${comparable} shared tasks`);
        }
        const headings = await page.locator('h1,h2,h3,h4,h5,h6').evaluateAll(elements => elements.map(e => ({level: Number(e.tagName.slice(1)), text: e.textContent.trim()})));
        assert.equal(headings.filter(h => h.level === 1).length, 1, 'Expected one page heading');
        for (let i = 1; i < headings.length; i++) assert(headings[i].level <= headings[i - 1].level + 1, 'Skipped heading level: ' + headings[i].text);
        result.headings = headings; recordCheck('heading hierarchy');
        const images = await page.locator('section img').evaluateAll(elements => elements.map(img => ({src: img.src, alt: img.getAttribute('alt'), decorative: img.getAttribute('role') === 'presentation'})));
        for (const img of images) {
          assert(img.alt !== null && (img.alt.trim() || img.decorative), 'Missing meaningful image alternative: ' + img.src);
          if (new URL(img.src).origin !== new URL(baseURL).origin && !img.src.startsWith('data:')) {
            result.skipped.push('External image loading requires manual review: ' + img.src); continue;
          }
          const loaded = await page.locator('section img').evaluateAll((elements, src) => elements.filter(img => img.src === src).every(img => img.complete && img.naturalWidth > 0), img.src);
          assert(loaded, 'Image failed to load: ' + img.src);
        }
        result.images = images; recordCheck('local image loading and image text alternatives');
        if (current) {
          for (const task of current.tasks) {
            if (task.kind === 'response') await taskField('data-answer', task.id).fill(`Current QA: ${task.id}`);
            else {
              const options = taskField('name', task.id);
              await options.nth((task.correct_index + 1) % task.options.length).check();
              await taskField('data-check', task.id).click();
              assert.match(await taskField('data-result', task.id).textContent(), /Revisit the idea/);
              await options.nth(task.correct_index).check();
              await taskField('data-check', task.id).click();
              assert.match(await taskField('data-result', task.id).textContent(), /That fits/);
              await options.nth(task.correct_index).focus();
              await page.keyboard.press('ArrowRight');
              assert(await options.nth((task.correct_index + 1) % task.options.length).isChecked());
            }
          }
          await page.reload();
          for (const task of current.tasks) {
            if (task.kind === 'response') assert.equal(await taskField('data-answer', task.id).inputValue(), `Current QA: ${task.id}`);
            else assert(await taskField('name', task.id).nth((task.correct_index + 1) % task.options.length).isChecked());
          }
          recordCheck('save and reload all response/choice tasks');
          if (current.tasks.some(t => t.kind === 'choice')) recordCheck('correct/incorrect feedback and radio arrow keys');
          await page.locator('#copy-answers').focus();
          await page.keyboard.press('Enter');
          await page.waitForFunction(() => document.getElementById('copy-status').textContent.includes('Copied'));
          const copied = await page.evaluate(() => navigator.clipboard.readText());
          assert(copied.trim());
          for (const task of current.tasks.filter(t => t.kind === 'response')) assert(copied.includes(`Current QA: ${task.id}`));
          await page.evaluate(() => { navigator.clipboard.writeText = () => Promise.reject(new Error('QA clipboard denial')); });
          await page.locator('#copy-answers').click();
          await page.waitForFunction(() => document.activeElement.id === 'copy-output');
          assert(await page.locator('#copy-output').isVisible());
          assert.equal(await page.locator('#copy-output').inputValue(), copied);
          recordCheck('keyboard copy and clipboard-denial fallback focus');
          if (await page.locator('#more-options').count()) {
            assert(await page.locator('#more-options').evaluate(e => e.open));
            await page.locator('#more-options > summary').focus();
            await page.keyboard.press('Enter');
            assert(!(await page.locator('#more-options').evaluate(e => e.open)));
            assert.notEqual(await page.locator('#more-options > summary').evaluate(e => getComputedStyle(e).outlineWidth), '0px');
            recordCheck('disclosure keyboard operation and visible focus');
          }
          if (current.feedback_endpoint) result.skipped.push('AI feedback endpoint was not invoked');
          // Capture an ordinary saved page, without QA-generated status/fallback clutter.
          await page.reload();
        } else result.skipped.push('Guided-response controls are not applicable; Canvas interactions are outside this preview');
        const unnamed = await page.locator('button,input:not([type=hidden]),textarea,select,summary,a[href]').evaluateAll(elements => elements.filter(e => {
          if (!e.getClientRects().length) return false;
          const labelled = (e.getAttribute('aria-labelledby') || '').split(/\s+/).map(id => document.getElementById(id)?.textContent || '').join('');
          return !(e.getAttribute('aria-label') || labelled || [...(e.labels || [])].map(l => l.textContent).join('') || e.textContent || e.getAttribute('title') || '').trim();
        }).map(e => ({tag: e.tagName, id: e.id})));
        assert.deepEqual(unnamed, [], 'Visible controls need names'); recordCheck('visible control names');
        result.screenshots = [];
        for (const width of [1280, 390]) {
          await page.setViewportSize({width, height: 900});
          assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), 'Page overflow at ' + width);
          const file = `screenshots/${index + 1}-${width}.png`;
          await page.screenshot({path: path.join(directory, file), fullPage: true}); result.screenshots.push(file);
        }
        await page.setViewportSize({width: 320, height: 900});
        await page.addStyleTag({content: 'html,body{font-size:32px!important}'});
        assert(!(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), 'Page overflow at 320px with enlarged base text');
        const zoomFile = `screenshots/${index + 1}-enlarged.png`;
        await page.screenshot({path: path.join(directory, zoomFile), fullPage: true}); result.screenshots.push(zoomFile);
        recordCheck('desktop/mobile overflow and enlarged base text');
      } catch (error) {
        result.errors.push(error.message);
        await page.screenshot({path: path.join(directory, 'screenshots', `${index + 1}-failure.png`), fullPage: true}).catch(() => {});
      } finally { await context.close(); }
    }
    const reviewContext = await browser.newContext();
    try {
      await reviewContext.route('**/*', route => new URL(route.request().url()).origin === new URL(baseURL).origin && ['GET', 'HEAD'].includes(route.request().method()) ? route.continue() : route.abort());
      const review = await reviewContext.newPage();
      await review.goto(new URL('comparison.html', baseURL).href);
      assert.equal(await review.locator('#page option').count(), preview.pages.length);
      for (const width of [1680, 390]) {
        await review.setViewportSize({width, height: 1000});
        assert(!(await review.evaluate(() => document.documentElement.scrollWidth > innerWidth + 1)), 'Comparison overflow');
        const file = `screenshots/comparison-${width}.png`;
        await review.screenshot({path: path.join(directory, file), fullPage: true});
        comparison.screenshots.push(file);
      }
    } catch (error) { comparison.errors.push(error.message); }
    finally { await reviewContext.close(); }
  } finally { await browser.close(); }
  const failed = results.some(r => r.errors.length) || comparison.errors.length > 0;
  const partial = results.some(r => r.skipped.some(s => !s.startsWith('Guided-response controls are not applicable')));
  const report = {status: failed ? 'failed' : partial ? 'partial' : 'passed', results, comparison,
    manual_review: 'pending', limitations: 'Scoped Chromium checks, not screen-reader certification or participant validation. External requests blocked. Enlarged-base-text check is not full browser zoom.'};
  fs.writeFileSync(path.join(directory, 'browser-results.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(`${report.status}: ${results.length} pages; inspect browser-results.json and screenshots.`);
  process.exitCode = failed ? 1 : partial ? 2 : 0;
}
run().catch(error => { console.error(error.stack); process.exitCode = 1; });
