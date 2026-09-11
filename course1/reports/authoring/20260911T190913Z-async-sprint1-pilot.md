# Sprint 1 asynchronous delivery pilot: audit and review

## Status and scope

Implemented locally at the user's explicit request: shared authoring instructions, the six participant-facing Sprint 1 V2 artifacts in course 180 (`course1/sprints/sprint-12`), and an opt-in guided-activity layout. This is an agent editorial assessment and a local review candidate, not human approval or observed learning effectiveness. No Canvas write, Git commit, merge, or website publication was performed. Production publication remains a separate step.

Baseline: Git `c2182cc007b3f47f18ed633b0ca2de16610a2f55`. Inspector used freshly fetched `canvas-state` revision `237638e5cd92d33b7d24a99ec5b502aa4afcfd97`, at `.canvas-state`. Ledger timestamp: 2026-09-11T19:01:30Z. All six target items passed the drift check; all are published and mapped in module 2079. This compares Canvas shells and settings, not remote hosted lesson HTML. The unmapped, unpublished older Introduction was preserved. Thirty legacy items with drift and six missing legacy paths outside Sprint 12 were not changed.

## Findings and corrective changes

| Contributor and evidence | Correction | Assessment |
| --- | --- | --- |
| Writing skills requested explanation, examples, and sufficient directions, while brevity guidance did not distinguish lesson, prompt, and criteria. | Explicitly assign teaching, action, and evaluative jobs; keep explanations only when they support an action or consequential distinction. | Instructions plausibly contributed to expansion; not proof of a single cause. |
| The September 10 first-half review records source wording preservation plus newly authored task metadata. The design decisions already identify excessive verification depth. | Distinguish faithful conversion from authorized instructional adaptation; record revised prose as adaptations. | Much length was inherited from the draft rather than invented by the renderer. |
| Previous Test and commit repeated specific-person guidance in prose, a comparison table, another example pair, task prompt, and criteria. The concept-check body repeated questions already in task configuration. | Keep one useful distinction/example at the task; remove duplicated question body and procedural criteria. | Reduced duplicate reading while retaining practice and feedback. |
| `guided_assignment.py` placed all lesson text in a collapsed panel before a second task sequence. Generated headings and copy/save controls occupied much of the first mobile screen. | Opt-in `instruction_section` places teaching visibly before its task. Compact framing; export controls follow work. | Verified in rendered desktop/mobile pages. |
| Prior review documented functional/source checks but accepted overall reading burden. | Require an assembled reading/action review, with separate counts and participant-test status. | Software validity remains separate from teaching quality. |

