---
purpose: Sprint 1, cut-ready source for Jeremy's rebuild, with a cover note for him and one build block per item
status: v5.4.2 (cut-ready), 16 September 2026. The final artifact is "Problem Frame"; the First frames are draft frames; no "version one/two" in participant text. Content is v5.3, reviewed by Leslie on every page, with the Problem Frame name, the Candidate Log link, interim Dojo Lab text, and reviewer markers in place. History and rationale for every choice are in sprint-1-decisions.md.
supersedes: sprint-1-half-one-working-draft-v4.md (frozen at v4.2) and sprint-1-half-two-working-draft-v1.md (v1.1), for the whole of Sprint 1
storage: replaces the sprint-12 first half; positions 1 to 10
---

# Sprint 1: cut-ready source, v5.4

## Cover note for Jeremy

This file is the source for the Sprint 1 rebuild. Everything below the line after this note is either participant text or a build block, and nothing in it needs a decision from you. This note is the only part you have to read.

**Rules for the run**

1. **Mode: faithful conversion, not instructional adaptation** (in the terms of `docs/AUTHORING.md`). Carry the text as written. Do not shorten, rewrite, or restyle. The draft is already at the length and register of the September cut (three to eight hundred words a page) and has had two full review passes from Leslie. Where Canvas mechanics force a change (a box label, a heading level), keep the meaning and list the change in the authoring report so we can see it.
2. **Bracketed markers are reviewer notes.** `[TEAM DECISION: ...]` and `[INTERIM: ...]` carry into the pages verbatim, highlighted in the review export the way Sprints 3 and 4 did it, and are stripped at publish. There are five of them.
3. **`[BUILD]` blocks and the italic line under each item title are configuration**, not page text: kind, position, points, submit or not, and the box prompts and criteria under each **Response tasks** heading (one response box per bullet, `presentation: reading` wherever there is more than one box). They do not appear in the pages.
4. **"More help" blocks.** Wherever a page has a paragraph beginning *More help*, the design intent is a disclosure on the same page: backbone visible, help one click away. The renderer does not appear to offer an authored disclosure (its `<details>` elements are its own self-check and More options), so if none exists, render each *More help* paragraph inline as an indented aside in the position it sits, and say so in the readback. Do not drop them. There are seven.
5. **Section-to-box mapping** for the pages with more than one box, since `instruction_section` wants a unique top-level heading per task: on **Dojo Lab**, section 1 feeds the challenges box, section 2 the framings box, section 3 the your-choice box. On **Problem Frame**, Part 1 feeds problem-frame, Part 2 what-changed, Part 3 which-assumptions-first. On **First frames**, all seven teaching sections come before the five frame boxes, which sit together at the end; nothing maps one to one. Single-box pages (Brainstorm, Get underneath) put the box after all the teaching.
6. **Send back the readback** (your authoring report or a rendered docx) before the pages go to Clare.

**Before you run**

- The old first half in `sprint-12` (Canvas module 2079) is superseded by this whole sprint. Retire or replace it as you see fit; Melisa has been running it, so keep her submissions reachable.
- The Candidate Log link is already in the Introduction, in the form that makes the participant's copy on click. Nothing to do.
- The name changed: the sprint's final artifact is **Problem Frame**, not Goal Plan and Problem Frame. The frames written on the First frames page are draft frames. That ripples to the Welcome page's five-artifact map, `course1/homepage.yaml` (the Sprint 1 entries, and "goal plan" in the Sprint 3 and 4 reflection lines), and Sprint 3's "mid-course goal plan revision." Those are outside this file.
- Your 15 September Sprint 0 says "Available now: the first half of Sprint 1, through Test and commit." Test and commit no longer exists once this sprint is built; the first-week items are Brainstorm your list and Get underneath three to five.
- Sprint 0 owes two lines before this sprint uses them: what "own your progress" and "graded item" mean, and that in assignments each part shows guidance, then an example, then a box.

**Items**

| Position | Item | Kind | Points | Submit | Boxes | Week |
|---|---|---|---|---|---|---|
| 1 | Sprint 1: Find the Problem Worth Solving | Module header | | | | |
| 2 | Introduction: Find the Problem Worth Solving | Page | | | | One |
| 3 | Brainstorm your list | Own your progress | 0 | must submit | 1 | One |
| 4 | Get underneath three to five | Own your progress | 0 | must submit | 1 | One |
| 5 | The problem frame | Page | | | | One |
| 6 | Sprint 1 Concept check | Self-check | 5 | completion | 6 questions | One |
| 7 | First frames | Graded item | 35 | one submission | 5 (2 optional) | One |
| 8 | Dojo Lab: test, widen, choose | Own your progress | 0 | must submit | 3 | Two |
| 9 | Problem Frame | Graded item | 50 | one submission | 3 | Two |
| 10 | Sprint 1 Reflection: what changed | Graded item | 10 | ai_activity, JSON upload | 1 | Two |

