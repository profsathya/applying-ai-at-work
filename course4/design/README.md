# Science of Computing Design Notes

Use this file for local course design decisions that should inform drafting.

## Course Identity

- Local course key: course4
- Course title: Science of Computing
- Course code: 201
- Term or cohort:
- Canvas course ID: 182
- Section count: 3

## Course Purpose

Science of Computing is a 201-level technical foundations course. It prepares participants to read, reason about, adapt, and debug LLM-generated code with enough programming fluency to succeed in 202A.

The course is not a replacement for a full Python programming course. It should cover major programming constructs and development practices at the level needed for code comprehension, AI-assisted development judgment, and confidence with small implementation tasks.

## Audience And Situation

Participants need enough programming knowledge to follow examples and collaborate with AI tools. They may be comfortable using LLMs to produce code but less comfortable explaining what the code does, where it might fail, or how to change it safely.

The design should avoid syntax drills. CodeChecks should be approachable confidence checks. AI use is allowed, but discouraged for these checks because the point is to help participants express their own coding skill.

## Course Arc

The course moves through three sections:

| Section | Focus | Course role |
|---|---|---|
| 1 | Code, abstraction, functions, basic operations, errors, CLI and IDE access | Build the first layer of code reading and small-program confidence. |
| 2 | Objects, collections, control flow, files, sets, support ticket systems, testing | Help participants model real-world work in code and protect behavior with tests. |
| 3 | Git, libraries, virtual environments, project structure, debugging, documentation, pull requests | Bridge participants into project development and 202A implementation workflows. |

Each section should include one LLM analysis lab using fixed starter code, one reliability thread, one set of simple CodeChecks, one applied project, and one quiz focused on reading and understanding code.

## Assessment Strategy

Assessments should measure practical code comprehension and project readiness.

- CodeChecks: Small, direct exercises for constructs covered in the section. They should be solvable without AI.
- LLM analysis labs: Participants inspect, refine, debug, and explain common code samples.
- Projects: Participants build or extend constrained tools using starter assets, datasets, or repositories.
- Quizzes: Participants read snippets, predict behavior, identify errors, and explain design choices.
- Community or peer work: Include only when it supports relatedness and confidence, such as optional hidden message exchange or debugging discoveries.

## Constraints

- Keep framework labels from CST-395 mostly internal unless a later design decision makes them participant-facing.
- Use participant-facing language consistently.
- Do not develop modules or artifact Markdown until explicitly requested.
- Do not manually write Canvas IDs into artifact frontmatter.
- Keep all future artifacts Canvas-native Markdown.
- Include sets as a required programming concept.
- Keep 202A as the next-course handoff: this course supplies conceptual and practical readiness, while 202A should carry deeper implementation and workflow development.

## Internal Design Foundations

Use these ideas as design pressure, not as a vocabulary list for participants:

- Superagency and human value proposition.
- Self-directed learner, adaptive learner, and integrated problem solver.
- Thinking as reading, writing, talking, and listening.
- Meta-habits: slow down, know yourself, and take the lead.
- AI partnership: 3Cs, creating and consuming, and DIKW.
- Self-determination theory: autonomy, competence, and relatedness.
- Techniques to habits to outcomes.

## Open Design Decisions

- Confirm whether the public course code is 201 or CST-201.
- Confirm whether the three sections are exactly three weeks or a compressed foundation before 202A.
- Select the standard IDE and Copilot setup path.
- Choose final starter code for calculator, support ticket system, and Section 3 app.
- Decide whether Section 3 should introduce language model development, AI pipelines, or agent orchestration before 202A.
- Select and place the classifier dataset.
