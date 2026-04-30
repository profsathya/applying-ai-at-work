# Course Context Specs

Course context specs are optional build inputs for the `build-course` skill. Use them when a human wants to describe a whole course in one Markdown file and have Codex generate the sprint/module artifact files locally.

You can provide a spec in either form:

- Paste the spec directly into a Codex chat request.
- Save a Markdown file in this folder and ask Codex to build from that path.

Specs are guidance, not schema-validated artifacts. Codex should treat explicit instructions in the spec as higher priority than inferred patterns from existing sprints, as long as they do not violate repo rules or Canvas schema constraints.

## File Naming

Use a descriptive Markdown filename:

```text
context/course-specs/course2-ai-implementation.md
```

If a user asks `build-course` for a course without naming a file, Codex may auto-select a spec when exactly one file matches:

```text
context/course-specs/<course>-*.md
```

## Recommended Structure

```md
# Course Context Spec: <Course Title>

## Target
- Course: course1 | course2
- Course title:
- Course code:
- Term or delivery context:

## Course Purpose
Describe what participants should be able to do by the end of the course.

## Audience And Situation
Name what participants already know, what workplace context they bring, and what constraints matter.

## Course Arc
Summarize the sequence from orientation through capstone.

## Sprint / Module Map

### Sprint 0: <Orientation Title>
- Week:
- Purpose:
- Required artifacts:

### Sprint 1: <Module Title>
- Weeks:
- Purpose:
- Required artifacts:

### Sprint 2: <Module Title>
- Weeks:
- Purpose:
- Required artifacts:

### Sprint 3: <Module Title>
- Weeks:
- Purpose:
- Required artifacts:

### Sprint 4: <Module Title>
- Weeks:
- Purpose:
- Required artifacts:

### Sprint 5: <Capstone Title>
- Week:
- Purpose:
- Required artifacts:

## Assessment Strategy
Describe points, rubrics, quiz expectations, discussions, stakeholder evidence, and capstone expectations.

## Required Ideas
- Idea, concept, or behavior that must appear.

## Constraints
- Due dates, if any, must be full Canvas-compatible timestamps.
- Name required submission types.
- Name anything to avoid.

## Tone And Voice
Describe the desired tone if it differs from the course default.

## Source Material
Link or summarize any human-provided notes Codex should use.

## Open Questions
List anything Codex should ask before writing.
```

## Minimal Pasted Spec

For quick chat use, this is enough:

```md
Build course2 as a six-module course on applying AI to implementation planning.
Audience: working professionals with real workplace problems.
Arc: orientation, problem selection, stakeholder framing, AI-fit analysis, implementation planning, risk review, capstone.
Artifacts per sprint: module header, briefing page, 2-3 assignments, one short quiz when useful, one peer discussion.
Constraints: no due dates, no file uploads, use real workplace stakeholders, write for professionals, generate Markdown only and stop before Canvas push.
```
