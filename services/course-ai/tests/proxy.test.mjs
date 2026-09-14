import test from 'node:test';
import assert from 'node:assert/strict';
import { createHandler } from '../netlify/functions/ai-proxy.mts';
const origin = 'https://profsathya.github.io';
const env = key => ({ ANTHROPIC_API_KEY: 'test-only', ANTHROPIC_BASE_URL: 'https://gateway.example', }[key]);
const request = (body, headers = {}) => new Request('https://example.test', { method: 'POST', headers: { origin, 'content-type': 'application/json', ...headers }, body: JSON.stringify(body) });
const input = { messages: [{ role: 'user', content: 'A fictional course response.' }], max_tokens: 512 };
test('preserves multi-block content and usage; fixes model and strips caller controls', async () => {
  const handler = createHandler(env, async (url, opts) => {
    assert.equal(url, 'https://gateway.example/v1/messages');
    const data = JSON.parse(opts.body);
    assert.equal(data.model, 'claude-sonnet-4-5-20250929');
    assert.equal(data.max_tokens, 2500);
    assert.equal(data.tools, undefined);
    return Response.json({ content: [{ type: 'thinking', thinking: 'internal' }, { type: 'text', text: 'first' }, { type: 'text', text: 'second' }], usage: { output_tokens: 4 } });
  });
  const r = await handler(request({ ...input, max_tokens: 9000, model: 'other', tools: ['x'] }));
  assert.equal(r.status, 200);
  assert.deepEqual(await r.json(), { content: 'first\nsecond', usage: { output_tokens: 4 } });
});
test('rejects malformed inputs and foreign origins before contacting provider', async () => {
  const handler = createHandler(env, () => { throw new Error('must not call'); });
  for (const body of [null, [], { ...input, max_tokens: -1 }, { ...input, max_tokens: 1.5 }, { messages: [{ role: 'user', content: [{ type: 'image', source: 'x' }] }] }]) assert.equal((await handler(request(body))).status, 400);
  assert.equal((await handler(request(input, { origin: 'https://foreign.example' }))).status, 403);
  assert.equal((await handler(request({ messages: [{ role: 'user', content: 'x'.repeat(60001) }] }))).status, 413);
});
test('empty/truncated/provider-error responses cannot masquerade as success', async () => {
  for (const response of [Response.json({ content: [] }), Response.json({ content: [{ type: 'text', text: '{partial' }], stop_reason: 'max_tokens' }), Response.json({ error: 'private error' }, { status: 500 })]) {
    const r = await createHandler(env, async () => response)(request(input));
    assert.equal(r.status, 502); assert.ok(!(await r.text()).includes('private error'));
  }
});
test('timeout, missing gateway, and preflight', async () => {
  assert.equal((await createHandler(env, async () => { throw new DOMException('timeout', 'TimeoutError'); })(request(input))).status, 504);
  assert.equal((await createHandler(() => undefined)(request(input))).status, 503);
  assert.equal((await createHandler(env)(new Request('https://example.test', { method: 'OPTIONS', headers: { origin } }))).status, 204);
});
