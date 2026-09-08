# Repository audit and implemented improvements

Date: 2026-09-08. Scope: Applying AI at Work, with read-only comparison against the saved Common Curriculum checkout.

The Markdown-to-Canvas architecture remains appropriate for the original product: a human supplies course or module context, the assistant drafts editable Markdown, deterministic code validates it, and reviewed content is published into an existing Canvas course. The main defects were at maintenance and recovery boundaries, not evidence that the model used to write older code made it obsolete. This audit implements focused fixes and preserves the curriculum.

## Review location and boundaries

- Worktree: `/Users/jeremyshaw/.codex/worktrees/fc1e/applying-ai-at-work`
- Branch: `codex/audit-canvas-maintenance`
- Starting commit: `a078404`.
- Comparison checkout: `/Users/jeremyshaw/Projects/common-curriculum`, observed at `dba3315`.
- Operator guide: [Canvas maintenance and recovery](../CANVAS_MAINTENANCE.md).

The worktree and both saved checkouts were clean at the start. Changes belong only to the audit worktree. No course sprint Markdown, design inputs, archive material, production manifest mappings, Common Curriculum output, or remote deployment state was edited. No Canvas API requests, production publish, merge, or remote push were used as tests. There is no new unattended model service or API-key requirement.

## Architecture and scope coverage

```text
Human course/module context
  -> Codex workflow and optional specialized authoring role
  -> editable Markdown with stable artifact_id
  -> schema validation and human review
  -> protected publish workflow
       -> Canvas native content or hosted assignment/page shells
       -> Common Curriculum HTML, activity JSON, indexes, progress map
       -> canvas-state IDs, content hashes, fingerprints, placement metadata
  -> inspection / reviewed reconciliation / maintenance using the same state
```

| Area reviewed | Responsibility and finding |
|---|---|
| `context/`, course designs, briefs, progress records, archive | Course intent and historical decisions. They are inputs and evidence, not interchangeable runtime state. Preserved. |
| All local sprint inventories and representative current assignments, quizzes, activities, and rubrics | Validated all 140 artifacts. Read the progression and newer revisions, including real stakeholder contact, confirmed versus inferred claims, and readiness judgments. Preserved instructional decisions. |
| `.agents/skills/`, `.codex/agents/`, root guidance | Drafting and planning belong to specialized authoring workflows; deterministic operations stay in Python. The audit is not a course rebuild. Updated five maintenance skills and two role instructions to carry external state selection consistently. |
| `schema.py`, schemas, `schema_windows.py` | Validation and course discovery. Fixed malformed frontmatter handling and named-course deployment paths. Retained the Windows validation shim; Windows writes were not tested. |
| `init_course.py`, bootstrap, hydrate, state, mapping, rubric acknowledgement | Local setup and deployment identity. Retained migration and mapping tools, added shared instance checks, and prevented a direct push from treating an unmigrated legacy-mapped course as empty external state. |
| `canvas_client.py`, `push.py`, completion | REST behavior, native/hosted delivery, identity, module placement and requirements. Fixed pagination, uncertain POST replay, early quiz identity persistence, short-answer answer payloads, and hosted batch rendering. Existing completion behavior remains covered by tests. |
| `publish_changed.py`, `publish_outcome.py` | Change selection, per-artifact isolation, output restoration, and state commit decisions. Fixed unproven fingerprint healing, renamed-source bookkeeping, and loss of known state during later failures. |
| Inspection, pull, single-item preparation, removal | Added a common external-state maintenance view and shared drift comparison. Hosted wrappers cannot replace source Markdown. Reconcile now has reviewed scopes, stale-token rejection, validation, and backups. |
| `hosted_html.py`, homepage metadata, Common Curriculum integration | Generated delivery, ActivityEngine configuration, Canvas links and progress integration. Rendered the complete hosted course and compared all output bytes against the starting implementation. Shared backend behavior was examined through its local callers, not live participant sessions. |
| GitHub workflows, cloud/devcontainer setup, requirements, config/script placeholders, operator docs | Protected publishing, validation, state preservation, multi-institution configuration and ownership. Named courses work in target resolution and state checks. Shared-code-only changes remain validation-only unless a course is explicitly dispatched. No dependency pins were changed. |
| Tests and legacy seams | Baseline 144 tests passed. Expanded meaningful recovery and compatibility coverage to 169 tests. Retained `CLAUDE.md`, the optional dual-CLI devcontainer, and archives because their present purpose is evidenced. Corrected misleading status documentation. |

