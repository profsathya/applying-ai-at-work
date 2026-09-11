# Clean page authoring instructions

Implemented the user's instruction-only plan on 2026-09-11. The approved visual first activity is a design reference, not participant-learning evidence. No course pages, renderer, schema, agent configuration, or publishing state changed in this pass. Existing earlier changes remain intact.

## Changes

| Owner | Revision | Change |
| --- | --- | --- |
| writing-to-teach | 2 → 3 | Direct openings, descriptive sections, selective grouping, purposeful visuals, mobile text order, image alternatives and reuse credit. |
| writing-assignments | 2 → 3 | Consolidate directions beside responses, keep essential teaching visible, preserve distinct tasks, use existing controls. |
| reviewing-course-text | 3 → 4 | Inspect rendered hierarchy, visuals, mobile layout, headings, keyboard/focus, labels, enlarged text, and attribution; report unavailable checks. |

The authoring contract now links to AUTHORING_PRESENTATION.md, which documents the approved example, tested Markdown indentation, section-reference behavior, compact eligibility, and the boundary between native Markdown and hosted styling. All three skills keep upstream commit 81a051324df61c41af464a0220f8085627729ad9 pinned and record the local adaptations. Existing routes already load these skills; no parallel instruction layer was added.

## Observed checks

- Parent ran the skill-creator `scripts/quick_validate.py` with the repository virtualenv on each changed skill: all three valid.
- Parent resolved 20 local Markdown links, parsed all 7 agent TOMLs using bundled Python 3.12 `tomllib`, and compared 187 course/renderer/schema/agent files with turn-start hashes: unchanged. System Python 3.9 lacked tomllib/tomli; no dependency was installed.
- Parent ran `.venv/bin/python canvas_sync/schema.py --all`: PASS, with the existing urllib3/LibreSSL warning only. `git diff --check`: PASS.
- Parent rendered the reference's exact Markdown through `markdown_body_to_html`: one ordered list, three complete stages, each continuation paragraph inside its list item.
- Two independent agents authored five isolated scenarios in /tmp under the updated skills. Parent inspected all outputs. Both guided drafts passed artifact schema validation as reported by the authoring agent. Single-response output used compact mode and one response; multi-task output retained both supplied IDs, standard layout, points, and submission behavior. Concept output used a readable timeline with no new task or submission. Exact-source and date-only equality checks passed both worker and parent assertions.
- Parent rendered all three authored scenarios and inspected desktop 1280px and mobile 390px screenshots. Browser measurements found no page overflow and 1, 2, and 0 response fields respectively. A first private selector looked for a nonexistent attribute; it was corrected to data-answer before recording final counts. No keyboard, copy, zoom, screen-reader, or participant test was performed in this instruction-only pass; these remain future authoring review requirements. No external image was used or licensed in the trials.

## Findings and limits

The scenarios adapted layout to the work instead of copying three steps or one diagram universally. Single-response teaching used an illustrative observed-versus-guessed example; two-response teaching preserved comparison followed by choice; concept teaching explained the practical significance of a timeline. Some reminder overlap remains a matter for editorial judgment, not a numerical threshold.

Rendered trials exposed inherited generic goal panels for artifacts without provenance and duplicated submission guidance in standard layouts. These prevent claiming that instructions alone reproduce the approved compact page everywhere. The implementation reference now explicitly tells authors to inspect and report those generated additions and never fabricate provenance to suppress them. Renderer changes are deliberately deferred because this pass authorizes instructions and documentation only. No other consequential missing decision found in this scope.

Parent used skill-creator, the three changed skills, the authoring contract, renderer/schema source, and the approved page reference. Workers also read writing-learning-goals revision 2 and the existing review-record contract. Skill changes were assessed by the agent; participant effectiveness is unobserved. No new source/research claims were introduced, and no upstream update was fetched.

Private evidence is under `.source-intake/visual-instructions-qa/`: turn-start hashes, isolated drafts, rendered HTML, screenshots, and browser measurements. This audit records instruction verification rather than a course-content authoring review; homepage maintenance was not triggered.

## Final fingerprints

| File | SHA-256 |
| --- | --- |
| `.agents/skills/writing-to-teach/SKILL.md` | `287bc0cace3cf26cad221981f2a35a26b8c8563ceabd98ff18ba29fe1ce38711` |
| `.agents/skills/writing-assignments/SKILL.md` | `469389aeb076ae0a290b14c2ff398df63633bc6a5e6b75b2ed5cad9b63e633b1` |
| `.agents/skills/reviewing-course-text/SKILL.md` | `48844ceb420eee471c842b6550757dea6c3cf1a7883c4981bbbf3b6200344f7b` |
| `docs/AUTHORING.md` | `4c3046d8ac5313d57935acfc16f038d722d5558d27d043ed6bd045a5c17a324d` |
| `docs/AUTHORING_PRESENTATION.md` | `6b2924062dd05b292278417003979eba496bb37333ea7ef366a67614c2cb853c` |

Reference versions: skill-creator `6656e54755638e8efcf275a472b9672eaa8a9a1b9e59dc210e275b03b59e1e66`; review-record contract `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`.
