// Execute the shipped script against a minimal DOM. Browser layout is reviewed separately.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const code = fs.readFileSync('canvas_sync/assets/guided-assignment.js', 'utf8');
function boot({saved = null, storageFails = false, clipboardFails = false, feedbackFails = false, compact = false, reading = false} = {}) {
  const config = {artifactId:'test', version:'1', title:'Decide', module:'Sprint One', feedback_endpoint:'https://example.invalid/feedback',
    tasks:[{id:'reason',prompt:'Why this one?',criteria:['Name the deciding check.']},
           {id:'choice',kind:'choice',prompt:'Choose the gap',criteria:['Compare states.'],options:['Complaint','Gap'],correct_index:1,explanation:'Compare current and possible.'}]};
  if (compact) config.presentation = 'compact';
  if (reading) config.presentation = 'reading';
  const nodes = new Map();
  function node(name) {
    if (!nodes.has(name)) nodes.set(name, {textContent:'',value:'',checked:false,disabled:false,listeners:{},
      addEventListener(event, cb){ this.listeners[event]=cb; }, focus(){this.focused=true;}, select(){this.selected=true;}});
    return nodes.get(name);
  }
  node('guided-config').textContent=JSON.stringify(config);
  const radios=[node('radio0'),node('radio1')]; radios.forEach((r,i)=>r.value=String(i));
  const writes=[], requests=[], copies=[], removed=[];
  vm.runInNewContext(code, {document:{getElementById:node,
    querySelector(s){return node(s);},querySelectorAll(){return radios;}},
    localStorage:{getItem(){if(storageFails)throw Error();return saved;},setItem(k,v){if(storageFails)throw Error();writes.push([k,v]);},removeItem(k){if(storageFails)throw Error();removed.push(k);}},
    navigator:{clipboard:{async writeText(text){if(clipboardFails)throw Error();copies.push(text);}}},
    fetch:async(url,options)=>{requests.push([url,JSON.parse(options.body)]);if(feedbackFails)throw Error();return {ok:true,json:async()=>({content:'Name what you observed.'})};},
    AbortController, setTimeout, clearTimeout, console});
  return {node,radios,writes,requests,copies,removed};
}
(async()=>{
  const app=boot(); assert.equal(app.requests.length,0); // No automatic outbound requests.
  await app.node('[data-feedback="reason"]').listeners.click(); assert.equal(app.requests.length,0);
  const input=app.node('[data-answer="reason"]'); input.value='I can reach the person involved.'; input.listeners.input();
  assert.equal(JSON.parse(app.writes.at(-1)[1]).answers.reason,input.value);
  assert.match(app.node('completion-status').textContent,/1 of 2/);
  await app.node('[data-feedback="reason"]').listeners.click();
  assert.equal(app.requests.length,1); assert.match(app.requests[0][1].messages[0].content,/I can reach/);
  assert.equal(app.requests[0][1].messages[0].content.includes('Choose the gap'),false);
  input.value='I observed the handover yesterday.'; input.listeners.input();
  assert.match(app.node('[data-feedback-result="reason"]').textContent,/earlier draft/);
  app.radios[0].listeners.change(); app.node('[data-check="choice"]').listeners.click();
  assert.match(app.node('[data-result="choice"]').textContent,/Revisit the idea/);
  app.radios[1].listeners.change(); app.node('[data-check="choice"]').listeners.click();
  assert.match(app.node('[data-result="choice"]').textContent,/That fits/);
  await app.node('copy-answers').listeners.click();
  assert.match(app.copies.at(-1),/I observed the handover yesterday/);
  assert.match(app.copies.at(-1),/Gap/); assert.equal(app.copies.at(-1).includes('Name what you observed'),false);
  assert.match(app.node('copy-status').textContent,/not submitted/);
  const restored=boot({saved:app.writes.at(-1)[1]}); assert.equal(restored.node('[data-answer="reason"]').value,input.value);
  app.node('clear-draft').listeners.click(); app.node('cancel-clear').listeners.click();
  assert.equal(input.value,'I observed the handover yesterday.');
  const inFlight = app.node('[data-feedback="reason"]').listeners.click();
  app.node('clear-draft').listeners.click(); app.node('confirm-clear').listeners.click();
  const countAfterClear = app.writes.length; await inFlight;
  assert.equal(app.writes.length,countAfterClear); assert.equal(input.value,'');
  assert.deepEqual(app.removed,['course-response:test:1']);
  assert.equal(app.node('[data-feedback-result="reason"]').textContent,'');
  const failure=boot({storageFails:true,clipboardFails:true,feedbackFails:true});
  const box=failure.node('[data-answer="reason"]');box.value='My own answer';box.listeners.input();
  assert.match(failure.node('save-status').textContent,/cannot save/);
  await failure.node('copy-answers').listeners.click();assert.equal(failure.node('copy-output').selected,true);
  assert.match(failure.node('copy-output').value,/My own answer/);
  await failure.node('[data-feedback="reason"]').listeners.click();assert.match(failure.node('[data-feedback-result="reason"]').textContent,/unavailable/);
  assert.equal(box.value,'My own answer');assert.equal(failure.node('[data-feedback="reason"]').disabled,false);
  const reading = boot({reading:true,clipboardFails:true,saved:app.writes.at(-1)[1]});
  reading.radios[1].listeners.change(); reading.node('[data-check="choice"]').listeners.click();
  assert.match(reading.node('[data-result="choice"]').textContent,/That fits/);
  await reading.node('copy-answers').listeners.click();
  assert.equal(reading.node('more-options').open,true);
  assert.equal(reading.node('copy-output').focused,true);
  reading.node('clear-draft').listeners.click();
  assert.equal(reading.node('cancel-clear').focused,true);
  reading.node('cancel-clear').listeners.click();
  assert.equal(reading.node('clear-draft').focused,true);
  const compact = boot({compact:true,clipboardFails:true});
  compact.node('[data-answer="reason"]').value='Preserve this response';
  compact.node('[data-answer="reason"]').listeners.input();
  await compact.node('copy-answers').listeners.click();
  assert.equal(compact.node('more-options').open,true);
  assert.equal(compact.node('copy-output').focused,true);
  assert.equal(compact.node('copy-output').selected,true);
  assert.match(compact.node('copy-output').value,/Preserve this response/);
  console.log('guided runtime passed: save/restore, copy/fallback, choice feedback, optional requests, stale feedback, failure retention');
})().catch(e=>{console.error(e);process.exitCode=1;});
