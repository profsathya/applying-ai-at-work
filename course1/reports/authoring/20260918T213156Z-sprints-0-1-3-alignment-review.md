# Sprints 0, 1, and 3 alignment review

## Target and status

- **Course:** CIS 501: Reframing Problems with AI (Course 180)
- **Scope:** current Sprint 0 (`sprint-6`), Sprint 1 (`sprint-14`), and Sprint 3 (`sprint-15`), with the current homepage as navigation context
- **Request:** review content alignment across the three sprints
- **Status:** recommendations-only editorial review. No participant-facing source was changed. The assessment below is the agent's editorial judgment; human approval and participant learning were not assessed.
- **Review revision:** detached `origin/main` at `8bbfafbdcd9975b5000189fecd26b6e15f65e316`. The primary working tree was not rebased, reset, or cleaned.

## Sources and files reviewed

Read all Markdown artifacts directly under:

- `course1/sprints/sprint-6/`
- `course1/sprints/sprint-14/`
- `course1/sprints/sprint-15/`

Also reviewed `course1/homepage.yaml`, `docs/AUTHORING.md`, `docs/AUTHORING_PRESENTATION.md`, and the approved Sprint 1 presentation examples under `course1/sprints/sprint-12/` as read-only context. No Google Drive or Canvas content was changed or inspected in this pass.

## Skills consulted

| Skill/reference | Revision or SHA-256 |
| --- | --- |
| `.agents/skills/reviewing-course-text/SKILL.md` | local revision 6; `1614ebaf7e321064f02c7a9041d5443e3c1c45c800a278a0fd54cd539fb7401c` |
| `.agents/skills/writing-to-teach/SKILL.md` | local revision 5; `7cd409b3a8bee0d7b5c5316ddbc152940753823cb649989d59174e20cafd2ca5` |
| `.agents/skills/writing-learning-goals/SKILL.md` | local revision 2; `0a9427039031806b7eea78d5bf6a9fb22c629bf70b9cd20e42169fe817eca9da` |
| `.agents/skills/writing-assignments/SKILL.md` | local revision 4; `767ad4bbc05b0333c0b95c8ec6632c872b389f403540d0d0794689b48ba0b4c2` |
| `.agents/skills/reviewing-course-text/references/review-record.md` | `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e` |

## Decisions and alignment

The three-sprint sequence is instructionally coherent at the level of capability, practice, and evidence:

1. Sprint 0 establishes a real problem context, a five-sprint evidence trail, the rule that AI supports while the participant decides, and the distinction between saving/copying and Canvas submission.
2. Sprint 1 begins from independent observation, produces a seven-part Problem Frame with confirmed/unverified assumptions, uses AI only after the participant's own drafts exist, and preserves a human accept/reject decision.
3. Sprint 3 carries the same problem forward, begins with an independent stakeholder map, uses AI to test and widen it, requires a real stakeholder conversation, and asks for an evidence-backed frame revision.

The point structures also align: Sprint 1 and Sprint 3 each total 100 points, each uses a zero-point must-submit Dojo transcript, and each ends with a 10-point AI-supported reflection that preserves human judgment. Sprint 3's four stakeholder relationships, real-person requirement, three-file conversation submission, and conflict-as-information principle all support the Problem Frame rather than introducing a competing artifact arc.

## Findings

### Consequential gaps for revision

