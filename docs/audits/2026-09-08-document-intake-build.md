# Document intake and first-half Sprint One build

The builder now accepts a Google Doc file link, DOCX, or exported ZIP through an attended source-preserving intake. The selected `S-half-one-working-draft-v2.md.docx` has also been built into seven actual unpublished course artifacts. This completes the local intake, integration, content authoring, homepage, and participant-preview work. No Canvas writes, Common Curriculum deployment, merge, or remote push were performed for this change.

## Review the result

- Course source: `course1/sprints/sprint-11/`, with adjacent `*.sources.json` evidence.
- Local module preview: `http://127.0.0.1:8768/deanza/course1/sprint-11.html` while the local preview server is running.
- Preview file: `.source-intake/preview-site/deanza/course1/sprint-11.html`.
- Private source packet and build map: `.source-intake/sprint-one-v2-final/`.
- Full source/editorial review: `.source-intake/sprint-one-v2-final/editorial-plan.md`.
- Machine content/coverage review: `.source-intake/sprint-one-v2-final/content-build-review.json`.
- Browser evidence: `.source-intake/sprint-one-v2-final/browser-qa.json` and sibling desktop/mobile PNGs.
- Workflow/operator instructions: [Document Intake](../DOCUMENT_INTAKE.md).

The physical storage number is 11 because sprints 0 through 10 were already present. The participant-facing module is **Sprint One: Find a Problem Worth Working On (First Half)**. The existing live Sprint One artifacts and mappings remain intact. The new homepage entry is closed and muted; every new artifact has `publish: false`.

| Order | File | Delivery | Proposed points |
| --- | --- | --- | --- |
| 1 | `sprint-one-first-half.md` | Module header | - |
| 2 | `start-with-what-bugs-you.md` | Reading page | - |
| 3 | `two-other-places-to-look.md` | Reading page | - |
| 4 | `candidate-list.md` | Guided text-entry assignment | 15 |
| 5 | `problem-finding-concept-check.md` | Guided formative choice check, text entry | 5 |
| 6 | `four-checks-for-a-workable-problem.md` | Reading page | - |
| 7 | `test-and-commit.md` | Guided text-entry assignment | 20 |

The source provides the first half, sections A-F, plus a planning outline for later work. The build does not claim to supply the rest of Sprint One. Its learning sequence remains the author's: situated observations, deeper descriptions, alternative candidates, human checks, AI challenge, human judgment, a defensible choice and runner-up, and later investigation with actual stakeholders.

## Source fidelity and editorial decisions

The selected original has SHA-256 `8c47807332cb71516b2c256be8522768598171d28bb2c42e9d7e7f1ecdbf1419`. Original DOCX bytes were retained unchanged. Intake keeps five comment threads and both base/proposed projections of the five text revision elements. The two affected learner paragraphs at source blocks 200 and 202 use the explicitly chosen proposed view; there is no global accept-all operation or source-comment mutation.

The final body assembly preserves **158 exact source passages**, **190 selected blocks including table cells**, and **all three learner tables**. Source body passages account for approximately 4,880 whitespace-delimited words. Fifty new/adapted body parts account for approximately 1,433 words, including renamed headings, repaired internal cross-references, transitions, templates, criteria, and new assessment instructions. Interactive task configuration and five concept-check questions are separately recorded as authored metadata, outside those body-word counts.

The build strips internal A-F heading prefixes from participant headings and translates five internal section references into participant-facing names. Editorial banners, notes, open questions, literal Mermaid code, and the later-half planning table remain in the private packet. The omitted Mermaid duplicates a chain and branches already fully described in the retained prose; no supplied video or completed diagram is claimed. Comments informed specific local decisions, such as making instructions easier to act on and keeping uncertainty visible.

The assembler verifies raw-source fingerprints and re-parses the original source before copying a block. Adjacent selected-source evidence makes normal schema validation reject later unrecorded body/title/metadata changes. Human em dashes are allowed only in verified source passages/titles; new writing retains the existing style rule. Script/HTML checks and normal schemas still run. The sidecar is a reproducible local record, not a cryptographic signature of authorship. Private raw documents and full review packets remain ignored by Git.

