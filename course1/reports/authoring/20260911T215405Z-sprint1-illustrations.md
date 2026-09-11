# Sprint 1 V2 illustrations

## Scope and decisions

Local revision of three pages in course 180, storage sprint 12, following the user's authorization to add a small set of stock-style visuals. The editorial assessment is the agent's; the resulting images have not been approved by the user or tested with participants. No Canvas publication occurred.

Added three original illustrations using the built-in image_gen tool: a workplace handoff in the Introduction, an annotated report-column mismatch in Things you stopped noticing, and an onboarding scene in Things somebody handed you. Images follow the opening action, use a consistent palette, and include alternative text and visible AI-generation disclosure. No outside stock sources were used. Exact prompts and generation provenance are saved in `course1/sprints/sprint-12/assets/illustration-provenance.json`.

The report illustration replaces its earlier stage-card layout; the Notice, Current work, and Possible gap explanations remain selectable text. It makes manual reordering concrete. The two workplace scenes provide human context beside the workflow/onboarding discussion; they are illustrative, not evidence about actual people. Essential instructions, uncertainty, real observation, cumulative tables, optional status, prompts, criteria, points, task identities, storage versions, and submission behavior remain intact. All three frontmatter objects match the turn-start snapshots exactly. The other three pages and their evidence files, other sprints, and agent instructions are byte-identical to those snapshots.

Local raster packaging was necessary for reliable preview and future hosted delivery. The renderer copies content-addressed images into each artifact's output, includes them in publish recovery paths, and changes the page hash when an image changes. Validation rejects missing files and paths outside adjacent assets/. Responsive CSS preserves the image composition. Three WebP files total 646,970 bytes; original PNGs remain in generation history and private evidence. Direct Canvas image uploads and AI-activity packaging were not added. The presentation reference documents the supported path.

## Reading and visual review

Parent inspected full-page desktop and mobile screenshots of all three revised pages. The first action remains ahead of the illustration; existing headings, selective panels, and adjacent response areas stay clear. Images scale without cropping or page overflow. The report's embedded labels become small on a phone, so its comparison is described by full alternative text and the surrounding explanation remains sufficient for the task. This is scoped visual/accessibility QA, not certification or evidence of improved learning. No new participant requirement or unresolved design decision was found in this scope.

These are diagnostic Markdown body counts, including image alt text, asset-path tokens, and captions; they are not visible reading counts or quality scores. This pass adds illustrations rather than targeting further word reduction.

| Page | Body before → after | Prompts | Criteria |
| --- | --- | --- | --- |
| Introduction: Find the Problem Worth Solving | 310 → 336 | 0 → 0 | 0 → 0 |
| Things you stopped noticing | 210 → 238 | 7 → 7 | 37 → 37 |
| Things somebody handed you | 386 → 420 | 8 → 8 | 47 → 47 |

## Sources, provenance, and homepage

Reviewed the current three artifacts and source evidence, turn-start snapshots, generated images, rendered pages, authoring/presentation guidance, and previous Sprint 1 visual-refresh review. The prior same-session read-only drift inspection found no target drift; no new Canvas inspection is claimed here. The original DOCX is unavailable. Adjacent source evidence records authorized adaptations of verified local Markdown with inherited lineage, baseline hashes, and adaptation-map hashes; this is not a fresh original-source conversion. Design inputs remain unchanged.

Homepage-maintainer reviewed all three changes and reported no metadata change needed: sequence, goals, cumulative-table evidence, and existing descriptions still align. Worker-reported homepage/full-schema checks passed; parent independently observed the full-schema pass and unchanged homepage hash.

Skills consulted: `.agents/skills/writing-to-teach/SKILL.md` revision 3, `.agents/skills/writing-assignments/SKILL.md` revision 3, and `.agents/skills/reviewing-course-text/SKILL.md` revision 4; imagegen for original images. Homepage worker applied maintain-homepage plus writing-learning-goals revision 2, writing-to-teach revision 3, and reviewing-course-text revision 4. Parent owns this record.

## Observed checks

- `.venv/bin/python canvas_sync/schema.py --all`: PASS, including all changed source-evidence sidecars and homepage.
- `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python -m unittest tests.test_local_images tests.test_hosted_html`: 20 passed. New coverage includes asset copying, changed-image hashes, recovery paths, duplicate/reference-style image references, missing files, path/symlink escape rejection, and unchanged remote-image handling.
- `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python -m unittest discover -s tests`: 219 passed, including existing renderer/runtime regressions. Offline Canvas environment overrides isolate fixtures. Existing urllib3/LibreSSL warning remains.
- `node .source-intake/sprint1-images/browser.cjs`: three image loads and alt text verified; 1280px/390px layouts and 320px with 200% text passed page-overflow checks. Heading hierarchy passed. Both response activities passed save/reload, keyboard copy, forced-denial fallback reveal/focus, disclosure keyboard operation, and visible focus. No page errors. Initial QA selector assumed a main element; corrected the selector to the actual section structure, then all checks passed. QA drafts were created only in an isolated browser context.
- Exact frontmatter and unaffected-file assertions passed; `git diff --check` passed. Source/adaptation validation passed. No participant trial, screen-reader session, or Canvas write occurred.

