# Sprint Templates

## sprint-template.html

A reusable HTML shell for sprint pages, adapted from CTI's existing curriculum infrastructure. It captures the visual design intent for sprint delivery:

- A sticky week counter showing progress through the sprint
- Journey navigation pills for moving between sprints
- A sprint header with theme color and metadata pills
- Collapsible sprint details (outcomes, assessment, weekly breakdown)
- A content zone for weekly briefings
- A footer

The template is provided as a static shell with placeholder content in `[BRACKETS]`. To make it dynamic, the team will need to decide whether to bring over CTI's existing JavaScript rendering system (config file + components.js) or build a different delivery approach.

## Customizing for each sprint

For each sprint, customize the following:

- **Theme color CSS variables** (`--theme-primary`, `--theme-dark`, `--theme-light`) to visually distinguish sprints
- **Sprint title and theme statement** in the header
- **Metadata pills** — weeks covered, scaffolding level, and stakeholder type
- **Sprint outcomes list** in the collapsible details section
- **Weekly briefing content** in the content zone

## Note for working professional audience

The "stakeholder" metadata field should describe the type of stakeholder relevant to that sprint (e.g., peer, manager, customer, cross-functional partner) — not the closeness of the stakeholder relationship as used in undergraduate courses. Working professionals engage different stakeholder types depending on their chosen problem and sprint focus.