The starting runtime inventory was 21 Python files, including `__init__.py`, and 18 test modules plus the tests package marker. Large files were not split merely because of line count. Three small modules now isolate shared drift comparison, the maintenance state view, and CI target resolution.

## Course and pedagogy findings

| Course | Local artifacts | Current evidence |
|---|---:|---|
| Course 1, Reframing Problems with AI / CIS 501 | 79 across 10 module names | 28 pages, 10 module headers, 19 assignments, 7 discussions, 15 quizzes. Nineteen artifacts use AI activity delivery. The legacy manifest holds 45 mappings; that count is not a live Canvas inventory. |
| Course 2, Building Solutions with AI | 0 | Design material for the follow-on solution course; no current production manifest or drafted sprint artifacts. |
| Course 3, Using the Agentic Course Workflow | 24 across 4 module names | 12 pages, 4 headers, 4 assignments, 4 quizzes; 24 legacy mappings. The course itself teaches human review and bounded operation of the repo. |
| Course 4, Science of Computing | 37 across 3 module names | 12 pages, 12 header artifacts, 9 assignments, 1 discussion, 3 quizzes; empty legacy mapping. Corrected its README's inaccurate claim that no artifacts had been drafted. |

The pedagogical center is human judgment in a real setting. Participants choose a consequential problem, direct and evaluate AI, seek stakeholder evidence, close a learning gap, and assemble a defensible readiness argument for later solution work. Their prior knowledge and relationships are inputs the model cannot supply.

Evidence in the actual materials supports that intent:

- `course1/sprints/sprint-7/stakeholder-conversation-v2.md` separates AI-assisted question preparation from contacting a real person, recording the interaction, and revising the problem frame. It includes concrete contact and follow-up steps.
- `course1/sprints/sprint-8/learn-and-check-v3.md` requires an independent check and distinguishes confirmed knowledge from inference. An unverified AI explanation remains an inference. It permits an unchanged goal plan when evidence honestly confirms it.
- `course1/sprints/sprint-5/final-integrated-problem-document-and-readiness-report.md` asks for evidence, human contribution, and a readiness judgment, including conditional readiness or a justified next step.
- Current Course 1 guidance broadens participation beyond people with a current employer while retaining real problems and affected people. The older audience document assumes current employment. This is instructional evolution, not grounds for deleting newer work.

Decisions left to the course owner:

1. Shared design material describes orientation plus four two-week sprints and a capstone week; current Course 1 describes five two-week sprints. Establish an explicit current authority map when revising the design documents.
2. The Sprint 5 V2 module at local `sprint-9` is explicitly a placeholder. Preserve the existing capstone until the new version is authored and reviewed. Physical sprint directory numbers, participant sprint numbers, and version labels are not equivalent.
3. The five-artifact map still contains authoring work to resolve. It is not automatically safe to publish because its schema passes.
4. Course 4 uses nine additional `module_header` artifacts as internal section headings within three module names. The current native push resolves modules by `module`, and does not create Canvas `SubHeader` items for those internal headings. Decide whether these are intended Canvas section labels before adding a new delivery type.

Empty PRD item lists are not automatically failures: the current full-course workflow intentionally does not require a PRD unless requested. Archive notes and progress logs describe earlier runs; they do not prove today's Canvas state. In particular, `publish: false` controls visibility, not whether a Canvas object can exist.

## Confirmed defects fixed

### 1. Maintenance could miss GitOps-published objects or use stale IDs

