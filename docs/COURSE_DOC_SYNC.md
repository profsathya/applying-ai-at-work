# Course 180 Google Doc sync

The implementation lives in Applying AI at Work. It adapts the Common Curriculum builder and Apps Script pattern; it does not invoke an upstream sync workflow. The sole upstream content dependency is the canonical shared Dojo Core text.

## Inputs and behavior

`canvas_sync/course_docs/sync.py` consumes the publisher's explicit `course-context-release.json`, schema version 1, containing `release_id`, `generated_at`, and ordered `pages` with `path`, `title`, HTTPS `source_url`, and participant-facing Markdown `content`. It never crawls the hosted site. An empty page list removes all previously exported course content. The publisher is responsible for selecting only published, visible content and withholding the inventory on partial failure.

Course and Dojo are independent sections. The Course tab contains exactly the release inventory. The Dojo tab contains only the canonical Core from `https://profsathya.github.io/Common-Curriculum/common/dojo/dojo-core.txt`. The payload includes a section content digest and source metadata. No participant responses or conversations are accepted as inputs.

The native publication workflow must gate sending on successful Canvas publication and hosted deployment of the corresponding content. A local preview or payload build alone is not evidence of publication. A Dojo-only job must not rebuild the Course tab.

## One-time administrator setup

Provisioning status (September 16, 2026): the [course document](https://docs.google.com/document/d/1V8L_oJVFwYVtaJmJoVBj4QSSGQXERdjRfhm4NlryAjE/edit) exists with Dojo and Course tabs and link-based viewer access. Its initial snapshot contains the canonical Core and 25 verified published artifacts; both tabs passed exact text readback. This initial fill used the Docs connector, not the automatic workflow. The document and participant setup page explicitly say automatic refresh is not enabled.

The [native Apps Script project](https://script.google.com/home/projects/1U4a1C-fv9eJBy307fyGaNYf9gOsRJbwjzpQLJk4wgUsrbdnfr-9iTKDT/edit) has the repository receiver source saved and `COURSE_DOC_IDS` configured. It has not been authorized or deployed. No sync credential has been created or exposed. The production document is in the currently connected Google account; the receiver must execute under an account with edit access.

1. Create a document named **CIS 501: Reframing Problems with AI — Dojo and Course Context** with tabs named **Dojo** and **Course**. Share participant viewer access according to course policy.
2. Create a standalone Apps Script project and install `scripts/apps-script/CourseDocSync.gs`. Use a dedicated receiver for this repository so generation ordering does not mix repositories.
3. Create a strong random shared token in your password manager and enter it directly as script property `COURSE_DOC_SYNC_TOKEN` and native repository secret of the same name. Do not send it in chat. Set `COURSE_DOC_IDS` to a JSON object mapping `course1` to the document ID. Keep tokens out of source files, payload artifacts, and logs.
4. Authorize and deploy the script as a web app executing as its owner, accessible to Anyone so GitHub Actions can POST; the configured shared token authenticates requests. Do this only after setting the token. Set native repository secret `COURSE_DOC_SYNC_URL` to the deployment's `/exec` URL. The receiver account needs document editing permission. Google authorization may grant document access beyond this course document; review the permissions before accepting.
5. Run against a test document first, verify both tabs and version markers, then configure the production document. Enable the native workflow only once provisioning is complete.

Before enabling production, perform a controlled test publication and confirm automatic workflow initiation, exact hosted commit success, tab readback, a second changed passage, and rejection of an older generation. Then remove the temporary snapshot-status sentence from the setup page. A protected production publication still requires the repository's authorization process. None of these live automation checks are implied by local tests.

## Delivery and verification

The CLI accepts `--release`, `--section course|dojo|all`, `--generation`, `--repository`, `--commit-sha`, and `--output`. Without `--send` it creates only a token-free payload. With `--send` it posts to the configured Apps Script endpoint and requires an exact generation and content-digest acknowledgement for every requested tab. Token values are injected in memory, never saved in the payload artifact.

The receiver serializes requests with a script lock and tracks a high-water mark per document and tab. Older generations and conflicting payloads at the same generation fail before any write. Same-generation identical retries are accepted. All target tabs are resolved first; bodies are backed up in memory and restoration is attempted on a rendering/save failure. Google Docs is not transactional: persistent service outages can also prevent restoration, so an error always requires readback before declaring recovery. Version properties advance only after successful document saving.

The native `sync-course-context.yml` workflow serializes jobs, checks out current main after acquiring the job slot, and uses monotonic GitHub run IDs. Reruns retain their original generation. It selects the newest successful same-repository main publication with a release artifact (skipping other-course, hosted-only, and pre-feature runs), validates its source commit, downloads only its exact root inventory, and waits for a successful Pages deployment of its hosted commit. Delayed callbacks therefore cannot select older publication content. A daily schedule refreshes only the Core; publication completion refreshes only Course, and manual retry refreshes both sections. Manual dispatch on historical branches is rejected. Native `config/course-docs.json` remains disabled until provisioning; its public document ID is configuration, not a secret.

Inspect the document's visible version marker and representative content after deployment. The receiver reopens the saved document and hashes normalized rendered text; the client checks that digest and the exact configured document ID in addition to section metadata. A real platform retrieval test is separate. A current Google Doc does not guarantee that a participant's model retrieved it.

## Checks

Run `.venv/bin/python -m unittest tests.test_course_docs` and `node tests/course_docs_receiver.cjs`. These cover explicit inventory, removal, core-only section isolation, malformed inventories, strict acknowledgement, digest stability, stale requests, conflicting retries, and independent section generations. They do not claim a live Google Docs or AI-platform test.
