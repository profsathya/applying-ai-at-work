# Module Context Specs

Module context specs are optional build inputs for the `build-sprint` skill. Use them when a human wants to describe a whole sprint or Canvas module without editing the durable course design docs.

You can provide a spec in either form:

- Paste the spec directly into a Codex chat request.
- Save a Markdown file in this folder and ask Codex to build from that path.

Specs are guidance, not schema-validated artifacts. Codex should treat explicit instructions in the spec as higher priority than inferred patterns from existing sprints, as long as they do not violate repo rules or Canvas schema constraints.

## File Naming

Use a descriptive Markdown filename:

```text
context/module-specs/course2-sprint-1-stakeholder-framing.md
```

If a user asks `build-sprint` for a course and sprint without naming a file, Codex may auto-select a spec when exactly one file matches:

```text
context/module-specs/<course>-sprint-<n>-*.md
```

## Recommended Structure

```md
# Module Context Spec: <Module Title>

## Target
- Course: <local course key>
- Sprint: <non-negative integer>
- Canvas module title: <title>
- Working title or theme: <short label>

## Purpose
Describe what participants should be able to do by the end of this module.

## Audience And Situation
Name what the participants already know, what workplace context they bring, and what constraints matter.

## Required Artifacts
List the desired Canvas artifacts in module order. Include type, title, points, submission type, and any special requirements.

Example:
1. module_header: Sprint 2: Stakeholder Framing, no points
2. page: Sprint 2 Briefing, no points
3. assignment: Stakeholder Map Draft, 20 points, text_entry
4. quiz: Stakeholder Framing Check, 5 points, online_quiz, 4-6 questions
5. discussion: Peer Exchange, 10 points, discussion_topic

## Required Ideas
- Idea, concept, or behavior that must appear.

## Activities Or Prompts
Include any specific instructions, quiz questions, discussion prompts, rubric criteria, or workplace tasks.

## Constraints
- Due dates, if any, must be full ISO 8601 timestamps with timezone.
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
Build course2 sprint 1 as "Stakeholder Framing."
Goal: participants should map real stakeholders, interview one person affected by the problem, and revise their problem frame.
Artifacts: module header, briefing page, stakeholder map assignment, interview notes assignment, 5-question quiz, peer discussion.
Constraints: no due dates, no file uploads, write for working professionals, use real workplace stakeholders only.
```
