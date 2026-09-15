# Sprint 0 visual adjustments

## Status and scope

Completed local visual revision requested by the user: a new Welcome illustration in the approved art style and additional blue accents. This is the agent's review; approval of the rendered result has not been observed. No publication occurred. This record supplements [the instructional review](20260915T231006Z-sprint-0-revision.md).

## Changes and source integrity

- New AI-generated scene: two working adults examining connected observations on a pinboard, one with an open notebook. Navy outlines, slate blue/teal, cream paper texture, natural adult proportions. Inspected the original Sprint 1 illustration for style. The new image is an unmodified generated PNG, with prompt, hash, date, disclosure, and alt text recorded beside the asset.
- Replaced the copied handoff illustration only in Sprint 0; its prior local bytes remain in the private before-source backup. Sprint 1 remains unchanged.
- Added four supported Markdown callouts: the integrated problem document, weekly rhythm, calendar example, and first-half no-AI guidance. Existing Start Here goals and Help submission-list accents remain. No CSS, renderer, assessment, or navigation changes.
- Rebuilt all seven Markdown/evidence pairs from the preserved source packet and an updated map using source_build. Reorganization is labeled adaptation. Apart from the image/alt/caption and blockquote markers, body wording is identical to the previous local revision. Every frontmatter field is unchanged.
- Homepage maintainer checked alignment and found no YAML change necessary. Goals, practice, evidence, and criteria remain as recorded in the instructional review.

## Visual review and validation

Inspected all four changed pages at desktop and mobile widths. The new scene remains readable without embedded labels, and its meaning is also conveyed in prose and alt text. Blue callouts emphasize existing content without repeating it. Next actions, heading order, and reading flow remain intact. No clipping or image-loading issue was found in scope.

Normal source-build validation and individual validate_artifact checks passed for all seven artifacts. Parent and homepage worker each observed `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python canvas_sync/schema.py --all` passing; worker also validated homepage. `git diff --check` passed. Existing LibreSSL warning only.

The following local browser command passed all six pages at 1280px, 390px, and 320px enlarged base text. Checks include image loading/alt text, headings, visible control names, and overflow. Native Canvas submission and AI services are not exercised. This is not browser-zoom or screen-reader certification, and no participant testing occurred.

```sh
CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python canvas_sync/preview_module.py --manifest course1/manifests/production.json --sprint 6 --state-dir .source-intake/sprint-0-revision-20260915T225941Z/canvas-state --output .source-intake/sprint-0-revision-20260915T225941Z/visual-v2 --baseline .source-intake/sprint-0-revision-20260915T225941Z/after --check-browser --node /Users/jeremyshaw/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --playwright-module /Users/jeremyshaw/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright --browser-executable '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
```

[Before/after comparison](../../../.source-intake/sprint-0-revision-20260915T225941Z/visual-v2/comparison.html#welcome-v2) · [Browser evidence](../../../.source-intake/sprint-0-revision-20260915T225941Z/visual-v2/browser-results.json)

## Measurements

Markdown body counts include image alternative text and paths. Configured prompt and criteria counts remain zero; the native discussion prompts are part of its body. This is a visual revision, not a verbosity intervention.

| Page | Body before | Body after | Prompts before/after | Criteria before/after |
| --- | ---: | ---: | ---: | ---: |
| Start Here | 239 | 239 | 0 / 0 | 0 / 0 |
| Welcome | 398 | 403 | 0 / 0 | 0 / 0 |
| How This Course Works | 591 | 591 | 0 / 0 | 0 / 0 |
| Your First Week | 242 | 242 | 0 / 0 | 0 / 0 |
| Introduction Post | 173 | 173 | 0 / 0 | 0 / 0 |
| Help and Resources | 703 | 703 | 0 / 0 | 0 / 0 |

## Skills and references

Authoring/review skill versions from the prior review continue to apply. This narrow follow-up additionally consulted the image-generation skill and reread the supported presentation and homepage workflow.

| File | SHA-256 |
| --- | --- |
| `/Users/jeremyshaw/.codex/skills/.system/imagegen/SKILL.md` | `681ddb4ad6d06a2acc78a3535b583f8d0c1ea800ecda3d56370d3310fd2cd4ba` |
| `.agents/skills/maintain-homepage/SKILL.md` | `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7` |
| `docs/AUTHORING_PRESENTATION.md` | `f6b7ed4fbabf468cc67012e9c5decafa83b6f751dce2f620ae8398c9e0aa3a56` |
| `.agents/skills/reviewing-course-text/references/review-record.md` | `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e` |

## Final output fingerprints

| Path | SHA-256 |
| --- | --- |
| `course1/homepage.yaml` | `8682137157f9e45da1d257ac956a10006123d96c12492dc10de289edf9129669` |
| `course1/sprints/sprint-6/assets/illustration-provenance.json` | `b7250440a393cf001272052a2ca6e114a5da3adc5ca754cc2524e20d61bfc12b` |
| `course1/sprints/sprint-6/assets/problem-investigation.png` | `6aefac80f3a56e7e5b90e2cf8215743f2c967fa56c2c66078e69a7e7e6979d02` |
| `course1/sprints/sprint-6/help-and-resources-v2.md` | `b4ebac2a8738be3c5621cdf94f02e2cd04251954fdef382859e5f856efd4c357` |
| `course1/sprints/sprint-6/help-and-resources-v2.sources.json` | `d9260ab5f222646d097095c9966cea027f4dc284b82488aab83dde4c18338e94` |
| `course1/sprints/sprint-6/how-this-course-works-v2.md` | `1ce08abce58fa281ac0b9fef20bfd782ece904d6252514819272ac5833f68288` |
| `course1/sprints/sprint-6/how-this-course-works-v2.sources.json` | `3483d0e721a3e213923514af75d6c1ef81a29a03d164047b214e343827e88436` |
| `course1/sprints/sprint-6/introduction-post-v2.md` | `de7da6d77a1c8b5017d7fe730fc5744f3bd2d0ca1ce5547695f464672fa1f505` |
| `course1/sprints/sprint-6/introduction-post-v2.sources.json` | `cf2315c43fff63454491e31659bbbbbee3b4a5704ecb107ce1aa7be161166d76` |
| `course1/sprints/sprint-6/start-here-v2.md` | `e0c575602b5fd6af49e0db60491d626fb72eb8c9c42eeec39c5224875ba97e2b` |
| `course1/sprints/sprint-6/start-here-v2.sources.json` | `935c972eb93f19e2e7f88ef32fe61ecf96a2e4be083660f9facd3d0c3e23ede6` |
| `course1/sprints/sprint-6/welcome-and-orientation-v2.md` | `e4d5524e8f9a477112fa3537428e443b988e1f13062f456e9083f5b7a665523d` |
| `course1/sprints/sprint-6/welcome-and-orientation-v2.sources.json` | `21f4a5362935109a436f68368c97e40074c670a76beea8661f7e822ad4d01951` |
| `course1/sprints/sprint-6/welcome-v2.md` | `134f10d59ee85e3e5971f824449518658bca8ad18f97c564b962b3424c0a1758` |
| `course1/sprints/sprint-6/welcome-v2.sources.json` | `97fcd1b1bee468b36ec6afc05ed5a116cf0563169c81fd745e6a6a1febb85e55` |
| `course1/sprints/sprint-6/your-first-week-v2.md` | `075bc7dea68a07ceca425136d098a4b31e92c3fc0343bac1b63aa417fd10385d` |
| `course1/sprints/sprint-6/your-first-week-v2.sources.json` | `3adb62479bce16c9266c2b444e099ce004081961ae244fa87f715f67e64bcb74` |
