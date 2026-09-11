---
name: reviewing-course-text
description: Review substantive course drafts, revisions, and curated homepage copy for teachability and alignment, including relevant neighboring material. Return scoped findings and evidence for a parent review record. For exact-wording requests, recommend without rewriting; skip date-only, inspection, reconcile, and sync mechanics.
metadata:
  local_revision: "5"
---

# Reviewing Course Text

Follow [the authoring contract](../../../docs/AUTHORING.md). Review the experience the supplied design intends. Use the relevant writing skills for their principles rather than inventing another style system.

## Read in context

Read the actual changed text and the material it depends on or leads into. For a new sprint, examine the assembled sequence; for one artifact, read the relevant prerequisite, follow-on task, and curated homepage copy if available. Inspect referenced response prompts or rubric fields when they affect what participants must do. State which dependencies were unavailable rather than claiming to have reviewed them.

A sentence-purpose map can reveal a tangled page: identify what each paragraph teaches, asks, or connects. Use it when helpful, not as mandatory paperwork. Compare material with a similar instructional function, not a universal word-count target.

## Final editorial pass

1. **Entry and first action:** Can the participant understand why they are here and take the first meaningful action with the prerequisites and directions provided?
2. **Agreement:** Do examples, non-examples, tasks, response prompts, submission expectations, and success criteria describe the same work? Are necessary instructions at their point of use?
3. **Sequence:** Does later work use something actually introduced or produced earlier? Does returning to an idea add practice, retrieval, or a new perspective rather than duplicate framing?
4. **Language and explanation:** Are terms introduced before use and causal connections explained? Does an example resolve a consequential ambiguity? Preserve useful vocabulary and complete reasoning.
5. **AI and judgment:** Does AI support the intended thinking, with evidence checking and the consequential judgment left to the participant? Does it preserve real stakeholder work?
6. **Reading effort and credibility:** Remove needless repetition, unsupported promises, generic reassurance, and unnecessary warnings. Check goals and payoff language against [writing-learning-goals](../writing-learning-goals/SKILL.md), including when they appear in body copy. Preserve detail that enables action or explains meaning.

For example, if a page says "choose one delay" but the rubric scores three proposed automations, identify the assessment mismatch. If a later task deliberately revisits the same delay with new stakeholder evidence, retain that return. Repetition alone is not a defect.

## Review the assembled asynchronous experience

Trace a participant through the rendered sequence: prerequisites, essential teaching, useful example, action, feedback or self-check, and submission. Check across pages and across lesson text, task prompts, criteria, and shared controls for repeated explanations or procedures. Required teaching must be available at its point of use, not presented as optional help. Check both an initial attempt and a return to saved work.

For page authoring or presentation revisions, inspect the complete rendered page at desktop and mobile widths. Check that the opening, headings, spacing, and selective grouping reveal the learning sequence; the next action and its response should be easy to locate. Review whether each visual clarifies a process, comparison, or decision and whether captions repeat it unnecessarily. Check image text alternatives, attribution and reuse evidence, and meaning without color.

Check heading order, keyboard operation of interactive controls, visible focus, control labels, and text enlargement. Inspect tables and diagrams for clipping or horizontal page overflow; confirm mobile order preserves meaning. When controls change, exercise saved work and copying as applicable. Use the existing renderer and [implementation reference](../../../docs/AUTHORING_PRESENTATION.md); a Markdown-only worker returns layout findings and hands rendered checks to the coordinating parent. If rendering or browser inspection is unavailable, report that limitation instead of claiming a visual pass. These checks do not establish accessibility certification or participant learning.

Use the reference's module-preview command to save a baseline before revision and generate the current pages, comparison, and browser evidence afterward. For new modules, omit the baseline. Read the actual results: skipped or failed checks are not passes. Automation supports the editorial review; the reviewer still inspects the complete rendered module and records concrete answers to these adult-learner questions: Can I see the next meaningful action? Does each section help me act or understand? Am I rereading directions? Does the visual help, with its essential meaning available as text? Can I leave and resume with my work and place clear? Resolve in-scope issues and regenerate affected evidence after changes. Report unobserved participant engagement separately.

For a verbosity revision, record before/after body, prompt, and criteria counts separately, alongside concrete examples of removed duplication and retained support. Counts reveal burden; they do not establish learning quality or screen visibility. Consider reading, practice, observation over elapsed days, and submission effort together; do not invent a time budget or cut required practice to meet a word target. Report participant testing separately from editorial judgment and software checks.

## Resolve and report within scope

Make routine, authorized improvements to the target, then review the final version. Preserve artifact identity, source wording protected by the request, and useful unconventional structures. If exact wording must be retained, return recommendations with locations and rationale without rewriting it. Do not silently edit a neighboring artifact to resolve a cross-artifact issue; report the issue when it lies outside scope.

Classify findings as resolved, deliberately deferred with a reason, or needing a human design decision. A missing assessment decision is different from a sentence the agent can clarify. Do not add an approval stage for ordinary copy improvements.

Return the source/file list, skills actually read and revisions, goal-to-evidence relationship, decisions, findings, and observed validation results. The parent workflow saves the record using [references/review-record.md](references/review-record.md), after final edits and validation. Restricted workers return this information in their response and write only their assigned output. A review-only request may produce recommendations without a content mutation; label that status explicitly.

## Keep judgments separate from measurements

"The first action appears clear because the prior artifact is named" is an agent assessment. A schema command's exit code is a tool observation. Neither is evidence of learning effectiveness or human approval.

Do not infer browser screens, visible text, or action readiness from raw Markdown word counts. Do not treat a utility control as a learning action, absent criteria as passing, or collapsed content as visibly read. Quote only text actually inspected. Do not fabricate a lint score, learner test, or successful command.

Verify participant and stakeholder quotations against their original source and preserve the wording exactly. Mark any authorized omissions or anonymization visibly, such as with ellipses or brackets. Keep paraphrases outside quotation marks; do not polish a response and present it as a verbatim quote. Clearly label invented teaching examples as illustrative.

## Provenance and local adaptation

- Origin: Common Curriculum [`skills/reviewing-course-text/SKILL.md`](https://github.com/profsathya/Common-Curriculum/blob/81a051324df61c41af464a0220f8085627729ad9/skills/reviewing-course-text/SKILL.md).
- Reviewed upstream commit: `81a051324df61c41af464a0220f8085627729ad9` (`81a0513`). Local revision: `5`.
- Adaptation: qualitative, scoped review of local Markdown and curated metadata with a parent-owned evidence record. Exclude HTML/slide workflows, course-specific policies, Canvas IDs, private dependencies, and `scripts/review_student_page.py`, whose visibility and first-action heuristics do not establish instructional quality.
- This skill is self-contained in this repo. Future upstream changes require explicit review before local adoption; increment `metadata.local_revision` for instruction changes.

- Local revision 3: require an assembled asynchronous reading/action review, including duplication across delivery components and honest before/after measurements.

- Local revision 4: inspect rendered hierarchy, visual usefulness, mobile reading order, accessibility behaviors, and image attribution; retain scoped worker handoffs and truthful validation limits.
- Local revision 5: reusable module previews and baseline comparison, explicit adult-learner review, and honest interpretation of automated, skipped, and manual checks; upstream pin unchanged.