Inspection, reconciliation, preparation and removal used path-keyed legacy manifest mappings while normal publishing used external state keyed by `artifact_id`. The new `MaintenanceState` adapter selects one authoritative source, checks its instance, resolves current local paths by stable ID, and writes external changes back without mutating static manifests. Missing external state does not silently fall back. Existing legacy local operation remains available.

The shared state store and publishing/hydration/drift readers now reject a deployment file whose instance differs from the selected manifest. A direct push into missing external state refuses when legacy mappings indicate a migration is needed.

### 2. Reconciliation could replace instructional Markdown with hosted wrapper content

The old pull converted Canvas descriptions directly into Markdown, including descriptions that were only iframe shells. It also compared raw source Markdown against HTML converted back to Markdown, producing formatting-only drift. Single-item preparation could replace a hosted discussion's semantic type with `assignment`.

The shared drift comparator uses the actual published representation, checks iframe source URLs as well as fallback content, and preserves hosted source bodies and semantic types. Native quiz question differences are visible instead of omitted; unsupported question types fail rather than being relabeled as short answers. Short-answer answer keys survive supported imports and publishes.

Reconcile apply requires the token from the corresponding dry run, supports repeated `--file` selections, blocks simultaneous local/Canvas conflicts, validates before replacement, records backups, and advances the selected state after completed file updates. It never makes Canvas writes. This is an intentional CLI change; the maintenance guide and reconcile skill document it.

### 3. Missing fingerprints were treated as permission to overwrite

Previously any existing object without `canvas_fingerprint` could be adopted and overwritten even when its live content differed from source. Automatic recovery now requires the live representation to match the current source. An uncertain item is blocked individually while proven healthy neighbors continue.

Historical incident tests were revised deliberately: avoiding a course-wide halt is still required, but an unrelated item missing its baseline no longer authorizes overwriting different live content. This does not retroactively prove the exact historical remote state.

### 4. Some remote side effects could lose their recovery state

A quiz ID was saved only after all question requests returned, so a question failure could leave a real quiz with no recorded identity. Creation now checkpoints its ID before those requests.

Additional commit-gating fixes preserve known successful Canvas writes when a later manifest interrupts the run, retain current fingerprints when hosted deployment fails after an update, and preserve new module-item placement recorded during a failed retry even when the underlying content ID did not change. Content-only hosted updates still revert their state when hosted deployment fails.

Native quiz replacement remains a multi-request operation. The fixes preserve identity and make recovery reviewable; they do not claim remote atomicity.

### 5. Canvas pagination could return an incomplete inventory

