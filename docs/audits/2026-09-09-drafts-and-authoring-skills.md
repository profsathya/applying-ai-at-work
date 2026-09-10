# Draft and authoring-skill audit

Date: 9 September 2026. Scope: the two first-half Sprint One drafts, Common Curriculum's seven current skills and its review script, and Applying AI at Work's relevant authoring, source-intake, rendering, and maintenance implementation. This is an evaluation, not a content revision or publishing run.

## Recommendation

**Use Leslie's v3 as the editorial source, retain our Working Draft's delivery structure, and use Sathya's four core writing skills to review the combined result.** For writing better teaching material, Common Curriculum is stronger. For preserving approved documents and building this certificate in Canvas, Applying AI at Work is stronger, particularly the unmerged document-intake branch. Neither is a complete substitute for the other.

The two drafts are not independent competitors. Our test was built from `S-half-one-working-draft-v2.md.docx`; Leslie's current file is a later revision of that same material. Better v3 passages do not establish which skills or agents produced them.

## Revisions and evidence examined

| Material | Audited revision |
| --- | --- |
| Applying AI at Work main, containing Leslie's v3 | `6805c41218d369481c18b8253caf025b5df30c82` |
| Our Working Draft and document-intake implementation | `codex/audit-canvas-maintenance`, `a8bf1f8025fa7b733b2813fda437f45e43dda44d` |
| Common Curriculum skills | Fetched `origin/main`, `81a051324df61c41af464a0220f8085627729ad9` |

The Common Curriculum review uses the fetched Git tree, not its older local working checkout. No course source, skill, Canvas object, hosted deployment, or branch was changed for this audit. Only this report was added.

## Draft comparison

| Dimension | Leslie's v3 | Our Working Draft |
| --- | --- | --- |
| Learning sequence | Coherent A-F arc, with later editorial improvements | Same source-derived arc, split into six Canvas items plus a module header |
| Teaching the four checks | Stronger explanations, examples, and recovery moves | Shorter v2 explanations, supplemented with task criteria |
| Personal problems | Explicitly permits a problem whose cost is primarily personal and a knowledgeable outside contact | Older requirement emphasizes another person with a stake |
| Commitment | Adds why the problem is yours to work and permission to reconsider a sole survivor you do not care about | Reasons, alternatives, switch condition, and runner-up; lacks the newer personal commitment requirement |
| Assessment | Suggested points and unresolved concept-check placement; no completed check | Five formative questions, response templates, completion guidance, and 15/5/20-point review guidance |
| Learner presentation | Editorial notes, unresolved items, and page-cut scaffolding still present | Participant-facing pages and working response controls, with some instructional weaknesses below |
| Source traceability | Detailed human/AI decision narrative | Original document, version choices, selected-block evidence, and deterministic reconstruction |
| Release readiness | Needs editorial resolution and conversion | Tested prototype, but older content, unavailable optional feedback in the last live test, and incomplete integration into main |

### Why I prefer v3's content

1. **The checks explain their purpose.** E1 connects checking people, current handling, liveness, and size to the later framing and stakeholder work. E2-E4 show how to answer and how an insufficient answer differs from a useful one. The earlier build is more likely to function as a checklist an instructor must explain.
2. **Check 4 improves access for personal problems.** It permits another person who knows the situation, even if that person does not bear its cost, and gives a concrete caregiving example. This matters for participants without a conventional workplace project.
3. **Reframing has an explicit follow-through.** V3 says to rerun all four checks after changing a problem's scope, rather than treating a new formulation as automatically workable.
4. **Commitment includes motivation.** The new “why you” requirement and the bored-survivor recovery path make a nine-week choice more than an exercise in satisfying four tests. Our response fields and review guide do not yet include that change.

