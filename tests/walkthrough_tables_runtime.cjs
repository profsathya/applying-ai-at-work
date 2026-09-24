const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.join(__dirname, '..');
for (const name of ['walkthrough-tables.js', 'walkthrough-docx.js']) {
  vm.runInThisContext(fs.readFileSync(path.join(root, 'canvas_sync/assets', name), 'utf8'), {filename: name});
}

const columns = [
  {id: 'situation', label: 'The situation'},
  {id: 'now', label: 'How it works now', width: 2},
  {id: 'cost', label: 'What it costs, and whom'},
  {id: 'gap', label: 'The gap'},
];
const guidance = ['Restate the item.', 'Two or three sentences.', 'Who is impacted?', 'What could be different?'];
const rows = [
  {id: 'guidance', cells: guidance.map(text => ({text}))},
  ...Array.from({length: 5}, (_, index) => ({
    id: 'candidate-' + (index + 1), label: 'Candidate ' + (index + 1),
    cells: columns.map(() => ({text: '', response: true})),
  })),
];
const task = {id: 'candidate-log', kind: 'table', prompt: 'Get underneath three to five', columns, rows};
const answers = {
  'candidate-log.candidate-1.situation': 'A < B',
  'candidate-log.candidate-1.now': 'First handoff\nThen review',
  'candidate-log.candidate-1.cost': 'Time',
  'candidate-log.candidate-1.gap': 'Clarify ownership',
};
const tableHtml = WalkthroughTables.html(task, answers);
assert.equal((tableHtml.match(/<th scope="col"/g) || []).length, 4);
assert.equal((tableHtml.match(/<tr>/g) || []).length, 7);
assert.ok(tableHtml.includes('<col style="width:40.0000%">'));
assert.ok(tableHtml.includes('A &lt; B'));
assert.ok(!tableHtml.includes('<textarea'));
assert.ok(WalkthroughTables.tsv(task, answers).includes('First handoff\nThen review'));
const feedback = WalkthroughTables.rowResponse(task, rows[1], answers);
assert.ok(feedback.includes('The situation: A < B'));
assert.ok(feedback.includes('The gap: Clarify ownership'));
assert.equal(WalkthroughTables.rowResponse(task, rows[2], answers), '');

const reference = {
  id: 'reference', kind: 'table', read_only: true, prompt: 'Read this grid',
  columns: [{id: 'one', label: 'First'}, {id: 'two', label: 'Second'}],
  rows: [{id: 'guidance', cells: [{text: 'Line one\nLine two'}, {text: 'Keep this blank'}]}],
};
assert.equal((WalkthroughTables.html(reference, {}).match(/<th scope="col"/g) || []).length, 2);
assert.ok(WalkthroughTables.html(reference, {}).includes('Line one<br>Line two'));
assert.equal(WalkthroughTables.rowResponse(reference, reference.rows[0], {}), '');
const fiveColumn = {
  id: 'wide', kind: 'table', prompt: 'Complete the wide grid',
  columns: Array.from({length: 5}, (_, index) => ({id: 'c' + index, label: 'Column ' + index})),
  rows: [{id: 'mixed', cells: [
    {text: 'Source guidance', response: true}, {text: ''}, {text: ''}, {text: ''}, {text: '', response: true},
  ]}],
};
assert.equal((WalkthroughTables.html(fiveColumn, {'wide.mixed.c0': 'Answer'}).match(/<th scope="col"/g) || []).length, 5);
assert.ok(WalkthroughTables.rowResponse(fiveColumn, fiveColumn.rows[0], {'wide.mixed.c0': 'Answer'})
  .includes('Column 0: Source guidance\nAnswer'));

function zipEntry(data, wanted) {
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
  throw new Error('Missing ZIP entry ' + wanted);
}

(async () => {
  const headerless = {...reference, header_rows: 0};
  const noHeaderHtml = WalkthroughTables.html(headerless, {});
  assert(!noHeaderHtml.includes('<thead>'));
  assert.equal((noHeaderHtml.match(/<tr>/g) || []).length, 1);
  assert(!WalkthroughTables.tsv(headerless, {}).startsWith('First\tSecond'));
  const headerlessXml = zipEntry(Buffer.from(await WalkthroughDocx.build({title: 'Form', tasks: [headerless]}, {})
    .arrayBuffer()), 'word/document.xml');
  assert.equal((headerlessXml.match(/<w:tr>/g) || []).length, 1);
  assert(!headerlessXml.includes('w:tblHeader'));
  assert(headerlessXml.includes('Line one'));
  const file = WalkthroughDocx.build({title: 'Candidate Log', tasks: [task]}, answers);
  const xml = zipEntry(Buffer.from(await file.arrayBuffer()), 'word/document.xml');
  assert.equal((xml.match(/<w:gridCol /g) || []).length, 4);
  assert.ok(xml.includes('<w:gridCol w:w="4200"/>'));
  assert.equal((xml.match(/<w:tr>/g) || []).length, 7);
  assert.ok(xml.includes('A &lt; B'));
  assert.ok(xml.includes('Restate the item.'));
  assert.ok(xml.includes('Clarify ownership'));
  const referenceXml = zipEntry(Buffer.from(await WalkthroughDocx.build({title: 'Reference', tasks: [reference]}, {})
    .arrayBuffer()), 'word/document.xml');
  assert.equal((referenceXml.match(/<w:gridCol /g) || []).length, 2);
  assert.equal((referenceXml.match(/<w:tr>/g) || []).length, 2);
  assert.ok(referenceXml.includes('Line one'));
  assert.ok(referenceXml.includes('Line two'));
  const wideXml = zipEntry(Buffer.from(await WalkthroughDocx.build({title: 'Wide', tasks: [fiveColumn]},
    {'wide.mixed.c0': 'Answer'}).arrayBuffer()), 'word/document.xml');
  assert.equal((wideXml.match(/<w:gridCol /g) || []).length, 5);
  assert.ok(wideXml.includes('Source guidance'));
  assert.ok(wideXml.includes('Answer'));
})().catch(error => { console.error(error); process.exitCode = 1; });
