---
purpose: What the Dojo course document actually holds (from the Common-Curriculum repo), how a CST499 activity runs in it, where Sprint 2's Dojo Labs stand against that, and the options; for Melisa and Jeremy
status: v0.1, 25 September 2026. Written after Leslie's morning conversation with Melisa and Jeremy, to correct the impression that the Dojo tab holds activity-specific pages
depends_on: Common-Curriculum common/dojo/dojo-core.txt (v1.13.0), config/course-docs.json, docs/course-doc-sync.md, cst499/setup-your-ai-dojo.html, cst499/find-your-gap.html; dojo-modules-sprint-2.md; dojo-setup-note.md
---

# The Dojo: what we now understand, and our options

Leslie and Claude, 25 September.

This morning Leslie said the Dojo tab holds activity-specific pages. Having read the Common-Curriculum repo, that is not right. Here is what is actually there and what it means for Sprint 2.

## What the course document holds

- The Dojo tab is the Dojo Core (v1.13.0) plus every module file in the common Dojo folder. Today that is three modules: Resume, Search Strategy, Referral Case. They are career modules, not tied to any course activity. The tab is identical in every course doc.
- The Course tab is the course's pages, synced from the repo, each with a Source link back to Canvas or the published page.
- The Syllabus tab is policies, schedule, grading.

## How a CST499 activity runs in the Dojo

- The activity page says: "The CST499 AI Dojo knows about this activity; asking it to 'Walk me through Find Your Gap' might be helpful if you feel stuck."
- The Dojo "knows" it only because the page text is on the Course tab. There is nothing on the Dojo tab written for that activity. The Core supplies the method (ask what the student makes of it, one question at a time, push where thin, make them commit to a change, recap), and the page supplies the task.
- Where Sathya wants a tighter script, he points at a separate hosted practice Dojo with the script built in, and the Canvas boxes remain what counts.

## Where Sprint 2 stands

- Both Sprint 2 Dojo Labs say "Open your Dojo and say: Walk me through Dojo Lab: [name]." The how lives in a module written for each lab (rounds, characters, do-nots), in Sathya's module format, in `dojo-modules-sprint-2.md`. A plain-chat fallback pastes a condensed Core plus the module.
- That is more scripted than anything in Sathya's tab. It is a design choice, not his practice.
- Our course does not have a course doc yet, so neither pathway is live. The pages are not on any Course tab, and the modules are not on any Dojo tab.

## Options

1. Keep the modules. Sprint 2's labs have specific moves the Core would not find on its own (push on rows where every answer leads to "so I proceed"; do not suggest solutions). The modules name them. Cost: two files to maintain and a longer fallback paste.
2. Sathya's style. No modules. The Dojo Lab page carries the goal, what the student brings, and what the conversation should cover, written for the student, and the Core does the rest. Cost: less control over what the Dojo pushes on.
3. Short modules. Three or four lines per round, the do-nots kept. A middle path.

## What decides it

- Two test runs with a set-up Dojo: one with Module 1, one with just the page text. If the Core alone finds the moves, option 2. If not, 1 or 3.
- What the course doc for this course will hold, and who owns it: the Course tab needs our pages synced, and any module needs adding to the shared Dojo folder or to a course-specific place. That is Jeremy's and Sathya's call.
- Whether Melisa's Sprint 3 and 4 Dojo Labs take the same shape, so learners meet one pattern.

## Open questions for Jeremy and Sathya

- Will this course get its own course doc, with our Sprint pages on the Course tab, before 5 October?
- If we keep modules, where do they live: the shared Dojo folder (every course sees them) or somewhere course-specific?
- Is the "Walk me through" one-liner plus the Course tab the intended pattern for our labs too?

Provenance: Leslie, the question and the morning conversation it corrects; Claude, the reading of the Common-Curriculum repo and the write-up.