Sources: [v3 E1-E5](/Users/jeremyshaw/Projects/applying-ai-at-work/course1/design/sprint-1-half-one-working-draft-v3.md:296), [v3 commitment](/Users/jeremyshaw/Projects/applying-ai-at-work/course1/design/sprint-1-half-one-working-draft-v3.md:443), [earlier checks](/Users/jeremyshaw/.codex/worktrees/fc1e/applying-ai-at-work/course1/sprints/sprint-11/four-checks-for-a-workable-problem.md:13), [earlier task configuration](/Users/jeremyshaw/.codex/worktrees/fc1e/applying-ai-at-work/course1/sprints/sprint-11/test-and-commit.md:14).

V3 also needs a length pass. A whitespace count of E1-E5, including headings, table syntax, and examples but excluding the inline OPEN note, is approximately **2,066 words**, compared with **886** in the equivalent earlier instructional section before its added response-field appendix. This is a comparison of source text, not visible browser words or reading-time measurements. Much of the extra explanation earns its place; repeated warnings and repeated justification do not all need to remain.

### Problems to fix in either version

- **Do not make rejection a target.** “Most of your list will not survive” and suspicion when more than two pass can train participants to manufacture failure. Ask for discriminating evidence and honest unknowns; several workable candidates are a legitimate result.
- **A useful goal need not be universally agreed.** C2's “nobody in the organization would dispute it” can erase real stakeholder tradeoffs. A goal should identify a valuable outcome without prescribing the solution; disagreement is information to investigate.
- **Resolve the personal-problem inconsistency.** V3 D2 still says a problem nobody else has a stake in cannot support Sprint 3, while E5 explicitly allows someone with relevant knowledge instead. The earlier build also retains the stricter wording. A participant needs one consistent eligibility rule.
- **Close the editorial loop.** V3 still contains a video TODO, open AI-tool and concept-check decisions, and notes saying the Introduction needs edits that the handoff says were applied. D5's internal grading note refers to four fields while D3 provides five. These are draft-state issues, not reasons to discard the design.

### What our implementation does well, and what it does not

Keep the reusable candidate template, five formative concept questions with explanations and revision, explicit distinction between saving/copying and Canvas submission, uncertainty marks, runner-up, and transparent review criteria. The questions test ideas introduced in A-D; they do not require the later check reading. The source preservation is real: a fresh build from the retained DOCX packet and reviewed map reproduced all **seven Markdown files and seven sidecars byte-for-byte**.

Three delivery issues remain:

1. **Essential teaching is too easy to skip.** The guided renderer places the full assignment prose, examples, and grading table in one closed “Read the full instructions and examples” panel. Criteria sit in per-task panels, but worked examples are not next to each task as Sathya's current assignment skill recommends. Preserve the prose while making essential examples and the grading summary easier to encounter.
2. **The feedback mechanism does not implement the complete E8 exchange.** It sends one response plus that task's criteria, not the candidate gaps and all four check answers together. Buttons are also available on the first four tasks despite the instruction to finish all four before AI. The code only requires the clicked response to be nonempty. Per-box formative feedback can help, but it is not evidence that the intended cross-candidate challenge occurred.
3. **Source fidelity does not protect deployment completeness.** Our branch passes its tests, but main does not contain its source/tooling. A later main-based render removed the homepage section. Integration and a check for disappearing published modules are required before calling the whole workflow dependable in shared use.