The full authorized ZIP also ingested successfully: 26 DOCX files and one feedback workbook. The older draft's inserted/deleted word fragments are preserved by run-level parsing. Workbook coordinates, text, formulas, and cached values are available as review context; formulas are not evaluated. Unsupported layout and review metadata are explicitly flagged and retained in originals.

## Common Curriculum comparison and adaptation

The user-selected [Test and Commit reference](https://profsathya.github.io/Common-Curriculum/deanza-trial/test-and-commit.html) was inspected live and compared with the current local `deanza-trial/test-and-commit.html`, `skills/writing-assignments/SKILL.md`, and the older activity engine. Its key behavior is task-based work with optional guidance, browser-local response boxes, self-checks, optional per-box AI feedback, copy buttons, and final **Canvas text entry**. It is not a native Canvas quiz, and copying does not send a grade or submission.

The new `guided_assignment` delivery mode implements that behavior within this builder's Markdown/schema/render/push conventions. It supplies purpose and prior-work framing, keeps the complete authored instructions in an optional panel, provides task-specific criteria/reflection, and supports response or formative choice tasks. Candidate List has one workspace for three to five candidates and no AI endpoint. Test and Commit has eight fields: four checks, AI challenges and human responses, committed gap, decision reasons, and runner-up. The concept check has five newly authored questions on A-D with explanations and revision. Its five points are instructor-reviewed completion, not an automatic score.

Browser drafts are scoped to artifact identity and version. A copied response can be edited elsewhere before being pasted into Canvas; clipboard failure exposes selectable text. Clearing uses an explicit inline confirmation and affects only that assignment's browser draft. An in-flight feedback response cannot restore a cleared draft. Stored feedback is marked when the participant edits the answer it assessed. Copy output contains current participant answers rather than hidden feedback or coach notes.

Only Test and Commit configures the reference's existing `ai-assisted-pedagogy.netlify.app/.netlify/functions/ai-proxy` endpoint. The builder creates no AI service, selects no provider/model, and adds no API key. A response is sent only on the participant's button click, with the task and criteria. Self-check, saving, and copying work without the service. Live feedback, CORS, provider availability, authentication, and backend billing were **not** verified; runtime/browser tests used mocked feedback. The existing `ai_activity` mode continues to mean activity-engine/JSON upload, and native quizzes keep their separate Canvas route.

## Validation

- Full Python regression suite: **202 tests passed**, including 28 new intake/source-build/guided-assignment tests. The guided runtime tests execute the shipped JavaScript with mocked storage, clipboard, and transport.
- Full repository schema: **PASS**, including all seven artifacts, paired source evidence, and final homepage metadata.
- Build-sprint skill validation: **PASS**.
- Git whitespace check: **PASS**.
- Final local browser QA: **PASS** in isolated Chrome at 1280x900 and 390x844. Checked all reading pages, module links, table readability, response save/reload, copying, answer revision, empty-answer handling, stale feedback, clearing/canceling, and absence of page errors or horizontal overflow.
- Feedback verification: one mocked browser request, zero live feedback requests. No real participant work or Canvas submissions were sent.
- Visual review: desktop module inventory and phone screenshots for the guided assignments, concept check, and table were inspected.
- Connected native Google capture, tab traversal, comment pagination, suggestion projections, public-link validation, and export failures are covered by synthetic fixtures. A live Google Doc link was not supplied for this test, so that integration is not represented as live-tested.

The browser relay encountered a native confirmation-dialog timeout during an early cleanup test. Draft clearing now uses an inline confirmation, and the final interaction/layout pass used an isolated headless Chrome session against the same local rendered pages. No existing browser profile or participant storage was used by that final pass.

## Remaining review boundaries

The document's point values are suggestions; the 40-point half-sprint total and the new review-guide bands need editorial review before publishing. Later-half teaching content, the requested video, and alignment of future Sprint 3/4 references with the eventual offering are not supplied by this source. Native Canvas rubrics remain manual. The earlier live native-quiz “unsaved changes” warning remains outside this change; it was not claimed fixed.

Keep the private source packet/map available when revising this source-backed build. Review the concrete local artifacts, then use the established explicit publishing/GitOps workflow if a later user instruction authorizes release.
