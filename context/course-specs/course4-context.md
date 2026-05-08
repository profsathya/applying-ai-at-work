# Course Context Spec: Science of Computing

## Target
- Course: course4
- Course title: Science of Computing
- Course code: 201
- Term or delivery context: CTI technical foundations course that prepares participants for 202A implementation and workflow work
- Sprint/module count: 3

## Course Purpose
Science of Computing is a three-section technical foundations course. It gives participants enough conceptual programming fluency to read, reason about, adapt, and debug LLM-generated code without positioning the course as a full Python programming replacement.

By the end of the course, participants should be able to follow common Python examples, recognize the major programming constructs in real code, explain how a small program is organized, use AI coding tools with better judgment, and move into 202A with enough confidence to participate in implementation workflows.

## Audience And Situation
Participants are building technical confidence, not preparing for drill-heavy syntax mastery. They may be new to programming, may have used AI tools to generate code without fully understanding the output, and need enough working vocabulary to ask better questions, read examples, and evaluate reliability.

The course should assume participants can learn simple programming concepts directly, but it should not require them to memorize syntax before seeing why a construct matters. AI is allowed, but CodeChecks should be simple enough that participants are encouraged to solve them independently and use them to express their own coding skill.

## Course Arc
The course moves from "what code is" to "how programs represent work" to "how projects are developed and changed."

Section 1 introduces code as a layered representation of decisions and procedures. Participants write and document functions, run programs, use basic input and output, inspect deterministic and non-deterministic code generation, and analyze a pre-built calculator before building a small CLI encryption and decryption tool.

Section 2 introduces richer data modeling and control flow. Participants represent real-world entities with objects, collections, conditions, loops, files, and dictionaries, then analyze and extend a support ticket system. Testing becomes the reliability anchor, and participants apply basic classification work using a provided dataset and starter training code.

Section 3 introduces project development practices. Participants learn project structure, README files, GitHub sync, documentation, dependency management, virtual environments, debugging across a larger codebase, and feature work through a fork and pull request. This section is the bridge into 202A, where implementation workflows become the main focus.

## Sprint / Module Map

### Sprint 0: Code, Abstraction, Functions, and Basic Reliability
- Week or sequence position: Section 1
- Purpose: Build the first layer of programming fluency. Participants should understand what code is, how algorithms and abstraction shape programs, why LLM code must be read critically, how to write and document basic functions, and how errors communicate what went wrong.
- Programming concepts: functions, documentation, basic input and output, math, strings, tuples, command line access, IDE access, basic operations, errors, exceptions, logging, prompts, and Copilot setup.
- LLM analysis anchor: A pre-generated basic calculator. Everyone uses the same sample so the learning target is code reading, refinement, debugging, and reliability instead of prompt luck.
- Project anchor: CLI tool for encryption and decryption using a provided RSA function. Participants receive encrypted samples and keys, then build a CLI interface to reveal hidden text. Optional relatedness extension: a secret message exchange board.
- Required artifacts when modules are later drafted: welcome page, what is code page, algorithms and abstraction page, environment setup page, first function practice, basic operations CodeChecks, LLM analysis lab, code reliability page, project assignment, optional community extension, section quiz focused on reading and understanding code.

### Sprint 1: Data Models, Control Flow, Objects, Files, and Testing
- Week or sequence position: Section 2
- Purpose: Help participants see programs as models of real work. Participants should represent entities and workflows with objects and collections, trace control flow, understand when to use lists, tuples, sets, dictionaries, and files, and use tests to protect behavior.
- Programming concepts: objects, classes, inheritance, lists, loops, conditionals, dictionaries, sets, file reading, UML and workflow diagrams, sqlite3 basics, pytest basics, fixtures, parameterized tests, markers, and user-defined tests.
- LLM analysis anchor: A pre-generated support ticket system. Participants define the system before prompting AI, then refine features such as database persistence, priority rules, spam filtering, tags, and supportee status updates.
- Project anchor: Basic classifier training using a provided dataset and starter training and testing code. Participants decide which feature vectors to include and manually reason about train-test separation.
- Required artifacts when modules are later drafted: welcome page, objects and real-world entities page, collections and control flow page, files and persistence page, intermediate operations CodeChecks, LLM analysis lab, testing and reliability page, classifier project assignment, section quiz.

### Sprint 2: Project Development, Git, Dependencies, Debugging, and Contribution
- Week or sequence position: Section 3
- Purpose: Prepare participants to work inside real projects. Participants should understand project structure, version control, documentation, libraries, virtual environments, debugging tools, stack traces, and how to make a scoped contribution through a fork and pull request.
- Programming concepts: Git, GitHub repositories, project structure, README files, AGENTS.md, libraries, virtual environments, testing in a project, errors across multiple files, breakpoints, debugger use, stack traces, documentation, vulnerability spotting, and project-level requirements.
- LLM analysis anchor: A fixed starter application, likely a Flask app for a video streaming, public chatroom, or similarly concrete use case. Participants define requirements, write a context file, create an MVP, publish if appropriate, and add features.
- Project anchor: Fork a self-hosted project and open a pull request with a new feature. The PR does not need to be accepted upstream. The learning target is contribution workflow, code reading, scoped change, and evidence of testing.
- Required artifacts when modules are later drafted: welcome page, project structure page, Git and GitHub workflow page, documentation and AGENTS.md page, project operations CodeChecks, LLM analysis lab, debugger and stack trace page, feature contribution project assignment, section quiz.


