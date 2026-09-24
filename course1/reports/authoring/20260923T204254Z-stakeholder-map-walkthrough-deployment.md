# Stakeholder Map Canvas Walkthrough: deployment verification

Only the requested Stakeholder Map conversion was staged. The agent's authoring and implementation review is in `20260923T203157Z-stakeholder-map-canvas-walkthrough.md`; the artifact bytes are unchanged from that review.

## Observed result

- New assignment: [Stakeholder Map Canvas Walkthrough](https://cti-courses.instructure.com/courses/180/assignments/7163), Canvas course 180, assignment 7163, module item 17995.
- Unpublished assignment and module item, verified by Canvas API and browser UI. Immediately after original item 17991 in module 2081, before the Dojo Lab. Prior items retain their relative order. Position sequence: original Stakeholder Map 4, new walkthrough 5, Dojo Lab 6.
- Original assignment 7159 remains published with unchanged title, description, points, grading type, submission types, assignment group, dates, and rubric. New assessment settings match, including allowed extensions/attempts and grade/override flags. 35 points, file upload, no rubric or dates.
- Exact-file [Publish Canvas run](https://github.com/profsathya/applying-ai-at-work/actions/runs/35916782685) succeeded from content commit `c00b4748447d876756abc60662a9ab39241224d3`. Deployment state commit: `7efa707`. Common Curriculum commit: `7f9549c6309e10afd77a062b67ec6527b394dae8`; [Pages deployment](https://github.com/profsathya/Common-Curriculum/actions/runs/35916913920) succeeded. Served HTML hash matches deployment state.
- The first GitHub run failed before any Canvas write because two pre-existing mapper tests hardcoded `.venv/bin/python`. Changed them to `sys.executable`; 13 table tests passed locally, and GitHub's full validation passed. PR validation also passes.

## Actual Canvas browser checks

The hosted page loaded inside the real Canvas assignment. The standard opening, workbook/document link, table inputs, feedback buttons, 35-point file-upload settings, and finish controls were present. Used four synthetic cell values only; no participant submission was made.

The actual iframe **Copy work** button copied rich tables. Normal browser paste into a new Google Doc reported “Pasted table cells.” Exported that saved Doc as DOCX and compared all 11 tables and 138 cells with the previously source-verified local paste. Source text, blank cells, four test answers, and the multiline answer all match after only outer whitespace/NBSP normalization. Scratch Doc: `https://docs.google.com/document/d/1vA5Y_qGnflhNsc4zcqpD6p__36Dv2fu6gc1HQ85d-Aw/edit`. Export SHA-256: `a3a022244865c24f7605a86cc3505264e2b63f8d88da17e361c5234d02709253`.

Real AI feedback succeeded through the Canvas iframe on the Role row of `stakeholder-1`, appeared below the correct table, and preserved the typed answer. It recognized the observation supporting Confirmed and asked the participant to clarify the person's relationship to the problem. This complements the eight reviewed provider checkpoint requests recorded before staging. The standalone hosted browser path also returned OPTIONS 204 and POST 200.

Two initial iframe attempts displayed the recoverable unavailable message. Direct CORS/provider checks and the hosted browser route succeeded; after reloading Canvas the same row request succeeded. The cause of those initial failures was not established, so they are retained here rather than reported as a fault-free run. No retries were hidden in the service and no fallback sample was passed off as real feedback. The failure message preserved all writing. Synthetic browser drafts were cleared after evidence capture, leaving a blank draft for the instructor. API tests and agent browser QA are not a human participant study.

## Fingerprints and evidence

| File | SHA-256 |
| --- | --- |
| `course1/sprints/sprint-16/stakeholder-map-canvas-walkthrough.md` | `7b169fcae73ea6d60db233d44e7ba1e82438c12ffa5abef99184fc768f27da70` |
| `course1/sprints/sprint-16/stakeholder-map-canvas-walkthrough.sources.json` | `a84d54b67e8c5fae7b768348fcddea8c3d4267e51ff2b50850fedbe129dc61ee` |
| `services/course-ai/netlify/functions/walkthrough-guidance.json` | `80bc7f8e5cc3084d05b168db0273be8cdb444d58a5c7d7e6c9d55cc5e772c441` |
| `.source-intake/stakeholder-walkthrough-20260923/canvas-final-verification.json` | `c34a24788f175bcd0aff263c12040f6af9f0015cab60d24881713602e0b3d4e2` |
| `.source-intake/stakeholder-walkthrough-20260923/canvas-paste-result.json` | `ce470365153f7e3bb3a388d49bbe3fe45fadec36d59f78d3f9e4739c188ea435` |
| `.source-intake/stakeholder-walkthrough-20260923/canvas-browser-feedback.json` | `5b62b9a9db26f86259043144eeea9e2ac0b64f3154a906490b265b3998dea72b` |
| `.source-intake/stakeholder-walkthrough-20260923/deployed-walkthrough.html` | `df41f9fedfba23b41f783a32a657481e011f7c89a826ed7fffd1da5a0f3bd33d` |
