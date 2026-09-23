import test from 'node:test';
import assert from 'node:assert/strict';
import {createHandler} from '../netlify/functions/walkthrough-feedback.mts';

const origin = 'https://profsathya.github.io';
const env = key => ({
  AI_ALLOWED_ORIGINS: origin,
  ANTHROPIC_API_KEY: 'test-only',
  ANTHROPIC_BASE_URL: 'https://provider.example',
}[key]);
const guidance = {example: {
  title: 'Example activity', rule: 'Review the participant draft, without drafting for them.',
  checkpoints: {reflection: 'Name a concrete event and one uncertainty.'},
}};
const request = (body, headers = {}) => new Request('https://example.test', {
  method: 'POST', headers: {origin, 'content-type': 'application/json', ...headers},
  body: JSON.stringify(body),
});

test('uses server criteria and only the selected response', async () => {
  const handler = createHandler(env, async (url, options) => {
    assert.equal(url, 'https://provider.example/v1/messages');
    const payload = JSON.parse(options.body);
    assert.equal(payload.model, 'claude-sonnet-5');
    assert.equal(payload.max_tokens, 640);
    assert.equal(payload.tools, undefined);
    assert.match(payload.messages[0].content, /Name a concrete event and one uncertainty/);
    assert.match(payload.messages[0].content, /<<<PARTICIPANT_RESPONSE>>>\nMy own observation/);
    return Response.json({content: [{type: 'text', text: 'What did you observe directly?'}]});
  }, guidance);
  const result = await handler(request({activity: 'example', checkpoint: 'reflection', response: 'My own observation'}));
  assert.equal(result.status, 200);
  assert.deepEqual(await result.json(), {content: 'What did you observe directly?'});
});

test('rejects caller controls and unconfigured checkpoints before provider use', async () => {
  const handler = createHandler(env, () => { throw new Error('provider called'); }, guidance);
  assert.equal((await handler(request({activity: 'example', checkpoint: 'reflection', response: 'x', model: 'other'}))).status, 400);
  assert.equal((await handler(request({activity: 'example', checkpoint: 'other', response: 'x'}))).status, 404);
  assert.equal((await handler(request({activity: 'other', checkpoint: 'reflection', response: 'x'}))).status, 404);
  assert.equal((await handler(request({activity: 'example', checkpoint: 'reflection', response: 'x'}, {origin: 'https://foreign.example'}))).status, 403);
});

test('returns an outage state without changing participant work', async () => {
  const allowed = createHandler(key => key === 'AI_ALLOWED_ORIGINS' ? origin : undefined,
    () => { throw new Error('provider called'); }, guidance);
  const unavailable = await allowed(request({activity: 'example', checkpoint: 'reflection', response: 'x'}));
  assert.equal(unavailable.status, 503);
});
