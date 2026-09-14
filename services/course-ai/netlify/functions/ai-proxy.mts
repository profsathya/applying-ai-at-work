// Same request/response contract as the course activity engine. No prompt logging.
function reply(status, body, origin = '') {
  const headers = { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', Vary: 'Origin' };
  if (origin) Object.assign(headers, {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
  });
  return new Response(JSON.stringify(body), { status, headers });
}

export function createHandler(env, transport = fetch) {
  return async (req) => {
    const origin = req.headers.get('origin') || '';
    const allowed = new Set((env('AI_ALLOWED_ORIGINS') || 'https://profsathya.github.io,https://cti-course-ai.netlify.app').split(',').map(s => s.trim()).filter(Boolean));
    if (!allowed.has(origin)) return reply(403, { error: 'This endpoint only serves the configured course pages.' });
    if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: {
      'Access-Control-Allow-Origin': origin, 'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Methods': 'POST, OPTIONS', Vary: 'Origin',
    } });
    if (req.method !== 'POST') return reply(405, { error: 'Method not allowed' }, origin);
    if (!req.headers.get('content-type')?.toLowerCase().startsWith('application/json')) return reply(415, { error: 'Send application/json.' }, origin);
    let body;
    try {
      const text = await req.text();
      if (text.length > 80000) return reply(413, { error: 'Request too large.' }, origin);
      body = JSON.parse(text);
    } catch { return reply(400, { error: 'Invalid JSON.' }, origin); }
    if (!body || typeof body !== 'object' || Array.isArray(body)) return reply(400, { error: 'Expected a request object.' }, origin);
    const { system, messages, max_tokens } = body;
    if (system !== undefined && typeof system !== 'string') return reply(400, { error: 'System instructions must be text.' }, origin);
    if (!Array.isArray(messages) || !messages.length || messages.length > 40) return reply(400, { error: 'Supply 1 to 40 messages.' }, origin);
    let length = (system || '').length;
    for (const m of messages) {
      if (!m || !['user', 'assistant'].includes(m.role)) return reply(400, { error: 'Invalid message role.' }, origin);
      if (typeof m.content === 'string') length += m.content.length;
      else if (Array.isArray(m.content) && m.content.length && m.content.every(p => p && p.type === 'text' && typeof p.text === 'string')) length += m.content.reduce((n, p) => n + p.text.length, 0);
      else return reply(400, { error: 'Only text messages are supported.' }, origin);
    }
    if (length > 60000) return reply(413, { error: 'Request too large.' }, origin);
    if (max_tokens !== undefined && (!Number.isInteger(max_tokens) || max_tokens < 1)) return reply(400, { error: 'max_tokens must be a positive integer.' }, origin);
    const key = env('ANTHROPIC_API_KEY');
    const base = env('ANTHROPIC_BASE_URL');
    if (!key || !base) return reply(503, { error: 'AI Gateway is not configured. Your response is preserved.' }, origin);
    const model = env('COURSE_AI_MODEL') || 'claude-sonnet-4-5-20250929';
    // Do not allow callers to choose a model, tools, thinking, or streaming.
    const payload = { model, max_tokens: Math.min(max_tokens ?? 1024, 2500),
      messages: messages.map(m => ({ role: m.role, content: typeof m.content === 'string' ? m.content : m.content.map(p => ({ type: 'text', text: p.text })) })),
      ...(system ? { system } : {}),
    };
    try {
      const upstream = await transport(base.replace(/\/$/, '') + '/v1/messages', {
        method: 'POST', signal: AbortSignal.timeout(45000),
        headers: { 'Content-Type': 'application/json', 'x-api-key': key, 'anthropic-version': '2023-06-01' },
        body: JSON.stringify(payload),
      });
      if (!upstream.ok) return reply(upstream.status === 429 ? 429 : 502, {
        error: `AI service unavailable (${upstream.status}). Your response is preserved; please try again.`,
      }, origin);
      const data = await upstream.json();
      const content = (Array.isArray(data.content) ? data.content : []).filter(p => p?.type === 'text' && typeof p.text === 'string').map(p => p.text).join('\n').trim();
      if (!content) return reply(502, { error: 'The AI returned no text. Your response is preserved; please try again.' }, origin);
      if (data.stop_reason === 'max_tokens') return reply(502, { error: 'The AI response was cut short. Your response is preserved; please try again with a shorter response.' }, origin);
      return reply(200, { content, usage: data.usage || null }, origin);
    } catch (error) {
      const timeout = ['TimeoutError', 'AbortError'].includes(error?.name);
      return reply(timeout ? 504 : 502, { error: timeout ? 'AI feedback timed out. Your response is preserved; please try again.' : 'AI feedback is unavailable. Your response is preserved; please try again.' }, origin);
    }
  };
}

export default async (req) => createHandler(name => Netlify.env.get(name))(req);

export const config = {
  rateLimit: { windowLimit: 120, windowSize: 60, aggregateBy: ['ip', 'domain'] },
};
