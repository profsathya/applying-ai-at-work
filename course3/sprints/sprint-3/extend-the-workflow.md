---
type: page
title: "Extend the Workflow"
slug: extend-the-workflow
artifact_id: course3-sprints-sprint-3-extend-the-workflow
sprint: 3
week: 4
module: "Module 4: Verification, Maintenance, and Extension"
position: 4
points: null
submission_type: none
publish: false
---

# Extend the Workflow

Good extensions preserve the repo's safety model.

Before adding a new workflow, decide which layer should own it:

1. **Documentation:** update operator guidance when the behavior already exists.
2. **Skill:** add or revise a repeatable Codex workflow in `.agents/skills`.
3. **Agent:** add a role-specific worker in `.codex/agents` when a separate context and role would help.
4. **Script:** add deterministic behavior in `canvas_sync` when the operation needs reliable parsing, validation, API calls, or file transforms.
5. **Schema:** update `schema/frontmatter.schema.json` only when the artifact contract itself needs to change.

Do not put mechanical Canvas operations inside an LLM prompt when a deterministic script should own them.

## Extension checklist

For any proposed extension, define:

- The user request it should handle.
- The current manual workflow it replaces or improves.
- The files or folders it may read.
- The files or folders it may write.
- Whether it can write to Canvas.
- The validation command that proves it worked.
- The stop condition that prevents unsafe writes.

## Examples

Add a new skill when the workflow is mostly orchestration:

```text
Review all unpublished local artifacts in a sprint and produce a validation report.
```

Add a script when the workflow needs deterministic behavior:

```text
Compare manifest-backed local files against Canvas module item positions and produce a machine-readable report.
```

Add an agent when the workflow benefits from a role:

```text
Use a dedicated reviewer agent to inspect drafted artifacts for voice, Canvas safety, and professional relevance.
```

## Keep the boundary visible

Every extension should make side effects obvious.

If it reads Canvas, say so. If it writes local files, say where. If it writes Canvas, require validation and explicit approval. If it can delete Canvas content, require inspection, dry run, and confirmation.

The extension is not done until a maintainer can explain how to use it safely from Codex in the app or IDE.
