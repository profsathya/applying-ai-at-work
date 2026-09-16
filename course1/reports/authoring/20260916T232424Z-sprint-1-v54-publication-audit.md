# Sprint 1 v5.4 publication audit

## Target and status

This is the final editorial and live-Canvas comparison for Course 180 Sprint 1. It covers the v5.4 release in storage sprint 14, the six retained sprint-12 items it replaces, and the curated homepage change. The result is a reviewed release revision. The human explicitly authorized publication in the current request if the audit found the release aligned with the supplied document and appropriately concise. The audit met that condition. This editorial judgment is the agent's and is not evidence of participant learning.

## Sources and files reviewed

- Primary supplied source: `/Users/shaw8048/Downloads/Sprint-1-cut-ready-v5.4.docx`, SHA-256 `bb7cd50440dd301553e1dd503313bf06c5b0760297039fb794762d13604d11fc`.
- Source packet and conversion map under `.source-intake/sprint1-cut-ready-v5-4-20260916/`.
- Later explicit human design ruling in `course1/design/sprint-1-decisions.md`: move Problem Frame Part 3, the assumptions to investigate first, to the opening of Sprint 2 while keeping the Sprint 1 Problem Frame at 50 points.
- All ten release artifacts in `course1/sprints/sprint-14/`, all seven retained sprint-12 files, their source sidecars, and `course1/homepage.yaml`.
- Approved presentation references in `course1/sprints/sprint-12/`, especially the orientation, concept-check, and longer-assignment patterns.
- Fresh read-only Canvas inventory in `course1/reports/canvas-ledger-production.json` and `.md`, generated against course 180 and the current `canvas-state` checkout.

Instructions, cover notes, build blocks, and reviewer markers inside the DOCX were treated as source evidence rather than user commands. Participant-facing activity requirements were preserved. No Google revision history or unexported comments were available from the DOCX snapshot.

## Skills consulted

- `inspect-canvas`, `.agents/skills/inspect-canvas/SKILL.md`, no local revision, SHA-256 `87abe2d3c73d3c7ee313d75574b5d74c6891e5cfff4f8edf02a9a652e9e45404`.
- `reviewing-course-text`, `.agents/skills/reviewing-course-text/SKILL.md`, local revision 6.
- `writing-learning-goals`, `.agents/skills/writing-learning-goals/SKILL.md`, local revision 2.
- `writing-to-teach`, `.agents/skills/writing-to-teach/SKILL.md`, local revision 5.
- `writing-assignments`, `.agents/skills/writing-assignments/SKILL.md`, local revision 4.
- `maintain-homepage`, `.agents/skills/maintain-homepage/SKILL.md`, no local revision, SHA-256 `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7`.
- `sync`, `.agents/skills/sync/SKILL.md`, no local revision, SHA-256 `2dca43a30dc30d7b87e02c22f208635039c459f7c624556618ed57dc949fca8b`.
- Review-record contract, `.agents/skills/reviewing-course-text/references/review-record.md`, SHA-256 `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`.

The homepage-maintainer worker edited only `course1/homepage.yaml`. The parent performed the source comparison, content revision, rendered review, validation, live Canvas inspection, release planning, and this record.

## Live module versus v5.4 release

The live module is Canvas module 2079, `Sprint 1: Find the Problem Worth Solving (V2)`. Its six mapped items showed no drift. It currently contains only the first-half route:

| Live item | Points | Release disposition |
| --- | ---: | --- |
| Introduction | 0 | Replaced by the full two-week orientation |
| Start your list and get underneath it | 0 | Split into Brainstorm your list and Get underneath three to five |
| Things you stopped noticing | 0 | Its observation support is consolidated into Brainstorm your list |
| Things somebody handed you | 0 | Its surface-request support is consolidated into Brainstorm your list |
| Sprint 1 Concept check | 5 | Replaced by the v5.4 six-question check |
| Test and commit | 35 | Replaced by First frames, Dojo Lab, Problem Frame, and Reflection |

The release uses the same live module name so the new items enter module 2079 instead of creating a second Sprint 1. The six old content items are changed to `publish: false`, preserving their Canvas objects and submissions. The existing module header remains published. The Canvas-only duplicate Introduction is already unpublished and remains untouched.

