/* Walk-through checks for the normal module preview browser run. */
const assert = require('node:assert/strict');
const fs = require('node:fs');

const answerKey = (task, row, column) => `${task.id}.${row.id}.${column.id}`;
const qaAnswer = key => `Preview QA: ${key}`;

async function fillInput(input, key) {
  if (await input.evaluate(element => element.tagName === 'SELECT')) {
    const choices = await input.locator('option').evaluateAll(options =>
      options.filter(option => !option.disabled && option.value).map(option => option.value));
    assert(choices.length, `${key}: select has no usable option`);
    await input.selectOption(choices[0]);
  } else await input.fill(qaAnswer(key));
  return input.inputValue();
}

function storedZipEntry(data, wanted) {
  let offset = 0;
  while (offset + 30 < data.length && data.readUInt32LE(offset) === 0x04034b50) {
    const size = data.readUInt32LE(offset + 18);
    const nameLength = data.readUInt16LE(offset + 26);
    const extraLength = data.readUInt16LE(offset + 28);
    const name = data.subarray(offset + 30, offset + 30 + nameLength).toString('utf8');
    const start = offset + 30 + nameLength + extraLength;
    if (name === wanted) return data.subarray(start, start + size).toString('utf8');
    offset = start + size;
  }
  throw new Error(`Word export is missing ${wanted}`);
}

async function fillBaseline(page) {
  const inputs = page.locator('[data-walk-answer]');
  const values = new Map();
  for (let index = 0; index < await inputs.count(); index++) {
    const input = inputs.nth(index);
    const key = await input.getAttribute('data-walk-answer');
    values.set(key, await fillInput(input, key));
  }
  if (await inputs.count()) await page.keyboard.press('Tab');
  return [...values];
}

async function verifyBaseline(page, values, recordCheck) {
  let restored = 0;
  for (const [key, value] of values) {
    const matching = page.locator(`[data-walk-answer="${key}"]`);
    if (await matching.count()) {
      assert.equal(await matching.inputValue(), value, `${key}: baseline draft was lost`);
      restored++;
    }
  }
  if (restored) recordCheck(`baseline drafts restored for ${restored} shared walk-through fields`);
}

