# Working Draft publication and live test

**Working Draft is published in Canvas Course 180.** Its hosted pages, homepage links, native resource settings, source fidelity, and idempotent publication passed verification. The authenticated Canvas walkthrough and a real test-student submission remain blocked because the Mac is locked. Optional AI feedback failed on the tested new-page request; the response and self-check remained usable. This is not a claim of complete end-to-end learner validation.

## Open the module

- [Canvas Working Draft module](https://cti-courses.instructure.com/courses/180/modules#module_2078), module **2078**, published at position **16**.
- [Canvas course homepage](https://cti-courses.instructure.com/courses/180).
- [Hosted course homepage](https://profsathya.github.io/Common-Curriculum/deanza/course1/home.html?context=web), with Working Draft expanded and visible.
- [Standalone module index](https://profsathya.github.io/Common-Curriculum/deanza/course1/sprint-11.html?context=web).

Target identity was verified live as `cti-de-anza-test-course`, course ID **180**, on `cti-courses.instructure.com`. It remains available/private. The current-turn instruction explicitly authorized this additive sandbox publication, hosted output, and deployment-state writes.

Seven local artifacts supply one module header and six Canvas items. Module headers create module metadata rather than a separate learner page. The six items preserve their source positions 2 through 7, in the order below.

| Item | Canvas type | Content ID | Module-item ID | Points |
| --- | --- | --- | --- | --- |
| [Start with what bugs you](https://cti-courses.instructure.com/courses/180/modules/items/17961) | Page | 3617 | 17961 | - |
| [Two other places to look](https://cti-courses.instructure.com/courses/180/modules/items/17962) | Page | 3618 | 17962 | - |
| [Candidate List](https://cti-courses.instructure.com/courses/180/modules/items/17963) | Assignment | 7139 | 17963 | 15 |
| [Problem-Finding Concept Check](https://cti-courses.instructure.com/courses/180/modules/items/17964) | Assignment | 7140 | 17964 | 5 |
| [Four checks for a workable problem](https://cti-courses.instructure.com/courses/180/modules/items/17965) | Page | 3619 | 17965 | - |
| [Test and Commit](https://cti-courses.instructure.com/courses/180/modules/items/17966) | Assignment | 7141 | 17966 | 20 |

All six are published. Assignments use `online_text_entry`, points grading, no due date, and `must_submit`. Pages use `must_view`. The concept check remains formative guided coursework with instructor-reviewed completion points, not a native Canvas quiz or automatic grade. No rubric object was added.

## Source and scope preservation

The reviewed build map was rebuilt with `source_build.py --publish-ready`, using the original packet and source bytes. Every selected source/body part remains identical to the prior committed first-half draft; metadata now uses module name **Working Draft** and publication enabled. Module title is also Working Draft. Adjacent evidence records were regenerated through the builder. No second-half content was created. See the [document intake/build audit](2026-09-08-document-intake-build.md) for source selection and provenance.

All 15 pre-existing modules, their 77 full module-item responses, all course settings, and the 88 prior deployment entries match their baseline. Original Sprint 1 (1946) and smoke module (2077) remain intact. The 30 pre-existing publication-status differences, six missing legacy local paths, and three empty unmapped modules were not changed. Final inspection found zero drift in sprint-11, no drift errors, and no orphaned objects.

Only ten generated paths were deployed: six instruction pages, `sprint-11.html`, `home.html`, its `index.html` alias, and `progress-map.json`. Other course output was rendered only into isolated staging. The homepage addition preserves the preceding module blocks, and previous progress-map entries are unchanged. After object creation, a second scoped deployment added actual Canvas destinations and completion mappings. Canonical URLs for all ten files returned HTTP 200 and matched generated SHA-256 bytes.

## Browser and API evidence

| Check | Result and scope |
| --- | --- |
| Full repository tests | **203 passed** after the deployment-state schema fix |
| Artifact, homepage, complete repository, external-state schema; diff checks | Passed |
| Native Canvas identity, title, publication, order, points, submission type, completion, hosted iframe/fallback | Passed API readback |
| Repeated scoped publication | Same module/content/item IDs, six items, **zero Canvas writes**, unchanged prior state |
| Live public homepage | Working Draft expanded; six actual link clicks opened the correct pages; each returned to the module |
| Canvas-context homepage routing | Browser verified all six links switch to the actual native Canvas destinations; this was a public hosted page with `context=canvas`, not an authenticated LTI session |
| Reading and tables | Three reading pages inspected; mobile table layout and all six pages fit 390px without horizontal overflow; no editorial markers or storage sprint number shown |
| Candidate List | Synthetic response saved and survived reload; copy output matched; clear removed its draft |
| Concept check | Unanswered guidance, wrong-answer explanation, corrected answer, and saved selection after reload passed; no AI call or automatic grade |
| Test and Commit | Eight response fields, explicit feedback request, preserved response on service failure, clear/cancel controls passed |
| Copy fallback | Live published Candidate List inside a local replica of the observed Canvas iframe triggered browser clipboard denial and displayed selectable text plus honest non-submission status |
| JavaScript runtime errors | None in the main live hosted-page suite |
| Authenticated Canvas homepage/LTI, native Next/Previous, student view and submission | **Pending Mac unlock**; not inferred from API or public-page tests |

Public browser tests used an isolated Chrome context and generic synthetic responses. No participant data was used, and no Canvas submission, enrollment, grade, or message was created. Browser drafts were cleared where exercised; all test contexts were closed. The local iframe replica is explicitly a permissions test, not a substitute for an authenticated Canvas walkthrough.

The native CUA tool twice reported that the Mac was locked and automatic unlock was unavailable. An unlock request was sent in this task and relayed to the originating task. No alternate access to the locked authenticated session was attempted. The module and homepage were queued in the Codex browser panel for review.

## Optional AI feedback investigation

A real browser click on the published Test and Commit page made one synthetic request to the existing `ai-assisted-pedagogy.netlify.app/.netlify/functions/ai-proxy`. The response was **HTTP 502**, JSON `{"error":"Empty response from AI service"}`. The page displayed its unavailable-feedback message and retained the typed response. The self-check remained available. No new account, provider credential, model, or service was configured.

The original [Common Curriculum Test and Commit reference](https://profsathya.github.io/Common-Curriculum/deanza-trial/test-and-commit.html) and the builder use the same transport contract: POST, `Content-Type: application/json`, `system`, one `messages` entry with role `user` and string content, and `max_tokens: 320`. Both accept a nonempty string from `content` or `text`. Our intentional differences are task/criteria prompt framing, a 30-second abort timeout, and stale-response protection. The observed HTTP error was returned before the new client's response parser ran, so a client `content`/`text` parsing mismatch did not create this 502. Prompt-specific or transient provider behavior remains possible.

One bounded synthetic comparison request was made through the actual reference page. Its response was received, but the test harness incorrectly waited for the button to re-enable; the reference intentionally keeps it disabled after a successful response until the answer changes. The harness timed out before persisting the HTTP status/body. **That comparison is inconclusive; it does not establish a reference failure or a service-wide outage.** The harness capture was corrected for future use, but no further paid request was made. Total attempted live feedback requests: two, one new page and one reference.

A separate no-provider preflight returned 204 with the GitHub Pages origin allowed; a request without Origin returned 403. The browser call supplied no application authorization header or credentials. Current Common Curriculum repository code routes this proxy to Anthropic and defaults to the configured Sonnet alias, but the deployed provider/model/account could not be verified from the failed live response. The connected Netlify lookup returned no matching project, so backend deployment identity and logs were unavailable. The root cause remains unresolved; no external service changes were made.

## Scoped fixes and commit records

The live state check exposed that `guided_assignment` was allowed in artifact frontmatter but missing from deployment/legacy-manifest delivery enums. Added the mode to deployment-state, manifest, and PRD schemas. A regression test now publishes a guided assignment to both external and legacy state, validates the persisted records, and loads them through `MaintenanceState`. A minor renderer fix also removes a whitespace-only line when a source-backed page has no generic goal banner.

| Repository / purpose | Commit or deployment |
| --- | --- |
| Source build from preceding turn | `8684d6826fa05f2b2a704d20d16f96efc00b9961` |
| Working Draft source publication metadata | `bbe1920` |
| Generated whitespace fix | `51000cf` |
| Guided deployment-state compatibility and regression | `a7c64a25bba5b10128344911fd25b42af1928ec0` |
| Initial hosted release | [cd4b70f](https://github.com/profsathya/Common-Curriculum/commit/cd4b70f1f234026ea1029e194f51757917b78681), [Pages run 34290092557](https://github.com/profsathya/Common-Curriculum/actions/runs/34290092557), succeeded |
| Hosted Canvas destinations and progress mappings | [6309735](https://github.com/profsathya/Common-Curriculum/commit/6309735f0f95c4ce771ad592234c336e84fe3242), [Pages run 34290382796](https://github.com/profsathya/Common-Curriculum/actions/runs/34290382796), succeeded |
| Authoritative `canvas-state` | [5d5a1ee](https://github.com/profsathya/applying-ai-at-work/commit/5d5a1ee0772a408f70726d0dc4cdee63f0916a82), committed and pushed |

Both accompanying Common Curriculum context-doc workflows succeeded. Source commits remain local on `codex/audit-canvas-maintenance`; they were not pushed or merged into main. Applying AI at Work main remains `a078404d358125045b85422e89e76e4ae49ffc14`. The isolated hosted and state checkouts are clean and their remote branches match the listed commits. Maintain this module from the feature branch until its source/schema changes are reviewed and integrated; do not use the older main schema to validate its new guided state.

Local raw evidence and reproducible attended scripts are under `course1/reports/working-draft-20260908/` (ignored diagnostics). Key files: `final-verified.json`, `final-ledger.json`, `final-hosted-http.json`, `live-hosted-browser.json`, `final-navigation.json`, `iframe-browser.json`, `feedback-contract-comparison.json`, `feedback-service-check.json`, `tests-final.log`, baseline/final API snapshots, and desktop/mobile PNGs. These records distinguish actual live results from simulated iframe permissions and pending authenticated checks.