## Assessment Strategy
Assessments should prioritize confidence, competency, and code comprehension over syntax drills.

- CodeChecks: Use simple, narrow problems that let participants express coding skill. AI is allowed, but discouraged. Problems should be easy enough to solve independently and should reinforce the current section's constructs.
- LLM analysis labs: Use pre-generated or starter code so all participants analyze the same baseline. The work should emphasize reading, refinement, debugging, and explaining tradeoffs.
- Projects: Each section should include one applied project that asks participants to build or extend something real enough to require decisions, but constrained enough to be approachable.
- Quizzes: Focus on reading and understanding code, interpreting behavior, identifying errors, and explaining constructs. Avoid trivia and syntax minutiae.
- Discussions or community work: Use sparingly and only when relatedness improves learning, such as optional hidden message exchange or peer explanation of debugging discoveries.

## Required Ideas
- Major programming concepts must be covered at a conceptual level: functions, input and output, math, strings, tuples, lists, sets, dictionaries, objects, inheritance, loops, conditionals, files, libraries, virtual environments, Git, testing, errors, debugging, documentation, and project structure.
- De-emphasize syntax in favor of constructs, paradigms, code reading, and reasoning about behavior.
- The course is not a Python replacement. It is a foundations bridge for understanding examples, collaborating with LLM tools, and succeeding in 202A.
- Include the missing topic from the prior course: sets, especially membership, uniqueness, and when sets are better than lists.
- AI use should be framed as a partnership that requires competence, autonomy, and judgment. Participants should slow down, know themselves, and take the lead.
- Incorporate the CST-395 foundation as internal design logic: superagency, human value proposition, self-directed learning, adaptive learning, integrated problem solving, reading, writing, talking, listening, meta-habits, AI partnership, creating and consuming, DIKW, self-determination theory, and techniques to habits to outcomes.
- Keep framework names internal unless a later design decision explicitly makes them participant-facing. Build the behaviors into tasks without making the course feel like a theory glossary.
- Thinking should show up in visible artifacts: reading code, writing small explanations, talking through design choices, and listening to error messages, tests, peers, stakeholders, or tool feedback.

## Constraints
- Due dates, if any, must be full Canvas-compatible timestamps.
- Artifact bodies must remain Canvas-native Markdown.
- Do not draft modules or artifact Markdown from this spec until explicitly asked.
- Do not position this as a drill-based programming course.
- Use participant-facing language consistently in generated course materials.
- Do not overemphasize Python syntax or memorization.
- Do not make CodeChecks dependent on complex AI usage.
- Use the same fixed starter code or pre-generated code for LLM analysis labs so differences in output do not become the lesson.
- Preserve the bridge into 202A: this course gives participants the concepts and confidence they need before deeper implementation and workflow work.
- Avoid role-play or simulation. When projects need context, use concrete artifacts, starter code, datasets, repositories, and real development evidence.

## Tone And Voice
Clear, pragmatic, confidence-building, and professional. The voice should treat participants as working adults who can learn technical concepts through meaningful examples. Avoid hype, academic gatekeeping, and syntax-first explanations.

## Source Material
Use the human-provided course notes from the course4 setup request on 2026-05-08 as the primary source. Key source anchors:

- The course is a new 201 course called Science of Computing.
- It has three sections.
- It prepares participants to follow LLM-generated code and succeed in later 202A implementation work.
- It incorporates selected CST-395 learning foundations and AI partnership concepts.
- Section 1 covers functions, documentation, basic input and output, math, strings, tuples, CLI and IDE access, calculator analysis, errors, logging, and a CLI encryption project.
- Section 2 covers objects, lists, loops, conditionals, dictionaries, files, sets, diagrams, support ticket system analysis, sqlite3, testing, and a classifier project.
- Section 3 covers Git, libraries, virtual environments, testing, errors, project structure, documentation, AGENTS.md, project operations, Flask app analysis, debugger use, and a fork plus pull request project.

## Open Questions
- What exact public course code should appear in participant-facing materials: 201, CST-201, or another catalog label?
- Should the three sections map to three weeks, three Canvas modules, or a longer pacing model with multiple weeks per section?
- Which IDE should be the default for setup and Copilot walkthroughs?
- Which fixed calculator, support ticket, and Flask starter repositories or files should become the source code anchors?
- Should the Section 3 LLM analysis app be video streaming, public chatroom, or another app that better matches 202A?
- Should language model development, AI pipeline integration, and agent orchestration be introduced lightly in Section 3 or deferred fully to 202A?
- What dataset should be used for the phone price classifier, and where should it live in the repo?
- Should optional community activities be included as discussions, ungraded pages, or omitted from the initial build?
