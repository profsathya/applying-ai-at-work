# Authoring Principles Integration Validation

Implemented on `codex/align-authoring-principles`, based on Applying AI at Work commit `6805c41218d369481c18b8253caf025b5df30c82`. This is an implementation and agent-behavior review, not human approval of generated course text or evidence of participant learning.

## Implementation

Four instruction-only skills live under `.agents/skills/`: `writing-to-teach` and `writing-assignments` at local revision `1`, and `writing-learning-goals` and `reviewing-course-text` at local revision `2` after the pre-main alignment review below. Each records its originating Common Curriculum file at reviewed commit `81a051324df61c41af464a0220f8085627729ad9` and its local adaptations. No upstream course policies, Canvas IDs, HTML or slide system, private workspace dependencies, or review script were copied.

Seven existing workflow skills and four existing agent instruction blocks now link to the shared guidance. All seven agent TOMLs retain their names, descriptions, reasoning settings, and sandbox settings. Root routing and operator documentation activate the practices for ordinary authoring requests. [The authoring contract](../AUTHORING.md) explains scope, source authority, workflow handoffs, and maintenance. [The record contract](../../.agents/skills/reviewing-course-text/references/review-record.md) assigns the saved review to the parent and preserves restricted worker write boundaries.

## Mechanical validation

| Check | Observed result |
|---|---|
| Repository `.venv/bin/python` with the installed skill-creator `scripts/quick_validate.py` on each new or edited skill | All 11 passed |
| Parse `.codex/agents/*.toml` using Python `tomllib`; compare all fields except `developer_instructions` with the baseline | All 7 parsed; roles and settings unchanged |
| Resolve local Markdown links in edited/new instructions and operator docs; check explicit agent skill/contract references | 52 local Markdown links and agent references resolved |
| `git diff --check` | Passed |
| `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python canvas_sync/schema.py --all` | PASS, exit 0 |
| `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python -m unittest discover` | 144 tests passed, exit 0 |

The existing Python environment emits an urllib3/LibreSSL warning. The offline suite also prints expected error-path diagnostics. Neither caused a failing result. These runs did not validate or perform live publishing.

## Behavioral fixtures

Independent agent passes used temporary repository copies with the local instructions, deterministic validators, a minimal professional-course brief, prior stakeholder-note work, and fake course configuration. The task prompts supplied realistic requests and necessary inputs without intended answers. No sibling Common Curriculum checkout was present in the fixtures. A shared virtualenv supplied Python dependencies; no credentials or `.env` were copied.

| Request exercised | Observed behavior and verification |
|---|---|
| One concept page from a PRD-shaped item | `canvas-author` wrote exactly one Markdown file. It retained the requested three-question structure, explained reported observation versus interpretation, and included ungraded application to existing notes without adding a submission. Parent inspected the file and write footprint. |
| One assignment from a PRD-shaped item | A separate invocation wrote exactly one assignment. Purpose, four evidence requirements, text submission, and the supplied 10-point full-credit criterion agreed. AI remained optional and could not supply missing stakeholder evidence or make the final choice. |
| Homepage update after those additions | A dedicated `homepage-maintainer` wrote only `homepage.yaml`, added both slugs in teaching order, and grounded goals in the actual work. It returned findings without writing a record. |
| Parent completion for the single-artifact workers | The parent reviewed the assembled outputs, independently reran two artifact checks, homepage validation, and full schema validation, then wrote the record. All passed; seven workflow/reference/output fingerprint entries were checked against actual files. |
| A two-artifact sprint with an unconventional structure | The coordinating fixture agent followed the local drafter and homepage workflows sequentially. It produced exactly a case-and-annotation page and a memo assignment, retaining inline directions and omitting an extra reflection section or discussion. It identified that earlier notes might contain only one delay and supplied an inline clarification for obtaining a second real observation without inventing evidence or another graded deliverable. |
| Exact source wording preserved during review | The assignment remained byte-for-byte identical. Recommendations addressed conflicting PDF/three-solution directions, the text-entry contract, and invented AI evidence. An existing unquoted YAML due value failed schema validation; the record reported that failure without silently changing protected metadata. Six recorded fingerprints were verified before later edits. |
| Date-only update | Only the due line changed. Other assignment bytes, homepage, and existing records remained intact; no new editorial record was added. Artifact and full local validation passed after the authorized date change. |
| Substantive local revision | The body was revised from the existing brief and stakeholder notes. All frontmatter bytes, the original credit criterion, neighbors, PRD, and manifest were preserved. Artifact/homepage/full validation passed. A new parent record distinguished the revised output from the earlier recommendations-only snapshot; eight file fingerprints were verified. |
| Read-only Canvas inventory | An offline driver called the unchanged inspector with a fixture client and a network prohibition. It reported one unpublished module and assignment, including mapping gaps, and wrote only the usual JSON and Markdown ledgers. No existing file changed and no authoring record was created. |

