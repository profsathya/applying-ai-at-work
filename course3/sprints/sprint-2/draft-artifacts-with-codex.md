---
type: page
title: "Draft Artifacts with Codex"
slug: draft-artifacts-with-codex
artifact_id: course3-sprints-sprint-2-draft-artifacts-with-codex
sprint: 2
week: 3
module: "Module 3: Building and Publishing Content with Codex and Agents"
position: 2
points: null
submission_type: none
publish: false
---

# Draft Artifacts with Codex

Codex drafts best when the request includes real course context, an explicit target, and a narrow file scope.

You do not need to name every internal tool. The repo guidance tells Codex how to route common requests. Still, you should understand the main drafting paths so you can review the result.

## Main drafting paths

Use a full course request when you have one course-level context source:

```text
Draft course3 from this pasted course plan. Write only under course3/sprints/sprint-0 through course3/sprints/sprint-3. Validate generated artifacts. Do not push to Canvas.
```

The matching workflow is:

```text
.agents/skills/build-course/SKILL.md
```

Use a module request when you have one sprint or module to build:

```text
Draft course3 sprint 2 from this module plan. Write only under course3/sprints/sprint-2. Validate generated artifacts. Do not push to Canvas.
```

The matching workflow is:

```text
.agents/skills/build-sprint/SKILL.md
```

Use an add-artifact request when you need one page, assignment, discussion, quiz, or module header:

```text
Add one page to course3 sprint 1 called "Setup Troubleshooting". Write only the new artifact and validate it. Do not push to Canvas.
```

The matching workflow is:

```text
.agents/skills/add-artifact/SKILL.md
```

## What good generated artifacts include

Every artifact should include valid frontmatter and Canvas-native Markdown.

Check for:

- Correct `type`.
- Correct `slug`.
- Correct `sprint`, `week`, `module`, and `position`.
- `publish: false` for staged local training content until review.
- No due date unless a full Canvas-compatible timestamp was supplied.
- No Canvas IDs in frontmatter.
- No HTML, scripts, iframes, inline styles, or external embeds.
- Clear second-person instructions for working professionals.

## What you review as the human

You are not just proofreading. You are checking whether the artifact is useful, safe, and placed correctly.

Ask:

1. Does this artifact teach or assess the intended workflow?
2. Does it use the actual repo paths?
3. Does it preserve the Canvas write boundary?
4. Does it avoid secrets and internal-only assumptions?
5. Does it validate locally?

If the answer is no, ask Codex to revise the specific file before publishing.