Sprint total 100. The Reflection uses the CTI-owned AI proxy that went live 14 September; its configuration is in the `[BUILD]` block on that item.

**Where things are.** This file: `course1/design/sprint-1-working-draft-v5.md`. Why each choice was made: `course1/design/sprint-1-decisions.md`, 14 September onward. The Log template source: `course1/design/candidate-log-template-v2.md`. The Dojo tool question, parked: `course1/design/dojo-setup-note.md`.

---

## Sprint 1: Find the Problem Worth Solving

*Module header. Position 1.*

You will start by brainstorming potential problems from your own life that you would be interested in solving. Over the course of this sprint, you will practice three things:

- Describe what actually happens in your potential problems, so you can see if there is a gap worth investigating.
- Write a problem frame that describes the problem as best you can, clearly marking what you do not know yet so you can look into it later.
- Use AI to test and widen your own thinking.

**What you carry forward.** One Problem Frame, for the problem you chose, with every assumption in it marked confirmed or unverified. Sprint 2 works on the unverified ones.

The Introduction lays out the route through the sprint, week by week.

---

## Introduction: Find the Problem Worth Solving

*Page. Position 2.*

This sprint is about choosing a problem you can investigate through this course. You will begin with your own experience.

### Sprint 1 key terms

A **problem** is a gap between how something works now and how it could work, where the gap costs someone something real.

You are going to come up with a list of problems you might be interested in exploring. We call them **candidate problems**.

A **problem frame** is your written account of a problem. It says what is happening, who it costs and what it costs them, how it is handled today, and what you do not yet know.

> **[BUILD]** Keep the existing illustration (workplace handoff) and caption.

### Your route through this sprint

The goal is to move from a wide list to one framed problem, following these steps over the course of two weeks.

**Week 1**

1. Read the Introduction.
2. **Brainstorm your list.** Ten minutes. Everything in your week that could hold a problem, by area of your life. (Own your progress, 0 points.)
3. **Get underneath three to five** of them. Describe how each works now and what it costs, and write the gap. (Own your progress, 0 points.)
4. **Read about problem frames**, then take the **Concept check** (5 points).
5. **Write your First frames**, one for each of your three to five candidates (35 points).

**Week 2**

6. **Run the Dojo Lab.** Tap into AI to widen your frames and help select one problem. (Own your progress, 0 points.)
7. **Select one problem and submit your Problem Frame.** Rewrite the frame of the problem you chose, and identify what changed from your draft (50 points).
8. **Write the Reflection** (10 points).

Spread week 1 across several days. The brainstorm's help asks you to watch your routine for a day or two if your list comes up short.

### What to keep and submit

- **Brainstorm your list, Get underneath, Dojo Lab: own your progress, 0 points.** Submit to record completion, or continue without submitting.
- **Concept check: 5 points.** Your instructor reviews completion.
- **First frames: 35 points.** One submission, all your frames, written part by part.
- **Problem Frame: 50 points.** One submission.
- **Reflection: 10 points.**

### About AI in this sprint

Two activities ask you to work without AI, the brainstorm and the table underneath it. The reason is narrow. AI has no access to what you have stopped noticing, what you keep putting off, or what you work around, and those are where problems hide. Once your own read is written down, AI can be your partner. The Dojo Lab uses it to test and widen your frames, and it will do that well only because you wrote them first.

### How to work

Use rough, specific notes, and say so honestly when a search produces nothing. You are choosing something to investigate, not proving its cause. The frame has its own way of marking what you are unsure of; until then, a guess written as a guess is fine.

Keep everything you write, including items you set aside. The Reflection compares your first frames with your final one, and your set-aside list is where you go if your choice does not survive.

### Where to write

