---
type: page
title: "Writing A Useful Codex Request"
slug: codex-builder-tutorial-writing-requests
sprint: 5
week: 10
module: "Using This Codex Course Builder"
position: 16
points: null
submission_type: none
publish: true
---

# Writing A Useful Codex Request

A useful Codex request tells the assistant what to build, where to put it, what source material to use, and what boundaries to respect.

You can write the request in normal language. You do not need to name the exact skill unless you already know it.

## Choose the build size

Use a whole-course request when you have a course spec and want Codex to draft every sprint:

```text
Draft course2 from context/course-specs/course2-ai-implementation.md.
```

Use a module request when you have one sprint or Canvas module to build:

```text
Draft course2 sprint 1 from context/module-specs/course2-sprint-1-stakeholder-framing.md.
```

Use a smaller artifact request when you only need one page, assignment, quiz, discussion, or module header.

If you are unsure, say what you are trying to produce and ask Codex to recommend the build size before writing files.

## Include the target and source

Name the course, sprint, and module title if you know them:

```text
course2 sprint 1, module title "Stakeholder Framing"
```

Tell Codex where the source context lives:

```text
Use context/module-specs/course2-sprint-1-stakeholder-framing.md as the source.
```

If the source is not in a file, paste the context into the request.

Source context does not need to be polished. It can be a short brief, meeting notes, an outline, or a module spec. It does need to explain the purpose, audience, required ideas, and any constraints Codex should follow.

## Include the artifact list

Tell Codex what Canvas items you want:

```text
Include a module header, three Canvas pages, a quiz, and a discussion board.
```

If points matter, say so:

```text
Make the quiz worth 5 points and the discussion worth 10 points.
```

## Include the audience and purpose

Name who the content is for and what they should be able to do:

```text
The audience is coworkers who build course materials. The purpose is to teach them how to prepare a course or module request, review drafts, and approve Canvas pushes only when ready.
```

## Include boundaries

Clear boundaries prevent accidental publication or unrelated edits:

```text
Generate Markdown only. Do not push to Canvas. Do not edit manifests. Validate the files and report the results.
```

For your first request, include `stop before Canvas` even if you think the draft will be ready. That keeps publication as a separate human decision.

## A strong request

```text
Draft a complete module for course1 sprint 5 called "Using This Codex Course Builder." The audience is coworkers who build course materials. Use the repo tutorial docs as source material, especially README.md, README-BUILDER.md, and context/module-specs/README.md. Include a module header, three pages explaining how to start Codex, how to write a course or module request, and how to review before Canvas. Add a 5-question quiz and a discussion where participants post one build prompt they would use. Generate Markdown only, validate it, and stop before Canvas.
```
