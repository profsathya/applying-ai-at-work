---
type: assignment
title: "Workflow Extension Proposal"
slug: workflow-extension-proposal
artifact_id: course3-sprints-sprint-3-workflow-extension-proposal
sprint: 3
week: 4
module: "Module 4: Verification, Maintenance, and Extension"
position: 6
points: 25
submission_type: text_entry
publish: false
rubric:
  - description: "Proposal names a real workflow problem and the current repo surface it affects"
    points: 5
  - description: "Proposal chooses the right ownership layer and explains why"
    points: 6
  - description: "Proposal defines read scope, write scope, Canvas side effects, and approval requirements"
    points: 6
  - description: "Proposal includes validation, rollback, and stop conditions"
    points: 5
  - description: "Proposal uses plain language that a technical or non-technical maintainer can follow"
    points: 3
---

# Workflow Extension Proposal

## Purpose

Propose one small extension to this repository's agentic course workflow.

## Scenario

You have used the repo enough to see one repeated pain point. Your job is to propose a narrow improvement that keeps the existing safety model intact.

The extension should solve a real operator problem. Keep it narrow enough that a maintainer could review it without redesigning the whole system.

## Your proposal

Write 600-900 words with these sections:

**1. Problem**

Describe the workflow problem. Who experiences it, when does it happen, and what risk or friction does it create?

Examples:

- Operators need a faster pre-publish checklist for one sprint.
- Reviewers need a clear way to detect unpublished local artifacts.
- Maintainers need a safer summary before destructive Canvas removal.
- Course drafters need a quality review pass before validation.

**2. Proposed extension**

Name the extension and explain what it would do.

Choose the ownership layer:

- Documentation.
- `.agents/skills`.
- `.codex/agents`.
- `canvas_sync`.
- `schema/frontmatter.schema.json`.

Explain why that layer fits.

**3. Boundaries**

Define:

- What it may read.
- What it may write.
- Whether it can call Canvas.
- Whether it can use paid APIs.
- What human approval it requires.

Be specific with paths. For example, name `course3/manifests/production.json`, `.agents/skills`, `.codex/agents`, or `canvas_sync/schema.py` if your proposal touches them.

**4. Verification**

State how you would prove the extension worked. Include local validation, expected output, and at least one manual review step.

**5. Rollback and stop conditions**

Name how a maintainer could undo the change or stop before harm occurs. Include at least two stop conditions, such as failed validation, unexpected write scope, wrong manifest, possible secret exposure, or an unapproved Canvas write.

## Submission

Paste your proposal into the assignment text box. Do not include real secrets, API tokens, or private participant data.

## Submission Format

Text entry.

## Expected Evidence Of Success

Your proposal should name a real repo surface, choose one ownership layer, define read and write scope, describe Canvas side effects or lack of side effects, and include validation plus stop conditions.

## Extension Option For Technical Users

Include a rough implementation outline with file paths and one test or validation command. Do not implement the extension as part of this assignment.

## Simplified Path For Non-Technical Users

Focus on the problem, the user request that should trigger the workflow, the safety boundary, and how a maintainer would know whether the improvement worked.

## Suggested Codex Prompt Starter

```text
Help me draft a narrow workflow extension proposal for this repo. Inspect the existing skills, agents, scripts, and schemas first. Recommend whether the extension belongs in documentation, .agents/skills, .codex/agents, canvas_sync, or schema. Do not edit files.
```

## Review Checklist Before Accepting Codex Changes

- The proposed change is narrow and repo-grounded.
- The ownership layer matches the risk and behavior.
- The proposal names what may be read and written.
- Canvas writes, paid API use, and secrets are handled explicitly.
- Validation, rollback, and stop conditions are included.
