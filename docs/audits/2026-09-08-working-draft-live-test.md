# Working Draft publication and live test

**Working Draft is published in Canvas Course 180, and the authenticated follow-up passed on September 9.** All six items were walked in Student View, a synthetic Candidate List submission was confirmed, and the disposable Test Student was reset. A homepage navigation defect was fixed, deployed, and verified through six actual Canvas homepage link clicks. Optional AI feedback remained unavailable on one bounded retry; the response and self-check remained usable. The external feedback service is the remaining unresolved limitation.

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

## September 8 browser and API evidence

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
| Authenticated Canvas homepage/LTI, native Next/Previous, student view and submission | Blocked on September 8 by the locked Mac; completed in the September 9 follow-up below |

September 8 public browser tests used an isolated Chrome context and generic synthetic responses. No participant data was used, and no Canvas submission, enrollment, grade, or message was created that day. Browser drafts were cleared where exercised; all test contexts were closed. The local iframe replica is explicitly a permissions test, not a substitute for an authenticated Canvas walkthrough.

The native CUA tool twice reported that the Mac was locked and automatic unlock was unavailable. An unlock request was sent in this task and relayed to the originating task. No alternate access to the locked authenticated session was attempted. The module and homepage were queued in the Codex browser panel for review.

## September 8 optional AI feedback investigation

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

Both accompanying Common Curriculum context-doc workflows succeeded. Source commits remain local on `codex/audit-canvas-maintenance`; they were not pushed or merged into main. Applying AI at Work main was `a078404d358125045b85422e89e76e4ae49ffc14` at the September 8 verification. The isolated hosted and state checkouts were clean and their remote branches matched the listed commits. Maintain this module from the feature branch until its source/schema changes are reviewed and integrated; do not use the older main schema to validate its new guided state.

Local raw evidence and reproducible attended scripts are under `course1/reports/working-draft-20260908/` (ignored diagnostics). September 8 files include `final-verified.json`, `final-ledger.json`, `final-hosted-http.json`, `live-hosted-browser.json`, `final-navigation.json`, `iframe-browser.json`, `feedback-contract-comparison.json`, `feedback-service-check.json`, `tests-final.log`, baseline/final API snapshots, and desktop/mobile PNGs. These records distinguish actual live results from simulated iframe permissions and the authenticated checks that were still pending that day.

## September 9 authenticated follow-up

The authenticated Codex in-app browser was available. The existing course tab was used through CUA, including Canvas's supported **View as Student**, **Reset Student**, and **Leave Student View** controls. No power or lock settings were changed. Generic, explicitly synthetic examples were used throughout; no real learner submission, grade, message, or enrollment was changed.

| Check | Observed result |
| --- | --- |
| Canvas homepage and LTI | Working Draft displayed all six items in the authenticated homepage and Student View |
| Native module flow | Next followed all six items in order; Previous returned from the second reading to the first; the final item had Previous and no Next |
| Candidate List in the actual Canvas iframe | Saved response survived reload; Copy my answers showed selectable copy text and an explicit non-submission message when clipboard access was denied |
| Actual Canvas submission | Exported guided response exactly matched the text entered into Canvas; Submit Assignment produced Submitted confirmation and visible submission preview |
| Homepage completion | Candidate List changed to Completed in Canvas after submission; the three viewed reading pages showed Completed; unsubmitted guided assignments remained Not completed |
| Concept check in the actual iframe | Unanswered guidance, wrong-answer explanation, corrected answer, and retained selection after reload passed; choices were cleared afterward |
| Test and Commit in the actual iframe | Eight response fields; saved response survived reload; Copy questions excluded the response; cancel-clear retained the response and clear removed it |
| Mobile reading | At 390 by 844, the Canvas document width was 390 and iframe document width 309, without horizontal document overflow; narrow table columns wrapped heavily and nested scrolling reduced reading space |
| Cleanup | Reset Student restored a clean disposable test account; all exercised browser drafts were cleared and Student View was exited |
| Final homepage navigation | After the fix below, all six actual homepage links opened the correct native Canvas item in the same tab; course breadcrumbs returned to the LTI homepage |

Candidate List assignment **7139** received synthetic Test Student **5707** submission **1619045** at **2026-09-09T16:37:37Z**. UI confirmation, submission preview, and API readback agreed: `online_text_entry`, attempt 1, submitted, and ungraded. The pre-test account had zero prior submission attempts or grades. Canvas Reset Student replaced it with Test Student **5813**; readback showed zero active submission attempts or grades. Candidate List's new record **1619111** was `unsubmitted`, with null body and attempt. This records supported account reset, not a claim that Canvas physically purged all historical records.

Exactly one live AI feedback click was made on September 9, inside the actual Test and Commit iframe in Canvas Student View. It first displayed Reading your response, then **Feedback is unavailable. Use the self-check criteria; your response is still here.** The synthetic response remained intact. CUA exposed the visible result and console logs but no raw network response, so the retry's HTTP status and body are unknown. The September 8 captured 502 must not be attributed to this retry. No additional paid comparison request or external service change was made; total attempted live feedback requests across both days is three. Backend identity and logs remain unavailable, leaving the service failure unresolved.

### Homepage navigation fix and final validation

The actual in-app Canvas homepage exposed a navigation defect: clicking a Working Draft link with `target="_blank"` did not open a page or new tab. Source-built homepage items now carry `data-canvas-target="_top"`, and the existing context handler applies that target when embedded in Canvas. Standalone web navigation retains its original target; legacy course links receive no override. A regression test covers both source-built and legacy behavior.

Source fix **`c410052`** changes only `canvas_sync/hosted_html.py` and its tests. All **204 tests passed**, along with repository schema validation and diff checks. No course Markdown, source evidence, Canvas artifact, or deployment-state change was needed for this fix.

The isolated Common Curriculum checkout first fast-forwarded over unrelated upstream updates, then deployed only `deanza/course1/home.html`, `index.html`, and `sprint-11.html` in [commit 5cdbb9d](https://github.com/profsathya/Common-Curriculum/commit/5cdbb9d5c97cbf40d21e50b739232ae0db4f0861). [Pages run 34378683954](https://github.com/profsathya/Common-Curriculum/actions/runs/34378683954) and [context-doc run 34378683851](https://github.com/profsathya/Common-Curriculum/actions/runs/34378683851) succeeded. All three canonical URLs returned HTTP 200 and matched the generated bytes. Six subsequent actual homepage link clicks confirmed the native destinations in the authenticated Canvas tab.

Before/after API checks again confirmed unchanged course settings, all **15** prior modules, **77** prior module items, and **88** prior deployment entries. Working Draft retained its published module and six item IDs. Authoritative `canvas-state` remains **`5d5a1ee0772a408f70726d0dc4cdee63f0916a82`**. Source fixes and this report remain committed locally on the feature branch; no source branch push or main merge was performed.

September 9 diagnostic evidence includes `september9-authenticated-browser.json`, `september9-test-submission.json`, `september9-test-student-after-reset.json`, `september9-before-verified.json`, `september9-after-verified.json`, `september9-navigation-http.json`, `september9-navigation-render.json`, and `september9-tests.log`. Actual browser screenshots were displayed during the attended CUA walkthrough. The course homepage was left available for review in the existing task browser.
