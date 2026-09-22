# CTI Course AI

A standalone Netlify service owned by CTI. It does not deploy or modify the Canvas progress service.

- Project: `cti-course-ai`
- Site ID: `5fbb91f5-6f85-4ef7-9c47-de3b5608b7a5`
- Endpoint: `https://cti-course-ai.netlify.app/.netlify/functions/ai-proxy`
- Request: `{system?, messages, max_tokens?}`
- Response: `{content, usage}`

## Provider

Production uses a project-specific Anthropic API key stored as a secret, production-context Netlify Functions environment variable (`ANTHROPIC_API_KEY`). `ANTHROPIC_BASE_URL` is set to `https://api.anthropic.com`, so requests go directly to Anthropic and provider usage is billed to the key's Anthropic account. Both variables must be present; the service returns 503 without them. Netlify still hosts the function.

The default model is `claude-sonnet-4-5-20250929`. `COURSE_AI_MODEL` is a server-side override. Callers cannot choose models, enable tools, or turn on streaming. Do not add credentials to source or browser code.

`/.netlify/functions/brainstorm-your-list` is a separate, activity-scoped route pinned to `claude-sonnet-5`. It accepts only a section key, an editable category label, and participant response text. Its curriculum instructions and criteria are server-side; callers cannot provide system messages, change models, or enable tools. Participant text is treated as untrusted data. The general `ai-proxy` endpoint and its model default are unchanged.

## Limits

Only configured browser origins are accepted (`AI_ALLOWED_ORIGINS`, comma-separated; defaults to the course GitHub Pages origin and this project's production origin). Origin checking is not authentication: scripts can spoof Origin. Netlify's function rate limit is 120 requests per minute per IP/domain, including preflights; a shared campus network shares this allowance. It is not a team-wide spending cap. Monitor provider usage in the Anthropic console and function usage in Netlify.

Text-only requests: 40 messages, 60,000 content characters, 80,000 serialized characters, and 2,500 output tokens maximum. Provider timeout: 45 seconds. Empty or truncated responses are reported as failures, never valid feedback. The function does not log prompts, responses, or provider secrets.

## Test and deploy

From this directory, with Node 22.18+:

```sh
npm test
netlify deploy --site 5fbb91f5-6f85-4ef7-9c47-de3b5608b7a5 --prod --dir public --functions netlify/functions --no-build
```

Deploy only this directory to this project. Never deploy it to `canvas-progress-lti`.

## Course connection

The course renderer already supports `ai_activity.default_ai_endpoint` in the production manifest. Set it to the endpoint above, then use the normal reviewed hosted-output publication workflow. Existing published activities keep their old endpoint until regenerated and published. This does not require changing assignment wording or submission types.

## References

- https://docs.netlify.com/build/ai-gateway/overview/
- https://docs.netlify.com/manage/security/secure-access-to-sites/rate-limiting/
