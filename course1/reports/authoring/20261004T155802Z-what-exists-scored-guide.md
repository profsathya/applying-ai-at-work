# What exists, and what it means: on-page scoring guide

Revision of one Course 1, Sprint 16 assignment. Jeremy explicitly authorized implementing and publishing the on-page scoring guide using the Problem Frame layout, with no native Canvas rubrics. The editorial assessment below is the agent's; no participant learning study or subsequent human review of the rendered result was performed.

The read-only source is `course1/design/sprint-2-self-checks.md` v0.5 at source commit `676f4da55b02bfb97552dd220e59ddc48516e67e`, including merged PR257. Its six full-points lines apply to this write-up. Only the off-page partial-credit rungs remain draft. The full-points wording is preserved exactly, with point labels appended: 8 + 10 + 10 + 8 + 10 + 4 = 50. No rungs, ranks, tags, new grading tiers, or native rubric are added to the participant page.

Reviewed sources: that record and `self-check-guide.md`; the target; Sprint 1 `problem-frame.md` and the live public Problem Frame; the approved longer-assignment reference `course1/sprints/sprint-12/test-and-commit-v2.md`; the prerequisite `what-solutions-already-exist-walk-through.md` and `dojo-lab-explore-what-already-exists.md`; the follow-on `problem-frame-is-it-worth-pursuing.md`; `course1/homepage.yaml`; and the authoring/presentation contracts. The saved baseline includes both public source and De Anza views before editing plus a local 15-page module render using the current protected deployment state. Native preparation returned `source_ready`, without drift, for assignment7175/module item18008.

The participant brings the table started without AI, investigates it through the Dojo and outside evidence, and submits the updated table and account of their judgment in two text responses. Four approved lines sit with the table response; two sit with the explanation. The existing reading layout, task IDs, version, submission contract, assignment identity and 50 points are preserved. Step labels now match the scoring record. A reading-only `criteria_open` flag keeps scored expectations visible initially; other reading pages keep their existing disclosure state. Text alone is sufficient for these evaluative statements; no new visual is needed.

Desktop and mobile inspection found a clear sequence from the table instructions to its response and four checks, then the worked example, second response and two checks, followed by the existing Download action. The first action and prior artifact are named. No teaching or example was removed. The two existing response tasks remain distinct. Local browser checks verified the exact six visible lines and total, keyboard disclosure/focus, draft retention across the before/after change, reload and actual Download output, at 1280px, 390px and 320px with enlarged text. All six source/adapter fixture views passed, without page errors, forbidden requests, or horizontal page overflow. These are software/editorial observations, not evidence of learning effectiveness.

Homepage maintenance was routed to homepage-maintainer: no YAML change was needed because the entry already says 50 points and the walkthrough says Practice · 0 points. Its homepage and full schema checks passed. No other source assignment, design record, manifest or deployment state was edited.

Validation observed: artifact and full schema PASS; link audit 172 artifacts/59 links/zero errors; supported artifact identity verification PASS; 18 guided-assignment tests PASS; 373 regression tests PASS with one existing skip after loopback-server permission was available; `git diff --check` PASS. An initial sandboxed regression attempt could not bind two localhost test servers. The full module browser check reports failed: eight pages use the existing Download UI while that checker expects `#copy-answers`, and an unchanged Stakeholder Map check expects one shared self-check where it finds two. Those broader checker issues are deliberately deferred. Byte comparison of local module renders changes only the targeted assignment HTML; the targeted replacement browser check tests the actual Download flow and passes. No broad module-browser pass is claimed.

Body, prompt and criterion counts are diagnostics, not observed reading time. Target counts from the preview: {"body": 228, "criteria": 83, "prompts": 46} to {"body": 228, "criteria": 158, "prompts": 46}. The new criterion wording increases detail to show the approved scoring expectations; the actual lines are six instead of eight placeholders. Live deployment and final native/served verification are recorded separately in the task receipt after publishing.

## Reviewed output fingerprints

| Path | SHA-256 |
|---|---|
| `course1/sprints/sprint-16/what-exists-and-what-it-means.md` | `c12820cd179e7d1a61398b3c7b660bc6a93494b395b6c31e3aab9706f656411f` |
| `canvas_sync/guided_assignment.py` | `e2f570c321d34ab2795c934085a3c04f7e8bcc70d5df3d3c1a7d2de9cb3f1e9d` |
| `canvas_sync/schema.py` | `c78328504523629608cc4dceb66c67683bb59310778e421be69f0f7eda204950` |
| `schema/frontmatter.schema.json` | `3e8a09cf9d4068be48af5ccfcbcb863c0223938f7f6a53e439992798353c5170` |
| `tests/test_guided_assignment.py` | `1909719b100e277e6432dead7548637dfba110d35c2127dbf3d354423a307e51` |
| `docs/AUTHORING_PRESENTATION.md` | `572b5b0b9a385e6cbb026661b3302927e95fa1ea5bf1456db0d0bbeeec6721be` |

## Skills and reference fingerprints

Writing Assignments local revision4; Reviewing Course Text local revision6. Workflow skills have no local revision, so their hashes identify the versions used. Maintain Homepage was applied by the homepage-maintainer worker; Sync supplies the already authorized protected publishing path. The record contract is fingerprinted below.

| Path | SHA-256 |
|---|---|
| `.agents/skills/update-artifact/SKILL.md` | `443d44074f11ae4b9caf65ab0820967a67314b6351a22758428515436ba13d80` |
| `.agents/skills/writing-assignments/SKILL.md` | `767ad4bbc05b0333c0b95c8ec6632c872b389f403540d0d0794689b48ba0b4c2` |
| `.agents/skills/reviewing-course-text/SKILL.md` | `1614ebaf7e321064f02c7a9041d5443e3c1c45c800a278a0fd54cd539fb7401c` |
| `.agents/skills/maintain-homepage/SKILL.md` | `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7` |
| `.agents/skills/reviewing-course-text/references/review-record.md` | `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e` |
| `.agents/skills/sync/SKILL.md` | `2dca43a30dc30d7b87e02c22f208635039c459f7c624556618ed57dc949fca8b` |