Sources: [guided renderer](/Users/jeremyshaw/.codex/worktrees/fc1e/applying-ai-at-work/canvas_sync/guided_assignment.py:15), [feedback request](/Users/jeremyshaw/.codex/worktrees/fc1e/applying-ai-at-work/canvas_sync/assets/guided-assignment.js:69), [source assembly](/Users/jeremyshaw/.codex/worktrees/fc1e/applying-ai-at-work/canvas_sync/source_build.py:117), [homepage replacement commit](https://github.com/profsathya/Common-Curriculum/commit/3f5851e).

## Common Curriculum skill audit

| Skill | Assessment | Recommendation for Applying AI at Work |
| --- | --- | --- |
| `writing-to-teach` | Strongest teaching guidance: reader starting point, teaching versus task prose, worked examples, non-examples, action interleaving, and limits on compressed prose | Use its teaching discipline. Adapt audience, pronouns, and page mechanics to this certificate |
| `writing-learning-goals` | Clear payoff, observable capability, plain language, and credible promises | Use for purpose and goal lines; supplement with alignment between each goal and the work that demonstrates it |
| `writing-assignments` | Strong task design: prior work, ordered actions, complete versus strong criteria, visible grading, and reflection | Use the educational structure. Exclude its course-specific publishing, naming, and navigation instructions |
| `reviewing-course-text` | Strong final editorial method, including duplication across pages and instructions at the point of action | Use the prose review. Treat the helper script as a fallible diagnostic |
| `hover-text` | Useful contextual definitions and explicit keyboard/render checks; includes a known summary-button interaction | Optional renderer feature. Do not insert its HTML directly into our Markdown artifacts |
| `building-canvas-fall-2026` | Detailed operational recipe with inventory, identity write-back, API readback, and course-specific exceptions | Do not use for this certificate. Its scope explicitly names three other Canvas courses |
| `slides` | Useful guidance on slide claims, sequencing, worked activities, and instructor edits | Use only when making a relevant deck, with the course policies replaced by the actual course record |

Pinned sources: [writing-to-teach](https://github.com/profsathya/Common-Curriculum/blob/81a051324df61c41af464a0220f8085627729ad9/skills/writing-to-teach/SKILL.md), [learning goals](https://github.com/profsathya/Common-Curriculum/blob/81a051324df61c41af464a0220f8085627729ad9/skills/writing-learning-goals/SKILL.md), [assignments](https://github.com/profsathya/Common-Curriculum/blob/81a051324df61c41af464a0220f8085627729ad9/skills/writing-assignments/SKILL.md), [review](https://github.com/profsathya/Common-Curriculum/blob/81a051324df61c41af464a0220f8085627729ad9/skills/reviewing-course-text/SKILL.md), [hover text](https://github.com/profsathya/Common-Curriculum/blob/81a051324df61c41af464a0220f8085627729ad9/skills/hover-text/SKILL.md), [Fall Canvas](https://github.com/profsathya/Common-Curriculum/blob/81a051324df61c41af464a0220f8085627729ad9/skills/building-canvas-fall-2026/SKILL.md), [slides](https://github.com/profsathya/Common-Curriculum/blob/81a051324df61c41af464a0220f8085627729ad9/skills/slides/SKILL.md).

### Where Sathya's skills are more robust

The rules identify concrete failure modes and give before/after examples. They distinguish teaching from instructions, completeness from quality, and helpful explanation from repetition. Their version notes record revisions when earlier advice caused bad results, such as persuasive openings that invented an objection. They also retain human review for judgments that a checklist cannot establish.

Applying AI at Work's main `canvas-author` is mostly an output/frontmatter contract and a short style list. Its `build-sprint` infers structure from existing sprints and validates files. These are useful mechanics, but neither provides comparable guidance for making an explanation teach or assessing whether every task advances a learning goal. `sprint-planner` explicitly decomposes a pre-existing design; it is not a substitute for designing the learning sequence.

### Where Common Curriculum is less robust or less portable

**The helper has reproducible measurement gaps.** The audit ran the current `review_student_page.py` on three minimal HTML fixtures:

| Fixture | Observed report | Limitation |
| --- | --- | --- |
| Two visible words, a one-word summary, 100 words inside closed details, then a textarea | 103 words before first action | Counts hidden text as visible workload |
| Copy-questions button, 100 teaching words, then a textarea | Zero words before first action | A utility button can hide the distance to the actual response |
| Task, textarea, Submit button, no criteria | “criteria before submit: YES” | Absence of recognized criteria becomes an affirmative result |

On our freshly rendered Candidate List and Test and Commit pages it reported 1,186 and 1,329 words before the first action, including closed full instructions. Those are not valid visible-word measurements. Its screen estimates are already labeled estimates in the code; the hidden-text problem adds another reason not to use them as browser evidence. The script also does not replace manual review of instruction-only actions or a live layout check. [Implementation](https://github.com/profsathya/Common-Curriculum/blob/81a051324df61c41af464a0220f8085627729ad9/skills/reviewing-course-text/scripts/review_student_page.py#L43).

**It is not a complete course builder.** The current inventory still has no general course-, sprint-, or module-design skill; the README explicitly names those gaps. It says operational skills live elsewhere, while the folder now includes a Fall Canvas recipe and slides. The README's current-skill list omits the new slides skill. These are manageable documentation gaps, but the package is not a fully self-contained framework. [Inventory](https://github.com/profsathya/Common-Curriculum/blob/81a051324df61c41af464a0220f8085627729ad9/skills/README.md#L18).

**Some instructions depend on another workspace.** The lock record, assignment-data files, `mk_assignments.py`, and `add_slide.py` named by the skills are not in the audited Common Curriculum Git tree. The principles can be read independently, but the operational recipes require their actual external workspace and configuration.

**Course policies and infrastructure leak into reusable writing advice.** `slides` mandates a 10% late penalty and an OYP substitution rule. `writing-assignments` says the course decides kinds, then hardcodes OYP/GI/Exam prefixes. Its navigation rule requires `_blank`, whereas our authenticated test required `_top` for Working Draft links. Its HTML/iframe and `assignments.html` pipeline differs from our Markdown, deployment state, and reconcile rules. Copying these files unchanged would import unrelated behavior. Separate the reusable writing discipline from those course-specific instructions before adopting it here.

## Which workflow to use

For **thinking through and writing the curriculum**, use `writing-to-teach`, `writing-learning-goals`, `writing-assignments`, and `reviewing-course-text` as explicit design references. Keep course policies and source authority in this course's own record. Their prose rules can guide Markdown without adopting their HTML markup or Canvas recipe.

For **turning a reviewed document into this course**, use the document-intake `build-sprint` path on our feature branch: preserve the source and review choices, map the selected content, assemble Markdown and evidence, update homepage metadata, and validate the rendered participant experience. This branch is more suitable than today's main for Google Doc/DOCX inputs. Main does not yet contain these protections.

For **shared publishing**, integrate the selected source and required implementation into main before relying on main-based regeneration. Preserve existing Canvas identities, reconcile live drift, and verify both content and navigation. The next revision must update the explanatory pages, response prompts, review criteria, and source evidence together; changing prose alone would leave the v2/v3 mismatch in the form.

I would retain Leslie's v3 decision log as the editorial record and our block-level source evidence as the transformation record. They answer different questions: why a decision was made, and exactly what was carried into the delivered artifact.

## Verification and limits

- Fresh schema validation passed on main and the Working Draft branch.
- Fresh offline suites passed: **144 tests on main; 204 on the branch**. Expected error messages from negative-path fixtures did not represent failed tests. Canvas URL/token environment overrides were empty.
- A fresh reconstruction reparsed the retained original source, selected 190 blocks, and reproduced all 14 deployed-source/evidence files exactly. This verifies fidelity to the selected v2 source, not that v2 remains the preferred editorial version.
- Three guided pages were freshly rendered locally. The review-script probes above ran against those pages and isolated fixtures.
- September 9's earlier authenticated walkthrough is documented in the [live-test report](/Users/jeremyshaw/.codex/worktrees/fc1e/applying-ai-at-work/docs/audits/2026-09-08-working-draft-live-test.md). Its successful submission and navigation checks, and unavailable optional AI feedback, are historical evidence, not fresh live claims from this audit.
- This audit did not make a new live AI request, enter Canvas Student View, test actual participant learning, or inspect Leslie's private AI sessions. Teaching-quality judgments are editorial assessments supported by the examples above, not measured learning outcomes or proof that a particular skill produced the draft.
