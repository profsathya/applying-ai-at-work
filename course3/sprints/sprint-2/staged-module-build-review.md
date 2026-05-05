---
type: assignment
title: "Staged Module Build Review"
slug: staged-module-build-review
sprint: 2
week: 3
module: "Module 3: Building and Publishing Content with Codex and Agents"
position: 6
points: 25
submission_type: text_entry
publish: false
rubric:
  - description: "Review identifies the intended skill or agent route and explains why it fits"
    points: 5
  - description: "Review checks file paths, artifact types, positions, publish flags, and frontmatter safety"
    points: 7
  - description: "Review includes validation commands or validation results for the staged artifacts"
    points: 5
  - description: "Review identifies at least two content quality issues or confirms why none are present"
    points: 4
  - description: "Review states a clear publish recommendation with conditions"
    points: 4
---

# Staged Module Build Review

## Purpose

Review a staged module build before it is eligible for Canvas publication.

## Scenario

Codex has generated or revised a set of local Markdown artifacts. You are the human reviewer who must decide whether the work is ready for another revision, ready for validation, ready for Canvas inspection, or ready for a separately approved push.

Use either a real staged module in this repo or a small sample generated for practice. Do not push anything to Canvas for this assignment.

## Your review

Write a review note with these sections:

**1. Build route**

Name the workflow that should have produced the files. Examples:

- `build-course`
- `build-sprint`
- `add-artifact`
- `canvas-author`

If a Codex agent would help, name the agent path, such as `.codex/agents/course-drafter.toml` or `.codex/agents/canvas-author.toml`.

**2. File and frontmatter check**

List each artifact you reviewed. For each one, note:

- File path.
- Artifact type.
- Position.
- Publish flag.
- Whether any Canvas IDs, due dates, or forbidden fields appear in frontmatter.

**3. Validation evidence**

State how validation was run or would be run:

```text
canvas_sync/schema.py --artifact <file>
canvas_sync/schema.py --all
```

If you have actual output, paste the relevant pass or failure result. Do not include secrets or tokens.

**4. Content quality check**

Identify at least two issues to fix, or state that you found no issues and explain what you checked. Look for unclear instructions, unrealistic tasks, missing verification steps, unsafe Canvas write language, or weak rubrics.

**5. Publish recommendation**

End with one of these:

- Ready for human-approved Canvas push.
- Not ready. Revise before validation.
- Not ready. Validation failed.
- Not ready. Canvas state must be inspected first.

Include the condition that would change your recommendation.

## Deliverable

Submit a review note with the five sections above.

## Submission Format

Text entry.

## Expected Evidence Of Success

Your review should include real repo paths, artifact types, positions, publish flags, validation evidence, at least two content quality observations, and a clear publish recommendation.

## Extension Option For Technical Users

Run the artifact validator on the reviewed files and include the pass or failure summary. If you find a validation failure, propose the smallest local fix.

## Simplified Path For Non-Technical Users

Use the Codex app or IDE diff view. Focus on titles, sequence, instructions, point values, Canvas safety language, and whether a participant would know what to do next.

## Suggested Codex Prompt Starter

```text
Review these staged course3 artifacts before any Canvas push. Identify the intended skill or agent route, check frontmatter and file paths, summarize validation status, flag content quality issues, and recommend go or no-go. Do not edit files unless I ask.
```

## Review Checklist Before Accepting Codex Changes

- The reviewed file list matches the intended scope.
- No secret or token appears in content or logs.
- `publish` flags, points, positions, and submission types are intentional.
- Validation passed or failures are clearly documented.
- Canvas was not changed during the review.
