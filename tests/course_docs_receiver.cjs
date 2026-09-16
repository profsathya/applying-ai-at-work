const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const context = vm.createContext({});
vm.runInContext(fs.readFileSync('scripts/apps-script/CourseDocSync.gs', 'utf8'), context);
const stored = {};
const props = {getProperty: key => stored[key] || null};
function payload(generation, tab='Course', digest='a'.repeat(64)) {
  return {metadata: {generation, repository:'owner/repo',commit_sha:'abc'},sections:[{tab,pages:[],content_digest:digest}]};
}
const versions = context.checkVersions(props, 'doc', payload(5));
stored['VERSION:doc:Course'] = JSON.stringify(versions.Course);
assert.throws(() => context.checkVersions(props, 'doc', payload(4)), /stale/);
assert.throws(() => context.checkVersions(props, 'doc', payload(5, 'Course', 'b'.repeat(64))), /conflicting/);
assert.equal(context.checkVersions(props, 'doc', payload(5)).Course.generation, 5);
assert.equal(context.checkVersions(props, 'doc', payload(6)).Course.generation, 6);
assert.equal(context.checkVersions(props, 'doc', payload(1, 'Dojo')).Dojo.generation, 1);
assert.throws(() => context.checkVersions(props, 'doc', payload(0)), /missing_source/);
console.log('Receiver ordering, conflict, idempotence, and tab isolation passed.');