The principles are grounded in [IES guidance](https://ies.ed.gov/ncee/wwc/PracticeGuide/1), which supports alternating examples with practice and retrieval, and [Quality Matters' online-learner expectations](https://www.qualitymatters.org/qa-resources/resource-center/articles-resources/bill-of-rights-for-online-learners), which call for efficient navigation, sufficient instructions, and alignment. Neither sets a universal word limit. No word quota or new assessment policy was introduced.

## Before and after

Word tokens use `\b[\w]+(?:['’-][\w]+)*\b`, including Markdown headings. Body, task prompts, and criteria are counted separately; figures exclude shared interface text, purpose/prerequisite metadata, options, and feedback. They are source-size measures, not visible-screen counts or time estimates.

| Artifact | Body before → after | Prompts before → after | Criteria before → after |
| --- | ---: | ---: | ---: |
| Introduction: Find the Problem Worth Solving | 1,464 → 386 | 0 → 0 | 0 → 0 |
| Sprint 1 Concept check | 309 → 64 | 83 → 83 | 96 → 54 |
| Start your list and get underneath it | 1,778 → 527 | 70 → 9 | 152 → 52 |
| Test and commit | 3,539 → 1,074 | 266 → 31 | 534 → 179 |
| Things somebody handed you | 1,686 → 509 | 66 → 11 | 122 → 47 |
| Things you stopped noticing | 361 → 178 | 63 → 8 | 95 → 37 |
| **Total** | **9,137 → 2,738** | **548 → 142** | **999 → 369** |

Body reduction: approximately 70%. No claim that this proves faster completion or improved learning.

## Alignment and review decisions

The audience remains working professionals drawing on their own situations. The capability is choosing a specific, workable problem with justified uncertainty, supported by observation rather than invented evidence.

| Capability/practice | Retained evidence and support |
| --- | --- |
| Move from irritation to a describable gap | Three-column cumulative table, illustrative rows, a repeated-examination example, distinction from blame/fixes, uncertainty, and stalled/empty routes. |
| Notice habitual workarounds | Real observation over a day or two; a no-new-observation result remains acceptable. |
| Look beneath requested solutions | Request → goal → alternative obstacles, self-issued requests, observable additions, and distinction between working notes and submitted table. |
| Recognize the taught distinctions | All six concept-check prompts, options, correct indices, and explanations preserved exactly. |
| Choose a workable candidate | Three to five four-line descriptions, four checks with verdicts, scope adjustment, uncertainty, commitment, alternatives, personal connection, runner-up, and recovery. |

Check 4 permits referring to the Part 2 current-state description rather than rewriting it. It still checks paragraph-sized scope, another person, and an unknown. No new interview, verification task, mandatory practice submission, or graded deliverable was added. The concept check remains 5 completion points; Test and commit remains one 35-point text entry. Practice remains optional to submit, at zero points. Artifact identities, task IDs/kinds, configuration version, positions, and other assessment metadata are unchanged.

Visual review resolved two issues after the first render: excessive setup/control space before teaching, and a narrow Introduction table. The Introduction now uses three numbered steps. The required example table has a keyboard-focusable horizontal scroll region on mobile. Task teaching is visible, self-checks are collapsible, and each referenced section appears once before its response. Parent reviewed all six final bodies/configurations, desktop/mobile captures, and the Check 4 clarification.

Homepage-maintainer reviewed every Sprint 12 artifact and the existing curated metadata; no homepage change was warranted. Goals, prerequisites, item descriptions, and open/muted state remain accurate. Parent confirmed all 82 other tracked sprint-content/evidence files (including the module header pair) and homepage bytes remain unchanged. Source design files and other course versions were not edited. The second-half roadmap remains existing context; this pilot does not supply missing second-half material.

## Source authority and reproducibility

The raw DOCX/private intake packet is unavailable in this checkout. The drafter verified each original Markdown/evidence pair and its bytes against the baseline Git commit. Rewritten bodies are `kind: new` adaptations with reasons and inherited references. Each sidecar records `revision_lineage`: baseline Git/path/MD hash/evidence hash and prior packet/map/source roles. Historical packet information is not represented as a newly parsed source.

The private repository-adaptation map is `.source-intake/async-sprint1-adaptation/adaptation-map.json`; current SHA-256 `215ccc3d409f3376398971500b6261f8962af3b15b7d5ab3355ef38925e8ce2d`. Baseline snapshots remain unchanged; earlier adaptation maps were archived. This is a documented repository adaptation, not a `source_build.py --packet` reassembly from unavailable original bytes. Standard evidence verification passes without changing the provenance validator.

## Delivery interface and compatibility

`guided_assignment.tasks[].instruction_section` is optional. It names one unique visible, top-level `##` heading; its section ends at the next top-level level-two heading. Inline emphasis is accepted. Missing/ambiguous headings and duplicate references fail validation; code-fence or quoted headings do not count. Referenced sections follow task order. Unreferenced teaching stays visible before the tasks. Existing activities without references retain their layout and controls. The metadata addition does not change local-storage identity/version, copying, grading, or submission semantics.

The new shared module is `canvas_sync/instruction_sections.py`; integration is in the guided renderer, hosted renderer, and schema validator. Generated HTML remains output only. No model service, endpoint, dependency, or Canvas API change was introduced.

## Observed validation

- Inspector-reported: live target drift clear using the current external state; no target errors/orphans.
- Parent: per-artifact validation and `verify_evidence` passed for all six final pairs; identity/assessment/storage comparison passed; all six concept question/option/key/explanation comparisons exact.
- Parent: `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python canvas_sync/schema.py --all` passed after final content and homepage review.
- Parent: `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python -m unittest discover` passed **213 tests** on the final runtime. Includes section matching/order/duplicates, legacy rendering, source tests, and save/copy/feedback runtime checks.
- Parent: four updated skills passed `quick_validate.py`; agent TOML parsed; local instruction links and `git diff --check` passed.
- Parent: Playwright with installed Chrome inspected six pages at 1280×900 and 390×844. Five activities restored drafts created through the prior layout; save/reload, copying and selectable output text, keyboard self-check operation, and all six correct/incorrect choice-feedback paths passed. No page errors, viewport overflow, or outbound writes occurred. External requests were blocked in the isolated browser context; no live submissions were made.
- Parent: the example table accepted keyboard horizontal scrolling without viewport overflow. Desktop/mobile screenshots were visually inspected. Screenshot answers are explicitly QA samples in an isolated browser, not participant work.
- Homepage worker: homepage and full-schema checks passed; no YAML mutation.

Initial full-suite run inherited local Canvas environment values and hit instance-guard fixture mismatches; rerunning with empty Canvas URL/token passed without weakening the guard. The first browser harness read clipboard status before its asynchronous update; waiting for the actual status resolved the harness race. Both preliminary runs and successful final runs remain in private QA logs. The environment emits an existing urllib3/LibreSSL warning. These checks do not establish learning effectiveness or production deployment behavior.

## Participant trial protocol (not yet run)

Use two or three consenting working professionals with a real situation and no prior exposure to this draft. Have them use the revised sequence independently, including the observation interval; do not coach unless they cannot continue. Keep trial responses local rather than submitting or grading them in Canvas.

For each page, record active reading time, active work time, elapsed observation time separately, the first action they took, every stall and the text/control involved, any clarification supplied, and the work they produced. Ask them to return to one saved response and identify what will be submitted. At the end, ask what they could safely skip and what they still needed explained.

Review output completeness against the retained table, candidate, check, uncertainty, and commitment/recovery criteria. Treat a repeated misunderstanding or missing instruction as a revision trigger. Distinguish a deliberate uncertain/no-result answer from failure. Keep useful examples when they prevent stalls. Use the observations to revise specific passages; do not infer causality or generalize effectiveness from this small trial. No invitations or participant contacts were sent.

## Local preview and evidence

Before/after review: `http://127.0.0.1:8871/` while the local server is running. Files: `.source-intake/async-pilot-qa/preview/index.html`. Restart with `python3 -m http.server 8871 --bind 127.0.0.1 --directory .source-intake/async-pilot-qa/preview`.

Private QA: `acceptance-final.json`, `browser-results.json`, `render-results.json`, `unit-tests-final.log`, `schema-final.log`, screenshot PNGs, and preview/browser helper scripts under `.source-intake/async-pilot-qa/`. Source content remains in the tracked Markdown/evidence pairs.

## Sources, skills, and ownership

Parent consulted root guidance, READMEs/migration guidance, AUTHORING, DOCUMENT_INTAKE, the relevant skill/agent instructions, renderer/schema/source-build code and tests, six original/final Sprint 12 artifacts and portable evidence, the September 10 authoring/publication records, Sprint 1 design decisions, legacy Sprint 1/2 concept pages, and current homepage metadata. Drafter additionally read Welcome V2, Stakeholder Conversation V2, and the legacy Goal Plan and Problem Reframing Document. These neighboring sources were read-only. Original DOCX/native comments, participant observations, and remote hosted-text drift comparisons were unavailable/not performed.

Skills actually used: writing-to-teach revision 2, writing-assignments revision 2, writing-learning-goals revision 2, reviewing-course-text revision 3; build-sprint/course-drafter workflow; inspect-canvas (inspector); maintain-homepage (homepage worker); system skill-creator (parent). Parent owns the audit, final checks, and preview. No unresolved decision blocks local review; participant outcomes and publication remain unassessed.

## Final fingerprints

Computed after final content, homepage review, and validation. Homepage is unchanged context. The record does not hash itself.

| File | SHA-256 |
| --- | --- |
| `course1/sprints/sprint-12/introduction-find-the-problem-worth-solving-v2.md` | `9ed8f975931abb2b7784d5bd6c438315eb34bf08e130e51cefa93bb59fd232ea` |
| `course1/sprints/sprint-12/sprint-1-concept-check-v2.md` | `7c1d0b0e5e593748a178c6cd4c355fce832ccfa5cc13253c67bf8c77cff56e3b` |
| `course1/sprints/sprint-12/sprint-1-find-the-problem-worth-solving-v2.md` | `f3eed7695e53e9e706971327d3d2342d95352ababdaf6d9ce27836db41344109` |
| `course1/sprints/sprint-12/start-your-list-and-get-underneath-it-v2.md` | `9f885766e0576ef3ceb4061e68fcca36523e18f230c1b1c05ace20435d674c6c` |
| `course1/sprints/sprint-12/test-and-commit-v2.md` | `0c29e583839dd5087279718c30e67bc847ac7dc98455eee03d7f83df423ee64c` |
| `course1/sprints/sprint-12/things-somebody-handed-you-v2.md` | `da763822d89b94b5ef6f10ad8076ea35f337dc3837b1a13ccd213ec60df55a6d` |
| `course1/sprints/sprint-12/things-you-stopped-noticing-v2.md` | `64a9d87f6a8020a09c681a351f650b040c2c95e9466d846bf49b916d479d601b` |
| `course1/sprints/sprint-12/introduction-find-the-problem-worth-solving-v2.sources.json` | `fb86eda821a28c4eca3a56af184e2b164cbd6b61d0d6e99822724c3be82b640c` |
| `course1/sprints/sprint-12/sprint-1-concept-check-v2.sources.json` | `63e75e2456f4f067838c7d428fffc30769e3f14c88c45bec0d60eedc352b6b07` |
| `course1/sprints/sprint-12/sprint-1-find-the-problem-worth-solving-v2.sources.json` | `e1e50d27abaae8d031c46ab8207ddf188a927904068a7a741b23351a15857dbe` |
| `course1/sprints/sprint-12/start-your-list-and-get-underneath-it-v2.sources.json` | `db876899c52d161de7cf7fde78ee5ff622825a0f5ba60bccfe315b2a62156fac` |
| `course1/sprints/sprint-12/test-and-commit-v2.sources.json` | `c48f158db25ecfcf418ccc08062d375fed2f6487fb922c471e1f4bbcad9d7cef` |
| `course1/sprints/sprint-12/things-somebody-handed-you-v2.sources.json` | `90ce3dfea75fd2f2372f52ae2b09d0c79fa878f4f88e84d659439d0515bdb690` |
| `course1/sprints/sprint-12/things-you-stopped-noticing-v2.sources.json` | `2f942047126d06c2c27841c8882cc5fa1e49a6b0df8f32abcd991017bc0a1138` |
| `course1/homepage.yaml` | `930b4293efbc41444bfd3dc72165ad5e72811c91b1c1608c60bfe79d344327ee` |

Instruction and implementation versions:

| File | SHA-256 |
| --- | --- |
| `.agents/skills/writing-to-teach/SKILL.md` | `280d1d3cffbce234fce4899185e80c89030dce31fb14aeed6da8c3fa6ef67dcc` |
| `.agents/skills/writing-assignments/SKILL.md` | `ce0b66defe8114b3d5e4ec5484e2af32e012ca51d70aa1a8bcfae9cb2a417a4c` |
| `.agents/skills/writing-learning-goals/SKILL.md` | `0a9427039031806b7eea78d5bf6a9fb22c629bf70b9cd20e42169fe817eca9da` |
| `.agents/skills/reviewing-course-text/SKILL.md` | `179bb37b2fbd2cc1c3067b2f0517c03d9de99de0f8622d2a870a29dcc757d1ab` |
| `.agents/skills/reviewing-course-text/references/review-record.md` | `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e` |
| `.agents/skills/build-sprint/SKILL.md` | `cfa1bb5dc2392b01b81b93974b9d9238a4c4b4b23adf2457d123e424f2e96ec3` |
| `.agents/skills/inspect-canvas/SKILL.md` | `87abe2d3c73d3c7ee313d75574b5d74c6891e5cfff4f8edf02a9a652e9e45404` |
| `.agents/skills/maintain-homepage/SKILL.md` | `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7` |
| `.codex/agents/course-drafter.toml` | `36bbc49224f8e6a6955327bb3921abe925521da44597af8d324bd9b4d54e4af4` |
| `docs/AUTHORING.md` | `e8e3b4a9a17344ba4919df9915f2d8f8592221e747b2e85cd1e9385d904bafe4` |
| `docs/DOCUMENT_INTAKE.md` | `a9285ff8ec542eb5be9873d679916d754f9b890dad0b1def58055138d157b9ab` |
| `canvas_sync/instruction_sections.py` | `0c3d7c31ebc00e8cd5bc833d4d94388087fb67f3f0b8f16b6e6eacec489600b3` |
| `canvas_sync/guided_assignment.py` | `8a95d4d48d5fad010da4a80b18a55d6e5623122ec801d63ad985916945c67920` |
| `canvas_sync/hosted_html.py` | `47b67a945adfac4908faff1f913656ca45a0601bbaef72f20209202f4702703a` |
| `canvas_sync/schema.py` | `338248611f2c7c251b520089d3e455fb4b2c4f21132e3074a9790e532095aba8` |
| `canvas_sync/assets/guided-assignment.css` | `f37eacbb07891b77dc6d9064a11f7d475c98ecd52223cfa1fc45301ba0ef55bd` |
| `schema/frontmatter.schema.json` | `b21ed7d785d510a2209e0d754c40672f426637bf6e4fb65a966a79c6f5905ed6` |
| `tests/test_guided_assignment.py` | `423243bbbede27eb12644995f5a4a971ed99ac6f7098c4370f96c6416bfa474b` |
| `/Users/shaw8048/.codex/skills/.system/skill-creator/SKILL.md` | `6656e54755638e8efcf275a472b9672eaa8a9a1b9e59dc210e275b03b59e1e66` |
