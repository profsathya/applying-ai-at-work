# Sprint 1 V2: remaining-page visual revision

## Scope and status

Local revision of the remaining five participant pages in course 180, storage sprint 12, using the approved first activity as the style reference. The first activity, other sprints, source design files, shared skills, and agent configuration are unchanged in this pass. No Canvas write or publication occurred. This is the agent's editorial judgment; the user authorized revision, not approval of the resulting five pages. No participant trial has been observed.

Fresh read-only `inspect_canvas.py --manifest course1/manifests/production.json --state-dir .canvas-state --include-items --drift --format json` found no target drift or inspection errors. Thirty older-sprint publish mismatches and an unpublished extra Introduction in the V2 module remain outside scope. The saved drift output is in the private evidence directory.

## Changes and alignment

- Introduction opens with the decision participants will make, shows the gather/check/choose route, groups submission expectations, and correctly states that this V2 module currently contains only the first half. Detailed distinctions stay where they are used.
- Workaround practice starts with observing a real routine over a day or two. An original report-formatting diagram illustrates the hidden cost before the cumulative-table response. The page deliberately gains an example.
- Request practice follows request → why → goal, then alternative obstacles. Self-requests, stuck rows, uncertainty, optional notes, and an honest no-result route remain explicit. The exact onboarding goal assessed by the concept check remains taught.
- Concept check preserves all six questions, options, correct answers, and criteria. Accessible question groups replace repetitive self-check disclosures; feedback remains on demand and does not grade in Canvas.
- Test and commit retains three to five candidates or documented recovery, four-line gaps, all four checks and verdicts, a two-week evidence horizon, a knowledgeable other person including the outside-household condition, size adjustment, uncertainty, personal connection, reasons for each alternative, runner-up, and recovery if nothing survives. Four response areas follow their instructions and export as one 35-point submission.

Schema now supports opt-in `guided_assignment.presentation: reading` for response/choice sequences without an AI feedback endpoint, and `page_presentation: reading` for pages. Compact remains restricted to one mapped response. The new presentation suppresses repeated opening/completion framing and uses one primary copy button with utilities in More options. Saved-draft keys, versions, identities, points, completion metadata, and Canvas submission behavior are preserved. Standard layouts retain their prior behavior. The implementation reference documents the added options.

Homepage-maintainer corrected the Introduction description to match orientation, first-half sequence, and submissions; existing goals and remaining copy still align.

## Before/after reading review

Counts use the same regex tokenizer on both snapshots. Visible words are browser innerText of the activity at 1280px with disclosures closed and a fresh context; they include controls and exclude collapsed criteria. Height is an observation, not a quality score.

| Page | Body before → after | Prompts before → after | Criteria before → after | Initially visible words before → after |
| --- | --- | --- | --- | --- |
| Introduction: Find the Problem Worth Solving | 386 → 310 | 0 → 0 | 0 → 0 | 421 → 319 |
| Start your list and get underneath it | 310 → 310 | 7 → 7 | 52 → 52 | 372 → 372 |
| Things you stopped noticing | 178 → 210 | 8 → 7 | 37 → 37 | 357 → 272 |
| Things somebody handed you | 509 → 386 | 11 → 8 | 47 → 47 | 691 → 449 |
| Sprint 1 Concept check | 64 → 69 | 83 → 83 | 54 → 54 | 471 → 392 |
| Test and commit | 1074 → 801 | 31 → 31 | 179 → 179 | 1288 → 892 |

The five revised bodies total 2211→1776 words, a 19.7% reduction. Initially visible text totals 3228→2324 words, a 28.0% reduction. The approved first page remains 310 body words and the same 2084px rendered activity height. No claim follows that fewer words demonstrate learning.

Parent inspected the before/after comparison for all five pages and the complete desktop/mobile revisions. Through a working-adult lens, the revised pages earn attention more effectively: the first action arrives sooner; examples expose useful distinctions; the table is carried forward rather than restarted; and participants can work immediately beside each explanation. Test and commit still asks substantial effort, because comparing and supporting candidates is the assessed work. It is easier to resume by labeled part, but should not be described as quick or empirically engaging.

Resolved visual findings: removed generated Overview and generic completion panels from opt-in reading pages; replaced the Test four-check table with labeled sections because mobile labels broke mid-word; replaced the Introduction submission table with labeled entries after inspecting 200% text. Semantic ordered-list diagrams remain readable without CSS arrows or color. All visuals are original text constructions; no external image license or credit is needed.

## Observed validation

- Worker per-artifact schema checks passed for all five; parent source evidence and identity/assessment assertions passed, followed by final `.venv/bin/python canvas_sync/schema.py --all`: PASS. Homepage worker also reported homepage and full-schema PASS. Final parent evidence regeneration accounts for the two visual corrections.
- `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python -m unittest discover`: 216 tests passed, including new reading-layout/schema tests, standard/compact regression, and runtime behavior. Initial unrestricted-environment run failed on fixture instance-URL mismatches; the isolated run passed. An initial new page test fixture retained assignment points; corrected to null before passing. No test failure was bypassed.
- Playwright/Chrome checked prior-version draft restoration, save/reload, primary copy, forced clipboard denial with revealed/focused fallback, cancel-clear, keyboard disclosure operation and focus, all six right/wrong concept explanations, and radio ArrowRight/Tab/Enter operation. No page errors. Desktop 1280px, mobile 390px, and 320px with 200% text passed page-overflow checks; screenshots and enlarged-text details were inspected. This is scoped accessibility QA, not screen-reader certification.
- Exact first-activity Markdown/evidence and compact CSS hashes match the turn-start snapshot. Other-sprint and agent/skill files match their snapshots. `git diff --check`: PASS. Existing urllib3/LibreSSL warning does not affect results.

