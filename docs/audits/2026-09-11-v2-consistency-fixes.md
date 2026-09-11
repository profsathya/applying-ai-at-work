# V2 consistency fixes and verification

This follow-up supersedes resolved findings in [the original Student View audit](2026-09-11-v2-student-view-audit.md). Scope: Orientation, Sprint 1 availability wording, Sprint 3, and Sprint 4. Sprint 2, Sprint 5, V1 placement, and unpublished duplicate drafts remain excluded.

## Implemented and verified in Canvas

- Native item order now matches the homepage in Orientation, Sprint 3, and Sprint 4. Existing module/item identities were retained. Ordering uses live Canvas state, handles sparse positions, and verifies the entire selected module sequence after publication, including repeat publishes without content changes.
- Quizzes 3096 and 3099 are published practice quizzes with unlimited attempts and no associated graded assignment. Existing questions were preserved. Settings-only publishing no longer deletes/recreates quiz questions; content replacements are refused when attempts exist.
- Introduction Post remains discussion 1533/assignment 7121, with zero points, complete/incomplete grading, exclusion from the final grade, and contribution-based completion. Its learning goal and peer-response directions now match the task.
- Rubrics 254, 255, and 256 are attached to assignments 7117, 7120, and 7119. Source criteria are unchanged: six criteria/35 points, seven/50, and four/10. Free-form criterion comments preserve the source's criteria-only grading approach. Criterion text, individual points, and assignment totals were read back before acknowledgment in deployment state.
- Scoped rendered headers use learner-facing module names and correct assignment labels. Raw TODOs were removed from the scoped Orientation and Sprint 4 pages. Submission guidance uses verified Canvas controls; optional unavailable assets are no longer promised. Essential unprovided instructor details remain operator follow-ups.
- Homepage wording explicitly bounds Sprint 1 to its first half, ending with Test and commit. Document-backed Sprint 1 source bodies and provenance were not altered.

A fresh API inspection found no source/content drift in storage sprints 6, 7, 8, or 12. Comparing complete before/after module records confirmed that modules outside the three corrected modules were unchanged, including Sprint 1, Sprint 5, V1 modules, and unpublished drafts.

## Actual Student View checks

- Read the final Modules list: all three corrected sequences match the requested order.
- Followed native Next from Stakeholder Conversation to Reflection; Previous points back to Stakeholder Map. AI Exchange now links back to Name the Gap and forward to Design the Learning Path.
- Completed Sprint 3 practice quiz: five questions rendered, a 5/5 feedback score appeared, and Take the Quiz Again allowed another attempt. Both practice checks are absent from the Test Student gradebook. Sprint 4 shows unlimited attempts and explicit ungraded instructions.
- Viewed all three native rubrics and verified their visible criteria and totals of 35, 50, and 10.
- Viewed Introduction Post's revised goal, complete/incomplete instructions, optional peer replies, and clean module label. No discussion reply was posted.
- Saved a disposable response in guided assignment 7144, reloaded and confirmed persistence, then submitted a disposable native Canvas text entry. Canvas displayed Submitted and submission details. Cleared the guided browser draft afterward.
- Homepage displayed the new first-half availability notice and read back completion progress after testing.

## AI Exchange: deployment dependency remains open

The frontend and proxy fixes are committed in Common Curriculum. The proxy now collects all supported text blocks, preserves the `{content, usage}` success interface, and returns actionable errors for empty output and timeout. The frontend validates question JSON, preserves input across errors/reloads, allows retry, and keeps failed/draft exchanges incomplete so they cannot unlock export. Updated scoped shells version the runtime URLs to avoid stale browser caches.

The live endpoint remains `https://ai-assisted-pedagogy.netlify.app/.netlify/functions/ai-proxy`. A real Student View request using a nonsensitive QA example still returned **Empty response from AI service**. Generation, follow-up completion, and successful JSON export/submission cannot be signed off.

