# Facilitator Review Guide

## What To Review In Learner Work

Look for evidence that the learner can:

- Open or connect the repo in Codex app or IDE.
- Ask Codex to inspect before acting.
- Scope the task with course, sprint, artifact, file, or workflow boundaries.
- Ask Codex to select a local skill or subagent safely.
- Separate local drafting from Canvas publishing.
- Review diffs and changed files.
- Verify outputs with schema validation or a documented non-technical review path.
- Escalate Canvas credentials, drift, push, reconcile, or removal decisions.

## Minimal Passing Evidence

- A prompt that includes goal, context, constraints, and done criteria.
- A short route explanation naming the relevant skill or subagent.
- A local-only safety boundary unless Canvas push was explicitly authorized.
- A changed-file or reviewed-file list.
- A verification checklist.

## Strong Evidence

- Learner identifies a mismatch or ambiguity and asks Codex to stop before acting.
- Learner distinguishes schema validation from instructional quality review.
- Learner can explain why `canvas_sync/push.py`, `pull.py`, `inspect_canvas.py`, and `remove.py` should remain deterministic script boundaries.
- Learner chooses not to publish because review or drift status is incomplete.