The client assumed another page existed only when a response contained the requested 100 items, then incremented a numeric page. Canvas documents an unspecified server cap and opaque `Link` URLs. The client now follows `rel=next`, retains its query parameters, rejects another origin before sending credentials, and reports malformed lists or loops instead of returning a partial inventory as success. [Canvas pagination documentation](https://developerdocs.instructure.com/services/canvas/basics/file.pagination)

### 6. Uncertain creates were replayed automatically

The client retried POST requests after network exceptions or server errors. A lost response does not establish that creation failed. Those uncertain creation requests now stop for inspection; idempotent reads/updates retain retries, and an explicit 429 rejection can retry. If the response containing a created ID never arrives, a human still needs to inspect and map the object before a new create attempt.

### 7. Hosted batches repeatedly rebuilt the entire course

Each changed artifact rendered the whole course, followed by another full render at the batch's end. Batch pushes now render affected artifacts and perform one final course render. Standalone pushes still produce complete hosted output. This removes the repeated whole-course factor from the batch work without changing generated content or removing failed-artifact restoration.

A stateful regression publishes two pages, reruns unchanged, edits only a hosted body, and renames its source. It verifies one full course render in the first batch, no duplicate objects, no unnecessary Canvas body update, correct generated text, and current `local_path` in state. Hosted fast-path state also records the current source commit when available.

### 8. Named course keys were accepted during setup but omitted later

Setup already accepted lowercase kebab-case names. Some manifest discovery, workflow paths, numeric-only `awk` targeting, and state-path validation only handled `course...` names. Discovery and validation now agree with the setup contract, and a small tested Python target resolver replaces the inline shell selection.

Shared-code-only changes still do not select every course for remote publishing. That is now explicit: such a selection could publish unrelated pending artifacts, including Course 4's unmapped source. Deploy shared changes with an explicitly reviewed course dispatch.

### 9. Malformed frontmatter could escape validation as an exception

YAML scalar/list frontmatter reached `.get()` calls, and splitting on every `---` could break a valid quoted title containing those characters. Parsing now recognizes delimiter lines and requires a mapping, producing a useful validation error without damaging the input.

## Common Curriculum and Alan comparison

This comparison uses the saved repository, not the complete Alan system. Its local `skills/README.md` credits Sathya with the process and hierarchy decisions and Alan with drafting that documentation. The vision page similarly distinguishes human decisions from Alan's task lists and page mechanics. Private cowork decisions and the full team-repo operating system were not inspected.

| Dimension | Common Curriculum evidence | Applying AI at Work implication |
|---|---|---|
| Design before production | Vision and skills link desired outcomes, teaching moves and evidence before build. | Keep context specs as substantive design inputs; validation alone cannot assess readiness or evidence quality. |
| Human-readable assignments | Writing skills distinguish purpose, prior work, task, success criteria and reflection. They separate teaching prose from instructions and put instructions where the reader acts. | Useful review questions for future De Anza authoring, without imposing new rubric weights, wording, or course categories in this technical audit. |
| Authority and edit survival | The Fall vision records an August decision that participant-facing HTML is directly edited and preserved. `assignments.html` is the generated registry. | A deliberate difference from this repository's generated-output model. Do not combine both authority models for the same files. |
| Generated De Anza content | `CONTRIBUTING.md` explicitly identifies `deanza/**` and `activities/deanza/**` as outputs from this repository. | Continue editing De Anza Markdown and regenerating output; do not repair its HTML by hand downstream. |
| Identity and verification | Assignment writing and Canvas build guidance emphasize same-pass ID recording and readback. | Consistent with stable artifact identity, early checkpoints, and preserved state after partial failures. |
| Scope-specific delivery | `building-canvas-fall-2026` explicitly applies to CST286, CST349 and CST499, including their grading and module gates. | Do not transplant its grading or gating choices into adult professional De Anza courses. |
| Completeness | The skill hierarchy names course/sprint/module design gaps. Older CSV-first documentation also coexists with the later `assignments.html` flow. | The visible Alan work is valuable comparison material, not evidence of a complete drop-in replacement builder. |

Specific local sources reviewed include Common Curriculum's `CONTRIBUTING.md`, `README.md`, `context/README.md`, `fall-2026-vision.html`, the skills index, writing-to-teach, writing-learning-goals, writing-assignments, reviewing-course-text and the Fall Canvas build recipe. The ActivityEngine callers and components were checked for the generated AI-discussion integration. No Common Curriculum files were modified.

## Verification evidence

| Check | Result |
|---|---|
| Starting repository tests | 144 passed; no pre-existing suite failures. The saved Python 3.9 virtualenv emitted a LibreSSL/urllib3 warning. |
| Test environment for final checks | New worktree-local `.venv`, CPython 3.11.15, existing pinned requirements. Matches CI's Python minor version. Saved checkout virtualenv unchanged. |
| Full unittest discovery | 169 passed, including 25 added test cases. |
| Full repository schema validation | PASS across current artifacts, manifests, PRDs and homepage metadata. |
| Python compilation | All `canvas_sync/*.py` compiled. |
| Skill validation | Five edited skills passed the skill-creator validator. A pre-existing angle-bracket description in inspect-canvas was corrected. |
| Config syntax | All workflow YAML and Codex TOML parsed. This does not execute GitHub environment rules. |
| Static checks | New modules and test files passed Ruff's undefined/unused-name checks; `git diff --check` passed. |
| Full Course 1 hosted render | 69 content pages, 11 indexes and activity/support outputs, totaling 120 files. |
| Render compatibility | All 120 files byte-identical to a separate render from starting commit `a078404`. |
| Local hosted dependencies | 102 distinct relative links resolved in the preview or the saved Common Curriculum checkout; none missing. External URLs and authenticated backend execution were not included. |
| Stateful publishing fixtures | Native quiz partial failure/retry preserves ID; hosted create/rerun/body-edit/rename preserves identity and output; existing native/AI assignment, completion, rubric, placement and restoration tests remain green. |
| Scope preservation | No changes under course sprint sources, `context/`, or `archive/`; both saved repositories remain unchanged by this work. |

Reproduce the core local gate from this worktree:

```bash
.venv/bin/python canvas_sync/schema.py --all
.venv/bin/python -m py_compile canvas_sync/*.py
.venv/bin/python -m unittest discover

git diff --check
```

Preview output is at `/tmp/applying-ai-audit-preview`. It is generated review material, not a deployment. The renderer comparison used an isolated archive of the starting commit. The committed tests are the durable regression evidence; temporary logs and previews may be removed by the operating system.

## Ranked remaining work and limits

1. **Version the complete Canvas drift baseline.** The existing persisted fingerprint covers content/title/points/publish/questions, but does not cover all due dates, submission settings, module position, completion requirements, or rubric state. The new source comparison detects more fields, but it does not make the stored baseline comprehensive. Extend and migrate it deliberately; silently changing the current hash shape would misclassify existing deployments as drift.
2. **Run a precisely scoped sandbox smoke test.** Test native assignment/page/discussion/Classic quiz and hosted AI activity creation, update, actual module requirements, permissions, publication state, hosted deployment and LTI progress. No live behavior is claimed by this audit. Canvas still documents separate Classic quiz and question requests; New Quizzes compatibility is not established. [Quiz API](https://developerdocs.instructure.com/services/canvas/resources/quizzes), [question API](https://developerdocs.instructure.com/services/canvas/resources/quiz_questions)
3. **Improve recovery for already-partially-mutated native quizzes and removals.** Identity survives more failure points, but remote multi-request changes are not transactions. Interrupted question replacement or deletion requires fresh inspection and an explicit recovery decision. Persisted operation journals or narrower quiz updates should follow a sandbox pilot rather than an untested rewrite.
4. **Define active curricular authority before another broad course publish.** Resolve the revised Course 1 arc, Sprint 5 placeholder, and Course 4 internal headings. A full course publish scans active Markdown, and `publish: false` can create hidden objects. Removing a Canvas object while retaining active source can allow recreation later. This audit did not invent a new archive or tombstone policy.
5. **Review participant experience end to end.** Byte preservation and resolved local dependencies do not establish phone accessibility, real iframe rendering, AI response behavior, JSON submission quality, or human assessment alignment. The Common Curriculum backend and remote resources remain downstream dependencies.
6. **Continue documentation alignment where it is instructional.** Course 3's participant-facing command references can lag the updated maintenance interface. They were preserved as course content; update them through the course editing and homepage workflow when requested. Historical design/archive assertions also need contextual reading rather than automatic cleanup.

No package was declared deprecated or upgraded based solely on age. The audit does not establish remote Canvas state, protected-environment configuration, current hosted availability, or the full Alan workflow. All requested local audit, implementation and verification work is complete; deployment and instructional decisions remain separate reviewed actions.

## Subsequent authorized live test

After this audit snapshot, the user authorized pushing the audit branch and a small additive test in Course 180. Native Page, text-entry Assignment, and Classic Quiz publication, repeat publication, and a hosted page edit passed live API checks. The test found a new-module publication issue and prompted quiet, post-question quiz publication; the resulting suite has 174 tests. See the separate [live smoke-test report](2026-09-08-live-canvas-smoke-test.md) for exact scope, deployment records, review links, and the features that remain untested. The original audit results above remain the record of the earlier offline phase.
