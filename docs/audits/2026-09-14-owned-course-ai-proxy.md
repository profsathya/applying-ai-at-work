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

Prepared `course1/manifests/production.json` with `ai_activity.default_ai_endpoint` set to the new endpoint. The existing renderer honors this setting. The manifest was committed and pushed as `f27f76e`. Publish Canvas run `34884667971` succeeded, generated Common Curriculum commit `d848797`, and changed exactly 19 activity endpoint values. GitHub Pages run `34884770335` succeeded. HTTP readback verified all 19 published configurations use the new endpoint. No participant content, grading, submission mechanics, provenance sidecars, or homepage metadata changed.

Backend deployment and hosted-output publication are complete. The publishing workflow reported zero failed or drifted artifacts, zero artifact content pushes, and a successful hosted render. All 231 repository unit tests and four proxy test groups pass. Browser interaction verification is recorded below.

## Published browser verification

An already-open browser initially retained the old unversioned configuration and reproduced the old service's error despite all 19 configurations reading back correctly over HTTP. Fixed the renderer to add a deterministic settings hash to each configuration URL. Added a regression assertion that changing the endpoint changes the rendered shell. All 231 unit tests passed again.

- Cache fix commit: `29972bd`.
- Hosted-only publish: run `34885133217`, success, no Canvas access.
- Generated shell commit: Common Curriculum `87e4a80`, 19 shell URL changes.
- GitHub Pages deployment: run `34885220459`, success.
- Live Sprint 4 shell: configuration URL contains `?v=210d3ec6ee957875`.
- Actual browser test after reload: generation displayed three questions; saving the revised response changed completion to 1 of 1; Copy JSON displayed a success modal with the original response, three AI questions, observation, revised response, and correct activity identity.
- Reload preserved the completed response. Cleared only the synthetic QA identity/responses through the activity's own reset confirmation and verified blank fields and 0 of 1 complete afterward.

This test used a fictional example on the hosted activity, not a real participant's work. No test submission was sent to Canvas. The existing Submit on Canvas link still targets assignment 7131. The generation, save, persistence, and JSON export path is verified; a new Canvas upload was not performed.

## Direct Anthropic credential update

On 2026-09-14, the user explicitly requested replacing Gateway authentication with their Anthropic key. Stored it as a secret production-context Functions environment variable, ANTHROPIC_API_KEY, and set ANTHROPIC_BASE_URL to https://api.anthropic.com. No credential was written to repository files. Provider charges now belong to the key's Anthropic account; Netlify still hosts the proxy. The model remains claude-sonnet-4-5-20250929.

Production deploy 6aa84f6b38b7e0500d6e6918 completed successfully. Environment readback confirmed variable presence and direct endpoint without printing the secret. The live production proxy returned HTTP 200 for the Canvas demonstration's actual runtime prompts, fictional sample, and 512-token cap: three nonempty questions and an observation, 693 input tokens and 236 output tokens. Netlify request ID: 01M2GQD0P5RSKCY1J255BVSDTN. All four proxy test groups pass. This check exercised the API request used by Canvas; no new browser export or Canvas submission test was performed.
