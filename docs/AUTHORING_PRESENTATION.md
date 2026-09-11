# Supported page presentation

Use this reference when arranging a participant page or adding an instructional visual. Teaching and review principles live in the shared skills linked from [AUTHORING.md](AUTHORING.md).

## Reference page and delivery boundary

[Start your list and get underneath it](../course1/sprints/sprint-12/start-your-list-and-get-underneath-it-v2.md) demonstrates a direct opening, grouped instructions, an illustrative process diagram, and an adjacent response. The user approved this visual direction; participant learning has not been measured. Its three steps and one example fit that activity, not every page.

Use the approved Sprint 1 V2 set as examples of different instructional jobs:

| Page pattern | Reference | What to carry forward |
| --- | --- | --- |
| Orientation | [Introduction](../course1/sprints/sprint-12/introduction-find-the-problem-worth-solving-v2.md) | Essential concept, route through the work, pacing and deliverables |
| Short practice | [Start your list](../course1/sprints/sprint-12/start-your-list-and-get-underneath-it-v2.md) | Direct action, one useful example, adjacent response |
| Illustrated worked example | [Things you stopped noticing](../course1/sprints/sprint-12/things-you-stopped-noticing-v2.md) | Concrete comparison with essential reasoning in text |
| Request-to-goal reasoning | [Things somebody handed you](../course1/sprints/sprint-12/things-somebody-handed-you-v2.md) | Human context, a connected explanation, alternatives to examine |
| Concept check | [Sprint 1 Concept check](../course1/sprints/sprint-12/sprint-1-concept-check-v2.md) | Distinct questions, clear feedback, intact assessed concepts |
| Longer assignment | [Test and commit](../course1/sprints/sprint-12/test-and-commit-v2.md) | Several meaningful parts with responses at their point of use |

Select the qualities that serve the new module. Do not copy its assessment policy, examples, number of steps, or submission count merely to match the reference.

Artifact bodies remain Canvas-native Markdown. The hosted guided-assignment renderer supplies cards, layout, and controls. Plain Canvas Markdown rendering preserves the content but does not promise the hosted styling or browser controls. Do not put HTML, CSS, JavaScript, iframes, or CDN references in an artifact to imitate the preview. Use existing supported presentation; report a needed renderer capability separately when it is outside the authorized scope.

## Choose a supported layout

- Standard guided assignments support multiple tasks. Omit `presentation` to keep the standard layout; do not consolidate distinct task identities just to obtain compact styling.
- Set `guided_assignment.presentation: compact` only for exactly one task of kind `response`, with an `instruction_section` and no `feedback_endpoint`. Preserve the task ID, artifact ID, version, and assessment metadata when revising an existing activity.
- Use `guided_assignment.presentation: reading` for a continuous sequence with multiple response or choice tasks and no AI feedback endpoint. It retains each task, groups radio options accessibly, places response self-checks after the response, and provides one primary copy action with secondary utilities under More options. Introductory pages can opt into the matching reading column with `page_presentation: reading`; this field is valid only for pages. Reading presentation omits generated goal/overview framing; informational reading pages also omit the generic completion panel, so their authored ending should give the next step.
- `instruction_section` matches the exact visible title of a unique top-level `##` Markdown heading. Each section may be referenced by only one task. Its content runs to the next `##` and renders once immediately before that task, in task order. Unreferenced content remains before the tasks. Check the assembled order when moving sections.
- Compact presentation supplies one response area, a self-check, a primary **Copy my answers** button, and secondary utilities under **More options**. Use `standing_instruction` for the activity's optional/points information near submission. Required purpose and prerequisite metadata remain present but are not shown in the compact opening; essential prerequisites must still appear in visible teaching. Copying and saving do not submit to Canvas.

Validate with `.venv/bin/python canvas_sync/schema.py --artifact <path>` and render through the normal local preview workflow. Do not claim browser verification from schema validation.

The outer hosted renderer can still add a generic goal panel for artifacts without source provenance, and standard layouts can repeat submission guidance. Inspect these generated additions as part of the assembled page. Report remaining renderer duplication separately when a code change is out of scope; do not invent source provenance or remove real prerequisites to suppress a panel. The approved source-derived compact page does not establish that every layout has the same opening or controls.

For a newly authored single-response activity without source provenance, `presentation: reading` also supports one mapped task and avoids that outer goal panel. Choose it when a continuous opening fits the activity, then inspect the result. Compact remains useful for source-derived activities like the approved first page.

## Markdown process diagram

In compact presentation, the following pattern produces three connected stages across on desktop and stacked on narrow screens. Use it for an actual sequence or relationship. The ordered text preserves the meaning without arrows or color.

```markdown
> **Illustrative worked example · Volunteer onboarding**
>
> 1. **Notice**
>
>     New volunteers come twice, then stop.
>
> 2. **Describe the process**
>
>     The shift lead gives each arrival whatever task is easiest to hand off.
>
> 3. **Find the possible gap**
>
>     Nobody plans the first month. Volunteers may lack an ongoing role. (?)
```

Keep four spaces after the blockquote's separating space before continuation paragraphs (`>     Text`). Insufficient indentation separates the explanations from their list items in the current Markdown renderer. Inspect the result, not just the source.

Current compact CSS treats blockquote lists as stage cards and uses three desktop columns. It is not a general diagram engine: do not force a different instructional structure into three stages or use this pattern for unrelated quoted lists. The reading layout also styles blockquote lists as stage cards, using flexible desktop columns and a single mobile column. Standard layouts retain ordinary Markdown behavior. Use a readable list or supported table when it fits better; keep comparison tables narrow enough for mobile use.