1. **The Sprint 3 Problem Frame handoff is not executable at the same level of specificity as Sprint 1.** Sprint 1 creates and carries forward one complete seven-part Problem Frame. Sprint 3 says to revise it, but the Stakeholder Validation Report asks for a one- or two-sentence starting frame and an unspecified "Revised Problem Frame," while the final reflection asks what changed and then says to save the reflection as the mid-course version. A participant cannot tell whether to update all seven parts, update only the affected parts in a separate file, or treat the reflection as the revised frame. The smallest coherent fix is to identify the seven-part Sprint 1 Problem Frame as the source artifact, say exactly where the revised version lives, and distinguish the revised frame from the reflection about it without changing points or submission mechanics.
2. **Evidence-status vocabulary changes without a bridge.** Sprint 1 marks Problem Frame assumptions `confirmed` or `unverified`; Sprint 3 marks stakeholder-map fields `Confirmed` or `Inferred`. Both distinctions are internally sound, but Sprint 3 never tells participants that the new labels apply to the map while the Problem Frame retains its existing assumption statuses. Add one short bridge at the first Sprint 3 use and preserve both schemes.
3. **Sprint 3's opening overstates AI availability.** "AI is your thinking partner throughout" appears before the Stakeholder Map's explicit "No AI on this one." Replace "throughout" with wording that says AI supports the designated testing and preparation steps after independent work. The rest of the sequence already enforces this correctly.
4. **"Pass the concept check" implies an unstated threshold.** The Sprint 3 module overview says to pass it, while the quiz is described as a low-stakes five-point anti-skim check with unlimited attempts and no participant-facing pass score. Use "complete" unless a pass threshold is an intentional Canvas policy.

### Minor consistency cleanup

- Sprint 1 retains British `neighbours`/`neighbourhood` in four participant-facing locations while the surrounding course uses American English. Normalize these in a future scoped revision.
- Sprint 1 describes choosing a problem for the "next nine weeks" even though Sprint 0 defines a ten-week course and the choice occurs during the two-week Sprint 1. Prefer "the rest of the course" to avoid calendar arithmetic.

### Intentionally unchanged

- Artifact identities, order, points, submission types, completion mechanics, templates, AI activity IDs, and the independent work -> AI testing -> human evidence -> revision sequence were not changed.
- The current four stakeholder relationships, Candidate Log, Dojo transcript continuity, real stakeholder conversation, honest evidence-backed no-change option, and three-file Sprint 3 conversation submission remain aligned.
- Hidden legacy homepage sections were treated as historical context; the active Sprint 6, 14, and 15 homepage entries align with the current artifact inventories.

There was no source conversion or adaptation in this pass, and no participant testing was observed.

## Observed validation

- `CANVAS_API_URL='' CANVAS_API_TOKEN='' /Users/jeremyshaw/Projects/applying-ai-at-work/.venv/bin/python canvas_sync/schema.py --all` -> **PASS**.
- Sprint 0 preview with `preview_module.py`, sprint `6`, and `--check-browser` -> **passed**, 7 participant pages, no reported errors.
- Sprint 1 preview with `preview_module.py`, sprint `14`, and `--check-browser` -> **partial**, 9 participant items. Eight rendered pages had no reported errors; the AI reflection was skipped because it requires its delivery-specific engine preview.
- Sprint 3 preview with `preview_module.py`, sprint `15`, and `--check-browser` -> **partial**, 6 participant items. Four rendered pages had no reported errors; the Stakeholder Conversation and Reflection AI activities were skipped because they require their delivery-specific engine previews.
- Manually inspected the desktop and mobile comparison screenshots for all three sprints. The openings, reading columns, illustrations, headings, and first actions were legible, with no visible horizontal overflow or doubled text. Automated enlarged-base-text checks reported no errors.
- Preview root: `.source-intake/module-review/sprints-0-1-3-alignment-20260918T213156Z/`

These checks establish schema and sampled rendering behavior, not teaching effectiveness, participant learning, live Canvas state, template permissions, or hosted AI behavior.

## Reviewed output fingerprints

Unchanged recommendations-only targets:

```text
557b9f64abafabec530b18221bc913d77fe615582d54cfd79179fa67e14259ac  course1/sprints/sprint-14/brainstorm-your-list.md
a1a8e332f3a5b791fd02668fe6412aeebc9cd8d4d8282facdbc521d75b60019d  course1/sprints/sprint-14/dojo-lab-test-widen-choose.md
5dbffad6acafeeae5282c6ff187fa75a378088bb6e897803052c1f20a2fe5dc7  course1/sprints/sprint-14/first-frames.md
25c51c1c23a13fea16f4d691980c171bea0ead6f84b9084d4e90bd42009069dd  course1/sprints/sprint-14/get-underneath-three-to-five.md
b1116c051edc009ef7908194ba7ec2f5fbbb5bf20535ba1ec933361c787da834  course1/sprints/sprint-14/introduction-find-the-problem-worth-solving.md
4597b454954abec009fa90818ad07df4b7885a84b89f6ec3b535e670e81f9867  course1/sprints/sprint-14/problem-frame.md
aa403b1909a34f071968ce9a5920ea211430152ad30f525dc2a8ea65bafcf287  course1/sprints/sprint-14/sprint-1-concept-check.md
1d37fa072ef45669fe87165dc80606a06648cfea894e6e1a39333ac325874431  course1/sprints/sprint-14/sprint-1-find-the-problem-worth-solving.md
8c06223691f2b63c0db9dab72091fa75b5a91e8182c3afc1d5732da0eb92f3d8  course1/sprints/sprint-14/sprint-1-reflection-what-changed-v54.md
1b6a8a0fa4650c07c41a912b3b0caaa7bd0af5a4b6007fff5b58b7e2fcc85145  course1/sprints/sprint-14/the-problem-frame.md
5e1d0c4cc8a21eef68b7057bf60ae0cc84b0082778a0382dab44ba5d580a4140  course1/sprints/sprint-15/dojo-lab-test-widen-choose-v3.md
90ef36232c498686fa883ce7ae87e6e50ee612c5e713d782fcdb03b7de8db417  course1/sprints/sprint-15/introduction-integrate-people-and-context-v3.md
3f5aa9ace07b746cc6c27fd135e6c36c20b1827c520ea9816cd3604f37d99283  course1/sprints/sprint-15/sprint-3-concept-check-v3.md
ed624c1e4342fbf2ffc8904e644f16df9f44f6d2124d348ebbc8bad531f2b395  course1/sprints/sprint-15/sprint-3-integrate-people-and-context-v3.md
ad03e08427bd4718234edff8f540e1e01f073c547ae383de8bddd656a26f73fa  course1/sprints/sprint-15/sprint-3-reflection-and-mid-course-problem-frame-revision-v3.md
10ef56cd1e22eaaa8662dfae191beb916727d2aea12c5a1452b362ea9631c8e8  course1/sprints/sprint-15/stakeholder-conversation-v3.md
f7114a439c6fe16df4cd66cc0633fe67f635ea8354df9bf8cfc441b5cf60688d  course1/sprints/sprint-15/stakeholder-map-v3.md
63202e6438282a98591b0db7bde07af791df4ea06d816c7ee32e66fd3b253146  course1/sprints/sprint-6/help-and-resources-v2.md
590275cae886b83c08c1c7da178b5744e230cadd0f82d2ee93eefa79e9f02951  course1/sprints/sprint-6/how-this-course-works-v2.md
04960de3bdb5b2c8b106a12c0a12ce04389b6889fe1572b19b150843741a1f50  course1/sprints/sprint-6/introduction-post-v2.md
a52d3bcc37c2c0fe6e7fd0bf415273b67594f92b8bd971f8cc6a4e38f583cea5  course1/sprints/sprint-6/set-up-your-ai-dojo-v2.md
3a1ad97150d68b681ceb80f87d263e82f69585e0aea25dce44c219c80b5e4f8b  course1/sprints/sprint-6/start-here-v2.md
826a0dd561f690ec0434bbcb40ed6ceb2839c366747202eb9489d3c21309e7ae  course1/sprints/sprint-6/welcome-and-orientation-v2.md
edd97f25303a3e5803d19e6631122851629e957c90238780dfb93162b76aa06b  course1/sprints/sprint-6/welcome-v2.md
ae14359c618e22d190899504c745f2c821cfc5786868608175bdd5f9303020a8  course1/sprints/sprint-6/your-first-week-v2.md
```

Read-only navigation context:

```text
4146efaf5315465f9f07fb57b37648fcfb777381500c74cc3172c4b4c86683af  course1/homepage.yaml
```