## Review sources, skills, and next observation

Read the five baseline/revised artifacts and sidecars, approved first activity, homepage, authoring/presentation contracts, renderer/schema/runtime code, and earlier pilot reports. Worker also read historical Sprint 1 Dojo/framing context without changing it. The original DOCX remains unavailable: provenance records authorized adaptation of verified local material, inherited source lineage, baseline hashes, and each private adaptation-map hash, not a new original-source conversion.

Skills consulted: writing-to-teach3, writing-assignments3, writing-learning-goals2, reviewing-course-text4; build-sprint and inspect-canvas workflows; maintain-homepage by the homepage worker. Parent owns this record. No consequential unresolved alignment decision found in this scope; second-half authoring and Canvas publication remain separate.

Participant-trial protocol: have a working professional attempt the same activity using each version with order counterbalanced across participants. Record time to first meaningful action, each reread/stall or clarification request, total active time separately from real observation days, and whether required evidence is complete. Ask what they would skip and why. Do not coach until the stall is recorded. No trial results are claimed here.

[Side-by-side comparison](http://127.0.0.1:8871/comparison.html) offers each page plus the unchanged reference. Private evidence: `.source-intake/sprint1-visual-refresh/` contains immutable before files, adaptation maps, drift output, counts, rendered measurements, test logs, browser scripts/results, and screenshots. QA responses were entered in an isolated browser context, not the user's browser drafts. Preview served from `.source-intake/async-pilot-qa/preview` on port 8871.

## Final reviewed fingerprints

| File | SHA-256 |
| --- | --- |
| `course1/sprints/sprint-12/introduction-find-the-problem-worth-solving-v2.md` | `267e0dd92dbbd64184744fc13367451c9efbb488b0196af1a2c0deabb05dead9` |
| `course1/sprints/sprint-12/introduction-find-the-problem-worth-solving-v2.sources.json` | `51eef0e1091d4b47cb4a8ccaeba4192aa89279d8c5330eb99fd1c4702dbe4203` |
| `course1/sprints/sprint-12/sprint-1-concept-check-v2.md` | `11642f31b10c5e385271238c982f280e96fc049efa9697e2fa32ccb062cac441` |
| `course1/sprints/sprint-12/sprint-1-concept-check-v2.sources.json` | `d7feb2346317cbaf6d737836da25876a29f58a8702b0f3402ec4142601e36a55` |
| `course1/sprints/sprint-12/test-and-commit-v2.md` | `7688765b551a996f1536a7ebb0aea3c4c680b7c2ce9da8d4b4249a8ac756a919` |
| `course1/sprints/sprint-12/test-and-commit-v2.sources.json` | `3e65e5d77976ba1e1a6430236b84a78dbf911dfa14157112e029614223b7286a` |
| `course1/sprints/sprint-12/things-somebody-handed-you-v2.md` | `00541f84468c38fa0e669db6299e67252ec32d1ea2a9b2fe611aadb4cc1941b4` |
| `course1/sprints/sprint-12/things-somebody-handed-you-v2.sources.json` | `0aef5885b98d68e7857578d21508c72246651aa6f18cb3eb30a83f17f51c28cc` |
| `course1/sprints/sprint-12/things-you-stopped-noticing-v2.md` | `6cf4def5e163d5a4fc0a2acc9c1824e5b31f874fe0b3997b6db3d7394c03731e` |
| `course1/sprints/sprint-12/things-you-stopped-noticing-v2.sources.json` | `60a0d6a8ee0cecd215ae88bf5ce73c311a29b9d880c12fa0767187ec6c149b15` |
| `course1/homepage.yaml` | `c6ba6b54386d0d89cbb2de55f9effd4820d6a08bc8becbc8ec2bb24b467d87a0` |
| `canvas_sync/guided_assignment.py` | `b6b8c40f8addcb5c00db184b2af22f5d80206147cf27c8a0ba03cb8d13b00b15` |
| `canvas_sync/assets/guided-reading.css` | `956d721bcf66ee4cb3c9cee53098ab6a1d2fb96b12a1ea66d272faa0ad04abba` |
| `canvas_sync/assets/guided-assignment.js` | `ed24b804fc9e5f1f3694a78910e090f4a3f073c1d1f157a2b2f67ec35a8fe690` |
| `canvas_sync/hosted_html.py` | `a762fd5cd0cb930ea8b32ebcbb8748ceb39034518c34cf9c35395910661f6007` |
| `canvas_sync/schema.py` | `a96c6703f0900f2ac476bc5fff0686a7f428b3f078f7567d7da875890289211e` |
| `schema/frontmatter.schema.json` | `02ac0d13fc9686b2871298f4dd234ae8086d4840f75e13455cffb90bdbb60fb1` |
| `tests/test_guided_assignment.py` | `477022e6008992c1ea0e1685c3b433cd115c8ebcebc427ab5ca1199271d39f80` |
| `tests/guided_assignment_runtime.cjs` | `99cfd8a8cd8d997b5d245a98bfeeb4788f79bc0ad7330a060d91c4019539538c` |
| `docs/AUTHORING_PRESENTATION.md` | `faccb2deb350632466a09e49aeb2ce9d4cb2af2fed4cb9c974fb946c87994412` |

Additional skill/reference hashes:

- `.agents/skills/reviewing-course-text/references/review-record.md`: `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`
- `.agents/skills/build-sprint/SKILL.md`: `cfa1bb5dc2392b01b81b93974b9d9238a4c4b4b23adf2457d123e424f2e96ec3`
- `.agents/skills/inspect-canvas/SKILL.md`: `87abe2d3c73d3c7ee313d75574b5d74c6891e5cfff4f8edf02a9a652e9e45404`
- `.agents/skills/maintain-homepage/SKILL.md`: `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7`