The parent independently inspected the generated artifacts and records, checked file boundaries and output hashes, and reran full schema validation on the single-artifact, sprint, and revised-course fixtures. Worker-specific checks in their records remain attributed to those workers; file checks do not substitute for live browser or participant testing.

One record-contract clarification followed these exercises: subsequent substantive changes require renewed editorial review, while a date-only change retains its narrow validation and leaves the earlier hash as historical evidence. A fresh independent fixture using the final contract changed only the requested date, passed artifact validation, and created no report. The contract also asks records to avoid repeated scope and approval statements.

## Review evidence and limits

Temporary evidence root on the validation machine:

```text
/var/folders/31/p34hb9mj7_n6bg5xzndw62s40000gn/T/authoring-alignment-checks-8rmos0gi/
```

It contains baseline file hashes, instruction fingerprints, and `single`, `sprint`, `revision`, `inspection`, and `mechanical-final` fixtures. The authoring records include:

- `single/course1/reports/authoring/20260909T212344Z-single-artifacts-and-homepage.md`
- `sprint/course1/reports/authoring/20260909T212124Z-sprint-1-choosing-what-to-investigate.md`
- `revision/course1/reports/authoring/20260909T211957Z-choose-a-delay-recommendations.md`
- `revision/course1/reports/authoring/20260909T212547Z-choose-a-delay-revision.md`

These are disposable validation artifacts, not runtime dependencies or production course drafts. Each record identifies the instruction/reference versions actually used during its run. The sprint record's six workflow/reference/output hashes matched its fixture; earlier records remain historical after later file changes.

## Scope preservation

SHA-256 comparison against the pre-change baseline found no modified or deleted tracked files outside the approved instruction and operator-documentation set. Both course drafts, all course content and curated homepages, Canvas manifests/state, publishing code, and design inputs in the real repositories were preserved.

The separate document-intake worktree at `/Users/jeremyshaw/.codex/worktrees/fc1e/applying-ai-at-work` retained its HEAD and all tracked file bytes. The Common Curriculum checkout likewise retained its HEAD and all tracked file bytes. Both remained clean. The earlier untracked draft/skills audit was preserved byte-for-byte. The initial implementation validation performed no Canvas writes, publishing calls, commit, push, or branch merge.

## Pre-main alignment review

After the user requested another alignment test followed by delivery to `main`, an independent agent compared the actual local instructions with the four originating skills at pinned Common Curriculum commit `81a0513`. It identified two omissions: explicit quotation fidelity and positive capability framing instead of fear, scarcity, or professional survival.

The local goal skill now owns the positive-framing principle and includes a consequential example. The review skill references that principle for body copy and requires original-source verification of participant/stakeholder quotations, visible markings for authorized changes, and paraphrases outside quotation marks. Both skills advanced to local revision `2`. A follow-up independent instruction review found both issues resolved and no new scope, source-authority, ownership, or publishing-permission problem.

The repository schema validator and 144 offline tests were rerun successfully with Canvas environment overrides empty. All 11 skills validated, all seven agent TOMLs parsed with unchanged role/model settings, and tracked-file comparisons again preserved the drafts, publishing implementation, state, and other worktrees. The 21 planned commit paths do not match the `Publish Canvas` workflow's push filters. The earlier draft audit is excluded from this commit.

Two fresh independent authoring requests provided additional behavioral evidence:

- A plain-language request to add an ungraded page followed `add-artifact`, preserved annotated-note structure, changed only the new page and homepage, and saved the parent record. Existing artifacts, design inputs, PRD, and manifest stayed unchanged. The parent verified nine file hashes in the record. This fixture began before the two revision-2 corrections; its record accurately identifies revision 1 of those skills.
- A revision request using the final revision-2 skills supplied an original interview note and a page with an altered quotation, an unsupported causal claim, and a fear-based payoff. The agent restored the exact original quote, explained what the source did and did not establish, and replaced the payoff with a credible capability. It preserved frontmatter and ungraded practice, changed only the page plus the parent record, and left all context unchanged. The parent independently read the result, compared the quotation with its source, verified six recorded file hashes, and reran full fixture schema validation successfully.

The final candidate again passed repository schema validation, all 144 offline tests, validation of all 11 skills, and resolution of 55 local Markdown links. The staged diff passed whitespace checks and contained exactly the 21 approved files.

Additional disposable evidence is under `/var/folders/31/p34hb9mj7_n6bg5xzndw62s40000gn/T/authoring-pre-main-tmpx4hhd/`. Records are `fixture/course1/reports/authoring/20260909T213458Z-when-evidence-disagrees.md` and `quotation-fixture/course1/reports/authoring/20260909T213739Z-ai-and-your-role-revision.md`. These tests observed agent behavior and local validation, not participant learning or live Canvas behavior.
