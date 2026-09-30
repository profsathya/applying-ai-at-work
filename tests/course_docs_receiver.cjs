const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const crypto = require('crypto');
const context = vm.createContext({});
vm.runInContext(fs.readFileSync('scripts/apps-script/CourseDocSync.gs', 'utf8'), context);
const stored = {};
const props = {getProperty: key => stored[key] || null};
function payload(generation, tab='Course', digest='a'.repeat(64)) {
  return {metadata: {generation, repository:'owner/repo',commit_sha:'abc'},
    sections:[{tab,pages:[],content_digest:digest,rendered_digest:digest}]};
}
const versions = context.checkVersions(props, 'doc', payload(5));
stored['VERSION:doc:Course'] = JSON.stringify(versions.Course);
assert.throws(() => context.checkVersions(props, 'doc', payload(4)), /stale/);
assert.throws(() => context.checkVersions(props, 'doc', payload(5, 'Course', 'b'.repeat(64))), /conflicting/);
assert.equal(context.checkVersions(props, 'doc', payload(5)).Course.generation, 5);
assert.equal(context.checkVersions(props, 'doc', payload(6)).Course.generation, 6);
assert.equal(context.checkVersions(props, 'doc', payload(1, 'Dojo')).Dojo.generation, 1);
assert.throws(() => context.checkVersions(props, 'doc', payload(0)), /missing_source/);
assert.throws(() => context.checkVersions(props, 'doc', {
  ...payload(6), sections:[{tab:'Course', pages:[], content_digest:'a'.repeat(64)}]
}), /invalid_section/);

const currentText = 'Course heading\nLine one\n\nLine two';
const currentDigest = crypto.createHash('sha256').update('Course heading\nLine one\nLine two').digest('hex');
let copied = false;
let saved = false;
const body = {
  getText: () => currentText,
  copy: () => { copied = true; throw new Error('Already current tab must not be copied'); }
};
const tab = {
  getTitle: () => 'Course', getChildTabs: () => [],
  asDocumentTab: () => ({getBody: () => body})
};
context.DocumentApp = {openById: () => ({getTabs: () => [tab], saveAndClose: () => { saved = true; }})};
context.Utilities = {
  DigestAlgorithm: {SHA_256: 'sha256'}, Charset: {UTF_8: 'utf8'},
  computeDigest: (_algorithm, text) => Array.from(crypto.createHash('sha256').update(text).digest(),
    byte => byte > 127 ? byte - 256 : byte)
};
const matched = context.rebuildDocument('doc', {
  sections:[{tab:'Course', pages:[{}], rendered_digest:currentDigest}]
});
assert.equal(matched.digests.Course, currentDigest);
assert.equal(matched.pages, 1);
assert.equal(matched.tabs.length, 0);
assert.equal(copied, false);
assert.equal(saved, false);
console.log('Receiver ordering, validation, and saved-document retry passed.');

// Diagnostic output contains fixed categories even when runtime errors contain secrets.
const logs = [];
let released = false;
context.console = {error: message => logs.push(message)};
context.PropertiesService = {getScriptProperties: () => ({getProperty: key =>
  key === 'COURSE_DOC_SYNC_TOKEN' ? 'test-secret' : key === 'COURSE_DOC_IDS' ? '{"course1":"doc"}' : null})};
context.LockService = {getScriptLock: () => ({tryLock: () => true, releaseLock: () => {released = true;}})};
context.jsonResponse = value => value;
context.DocumentApp = {openById: () => {throw new Error('Service Documents failed while accessing document private-id test-secret');}};
const rejected = context.doPost({postData: {contents: JSON.stringify({
  ...payload(7), token: 'test-secret', course: 'course1', document_id: 'doc'
})}});
assert.equal(rejected.error, 'document_update_failed');
assert.equal(rejected.diagnostic.phase, 'open_document');
assert.equal(rejected.diagnostic.reason, 'document_service');
assert.equal(rejected.diagnostic.kind, 'Error');
assert.equal(released, true);
assert.equal(logs.length, 1);
assert.doesNotMatch(JSON.stringify(rejected) + logs[0], /private-id|test-secret/);
assert.equal(rejected.message, undefined);
const unknownDiagnostic = context.safeUpdateDiagnostic({name: 'private-name', message: 'private-message'}, {phase: 'private-phase'});
assert.equal(JSON.stringify(unknownDiagnostic), '{"phase":"unknown","kind":"unknown","reason":"unknown"}');
console.log('Receiver diagnostics redact runtime details and preserve lock cleanup.');
