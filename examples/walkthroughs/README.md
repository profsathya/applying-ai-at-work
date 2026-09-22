# Canvas walk-through examples

`stakeholder-map-local-dry-run.md` is a local design example, not a Canvas item. Its source is `course1/sprints/sprint-15/stakeholder-map-v3.md` and the linked [Stakeholder Map template](https://docs.google.com/document/d/1Z0Sg2_2lnQNiryTOpzerdhIovuE4a4-AGivkxR2bRP4/edit). The source assignment is worth 35 points and accepts a file upload. The template supplies four stakeholder tables with seven answer and evidence-status rows, two or three assumption blocks, a first contact and backup, and sections continued later in the sprint.

This example keeps the independent-work rule, so no AI feedback endpoint is configured. It uses table-based response groups, browser saving, copy and text downloads, and a client-generated Word document that retains the table structure and later-use sections. It is deliberately outside `course1/sprints/`, has `publish: false`, and is never picked up by the Canvas publisher.

To render this example locally, parse its frontmatter and body with `canvas_sync.schema.parse_frontmatter`, then call `canvas_sync.hosted_html.render_artifact_document` using the course 1 manifest and `artifact_hosted_info`. Serve the resulting HTML with a local HTTP server before opening it in a browser; opening the file as source does not show the interactive page.