Preview: [updated comparison](http://127.0.0.1:8871/comparison.html), with the earlier pilot on the left and current illustrated pages on the right. Private evidence in `.source-intake/sprint1-images/` includes before snapshots, image originals, adaptation maps, render output, browser results/screenshots, and test logs. The separate before-illustrations route preserves this pass's immediate baseline.

## Final output fingerprints

| File | SHA-256 |
| --- | --- |
| `course1/sprints/sprint-12/introduction-find-the-problem-worth-solving-v2.md` | `2aaefbb523c5c43cec9434f17398229ceda7d34a24e1569b02d1eae0e6124d7b` |
| `course1/sprints/sprint-12/introduction-find-the-problem-worth-solving-v2.sources.json` | `eb29b3ccaa609c40e46191769d737e66e0fb4ee098f2c098d82228d30644b6c9` |
| `course1/sprints/sprint-12/things-you-stopped-noticing-v2.md` | `ec18c172e4761a9bfcebb3154cb5bd5c005a9ce5f68c40c94637aefee7c6aa07` |
| `course1/sprints/sprint-12/things-you-stopped-noticing-v2.sources.json` | `b54c864557af8fa9fa31208f4d2c0b6a136592bcf58d7d45e7853585dfc974a8` |
| `course1/sprints/sprint-12/things-somebody-handed-you-v2.md` | `a0dabd8d989046ab9c88e0b40b8e0a35387589eab07e7a88e548fcd3086c71d0` |
| `course1/sprints/sprint-12/things-somebody-handed-you-v2.sources.json` | `bd641f1e15fece52211c89a5fb25c08259416bee789aa81a7a46a7028cf63e9d` |
| `course1/sprints/sprint-12/assets/illustration-provenance.json` | `de97ef11bac984627b37b639acbd417bba06c7c02e17426f26baaf289abb751f` |
| `course1/sprints/sprint-12/assets/onboarding-help.webp` | `327f093e5f0157712a73bc600afdd7be32aabba9ee434f12d8d734fcf34fa20b` |
| `course1/sprints/sprint-12/assets/report-column-workaround.webp` | `fbf6daf2c9fd249a528b205b23c9b699fe1c66ae2cd3a87f05ff809a7f7dbaf8` |
| `course1/sprints/sprint-12/assets/workplace-handoff.webp` | `c523ce8e1506648aaa76becaaa7e9b86bf85ea0a3d7484895713ad191bfac701` |
| `canvas_sync/local_images.py` | `30968eb46be29f3cbe8d699d2194e40515eef25caec0e36fb1a92549b21b4e81` |
| `canvas_sync/hosted_html.py` | `fd615761deb2893de7ac62f4cb902e047ff90e42cd6821a28f6373fe6b92d4e9` |
| `canvas_sync/schema.py` | `b3efce2336ce55fa9bb1f526689f9c77427bed79a2bc483ace3e92a59d417bd2` |
| `canvas_sync/assets/guided-compact.css` | `2efd59c6bdae9da127455f623aaaeca1a0a44dd44d79b69787743153c6d6e097` |
| `canvas_sync/assets/guided-reading.css` | `a17683b923413df8633ccf3bdfc681c2add939fb9b3d413d9ac60fcef985c48b` |
| `tests/test_local_images.py` | `12b0ae3197f4e3f4f1522945e3836c7804ddde6ff1b609feaa6acdc355ec9308` |
| `docs/AUTHORING_PRESENTATION.md` | `6fb5a458bac04a20f6808654ac5f4f451b1935174fcd077bed3b80d51ea997ce` |

Unchanged homepage context: `course1/homepage.yaml`: `c6ba6b54386d0d89cbb2de55f9effd4820d6a08bc8becbc8ec2bb24b467d87a0`.

Additional skill/reference hashes:

- `.agents/skills/reviewing-course-text/references/review-record.md`: `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`
- `.agents/skills/maintain-homepage/SKILL.md`: `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7`
- `/Users/shaw8048/.codex/skills/.system/imagegen/SKILL.md`: `681ddb4ad6d06a2acc78a3535b583f8d0c1ea800ecda3d56370d3310fd2cd4ba`