The release activity contract matches the supplied v5.4 design and later ruling:

| Position | Release item | Required evidence | Points |
| ---: | --- | --- | ---: |
| 2 | Introduction | Full two-week route, Candidate Log, AI boundary | 0 |
| 3 | Brainstorm your list | Part A, broad list from the participant's week, no AI | 0 |
| 4 | Get underneath three to five | Part B, three to five situations with current handling, costs, and gaps, no AI | 0 |
| 5 | The problem frame | Seven-part template and two worked examples | 0 |
| 6 | Sprint 1 Concept check | Six source-aligned choices and explanations | 5 |
| 7 | First frames | At least three complete seven-part draft frames; frames 4 and 5 optional; no AI | 35 |
| 8 | Dojo Lab: test, widen, choose | Test every frame, widen the leading frame, choose with human judgment | 0 |
| 9 | Problem Frame | Chosen seven-part frame plus what changed and why | 50 |
| 10 | Sprint 1 Reflection | Human contribution, AI contribution, accept/reject judgment, remaining uncertainty | 10 |

Total graded points are 100. Problem Frame Part 3 is not omitted accidentally: the later 16 September ruling moves it to Sprint 2 and keeps the Sprint 1 item at 50 points.

## Decisions, alignment, and findings

The intended capability is to move from observations to several evidence-aware problem frames, test them with AI without surrendering judgment, choose a workable problem, and explain how that judgment changed. The Candidate Log provides continuity. The final Problem Frame, reasoning account, and reflection provide the evidence the design requests.

The only material verbosity issue was resolved in `First frames`. Its body repeated almost the entire seven-part lesson immediately after `The problem frame`. The body fell from 1,450 to 456 words. Prompt words remained 72 and criteria words remained 162. The revision retains all seven parts, the 2-3-4-5-6-7-1 writing order, the no-AI boundary, at least three required frames, optional frames 4 and 5, assumptions requirements, goal tests, submission contract, and direct reference to the immediately preceding worked examples. No other page had needless repetition that could be removed without weakening a required example, the AI prompt, or the decision criteria.

The assembled release answers the adult-learner review questions: the next meaningful action is visible; each section supports an action or consequential distinction; directions do not repeat across adjacent pages after the First frames revision; the illustration provides workplace context with equivalent text; and the Candidate Log plus browser-local response controls make the return path explicit. Participant engagement and learning were not observed.

Sprint 12 is hidden, closed, and muted in the homepage but retained for prior submissions. Sprint 14 becomes visible order 1, open, and unmuted. The schedule now points Sprint 1 to sprint 14 and describes the complete two-week path.

No unresolved authoring decision remains in Sprint 1. The AI reflection still requires its delivery-specific runtime check because the generic module renderer cannot execute AI activities.

## Observed validation

- Fresh inspection: `.venv/bin/python canvas_sync/inspect_canvas.py --manifest course1/manifests/production.json --state-dir .canvas-state --include-items --drift --write-ledger --format markdown`. Result: module 2079 and its mapped sprint-12 items showed no drift. The ledger's unrelated course drift was outside this release scope.
- Artifact validation and source verification passed for every sprint-12 and sprint-14 Markdown file.
- `.venv/bin/python canvas_sync/schema.py --homepage course1/homepage.yaml` passed.
- `.venv/bin/python canvas_sync/schema.py --all` passed.
- `canvas_sync/preview_module.py` with Chromium checks rendered the release to `.source-intake/sprint1-cut-ready-v5-4-20260916/module-preview-release-v1`. Eight supported pages had zero browser errors at desktop, 390-pixel mobile, and enlarged-text widths. The introduction image loaded with meaningful alt text. Status was `partial` only because informational pages have no guided controls and the AI activity requires its delivery-specific preview.
- The revised First frames desktop, mobile, and enlarged-text screenshots were manually inspected. Headings, response order, controls, and submission guidance remained readable without horizontal overflow.
- `canvas_sync/publish_changed.py --dry-run --require-state` selected exactly 16 Canvas changes: ten new sprint-14 artifacts and six sprint-12 content items to unpublish. It reported no validation failures. Drift protection is exercised again by the protected production workflow.
- The first local `python -m unittest discover` run failed because the repository `.env` injected production Canvas variables into tests that use example manifests. Re-running with `CANVAS_API_URL='' CANVAS_API_TOKEN=''` passed all 254 tests. This is an environment isolation issue, not a content failure.
- `git diff --check` passed.