The authenticated Netlify account lists seven accessible sites, but not `ai-assisted-pedagogy`. The connected Netlify project reader also returned no matching project. The local checkout is linked to the separate `canvas-progress-lti` site. No proxy was deployed to that unrelated site, and no provider/model or credential was changed. The site owner must deploy the committed proxy fix to `ai-assisted-pedagogy` (or provide access to that existing site), then repeat the successful-generation/export/submission test. GitHub Pages frontend deployment does not establish a Netlify function deployment. The underlying empty-output cause is not proven without that service's deployment/log access.

## Validation and rollout evidence

- `.venv/bin/python canvas_sync/schema.py --all`: PASS.
- `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python -m unittest discover`: 210 tests PASS. Empty variables isolate offline fixtures from local live credentials.
- `node --test tests/ai-proxy-response.test.js` in Common Curriculum: three tests PASS, covering multi-block/empty/timeout responses, malformed question JSON, and incomplete draft export gating.
- Broad Common Curriculum JavaScript test discovery ran 301 tests: 287 passed and 14 failed in unrelated existing curriculum-file and homepage expectations. Those content areas were not changed in this task; the full suite is not claimed green.
- Source commits: `8c1f164` (content/settings), `1b6e051` (sparse ordering), `f4a005a` (runtime cache refresh), and `4b63fb7` (versioned launch and sparse-position fixture). Common Curriculum runtime/proxy changes are included through `309ff3f`.
- [Publish 34625930101](https://github.com/profsathya/applying-ai-at-work/actions/runs/34625930101) published 17 items and blocked Stakeholder Map while the rubric API temporarily changed its points. Points were immediately restored to 35, the corrected rubric was read back, and its baseline fingerprint matched before continuing.
- [Publish 34626118181](https://github.com/profsathya/applying-ai-at-work/actions/runs/34626118181) completed the remaining content but correctly failed final order verification. The sparse-position correction followed.
- [Publish 34626400317](https://github.com/profsathya/applying-ai-at-work/actions/runs/34626400317) succeeded and recorded exact verified sequences for modules 2075, 2071, and 2074. Browser readback confirmed those sequences.
- [Repeat publish 34626882297](https://github.com/profsathya/applying-ai-at-work/actions/runs/34626882297) and [launch refresh publish 34627358361](https://github.com/profsathya/applying-ai-at-work/actions/runs/34627358361) succeeded with unchanged content and verified order.
- Rubric acknowledgment state commit: `54eefc5`; content state: `237638e`.
- [Common Curriculum Pages run 34626530454](https://github.com/profsathya/Common-Curriculum/actions/runs/34626530454) deployed runtime commit `309ff3f` successfully.

## Remaining inputs

Instructor biography and optional welcome video; verified weekly hour estimate; preferred instructor contact/response-time policy; dedicated Dojo walkthrough. Existing Canvas Inbox and lab guidance remain available without inventing those details. No Sprint 2 or Sprint 5 development is included.

The editorial review record is `course1/reports/authoring/20260911T170706Z-v2-consistency.md`. Rubric API behavior was checked against [Canvas's rubric documentation](https://developerdocs.instructure.com/services/canvas/resources/rubrics).

## Final runtime and cleanup verification

[Pages deployment 34627459710](https://github.com/profsathya/Common-Curriculum/actions/runs/34627459710) succeeded for generated-output commit `8381965`. In the actual Canvas iframe, the activity launch and both runtime scripts now include `v=v2-consistency-20260911`. The previously saved failed exchange remained available to edit but showed an unfinished question and disabled export even with a name entered. Clearing the test prompt and name persisted across reload; the activity returned to 0 of 1 questions answered. This verifies failure handling and draft cleanup, not successful AI generation.

Canvas Test Student was reset after testing and instructor view restored. API readback found zero Sprint 3 quiz attempts and returned 404 for the disposable test submission, confirming it was removed. The original course tab was restored to the course homepage. No real participant submission or discussion reply was created or altered.

The only functional blocker remaining from this scope is the AI service deployment/access dependency described above. Missing human-supplied assets and policies remain documented inputs; Sprint 2 and Sprint 5 remain deferred by instruction.
