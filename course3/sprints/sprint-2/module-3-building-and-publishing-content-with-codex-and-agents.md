---
type: module_header
title: "Module 3: Building and Publishing Content with Codex and Agents"
slug: module-3-building-and-publishing-content-with-codex-and-agents
sprint: 2
week: 3
module: "Module 3: Building and Publishing Content with Codex and Agents"
position: 1
points: null
submission_type: none
publish: false
---

# Module 3: Building and Publishing Content with Codex and Agents

This module focuses on the content build path.

You will practice turning a human course or module request into local Canvas artifact Markdown, validating the result, reviewing it, and preparing a publish request. You will also learn when to rely on skills, when specialized agents help, and why publishing remains a separate reviewed step.

By the end of this module, you should be able to:

1. Choose between `build-course`, `build-sprint`, `add-artifact`, and `canvas-author`.
2. Explain how `.agents/skills` and `.codex/agents` work together.
3. Review generated artifacts for schema, voice, position, and Canvas safety.
4. Prepare a publish request that uses `canvas_sync/push.py` only after explicit approval.

## Estimated Time

90 to 150 minutes.

## Audience Note

If you are non-technical, focus on clear task prompts, local-only boundaries, and content review. If you are technical, also inspect the frontmatter, validation path, manifest behavior, and push sequence.

## Required Artifacts

Complete these items in order:

1. Draft Artifacts with Codex
2. Use Skills and Agents for Builds
3. Review and Publish Path
4. Content Build Check
5. Staged Module Build Review

## Learning Sequence

Start with local drafting prompts. Then learn how Codex routes work through skills and agents. Next, practice the review and publish decision path. Finish with a staged module review that stops before Canvas.

## Formative Check

Complete `Content Build Check`.

## Applied Task

Complete `Staged Module Build Review`.

## Completion Criteria

You are done when you can ask Codex to draft within a scoped folder, verify which skill or agent route applies, review generated artifacts, and prepare a publish recommendation without pushing.

## Common Misunderstandings

- Naming a skill is optional, but the task still needs clear target, source, scope, and constraints.
- `publish: false` in a local artifact is not the same as Canvas publish state after a push.
- A Canvas push can update or overwrite the targeted live item.
- Subagents help route specialized work, but scripts still own deterministic Canvas side effects.

## Repository-Specific References

- `.agents/skills/build-course/SKILL.md`
- `.agents/skills/build-sprint/SKILL.md`
- `.agents/skills/add-artifact/SKILL.md`
- `.agents/skills/sync/SKILL.md`
- `.codex/agents/course-drafter.toml`
- `.codex/agents/canvas-author.toml`
- `canvas_sync/push.py`
- `schema/frontmatter.schema.json`

## Codex App Or IDE Workflow Notes

Ask Codex to choose the safest local skill or subagent and explain the route before editing. For publishing, name the exact reviewed files and require validation before any Canvas write.