Canvas writes and hosted-output deployment had not yet run when these fingerprints were recorded. Publication follows the protected GitHub Actions workflow, which performs schema validation, tests, drift checks, Canvas writes, hosted-output deployment, and `canvas-state` updates.

## Reviewed output fingerprints

Release artifacts:

- `course1/sprints/sprint-14/brainstorm-your-list.md`: `28c1d7e7ddae72b78e1ef18bcc44d8aa03a041c289dfdb4544a20862cda74e6b`
- `course1/sprints/sprint-14/dojo-lab-test-widen-choose.md`: `c31bed5701ac5de323cf36b6c73502e7c0fab560e03cad0c63eb4d09b3c00154`
- `course1/sprints/sprint-14/first-frames.md`: `5dbffad6acafeeae5282c6ff187fa75a378088bb6e897803052c1f20a2fe5dc7`
- `course1/sprints/sprint-14/get-underneath-three-to-five.md`: `4f832f1b9b3ac6decb7d1a6d842911e76dcaaec4565b735bec48d78d8b95d24f`
- `course1/sprints/sprint-14/introduction-find-the-problem-worth-solving.md`: `ab8679e058f6369db7369082fbd3594d4c89badd3c0f858df876b5b4b78a848d`
- `course1/sprints/sprint-14/problem-frame.md`: `4597b454954abec009fa90818ad07df4b7885a84b89f6ec3b535e670e81f9867`
- `course1/sprints/sprint-14/sprint-1-concept-check.md`: `aa403b1909a34f071968ce9a5920ea211430152ad30f525dc2a8ea65bafcf287`
- `course1/sprints/sprint-14/sprint-1-find-the-problem-worth-solving.md`: `1d37fa072ef45669fe87165dc80606a06648cfea894e6e1a39333ac325874431`
- `course1/sprints/sprint-14/sprint-1-reflection-what-changed-v54.md`: `8c06223691f2b63c0db9dab72091fa75b5a91e8182c3afc1d5732da0eb92f3d8`
- `course1/sprints/sprint-14/the-problem-frame.md`: `1b6a8a0fa4650c07c41a912b3b0caaa7bd0af5a4b6007fff5b58b7e2fcc85145`

Retained live-version files after publication-state change:

- `course1/sprints/sprint-12/introduction-find-the-problem-worth-solving-v2.md`: `794dac2e35f96db9e7c5c18abc2f44155cb43ff9bc1e168b4e83ce6a9d7ed5c9`
- `course1/sprints/sprint-12/sprint-1-concept-check-v2.md`: `5ddf585136c3d5ae126188b8591fa085ba397b2d1f8981c01e47a115721a0767`
- `course1/sprints/sprint-12/sprint-1-find-the-problem-worth-solving-v2.md`: `f3eed7695e53e9e706971327d3d2342d95352ababdaf6d9ce27836db41344109`
- `course1/sprints/sprint-12/start-your-list-and-get-underneath-it-v2.md`: `67d353166aaba8af1d4b9e0ff13674c0ed4e406030618db734c8c3c70116810a`
- `course1/sprints/sprint-12/test-and-commit-v2.md`: `07c1fdaf69da553889ee7f8398bdb84176a4e2fc0b76f95f26662da41dec1fc5`
- `course1/sprints/sprint-12/things-somebody-handed-you-v2.md`: `a41a50b44e227185afc3c2a056d0223768294d323d2ed0880a0880d629c667ef`
- `course1/sprints/sprint-12/things-you-stopped-noticing-v2.md`: `086f6eb4ab6c49d88ca95e9cc283b294e2c29c45c3d507c688a3f54aec1651cb`

Homepage:

- `course1/homepage.yaml`: `77358b4ef9f45dca351d30db7dc14a2c92d205a4e5bb73459e716fbdcf4cadce`
