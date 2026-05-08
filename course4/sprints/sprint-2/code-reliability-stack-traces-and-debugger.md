---
type: page
title: "Code Reliability: Stack Traces and Debugger"
slug: code-reliability-stack-traces-and-debugger
artifact_id: course4-sprints-sprint-2-code-reliability-stack-traces-and-debugger
sprint: 2
week: 3
module: "Module 3: Project Development, Git, Dependencies, Debugging, and Contribution"
position: 8
points: null
submission_type: none
publish: false
---

# Code Reliability: Stack Traces and Debugger

When a project has multiple files, errors can look intimidating. A stack trace is a map of how the program reached the error.

## Reading A Stack Trace

A stack trace usually tells you:

- Which file was running.
- Which line failed.
- Which functions were called before the failure.
- What type of error occurred.
- What message Python produced.

Read from the bottom for the final error, then move upward to understand the path.

## Example

```text
File "app.py", line 18, in calculate_total
    return price + tax
TypeError: can only concatenate str (not "float") to str
```

This tells you:

- The failure happened in `app.py`.
- The function was `calculate_total`.
- The line tried to add `price` and `tax`.
- One value was a string and one was a float.

The question is not "How do I make the error go away?" The question is "Where did the wrong type enter the program?"

## Breakpoint Debugging

A debugger lets you pause the program and inspect values.

Common debugger moves:

- Set a breakpoint before the suspicious line.
- Run the program.
- Inspect variable values.
- Step to the next line.
- Step into a function.
- Continue until the next breakpoint.

Use the debugger when print statements are not enough or when you need to see how a value changes across files.

## Finding Potential Issues

Look for:

- Inputs that are not validated.
- Files that may be missing.
- Environment variables that may not exist.
- Lists or dictionaries that may be empty.
- User text that is displayed without thought.
- AI-generated code that assumes a library or path exists.

## Clarifying Code

Sometimes reliability improves before you add features.

Good clarification changes include:

- Rename a vague variable.
- Split a long function.
- Add a docstring.
- Add a small test.
- Add a clear error message.
- Remove unused code.

These changes make the project easier for humans and AI tools to reason about.

## Debugging Prompt

If you ask AI for help, use a narrow prompt:

```text
Here is the stack trace and the function involved. Explain what the error means, what line failed, and what variable I should inspect first. Do not rewrite the whole file.
```

The goal is to understand before changing.
