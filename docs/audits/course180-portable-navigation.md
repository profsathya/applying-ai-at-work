# Course 180 portable hosted navigation

Source base: 0cd5a8a38dc9f6856a3025f641c00ab45bad9659 (includes Sprint 5 PR210).
Hosted base: 6dd1ced381be4c576326a903cf40661e5fdff4a4.

The shared hosted pages remain in their existing iframes. Opt-in
`hosted_html.native_canvas_navigation` removes generated Canvas-ID shortcuts,
custom progress indicators/client, and progress-token transport. Useful authored
references, hosted browsing, AI activity configuration, draft controls, downloads,
and submission instructions remain. In Canvas, a short notice directs participants
to native Modules for completion and to the enclosing activity for submission.
There is no attempt to infer destination IDs from a cross-origin iframe referrer.

No Canvas requirements or objects are changed. Read-only instructional metadata
confirmed 11 must_view, 26 must_submit, one must_contribute, and one item without
a requirement among 39 published logical items. Orientation alone requires
sequential progress; no published module has prerequisites. Existing optionality,
points, rubrics, submissions and publication states remain authoritative.
The old progress-map JSON can remain as an unused compatibility artifact; the
portable hosted UI neither fetches the service nor consumes that map.

## Reviewed delivery scope

52 existing HTML files: 39 published item pages, two required AI activity shells,
home/index/modules, and eight reachable sprint directories. No unpublished Sprint
5 placeholder is included. Seven orientation pages regenerate the ten sequential
hyperlinks already removed by PR202 and acquire the shared styles already merged
in PR208. Remaining pages receive only the navigation/progress presentation pass,
so unrelated instructional releases are not introduced.

A text comparison of all 52 files found only the native-Canvas notice, generated
submission shortcut/progress-label removals, and punctuation spacing caused by
removing the ten hyperlink tags. AI JSON and shared engine files are unchanged.

## Validation

- Schema and repository link audit pass.
- Full suite: 356 tests, one skipped (before final token/AI-shortcut refinements);
  targeted native-navigation/style tests pass after those refinements.
- 104 browser views: 52 pages at 1280px and 390px; no horizontal overflow,
  JavaScript errors, CTI anchors, visible Canvas back-links or custom progress
  requests. Standalone web navigation remains available.
- Walkthrough responses persist on reload; DOCX downloads are valid ZIP packages;
  homepage disclosure works by keyboard. No AI provider call or actual Canvas
  submission was made.

Publish the reviewed HTML through Common-Curriculum GitOps. Existing iframe URLs
stay unchanged, so this scope requires no Canvas API write. Source merges must
avoid triggering an unrelated broad Canvas publish. Keep experimental work separate
from deliberate updates to these shared URLs: the official De Anza course will
consume the same hosted content. This change adds no hosting architecture.
