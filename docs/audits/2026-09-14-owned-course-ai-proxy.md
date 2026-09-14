# CTI-owned course AI proxy

User requested rebuilding the feedback proxy on their Netlify account. Built and deployed a dedicated project so the existing Canvas progress/LTI deployment is not replaced.

## Deployment

- Team: Computing Talent Initative (`jeshaw`).
- Project: `cti-course-ai`.
- Site ID: `5fbb91f5-6f85-4ef7-9c47-de3b5608b7a5`.
- Production deploy: `6aa844820b42a55c8beb3159`, state `ready`.
- Dashboard: https://app.netlify.com/projects/cti-course-ai
- Endpoint: https://cti-course-ai.netlify.app/.netlify/functions/ai-proxy
- Source: `services/course-ai/`.
- Provider: Anthropic through Netlify AI Gateway, using injected gateway configuration.
- Model: `claude-sonnet-4-5-20250929`, fixed by server; caller cannot select a different model.

No provider credentials were copied from another site or added to source. Gateway requests consume the team's Netlify credits. No progress-service deployment or Canvas write was performed.

## Verification

- Four Node test groups pass: validation/origins, bounded model-controlled upstream calls and multi-block extraction, empty/truncated/error responses, timeout/configuration/preflight handling.
- Full repository schema validation passes.
- All 17 hosted-renderer tests pass.
- Live Sprint 4 request, using the existing runtime's exact discussion system prompt and the existing activity's question/context with a fictional handover example, returned HTTP 200 and a parseable JSON object containing three nonempty questions. Request ID: `01M2GMRBX3V26R8CVD4KWK6VBS`. The same request shape previously returned HTTP 502 from Sathya's endpoint.
- Live allowed-origin preflight returns 204 with the course GitHub Pages origin.
- Foreign-origin POST returns 403 before provider access.
- Empty message list returns 400.

Code declares a Netlify rate limit of 120 requests/minute/IP/domain. Production deploy summary confirms the function, but does not expose rate-limit validation; enforcement has not been load-tested. Origin restrictions are not authentication or a hard spend cap.

## Course connection and boundaries

Prepared `course1/manifests/production.json` with `ai_activity.default_ai_endpoint` set to the new endpoint. The existing renderer honors this setting. The manifest change is local and uncommitted; hosted course configs have not yet been regenerated/published, so existing Canvas activity links still use Sathya's endpoint. No participant content, grading, submission mechanics, provenance sidecars, or homepage metadata changed.

The backend build/deployment is complete. Hosted-output publication and the browser generation/save/export/Canvas-submission flow remain to be completed before claiming the learner-facing course is switched and verified.
