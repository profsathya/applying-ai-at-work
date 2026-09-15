# Approved Sprint 1 authoring default

Date: 2026-09-15. Scope: repository instructions, supporting documentation, and validation triggers. Base: remote `main` at `f6431bd36a42ad6cabf1baebeabffbee9499a9e6`.

## Finding and changes

The earlier instruction work was present on remote `main`: commit `cd21aa329fd76e5d4ccefcb74e70a1e550aba4a5` was included through PR #54. Root guidance, the authoring documents, and the shared teaching/review skills matched remote copies before this change. The gap was the prominence and explicitness of the default, not a missing local commit.

The default is now named **the approved Sprint 1 authoring workflow and presentation**, with the six course 180 `sprint-12` pages mapped to their instructional jobs in [the presentation reference](../AUTHORING_PRESENTATION.md). This replaces a broad style label with concrete examples to inspect before ordinary substantive authoring.

| Owning instructions | Corrective change |
| --- | --- |
| Root `AGENTS.md`, editor guide, reader/builder guides, authoring contract | Prominent default, concise initial prose, consolidated directions, selective grouping, useful visuals, and responses at the point of use |
| Build-course, build-sprint, add-artifact, update-artifact, canvas-author entry points; drafter/author roles | Required matching-reference inspection, without changing task routing or role permissions |
| Writing to teach, assignments, reviewing course text | Explicit authoring and editorial expectations; record actual references and visual decisions |
| Presentation and document-intake references | Source-to-render production sequence; approved illustration family; supported reading/compact layouts and existing rendering caveats |
| Schema validation workflow | Instruction, skill, agent, and documentation paths now trigger existing validation on PRs and pushes to main |

Local skill revisions: writing-to-teach 4 → 5, writing-assignments 3 → 4, reviewing-course-text 5 → 6. Their upstream revision remains pinned to `81a051324df61c41af464a0220f8085627729ad9`. Existing source authority, exact wording, grading, identity, author file boundaries, and publication permissions remain intact.

## Independent authoring trials

Two fresh-context workers received repository access and isolated output directories. The ordinary prompt requested a module about checking process evidence for working professionals: one concept page, an optional zero-point handoff practice, and a five-point two-task assignment. It supplied learning requirements and task identities, but did not mention Sprint 1, style, brevity, visuals, or the expected result.

The author reported reading the authoring contract, presentation reference, relevant skills, and the approved Introduction, Start your list, Things you stopped noticing, and Test and commit examples. The coordinator inspected the resulting Markdown and rendered pages.

| Trial | Observed result and comparison |
| --- | --- |
| Short practice: Record one handoff | Direct opening; one descriptive section; four concrete evidence fields; adjacent response; optional/zero-point status beside submission. Compared with Start your list, it retained the reading sequence without copying three steps or adding a gratuitous image. |
| Multi-task: Compare two handoffs | Two distinct instruction/response pairs and intact task IDs. Compared with Test and commit, it used the same progressive response placement and a useful example/non-example. Its first section remains comparatively text-heavy; the output demonstrates better structure, not guaranteed optimal concision. |
| Concept: Observations and assumptions | Essential distinction first, a narrow semantic comparison table, and an explicit next step. Compared with the Introduction and illustrated explanation, it used a visual relationship suited to its content. No raster image was necessary to explain this particular distinction. |
| Exact wording | The supplied two paragraphs after the page title were preserved byte-for-byte, verified independently by the coordinator. No extra teaching or visuals were inserted. |
| Date only | The result equaled the input bytes with only the requested due-date replacement. No prose or presentation changes. |

All three ordinary outputs preserved supplied points, submission requirements, and response IDs. Optional practice remained optional. No additional assessments, dates, AI services, or prior-work requirements were added. The trials wrote only ignored fixtures; no course pages changed.

## Observed checks

- All eight changed skills passed the skill-creator validator. Relative Markdown file links in changed instruction documents passed existence checks, excluding fenced examples and external URLs.
- All agent TOML files parsed; non-instruction configuration fields matched the base revision. The three upstream skill pins remained unchanged.
- Full schema validation passed. All 232 repository unit tests passed with Canvas environment variables cleared for isolated fixture behavior.
- The existing preview command rendered and browser-checked all three trial pages and all six reference pages successfully. Chromium checks covered applicable heading order, image loading/alternatives, overflow, enlarged base text, draft restoration, keyboard copying, clipboard-denial fallback focus, disclosure operation, visible focus, and control names. Concept-check feedback was exercised on the reference set.
- The coordinator inspected full-page desktop and mobile screenshots of the trial outputs alongside the relevant reference pages. Sections, comparison columns, and response areas remained readable in the inspected views. Essential instructions stayed visible; controls remained secondary to the work.
- Validation path coverage was checked for PR and main-push events. Course files, renderer/schema/runtime tests, and the Canvas publishing workflow have no changes in this patch. The changed paths do not match the Canvas publishing workflow's filters.
- `git diff --check` passed. Homepage maintenance is not applicable because this patch changes no course artifacts or homepage metadata.

Local evidence, trial fixtures, output fingerprints, preview reports, and screenshots are in the ignored `.source-intake/approved-workflow-validation/` directory. They are local review evidence, not a committed course module or a permanent CI fixture.

## Limits

These are a small number of fresh-context authoring trials, not proof of consistent behavior across every model or course. The ordinary trial produced a useful semantic visual, but did not exercise new raster-image generation or asset reuse; those production instructions were reviewed against the existing approved illustration workflow. No image quota is implied.

Automated browser checks use Chromium and enlarged base text, not full browser zoom or screen-reader certification. The coordinator's visual comparison is an editorial judgment, not observed adult-learner engagement or learning validation. External Canvas submission and AI endpoints were not exercised. No Canvas publication was performed or authorized by this instruction change.