async function checkWalkthrough(page, config, result) {
  const recordCheck = name => result.checks.push(name);
  assert.equal(await page.locator('.walk-intro h2').innerText(), 'How this walk-through works');
  const intro = await page.locator('.walk-intro').innerText();
  assert(intro.includes('Canvas walk-through assignment'), 'Walk-through context is missing');
  const finish = page.locator('.walk-finish');
  const finishText = await finish.innerText();
  if (!config.hasWritable) {
    assert(finishText.includes('no response to submit'), 'Reference-only page implies a submission');
    assert.equal(await finish.locator('#walk-copy').innerText(), 'Copy reference table');
  } else if (config.submissionType === 'file_upload') {
    assert(finishText.includes('Submit this walk-through in Canvas'));
    if (config.pdfFromDocument) {
      assert(finishText.includes('upload that PDF'));
      assert.equal(await finish.locator('#walk-copy').innerText(), 'Copy work into your document');
      assert.equal(await finish.locator('#walk-download').innerText(), 'Download Word backup');
    } else {
      assert(finishText.includes('select Start Assignment'));
      assert(finishText.includes('attach the Word document'));
      assert.equal(await finish.locator('#walk-download').innerText(), 'Download as Word document');
      assert.equal(await finish.locator('#walk-copy').count(), 0);
      assert.equal(await finish.locator('#walk-text-download').count(), 0);
    }
  } else {
    assert(finishText.includes('Submit this walk-through in Canvas'));
    assert(finishText.includes('text-entry box'));
    assert.equal(await finish.locator('#walk-copy').innerText(), 'Copy text for Canvas submission');
  }
  recordCheck('walk-through context and Canvas submission action');
  const tables = config.tasks.filter(task => task.kind === 'table');
  const writableTasks = config.tasks.filter(task => task.kind !== 'table' || !task.read_only);
  if (writableTasks.length && !config.feedbackEndpoint) {
    assert(config.feedbackOmissionReason, 'Writable walk-through lacks AI feedback or an omission reason');
  }
  const answerKeys = [];
  let feedbackButtons = 0;
  for (const task of writableTasks) {
    if (task.feedback_enabled === false) {
      assert(task.feedback_omission_reason, `${task.id}: AI feedback omission has no reason`);
    }
    if (task.kind === 'table') continue;
    const step = page.locator(`[data-walk-step="${task.id}"]`);
    const expected = config.feedbackEndpoint && task.feedback_enabled !== false
      ? (task.kind === 'group' ? task.repeat_count : 1) : 0;
    assert.equal(await step.locator('[data-walk-feedback]').count(), expected,
      `${task.id}: missing AI feedback controls`);
  }
  recordCheck('AI feedback controls cover every writable step or have a recorded exception');
  for (const task of tables) {
    const step = page.locator(`[data-walk-step="${task.id}"]`);
    const table = step.locator('table.walk-source-table');
    assert.equal(await table.count(), 1, `${task.id}: expected one source table`);
    assert.equal(await table.locator('thead th').count(), task.header_rows === 0 ? 0 : task.columns.length);
    assert.deepEqual(await table.locator('thead th').allTextContents(), task.header_rows === 0 ? [] : task.columns.map(column => column.label));
    const rows = table.locator('tbody tr');
    assert.equal(await rows.count(), task.rows.length);
    let responseRows = 0;
    for (let rowIndex = 0; rowIndex < task.rows.length; rowIndex++) {
      const row = task.rows[rowIndex];
      const cells = rows.nth(rowIndex).locator('td');
      assert.equal(await cells.count(), task.columns.length, `${task.id}: row width changed`);
      if (row.cells.some(cell => cell.response)) responseRows++;
      for (let columnIndex = 0; columnIndex < task.columns.length; columnIndex++) {
        const cell = row.cells[columnIndex];
        const rendered = cells.nth(columnIndex);
        const source = rendered.locator('.walk-source-cell-text');
        assert.equal(await source.count(), cell.text ? 1 : 0);
        if (cell.text) assert.equal((await source.innerText()).replace(/\r/g, '').trimEnd(), cell.text.trimEnd());
        const input = rendered.locator('[data-walk-answer]');
        assert.equal(await input.count(), cell.response ? 1 : 0);
        if (cell.response) {
          const key = answerKey(task, row, task.columns[columnIndex]);
          assert.equal(await input.getAttribute('data-walk-answer'), key);
          const label = await input.evaluate(element => element.labels?.[0]?.textContent || '');
          assert(label.includes(task.columns[columnIndex].label), `${key}: missing column label`);
          assert(label.includes(row.label || `Row ${responseRows}`), `${key}: missing row label`);
          answerKeys.push(key);
        }
      }
    }
    const expectedButtons = task.read_only || !config.feedbackEndpoint || task.feedback_enabled === false ? 0 : responseRows;
    const buttons = step.locator('[data-walk-feedback]');
    assert.equal(await buttons.count(), expectedButtons, `${task.id}: row feedback controls`);
    assert.equal(await step.locator('.walk-check').count(), task.read_only ? 0 : 1);
    if (task.read_only) assert.equal(responseRows, 0, `${task.id}: read-only table has inputs`);
    for (let index = 0; index < expectedButtons; index++) {
      const button = buttons.nth(index);
      const row = button.locator('xpath=ancestor::tr');
      const lastCell = await row.locator('td').last().boundingBox();
      const buttonBox = await button.boundingBox();
      assert(lastCell && buttonBox && buttonBox.x >= lastCell.x + lastCell.width - 2,
        `${task.id}: feedback button is not to the right of its row`);
      assert(buttonBox.y < lastCell.y + lastCell.height && buttonBox.y + buttonBox.height > lastCell.y,
        `${task.id}: feedback button is not aligned with its row`);
      feedbackButtons++;
    }
  }
  if (tables.length) recordCheck('table headings, source cells, dimensions, labels, and row-side controls');

  const inputs = page.locator('[data-walk-answer]');
  const entered = new Map();
  for (let index = 0; index < await inputs.count(); index++) {
    const input = inputs.nth(index);
    const key = await input.getAttribute('data-walk-answer');
    entered.set(key, await fillInput(input, key));
  }
  if (await inputs.count()) await page.keyboard.press('Tab');
  await page.reload();
  for (let index = 0; index < await inputs.count(); index++) {
    const input = inputs.nth(index);
    assert.equal(await input.inputValue(), entered.get(await input.getAttribute('data-walk-answer')));
  }
  recordCheck('walk-through draft save and reload');

  if (feedbackButtons) {
    const button = page.locator('.walk-source-table [data-walk-feedback]').first();
    assert(await button.isEnabled(), 'Row feedback did not enable after writing');
    await button.click();
    const resultSelector = `[data-walk-feedback-result="${await button.getAttribute('data-walk-feedback')}"]`;
    await page.waitForFunction(selector => document.querySelector(selector)?.textContent.includes('Preview sample feedback'), resultSelector);
    const feedback = page.locator(resultSelector);
    const tableBox = await button.locator('xpath=ancestor::table').boundingBox();
    const feedbackBox = await feedback.boundingBox();
    assert(tableBox && feedbackBox && feedbackBox.y >= tableBox.y + tableBox.height,
      'Row feedback result should appear below the table');
    recordCheck('row feedback preview and below-table result');
    result.skipped.push('Live AI feedback endpoint was not invoked');
  }
  if (!feedbackButtons && await page.locator('[data-walk-feedback]').count()) {
    const button = page.locator('[data-walk-feedback]').first();
    assert(await button.isEnabled(), 'Step feedback did not enable after writing');
    await button.click();
    const resultSelector = `[data-walk-feedback-result="${await button.getAttribute('data-walk-feedback')}"]`;
    await page.waitForFunction(selector => document.querySelector(selector)?.textContent.includes('Preview sample feedback'), resultSelector);
    recordCheck('non-table step feedback preview');
    result.skipped.push('Live AI feedback endpoint was not invoked');
  }

  const hasCopy = Boolean(await page.locator('#walk-copy').count());
  if (hasCopy) {
    await page.locator('#walk-copy').focus();
    await page.keyboard.press('Enter');
    await page.waitForFunction(() => /Copied as a table|Copied the reference table|Clipboard access is unavailable|Copied\./.test(
      document.getElementById('walk-copy-status').textContent));
    const copied = await page.evaluate(async () => {
      const items = await navigator.clipboard.read();
      const item = items.find(entry => entry.types.includes('text/html'));
      return item ? await (await item.getType('text/html')).text() : '';
    });
    const plain = await page.evaluate(() => navigator.clipboard.readText());
    for (const value of entered.values()) assert(plain.includes(value), 'Plain copy lost a response');
    if (tables.length) {
    assert(copied, 'Rich table copy was not written to the clipboard');
    const copiedTables = await page.evaluate(html => {
      const document = new DOMParser().parseFromString(html, 'text/html');
      const cellText = cell => {
        const copy = cell.cloneNode(true);
        copy.querySelectorAll('br').forEach(lineBreak => lineBreak.replaceWith(document.createTextNode('\n')));
        return copy.textContent;
      };
      return [...document.querySelectorAll('table')].map(table => ({
        headings: [...table.querySelectorAll('thead th')].map(cell => cell.textContent),
        rows: [...table.querySelectorAll('tbody tr')].map(row => [...row.cells].map(cellText)),
        controls: table.querySelectorAll('button,textarea').length,
      }));
    }, copied);
    assert.equal(copiedTables.length, tables.length);
    for (let index = 0; index < tables.length; index++) {
      const task = tables[index];
      assert.deepEqual(copiedTables[index].headings, task.header_rows === 0 ? [] : task.columns.map(column => column.label));
      assert.deepEqual(copiedTables[index].rows, task.rows.map(row => row.cells.map((cell, columnIndex) =>
        [cell.text, cell.response ? qaAnswer(answerKey(task, row, task.columns[columnIndex])) : '']
          .filter(Boolean).join('\n'))));
      assert.equal(copiedTables[index].controls, 0);
    }
    for (const key of answerKeys) assert(copied.includes(qaAnswer(key)));
    assert(!copied.includes('Preview sample feedback'), 'AI feedback leaked into copy');
    for (const key of answerKeys) assert(plain.includes(qaAnswer(key)));
      recordCheck('rich clipboard tables and plain text retain grid, answers, and source text');
    }
  }

  if (tables.length) {
    const [download] = await Promise.all([page.waitForEvent('download'), page.locator('#walk-download').click()]);
    const documentXml = storedZipEntry(fs.readFileSync(await download.path()), 'word/document.xml');
    assert((documentXml.match(/<w:tbl>/g) || []).length >= tables.length);
    for (const task of tables) {
      const escapedPrompt = task.prompt.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
      const start = documentXml.indexOf(escapedPrompt);
      assert(start >= 0, `${task.id}: Word export lost prompt`);
      const tableStart = documentXml.indexOf('<w:tbl>', start);
      const tableEnd = documentXml.indexOf('</w:tbl>', tableStart);
      assert(tableStart >= 0 && tableEnd > tableStart, `${task.id}: Word export lost table`);
      const grid = documentXml.slice(tableStart, tableEnd);
      assert.equal((grid.match(/<w:gridCol /g) || []).length, task.columns.length);
      assert.equal((grid.match(/<w:tr>/g) || []).length, task.rows.length + (task.header_rows === 0 ? 0 : 1));
      for (const column of task.header_rows === 0 ? [] : task.columns) assert(grid.includes(column.label.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')), `${task.id}: Word export lost heading`);
    }
    for (const key of answerKeys) assert(documentXml.includes(qaAnswer(key)));
    assert(!documentXml.includes('Preview sample feedback'), 'AI feedback leaked into Word export');
    recordCheck('Word export retains table grids and answers');
  }
  if (config.submissionType === 'file_upload' && !tables.length) {
    const [download] = await Promise.all([page.waitForEvent('download'), page.locator('#walk-download').click()]);
    const documentXml = storedZipEntry(fs.readFileSync(await download.path()), 'word/document.xml');
    for (const value of entered.values()) assert(documentXml.includes(value), 'Word upload lost a response');
    recordCheck('file-upload Word document retains answers');
  }

  if (hasCopy) {
    await page.evaluate(() => {
      Object.defineProperty(navigator.clipboard, 'write', {configurable: true, value: () => Promise.reject(new Error('QA clipboard denial'))});
      Object.defineProperty(navigator.clipboard, 'writeText', {configurable: true, value: () => Promise.reject(new Error('QA clipboard denial'))});
      document.execCommand = () => false;
    });
    await page.locator('#walk-copy').click();
    if (tables.length) {
      await page.waitForFunction(() => document.activeElement?.id === 'walk-rich-output');
      assert(await page.locator('#walk-rich-output').isVisible());
      assert.equal(await page.locator('#walk-rich-output table').count(), tables.length);
      recordCheck('clipboard-denial selectable-table fallback');
    } else {
      await page.waitForFunction(() => document.activeElement?.id === 'walk-output');
      recordCheck('clipboard-denial text fallback');
    }
  }
  await page.reload();
}

module.exports = {fillBaseline, verifyBaseline, checkWalkthrough};