Use the **Candidate Log**, a document template you copy once and keep for the whole sprint. [Make your copy of the Candidate Log](https://docs.google.com/document/d/1aTgaDgf1ugkQujJkgvo-EHXUqm9ztN1jMA5SDy3lTjI/copy). It runs the whole sprint. Part A holds your brainstorm, Part B your table, Part C your draft frames, one per candidate, and Part D your Problem Frame. Each activity names the part it fills. Paste that part, or a link to your Log, into the activity's response box.

Begin with **Brainstorm your list**.

---

## Brainstorm your list

*Own your progress. Position 3. 0 points. Submit to mark it complete.*

### 1. Set up your categories

Take a page. Write three or four headings for the areas of your life where things happen. **Work**, **home**, and **other** is enough. Add **job search**, **volunteering**, **caregiving**, or **side business** if those are part of your week. Work without AI here. AI cannot see your week.

### 2. Walk your week and write everything down

Ten minutes. Under each heading, list situations that could hold problems. A phrase per item. Do not examine anything yet, and do not decide whether it counts.

Walk through your typical week in order. You may want to open your to-do list, your calendar, and your inbox, and look for:

- Things you do over and over.
- Things you dread or that bug you.
- Things you wish worked differently.
- Things somebody asked you for that do not feel quite right.
- Things you have been putting off.

> **Here is an example list**
>
> **Work**
> - Account handovers always get dropped
> - Monthly report columns have to be reformatted to fit the tracking spreadsheet
> - Reminding people about compliance training
> - Nobody reads the meeting notes
> - Two clients who called about the same question
> - Onboarding: new people sit idle for days
>
> **Home**
> - Groceries run out midweek and somebody makes a second trip
> - The shared family calendar is wrong about half the time
> - Insurance paperwork that has sat on the counter since spring
>
> **Other**
> - Volunteer shift sign-ups happen across three group texts
> - Half the new plots at the community garden went to weeds by August
> - My resume has not been touched in two years

A long list is the goal. Twelve to twenty items across all headings is normal. Nothing on it is a problem yet, and most of it will not become one.

### 3. If your list is short

Three places to look. Each is a collapsed block; open the ones you need.

*More help: what bugs you.* Something you dread or complain about. Describe the last time it happened, step by step, who did what. Each step that made you sigh goes on your list.

*More help: what you stopped noticing.* A **workaround** is something you do to get around a difficulty, and repeating it makes its cost feel like an ordinary part of the job. Over the next day or two, notice a step you redo, a person you chase, or a private file you keep because the shared version does not work for you. Every month, one team fixed the exported report columns by hand, each analyst in a separate copy, and nobody called it a problem.

*More help: what somebody handed you.* A **surface request** names a solution before the problem is clear: "we need an app to track onboarding" says what to build, not what needs to change. Ask why, then why does that matter, until you reach a goal nobody would dispute (new hires contribute as quickly as possible), then list what could be in the way of that goal (an unowned handoff from HR to IT; managers not knowing what a new hire can take on). Each obstacle goes on your list. Requests you make of yourself count too: "I need to fix my resume" has a goal underneath it.

Keep the list in Part A of your Candidate Log. Next, **Get underneath three to five**.

### Response tasks

- **your-list** (response). Prompt: *Your list, by heading. Paste Part A of your Candidate Log, or a link to it.* Criteria: at least two category headings; items are phrases from the participant's own week, specific items rather than categories; nothing on the list is examined or ruled out yet; a short list is reported honestly with what was tried.

---

## Get underneath three to five

*Own your progress. Position 4. 0 points. Submit to mark it complete.*

### 1. Pick three to five

From your list, choose three to five situations to look at more closely. There is no perfect way to pick which three to five, but think about items that:

- Would make a real difference if they were different.
- You could not fix this week.
- You do not already know a solution for.

These are your **candidate problems**, or candidates for short. Do not pick the one you already care most about and stop. Three is the minimum because the next activities compare them. Work without AI here, for the same reason as before.

### 2. Fill four columns for each

The fact that you came up with each of these problems is an **indicator** that something may be wrong. Getting underneath it means describing how it works now, closely enough that a gap starts to show. For each of your three to five items, complete a table with four columns:

- **The situation:** restate the item from your list, a phrase.
- **How it works now:** describe in two or three sentences. Who does what, in what order. Describe the actions that happen now, not how they should be and not possible solutions.
- **What it costs, and whom:** name who is impacted (you very likely have several people or roles) and, for each of them, what the cost is in time, money, errors, or strain.
- **The gap:** combine the other two columns into one sentence that says what could be different, and who feels the cost. Name who does not know, cannot do, or has to redo what. If your sentence describes a process (manual, informal, inconsistent, slow), it is not finished yet, so say who pays for that.

*More help: if the gap will not come.* Ask **"How does that part work now?"** two or three times about the step where the cost appears. In the example below, asking it about "nobody else is told" is what produced the gap.

> **Worked example: account handovers**
>
> **The situation:** Account handovers always get dropped.
>
> **How it works now:** When an account changes hands, the outgoing manager tells the incoming manager in a conversation or a short email. Nobody else is told. The rest of the team finds out when a client mentions it or when something goes wrong.
>
> **What it costs, and whom:** Clients: at least two this month repeated their history to someone who should have known it. The four other account managers: they act on stale ownership for days at a time.
>
> **The gap:** The rest of the team does not know when an account changes hands, so they act on stale ownership and clients repeat themselves.

Keep the table in Part B of your Candidate Log. Next, **The problem frame**.

### Response tasks

- **your-table** (response). Prompt: *Your table, three to five rows, four columns each. Paste Part B of your Candidate Log, or a link to it.* Criteria: three to five situations from the participant's own list; each "how it works now" describes actions rather than blame or fixes; each cost names a person or role; each gap names who lacks or must redo what, not a process description.

---

## The problem frame

*Page. Position 5.*

You have three to five candidate problems in your table, each with a described gap. Now you write up a draft problem frame for each of them, so you can tell which one is worth the next nine weeks.

A **problem frame** is your account of a problem. It says what is happening, who it costs and what it costs them, how it is handled today, and what you do not yet know. A frame is not a proposal. You are not thinking about what potential solutions you would build. It is your description of the problem. It is as important to mark clearly what you do not yet know as it is to detail what you do know. You will spend time later in the course filling in those gaps.

### The template

A frame has seven parts. This is the whole of it, and Part C of your Candidate Log repeats it once per candidate.

1. **The goal it serves.** One sentence. Nobody involved would dispute it, and it points at this problem rather than its neighbours.
2. **The problem.** The gap between now and that goal, as a condition someone is living in. One or two sentences.
3. **Who is affected, and what it costs them.** 3a names the people or specific roles. 3b says what it costs each of them, in time, money, errors, or strain.
4. **How it is handled today, and where that falls short.** 4a describes the system, process, habit, or person coping with it now, and anything tried and abandoned. 4b names the moment it stops working, not the consequence that follows.
5. **What fixed would look like.** A changed state, not a solution. One sentence.
6. **Find your assumptions.** Everything in parts 2 to 5 that you wrote as if it were true without having seen it yourself or heard it from someone who would know. Each one marked **confirmed** or **unverified**, and for each unverified one, who could tell you.
7. **What you do not know yet.** What is left after part 6.

As you can see, the problem frame includes some information that you already wrote in your table. You will reuse your gap, the people you listed, and your description of how things work now. Reuse it freely. You do not need to mark or tidy it.

### Write in this order

Write **2, 3, 4** first. Then **5**. Then **6 and 7**. Then **1** last.

Part 1 is presented first because that is how the finished frame reads, but you cannot write it until you know what fixed looks like. Expect to write it at the end.

### Worked example A: account handovers

**1. Goal:** Clients are handled by someone who knows their history, from the first day an account changes hands.

**2. Problem:** Handovers happen in a conversation between the outgoing and incoming owner, and nothing reaches the rest of the team.

**3a. Who:** The two clients who changed hands this month. The four other account managers.

**3b. Cost:**
- Clients: repeated their history to someone who should have known it.
- Account managers: act on stale ownership for several days. *(number of days unconfirmed)*

**4a. Handled today:** The outgoing owner tells the incoming owner directly. Nobody remembers anyone trying anything else.

**4b. Stops working:** At the moment a third person needs to know. The conversation works for the two people in it and reaches nobody else.

**5. Fixed looks like:** Everyone on the team knows within a day when an account changes hands.

**6. Assumptions:**

| From | Assumption | Status | Who could tell me |
|---|---|---|---|
| 2 | Nothing reaches the rest of the team | unverified | the other managers |
| 3a | All four managers are affected, not just the one I sat next to | unverified | the other three managers |
| 3b | Clients notice and it costs them something | unverified | the account lead |
| 3b | Managers act on stale ownership for *days* | unverified | the other managers |
| 4a | Nobody has tried to fix this before | unverified | the account lead |
| 5 | One day is fast enough to matter | unverified | nobody has said what fast enough is |

**7. Left over:** I do not know who owns the handover process, if anyone. Nobody obvious to ask. Start with the account lead.

### Worked example B: a neighbourhood garden plot

Shorter, and nothing in it is countable. That is fine.

**1. Goal:** People who sign up for a plot are still gardening it in August.

**2. Problem:** New plot-holders start alone in April and have no one to ask when something goes wrong, so most of them stop coming by midsummer.

**3a. Who:** The six people who took plots this spring. Ramona, who runs the sign-ups and ends up fielding every question herself.

**3b. Cost:** New plot-holders: frustration, then quitting. Ramona: a stream of questions she did not sign up for, and the awkwardness of watching plots go to weeds.

**4a. Handled today:** Ramona answers questions when people find her, which is by chance at the water spigot.

**4b. Stops working:** When someone's problem shows up on a day Ramona is not there. Most people do not follow up later.

**5. Fixed looks like:** A first-year plot-holder has someone to ask by the time their first thing goes wrong.

**6. Assumptions:**

| From | Assumption | Status | Who could tell me |
|---|---|---|---|
| 2 | Most new plot-holders quit by midsummer | unverified | Ramona |
| 2 | They quit because they had no one to ask | unverified | the people who quit, if I can find them |
| 3b | Ramona finds this burdensome | confirmed, she said so | |
| 5 | Having someone to ask would keep them going | unverified | nobody can say yet |

**7. Left over:** Whether this happens every year or was unusual this year. Whether anyone tried pairing new people with returning gardeners before. Ramona has been here longest, but there may be nobody who remembers.

Take the **Concept check**, then continue to **First frames**.

---

## Sprint 1 Concept check

*Self-check. Position 6. 5 points. Six choice questions with feedback. Ungraded self-check; instructor reviews completion.*

Answer all six from your own thinking, without AI. Review each explanation; if it surprises you, revisit the page it points to and try again. Your instructor reviews completion in Canvas; the on-page checks do not assign your grade.

[TEAM DECISION: where the Concept check sits in the sequence is reconsidered once the content is done. It sits after The problem frame because questions 4 to 6 draw on that page.]

> **[BUILD]** Six choice questions with feedback, in Jeremy's concept check format. Correct answer marked in bold.

1. **You write "I dread the weekly handover" on your list. What is that, at this stage?** A confirmed cause / **An indicator, to get underneath by describing how it works now** / A solution. *Feedback: a feeling that something is off points toward a problem. Describing how it works now is what shows the gap.*
2. **Which sentence belongs in "How it works now"?** We should buy a handover app / Nobody cares about communicating / **The outgoing owner tells the incoming owner; the rest of the team hears later.** *Feedback: that column describes what happens and who does what. It does not prescribe a fix or replace observation with blame.*
3. **Your gap reads "The process is manual and inconsistent." Is it finished?** Yes, submit it / **No. It names a process, not who does not know, cannot do, or has to redo what** / No. It needs a solution. *Feedback: a process description is not a gap yet. The gap shows when it names who pays.*
4. **Which of these is a changed state rather than a solution?** Build a shared handover checklist / Set up an alert / **Everyone on the team knows within a day when an account changes hands.** *Feedback: part 5 of a frame says what is true once the problem is gone, not what was built. Solutions come later in the course.*
5. **Which of these is the moment current handling stops working, rather than its consequence?** Which means clients repeat their history / Handovers are informal / **The instant a third person needs to know who owns the account.** *Feedback: 4b names the condition under which the current handling breaks. The consequence is what follows from it.*
6. **"Better client communication" as the goal a problem serves fails which test?** Nobody involved would dispute it / **It would serve any client problem anywhere** / It names a solution. *Feedback: a goal has to be specific enough to point at your problem and not its neighbours.*

---

## First frames

*Graded item. Position 7. 35 points. One submission.*

Now you are going to write a draft frame for each of your three to five candidates. This page walks you through the seven parts in the order you write them. Remember, for each part you will see the guidance, then the example. Write each frame whole, one candidate at a time, in Part C of your Candidate Log, which repeats the seven parts in this order with a line of guidance beside each slot. When a frame is done, paste it into its box below, and start the next.

Rough is right. A part you cannot fill gets "I do not know yet," and that line is part of the deliverable, not a failure of it.

Work without AI on this one. The draft is your own read. The Dojo Lab uses AI to test and widen these frames, and that only works if there is an independent view to test.

Expect the first frame to take longest and the others to go faster. Three frames in a sitting is normal.

### 1. Part 2: the problem

Part 2 is the gap between now and the goal, in one or two sentences, and you already have it. It is the gap column from your table. Write it as a condition someone is living in rather than as a task that annoys you. "The rest of the team does not know when an account changes hands" is a condition. "Handovers are a hassle" is a task.

> **Example.** *2. Problem:* Handovers happen in a conversation between the outgoing and incoming owner, and nothing reaches the rest of the team.

### 2. Part 3: who is affected, and what it costs them

This part has two halves, and both are required.

**3a. Who.** Name the people or the specific roles. Not "the team," but actual people. If you cannot name them yet, acknowledge that, but say who you would have to ask to find out.

**3b. What it costs each of them.** Time, money, errors, or strain. Different people usually pay different costs, so say which cost belongs to whom. A cost with nobody attached to it is not a cost yet.

Your table's cost column feeds both halves. The people go in 3a, and 3b says which cost is whose.

> **Example.** *3a. Who:* The two clients who changed hands this month. The four other account managers. *3b. Cost:* Clients repeated their history to someone who should have known it. Account managers act on stale ownership for several days (number of days unconfirmed).

### 3. Part 4: how it is handled today, and where that falls short

Two halves again.

**4a. How it is handled.** Describe the system, process, habit, or person coping with this now. Your "how it works now" column goes here. "Nobody handles it" is rarely true, and "handling it" can sometimes mean it is an item on someone's to-do list that just does not get done, or does not get done well. Also look for anything that was tried and abandoned. An abandoned attempt is the best evidence you have of where the current handling falls short.

**4b. At what moment it stops working.** Not the consequence but the moment. Current handling usually works fine under some conditions and fails under others, so name the condition where it breaks. In the handover case, "which means clients repeat their history" is a consequence. "The instant a third person needs to know who owns the account" is the moment.

*More help.* If 4b is blank, look at your cost column. The moment it stops working is usually the moment the cost appears.

> **Example.** *4a. Handled today:* The outgoing owner tells the incoming owner directly. Nobody remembers anyone trying anything else. *4b. Stops working:* At the moment a third person needs to know. The conversation works for the two people in it and reaches nobody else.

### 4. Part 5: what fixed would look like

Answer the question "what would fixed look like?" in one sentence, and stop there. It describes a changed state, not a solution. "New hires would have working access on day one" is a changed state. "Building an onboarding app to track new hires" is a solution.

*More help.* Two solution-shaped lines rewritten as states. "A shared handover checklist" becomes "everyone on the team knows within a day when an account changes hands." "Pair new gardeners with returning ones" becomes "a first-year plot-holder has someone to ask by the time their first thing goes wrong."

> **Example.** *5. Fixed looks like:* Everyone on the team knows within a day when an account changes hands.

### 5. Part 6: find your assumptions

Odds are that in framing your problem, you are making some assumptions about how things work now, who is impacted, what the cost is, and so on. Go back through parts 2 to 5 one part at a time, in order. In each part, look for what you assumed and write it down. Make the whole list first. Then go back through the list and mark each one.

**Finding them.** An assumption is anything you wrote as if it were true without having seen it yourself or heard it from someone who would know. They hide in plain sight, and the ones that feel most obvious are usually the ones worth writing down. Part by part, in the handover case:

- Part 2 says nothing reaches the rest of the team. Assumed. I have seen it happen twice, not every time.
- Part 3a says all four managers are affected. Assumed. I sat next to one of them.
- Part 3b says clients notice and it costs them something. Assumed. Two clients repeated their history, and whether they minded is a guess.
- Part 4a says nobody has tried to fix this before. Assumed. The two people I asked do not remember anything.
- Part 5 says one day is fast enough to matter. Assumed. Nobody has said what fast enough is.

**Marking them.** For each one, write **confirmed** if you have seen it yourself or someone who knows told you, or **unverified** if not. Then, for each unverified one, name who could tell you. If everything comes out unverified, you have not looked hard enough at what you actually do know. If everything comes out confirmed, you have not looked hard enough at what you assumed.

[TEAM DECISION: two statuses (confirmed, unverified) or three (seen, told, assumed). Two for now.]

> **Example.** The handover assumptions table on The problem frame page. Notice that the cost assumption in 3b about clients is its own row, and that part 5 produced one.

### 6. Part 7: what you do not know yet

Most of what you do not know is now a row in part 6 with a name beside it. This part is for what is left over. Questions that do not attach to any single assumption. Assumptions where you could not name anyone who could answer. Things you realized you do not know about the situation itself, such as who owns a process or whether anyone has tried this before. This part is small. That is expected.

**Nothing here is a step toward building.** If you have written "research what tools exist" or "see if this can be automated," you have jumped to solutions. The question is what you do not know about the *problem*.

> **Example.** *7. Left over:* I do not know who owns the handover process, if anyone. Nobody obvious to ask. Start with the account lead.

### 7. Part 1: the goal it serves, last

Part 1 says what should be different, in one sentence, and you write it last because it comes out of part 5. Take your part 5 sentence and ask why that would matter. Then ask why again, and keep going until you reach something nobody involved would dispute and that says nothing about what to build. Then run one more test. Would this goal serve any problem of this type anywhere? "Better client communication" passes the first test and fails this one. Narrow it until it points at your problem specifically. Part 5 is the changed state, and part 1 is why that state is worth having.

*More help.* The why-chain on the handover case. Why does it matter that everyone knows within a day? Because people act on stale ownership. Why does that matter? Because clients repeat themselves to people who should know them. So the goal is that clients are handled by someone who knows their history from the first day an account changes hands.

> **Example.** *1. Goal:* Clients are handled by someone who knows their history, from the first day an account changes hands.

Keep every draft exactly as you wrote it. The Reflection compares your drafts with your Problem Frame, and that only works if the drafts stay unedited.

### Response tasks

> **[BUILD]** One box per frame, `presentation: reading`. Boxes 4 and 5 optional. The criteria repeat.

- **frame-1** (response). Prompt: *Frame 1, the seven parts labeled, pasted from Part C of your Candidate Log.* Criteria: all seven parts present, 3 and 4 in their a and b halves; part 2 is a condition someone is living in, not a task; 3b assigns a cost to each person or role; 4b names a moment, not a consequence; part 5 is one sentence describing a state, not a solution; part 6 lists at least four assumptions across parts 2 to 5, at least one from 3b, each marked confirmed or unverified, with who could tell you for each unverified one; part 1 passes both goal tests; unknowns are written as "I do not know yet" rather than filled with guesses.
- **frame-2** (response). Same prompt and criteria for frame 2.
- **frame-3** (response). Same for frame 3.
- **frame-4** (response, optional). Same for frame 4, if you have one.
- **frame-5** (response, optional). Same for frame 5, if you have one.

---

## Dojo Lab: test, widen, choose

*Own your progress. Position 8. 0 points. Submit to mark it complete.*

Bring your frames. This activity uses AI in the one way Sprint 1 asks for, which is to test a frame you are too close to see around, and to widen it. AI can find the assumption you made without noticing in four seconds. It cannot know which of your situations your director would care about or which colleague would quietly block it. You can. That is the division of labor here.

Use any AI chat you already have (ChatGPT, Claude, or Gemini). Do not paste confidential workplace, client, or personal details. Change names and drop anything sensitive before you start.

[INTERIM: this page runs in any chatbot with the prompts below. The course-wide Dojo setup, in which the same activity runs as a coached conversation, is being built and will replace the prompts. The activity and what you submit do not change.]

One rule holds for the whole activity. **Your frames stay in your words.** AI may point at a part, and you rewrite it. If you find yourself pasting its sentences into your frame, stop and write the sentence yourself.

### 1. Test each frame

Paste one frame at a time and use this prompt:

> I am going to paste a problem frame. It has seven parts: 1 the goal it serves, 2 the problem, 3 who is affected and what it costs them, 4 how it is handled today and the moment that stops working, 5 what fixed would look like (a changed state, never a solution), 6 my assumptions marked confirmed or unverified, and 7 what I do not know yet. This is a first draft. Most of my assumptions are unverified, and that is expected; I will check them over the next nine weeks. Your job is to be a skeptic who works in this situation, not an editor. Do not rewrite anything and do not suggest solutions. Do not list everything you notice.
>
> 1. Is this frame specific enough to be a starting point? Answer "yes" or "not yet," with one reason.
> 2. The three findings that matter most before I move on, ranked. One or two lines each, naming the part and quoting my words. Look especially for a cost with nobody attached, a solution hiding in part 5 or 7, and a part still empty.
> 3. One question someone who works in this situation would ask me first.
>
> Nothing else. Here is the frame:

Take what lands and fix the frame yourself, in your Log. Add an assumption where it found one you missed. Move a solution out. Attach a cost to a person. If a finding needs more than a line or two to fix, it is desk work, so go and do it in the Log rather than in the chat. Do this for every frame.

### 2. Widen each frame

Follow up with:

> Now give me three other ways to see the same situation, two lines each: what it makes visible that my frame does not, and who would have to be involved. Then one line on whether any of them suggests this problem is already handled somewhere I have not looked.

Read the three framings against your own situation. One will usually be generic and worth ignoring. One will usually land. If one lands, decide what it changes in your frame, and write that change yourself.

### 3. Choose

With all your frames tested, choose one.

[TEAM DECISION: the criteria for choosing are not settled. The three size questions below are a draft. Candidates to add or replace them: whether the frame held up under testing; whether someone in 3a is reachable in Sprint 3; why you.]

Three questions decide whether a frame is the right size, and they are answerable now because the frame exists:

- Can you describe how it works now in one paragraph? (Part 4a.)
- Is there at least one person other than you, with a stake in it or knowledge of it, who would talk to you about it? (Part 3a, or part 7.) For a household problem, someone **outside the household** whom it would be normal to ask.
- Is there at least one thing you would have to find out to move on it? (Part 6.)

A frame that fails the first is too big, so pick one instance you have seen. A frame that fails the second or third is too small, or too private, so ask what it is an instance of, and go up.

Then choose the one that passes and that you want to stay with. Write your reasoning down, because the Problem Frame page asks for it. Its Part 2 reuses why you chose this one and what testing changed, and your runner-up is where you go if the choice does not survive Sprint 2. The box below collects it.

- **Why this one:** what in the frame and the testing makes it workable.
- **Why not the others:** one or two sentences each, including those that mostly held up.
- **Why you:** your connection to it and why you want the next nine weeks on it.
- **Runner-up:** your fallback, or that none is currently workable.

If nothing holds up, or the only survivor does not matter to you, go back to your list. Items you set aside are still there. Report what you tried and where you will look next instead of forcing a choice.

> **Illustrative choice**
>
> Handovers and the garden plot both held up under testing. I chose handovers because I work on them weekly and the four managers and the account lead sit near me. The garden plot depends on Ramona, whom I see once a month, so it is my runner-up.

### Response tasks

- **challenges** (response). Prompt: *For each frame: the findings the test raised, and what you changed or did not change in response.* Criteria: every frame appears; each response names what was accepted or rejected and why; at least one response is a specific "no, I have seen this directly" and at least one a specific "fair, I do not know that"; no response is a bare agreement.
- **framings** (response). Prompt: *For the frame you are leaning toward, the three other framings, one line each, and which one, if any, changed your frame.* Criteria: three framings in the participant's words; a decision stated for each; at least one rejected with a reason.
- **your-choice** (response). Prompt: *Your choice, the three size questions answered for it, why this one, why not the others, why you, and your runner-up.* Criteria: the three size questions answered from the frame's own parts; each alternative receives a reason; the why-you line is present and specific; a runner-up is named or its absence explained; an unsuccessful search reports what was tried and a next step instead of a forced choice.

---

## Problem Frame

*Graded item. Position 9. 50 points. One submission.*

You chose one problem at the end of the Dojo Lab. From here on, everything in the course works on that one. This is where you write it up properly, in three parts and one submission. Your Problem Frame is what the rest of the course builds on. Parts 2 and 3 tell your instructor how you got there and what you will check first.

### Part 1. Your Problem Frame

Rewrite the draft frame you chose with everything that changed as a result of the Dojo Lab. All seven parts, in your words. Bring part 6 up to date, so that it lists every assumption you still hold, each marked confirmed or unverified, and for each unverified one, who could tell you.

### Part 2. What changed, and why

Your instructor cannot see your Dojo Lab session. This paragraph is where they see that the frame was tested and that you, not the AI, made the changes. Start from the recap your Dojo session gave you and check it against your Log. Then, in one short paragraph and in your words, say what moved between your draft and your Problem Frame, what argument or evidence moved it, and one thing the Dojo suggested that you rejected, and why. A frame that did not change is a legitimate result if you can say what you tested it against.

### Part 3. Which assumptions should you investigate first

Look at part 6 of your frame. Pick the two or three assumptions whose failure would break the frame rather than adjust it. For each one, write what would have to be true for it to hold, and who could tell you or what you could observe. These are what you check first in Sprint 2, and one of them is what your Sprint 3 conversation is for.

[TEAM DECISION: Part 3 may move to Sprint 2's opening activity once Sprint 2 is drafted. Kept here as the hand-off for now.]

> **Worked example: account handovers, part 3**
>
> **All four managers are affected, not just the one I sat next to.** If it is one person's habit, this is one conversation, not a problem worth nine weeks. To hold, at least two of the other three would have to describe the same thing. The three other managers could tell me, and I could ask them this week.
>
> **Clients notice and it costs them something.** If clients do not notice, the cost is internal only and the goal in part 1 is wrong. The account lead would know whether a client has ever raised it.

Your runner-up and your set-aside list are still in your Candidate Log, in case this frame does not survive Sprint 2.

### Response tasks

- **problem-frame** (response). Prompt: *Your Problem Frame, all seven parts, with part 6 up to date.* Criteria: all seven parts present, in the participant's words; part 5 is one sentence describing a state; every assumption carries a status, and every unverified one names who could tell you; at least one unverified assumption remains, since a frame with none at this stage is a warning sign; part 1 passes both goal tests.
- **what-changed** (response). Prompt: *What changed from your draft, what moved it, and one suggestion you rejected.* Criteria: names a specific change or a specific reason for no change; names the evidence or argument; includes one rejected suggestion with a reason; in the participant's words rather than the Dojo's.
- **which-assumptions-first** (response). Prompt: *The two or three assumptions whose failure would break the frame, what would have to be true, and who could tell you or what you could observe.* Criteria: two or three assumptions, not a list of all of them; a clear condition for each to hold; a named person, role, or observation for each; at least one is reachable within two weeks.

---

## Sprint 1 Reflection: what changed

*Graded item. Position 10. 10 points. ai_activity, JSON upload, same mechanism as Sprints 3 and 4.*

Put your draft frames beside your Problem Frame and write about the distance between them. You have already written what changed. Here, write about how it changed. What did AI find that you would not have reached alone? What did you contribute that AI could not, because it depends on what you know about the people and the place? How did you decide what to accept and what to reject? And what is the one thing you are still unsure of and are carrying forward on purpose?

> **[BUILD] ai_activity configuration.** One `ai-discussion` question. Prompt as above, minLength 150, numQuestions 3. aiContext: *This is the Sprint 1 reflection for Reframing Problems with AI. The participant wrote draft frames for three to five situations, had AI test and widen them, chose one, and wrote their Problem Frame. Ask follow-up questions that catch a change attributed to AI that the participant actually made, a contribution described as "judgment" without saying what was judged, an accept-or-reject decision with no reason behind it, and a carried-forward uncertainty that is really a to-do. Push them to name one thing they are still unsure of. Do not rewrite the reflection.* summaryLabel: Your Sprint 1 Reflection. The CTI-owned AI proxy is live as of 14 September (`docs/audits/2026-09-14-owned-course-ai-proxy.md`), so this no longer waits on Sathya's deployment; falls back to text entry if it goes down.

---

---

## Provenance

Human (Leslie): the resequence and every finding behind it; the frame page, its two examples, and its designer notes; the points; every ruling recorded in the decisions log from 14 September on; two full review passes. AI (Claude): the prose of every other page, the handover and garden examples carried through, the concept check questions, the response tasks and criteria, the collapsed help blocks, the reflection's aiContext, the interim Dojo Lab prompts. Nothing from Leslie's own run appears in the material.
