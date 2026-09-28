const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const code = fs.readFileSync('canvas_sync/assets/guided-walkthrough.js', 'utf8');

function boot({gate = true, saved = null, failStorage = false, failExport = false} = {}) {
  const tasks = Array.from({length: 5}, (_, i) => ({id: `frame-${i + 1}`, kind: 'response',
    prompt: `Frame ${i + 1}`, ...(gate && i < 3 ? {min_response_chars: 100} : {})}));
  const config = {artifactId: 'new-frames', version: '1', tasks, hasWritable: true,
    title: 'First frames', submissionType: 'file_upload', exportFilename: 'first-frames.docx'};
  const nodes = new Map();
  function node(id) {
    if (!nodes.has(id)) nodes.set(id, {value: '', textContent: '', hidden: id === 'walk-recovery',
      disabled: false, dataset: {}, listeners: {}, style: {},
      addEventListener(event, fn) {this.listeners[event] = fn;},
      closest() {return null;}, focus() {this.focused = true;}, select() {this.selected = true;}});
    return nodes.get(id);
  }
  node('guided-config').textContent = JSON.stringify(config);
  const inputs = tasks.map(task => {const input = node(task.id); input.dataset.walkAnswer = task.id; return input;});
  const storage = new Map([['course-response:old-frames:1.0', 'original draft']]);
  if (saved) storage.set('course-response:new-frames', JSON.stringify({answers: saved}));
  let exported = 0;
  const absent = new Set(['walk-copy', 'walk-text-download', 'walk-rich-output']);
  vm.runInNewContext(code, {document: {
    getElementById(id) {return absent.has(id) ? null : node(id);},
    querySelectorAll(selector) {return selector === '[data-walk-answer]' ? inputs : [];},
    createElement() {return {click() {}, remove() {}};}, body: {appendChild() {}},
  }, localStorage: {
    getItem(key) {if (failStorage) throw Error(); return storage.get(key) || null;},
    setItem(key, value) {if (failStorage) throw Error(); storage.set(key, value);},
    removeItem(key) {storage.delete(key);},
  }, WalkthroughDocx: {build() {if (failExport) throw Error(); exported++; return {}; }},
  URL: {createObjectURL() {return 'blob:test';}, revokeObjectURL() {}},
  setTimeout() {return 1;}, clearTimeout() {}});
  return {node, storage, get exported() {return exported;},
    fill(id, value) {node(id).value = value; node(id).listeners.input(); node(id).listeners.blur();},
    download() {node('walk-download').listeners.click();}};
}

const app = boot();
assert(app.node('walk-download').disabled);
app.fill('frame-1', ' \t\n\u00a0'.repeat(100));
app.download(); assert.equal(app.exported, 0);
app.fill('frame-4', 'x'.repeat(100)); app.fill('frame-5', 'x'.repeat(100));
assert(app.node('walk-download').disabled); // Optional fields cannot stand in for required ones.
app.fill('frame-4', ''); app.fill('frame-5', '');
for (let i = 1; i <= 3; i++) app.fill(`frame-${i}`, 'x'.repeat(100));
assert.equal(app.node('walk-download').disabled, false);
app.download(); assert.equal(app.exported, 1);
app.fill('frame-2', 'x'.repeat(99) + ' '.repeat(100));
assert(app.node('walk-download').disabled);
app.download(); assert.equal(app.exported, 1); // Handler guard survives forced dispatch.
app.fill('frame-2', '😀'.repeat(99)); assert(app.node('walk-download').disabled);
app.fill('frame-2', '😀'.repeat(100)); assert.equal(app.node('walk-download').disabled, false);
const saved = JSON.parse(app.storage.get('course-response:new-frames')).answers;
const restored = boot({saved}); assert.equal(restored.node('walk-download').disabled, false);
assert.equal(restored.node('frame-2').value, '😀'.repeat(100));
restored.node('walk-clear').listeners.click(); restored.node('walk-clear-no').listeners.click();
assert.equal(restored.node('frame-1').value, 'x'.repeat(100));
restored.node('walk-clear').listeners.click(); restored.node('walk-clear-yes').listeners.click();
assert(restored.node('walk-download').disabled);
assert(!restored.storage.has('course-response:new-frames'));
assert.equal(restored.storage.get('course-response:old-frames:1.0'), 'original draft');
const failure = boot({saved, failExport: true}); failure.download();
assert.equal(failure.node('walk-recovery').hidden, false);
assert(failure.node('walk-output').value.includes('x'.repeat(100)));
assert(failure.node('walk-output').selected);
const storageFailure = boot({failStorage: true}); storageFailure.fill('frame-1', 'Keep this partial response');
assert.equal(storageFailure.node('walk-recovery').hidden, false);
assert(storageFailure.node('walk-output').value.includes('Keep this partial response'));
assert(storageFailure.node('walk-download').disabled);
const existing = boot({gate: false}); assert.equal(existing.node('walk-download').disabled, false);
existing.download(); assert.equal(existing.exported, 1);
console.log('Walkthrough minimum runtime passed: boundaries, Unicode, saved drafts, optional fields, recovery, independent storage, and unguarded export.');
