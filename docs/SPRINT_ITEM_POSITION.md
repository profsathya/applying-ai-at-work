# Sprint item position

Hosted course item headings display `Item 3 of 6 · 3 items remaining`. This is
position in the published sprint, not completion tracking. Titles and navigation
stay unchanged. The text wraps naturally on narrow screens.

Production publication reads Canvas modules and module items after publishing and
ordering. Only published items in published modules count. Subheaders, historic
modules hidden by homepage metadata, and not-ready scheduled modules are excluded.
Published optional pages, assignments, quizzes, discussions, and external links
count. Sparse Canvas positions are enumerated consecutively. Module membership,
not the source directory, determines a walkthrough's sprint.

Offline rendering previews intended source publication: module membership,
`position`, `publish`, and `walkthrough_after` determine the order. This preview
is not evidence of a live release. Production never falls back to guessed source
positions when Canvas reads fail.

Partial publication refreshes the annotation on existing hosted sibling pages
without rendering their potentially unpublished Markdown bodies. Failed artifact
body restoration also refreshes annotations against final live membership.
A subsequent publication refreshes counts after additions, removals, or reordering;
Canvas-only edits require a publication refresh to reach static hosted pages.

Both batch publication and direct `push.py` publication use fresh Canvas sequence
reads. Direct pushes obtain the sequence before rendering; batch publication
preserves a complete pre-run hosted baseline. A failed course-wide render or
sequence read restores that baseline and blocks the hosted commit, even after
successful Canvas writes or alongside another successful course. Canvas state
still records actual remote writes; existing workflow reconciliation handles
content-only state when the hosted deployment is skipped. Rendering failures
also remove newly generated files and restore sibling annotations and assets.

Validation: `python -m unittest tests.test_item_sequence tests.test_hosted_html tests.test_publish_changed`.