For an outside image, use normal Markdown image syntax with meaningful alternative text and a nearby creator/source/license credit after verifying reuse permission. Choose an asset location supported by the delivery workflow and verify it loads in the rendered preview. Do not treat an unverified image URL or a text-only mockup as a completed visual integration.

## Local illustrations

For hosted pages and guided assignments, keep raster images in an `assets/` directory beside the Markdown and reference them normally:

```markdown
![A description of the information the image conveys.](assets/example.webp)

*Brief context and creator/source/license credit, or an AI-generation disclosure.*
```

The renderer copies local PNG, JPEG, WebP, and GIF assets into the generated page's output directory using content hashes. Missing files and paths outside the adjacent `assets/` directory fail validation. Changing an image changes the page's delivery hash; publish recovery includes its image files. This packaging applies to ordinary hosted pages and guided assignments. Direct Canvas image uploads and AI-activity packaging are separate workflows.

Reading and compact layouts scale illustrations to the reading column without cropping. Place them after the opening action and beside the idea they clarify. Keep essential teaching in selectable text, and inspect the image at mobile width. The [Sprint 1 illustrations](../course1/sprints/sprint-12/assets/illustration-provenance.json) provide an example of recorded prompts and generation provenance for original AI images; these are illustrative scenes, not records of actual participants or workplaces.

## Reusable illustration brief

Before choosing an image, state its instructional purpose, subject or relationship, location in the page, and required text equivalent. Check the course's existing assets first. When reusing an asset in another module, copy it into that module's adjacent `assets/` directory and retain its original provenance/credit. A new module does not require new imagery if an existing asset serves the same purpose.

For the approved visual family, adapt this brief to the actual subject:

> Create a professional editorial textbook illustration for working adults. Show [specific scene or comparison] to help the reader [understand or do something specific]. Use restrained navy outlines, muted slate blue and teal, a warm cream background, light paper texture, natural adult proportions, and uncluttered composition. Keep a consistent style with the supplied course reference. Use a wide composition for a context scene; choose the aspect ratio for the information. Omit logos, decorative interface elements, and unreadable small text. Keep labels short and large only when they clarify the comparison. This is an illustrative example, not documentary evidence.

Inspect the actual result for misleading details, incorrect labels, and mobile legibility before integration. Prefer semantic text for dense labels or relationships. Save the final prompt, tool/source, creation date, asset filename, and any delivery conversion in a local provenance file. Include visible AI disclosure for generated scenes or verified creator/source/license credit for outside images. No fixed image quota applies.

## Module preview and checks

Run from the repository root using the repo virtualenv. The command is local-only and writes to a new output directory; it never calls Canvas or changes course source. It previews the selected storage sprint, including unpublished local artifacts. Preserve each output as a review snapshot.

Before a revision:

```bash
.venv/bin/python canvas_sync/preview_module.py --manifest course1/manifests/production.json --sprint 12 --output .source-intake/module-review/before
```

After the revision:

```bash
.venv/bin/python canvas_sync/preview_module.py --manifest course1/manifests/production.json --sprint 12 --output .source-intake/module-review/after --baseline .source-intake/module-review/before --check-browser
```

For a new module, omit `--baseline`. Substitute the course and storage sprint; use a fresh output path for each pass. Optional `--state-dir .canvas-state` uses existing local deployment state for Canvas links without contacting Canvas. Serve the output for manual inspection:

```bash
.venv/bin/python -m http.server 8872 --bind 127.0.0.1 --directory .source-intake/module-review/after
```

Open `http://127.0.0.1:8872/comparison.html`. The output includes an artifact inventory, source hashes, body/prompt/criteria counts, metadata changes against the baseline, and explicit browser-check status. Counts include Markdown image alt text and paths; they are diagnostics, not rendered word counts. Baselines retain their original generated styles and assets. Module navigation covers only the selected module.

Browser checks require Node, Playwright, and Chromium. Use existing workspace dependencies when available; `--playwright-module <absolute-module-path>` and `--browser-executable <browser-path>` support bundled installations, and `--node <node-path>` selects Node. Missing dependencies fail the requested check explicitly. Without `--check-browser`, the report says `not_run`. Checks use an isolated browser and temporary localhost server, so test responses do not touch the user's drafts. Network writes are blocked during QA; AI feedback endpoints and external Canvas submission are never exercised.

Automated QA also blocks external reads. Locally packaged images are checked; remote image loading is marked for manual review. Exit status is `0` for passing requested checks (or rendering without requesting checks), `1` for failure, and `2` for partially checked delivery. `preview.json` distinguishes rendering-only `not_run` from a browser pass. Enlarged-text checks double the base text size at 320px; manual review should also inspect actual browser zoom, text within illustrations, and any delivery-specific controls.

The checker covers loaded images and text alternatives, heading order, desktop/mobile overflow, enlarged text, visible control names, and guided-response saving, reloading, copying, fallback, choice feedback, and selected keyboard/focus behavior. It captures screenshots for review. AI-activity engine previews are explicitly unsupported by this command; use their delivery-specific workflow. A rendered page or passing automation is not a completed editorial review: inspect the screenshots and full pages, answer the adult-learner questions in the review skill, and record untested interactions and limitations in the authoring record.
