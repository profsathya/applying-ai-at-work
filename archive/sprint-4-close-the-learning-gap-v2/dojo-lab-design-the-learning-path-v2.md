---
type: assignment
title: 'Dojo Lab: Design the Learning Path'
slug: dojo-lab-design-the-learning-path-v2
artifact_id: course1-sprints-sprint-4-close-the-learning-gap-v2-dojo-lab-design-the-learning-path-v2
sprint: 8
week: 7
module: 'Sprint 4: Close the Learning Gap (V2)'
position: 4
points: 35
submission_type: text_entry
publish: false
rubric:
  - description: Own gap list written before the Dojo, with blocking, useful, and interesting marked honestly
    points: 5
  - description: What is already understood well enough is named, with how you know
    points: 2
  - description: The committed gap names the decision waiting on it and what would change in the frame
    points: 5
  - description: Learning path is five steps or fewer and sequenced toward the decision, not toward the topic
    points: 5
  - description: Each step names its source and what would count as knowing it
    points: 3
  - description: Two claims identified that the frame rests on, each with a check that could come back negative
    points: 7
  - description: Exclusions carry a named risk and a check small enough to run, and the Dojo pushback is recorded
    points: 3
  - description: Decision record distinguishes kept, rejected, and still open, and at least one rejection names what it cost
    points: 3
  - description: First check and backup are chosen, with the choice justified
    points: 2
---

# Dojo Lab: Design the Learning Path

Turn a gap into something you can close in a week. First write down what you think you don't know, then use AI to sequence it, test whether your checks are real, and attack what you've decided to skip.

## Start with What You Already Know You Do Not Know

Before bringing in the Dojo, write your own gap list. Ask any AI what someone working on your problem would need to learn and it will hand you a clean, sensible, complete-looking list. It will be right in general and wrong about you, and you won't be able to tell the difference unless you wrote yours first.

Open your Sprint 3 conversation report, your revised problem statement, and your Goal Plan, and look for three things:

- Something the stakeholder said that you had no response to.
- Something still marked *inferred* that the frame depends on.
- Something you've been describing vaguely because you don't actually know the specifics.

That third one is the most productive and the easiest to miss.

### 1. What you don't know yet

List five to eight gaps. One line each, and a mark:

- **Blocking:** a decision or next step is waiting on this.
- **Useful:** it would improve the work, but nothing is stopping.
- **Interesting:** you want to know it. Be honest about which is which.

### 2. What you already understand well enough

Two or three things about this problem you understand well enough to act on right now, with one line each on how you know.

This section is short and it matters. Without it, a sprint about what you don't know quietly becomes an audit of everything you've ever not known, which is both demoralising and unbounded. Naming what's solid tells you where the edge actually is.

"How you know" is the important half. If the honest answer is "someone told me once" or "I've always assumed," that isn't solid ground. It's a gap you hadn't noticed. Move it up to the list above.

### 3. The gap you're committing to

Pick one from the blocking list and write a short paragraph: what specifically you don't know, what decision is waiting on it, and what would change in your problem frame if the answer went one way rather than the other. That last question is the real test. If the answer changes nothing in your frame, you've picked a Useful or an Interesting one.

> **Quick self-check.** Could you finish the sentence "until I know this, I can't ___"? If not, keep looking.

### What this looks like

*Problem: new hires wait an average of nine days for system access, and nobody owns the handoff between IT and the hiring manager.*

**Gap list (partial).** How our ticket system measures ticket age: *blocking*. Whether the nine-day figure counts weekends: *blocking*. Who owns the offboarding equivalent: *useful*. How service-level agreements are designed in general: *interesting*.

**Already good enough.** Who the handoff runs between: I've watched it happen twice and both hiring managers described it the same way. What new hires actually need access to on day one: I have the checklist and I've compared it against what two recent hires said they were missing.

**Committed gap.** I don't know how our system counts the age of a ticket that gets reassigned. My whole frame rests on nine days being real. The decision waiting on it is whether I take this to the IT lead as a process problem or go back and re-measure first. If ticket age resets on reassignment, the true wait is longer than nine days and the handoff problem is worse than I've been saying. If it doesn't, my number holds and I can move.

## Use the Dojo

Use the [Open the Symbiotic Thinking Dojo](https://dojo.symbioticthinking.ai/) link for this lab. First-time users should open Learn About -> Privacy & Setup and configure a Gemini API key in the browser before starting.

[TODO] Dojo setup steps and API key instructions, pending the team decision and the Dojo Setup page in the Welcome module. Same block that holds Sprint 1's Dojo Lab.

Do not paste confidential workplace, client, education, patient, or personal data into the Dojo. De-identify details and keep sensitive information out of the prompt.

Use this prompt with the Dojo:

```text
I am trying to close this gap in what I know:
[paste your committed gap]

Here is the problem it is blocking:
[paste your problem statement]

Here is the decision waiting on it:
[paste]

Use Learn + Solve mode. Start with @framer. Help me sequence:
1. What is the smallest set of things I need to learn to make that
   decision, not to understand the topic, to make that decision?
2. What order, and what would count as knowing each one?
3. What source teaches each one fastest?
4. Cut this sequence in half. What is lost?
5. Where is this plan too broad, too vague, or disconnected from
   the problem I actually described?

Then use @auditor:
- Which claims here would actually change my frame if they were wrong?
- For each check I have planned, what would it fail to catch?
- Where am I about to verify an AI explanation with another AI explanation?

Then use @challenger:
- Here is what I have decided not to learn: [paste your exclusions].
- Make the case that I am avoiding rather than focusing.
- What could go wrong that I have not named?
```

Review the Dojo output as preparation, not evidence. Do not treat the Dojo as a source.

Keep the session. You'll need what it offered and what you turned down in Part 2.

[TODO] Link to the Dojo how-to video, 3 to 5 minutes. Added on the Canvas page after publish.

## Build Your Learning Path, Part 1

After working with the Dojo, write out the path. Five steps maximum. For each step, record the following:

| Field | What to record |
| :---- | :---- |
| Step | What you'll learn, stated narrowly enough to finish |
| Why it's in the path | What it contributes to the decision |
| Source | The actual one. "Our admin console," not "documentation" |
| What counts as knowing it | Something you could point at, not a feeling |
| Roughly how long | Your estimate. You'll compare it against reality next week |

Five steps is a ceiling, not a target. Three is often right. If the path doesn't fit in five, the gap was a topic.

## Build Your Learning Path, Part 2

Now step back from the path and add these four items below it.

### 1. What you are choosing not to learn

Two things from your gap list you're deliberately setting aside. For each: why it's reasonable now, what risk it creates, and the smallest check that would catch that risk.

Then record what **@challenger** came back with, and what you did: kept it, tightened the check, or moved it into the path. An exclusion nobody argued with usually wasn't tested.

### 2. The two claims you will check

Identify the two claims your frame will rest on once the learning is done, and design a check for each. A check has three parts: the claim stated so it could be false, what you'll check it against, and the result that would tell you you were wrong.

Some examples of weak versus strong checks:

- **Weak:** "I'll verify this with documentation." Which documentation, and what would it have to say for you to change your mind? This can't fail, so it isn't a check.
- **Strong:** "I'll open our own admin console and look at how ticket age is calculated. If reassigned tickets start a new count, my nine-day figure is wrong and I have to re-measure before I take this anywhere."
- **Weak:** "I'll ask AI to double-check its answer." An explanation checked against another explanation from the same kind of source is still one source.
- **Strong:** "I'll ask the service desk lead what actually happens to a ticket when it gets handed to another team."

**At least one of your two checks must involve a person.** Documentation, data, and policy tell you what a system is supposed to do. Only a person can tell you what actually happens.

### 3. Your first check and your backup

Name the person you'll go to for the human check, and a backup in case they don't respond. Then explain your reasoning: why this person first?

Some strong reasons to ask someone first:

- They can settle the claim that most of your frame is standing on.
- They do the work daily, so the gap between the official process and the real one is visible to them and not to you.
- You already have a relationship. Your Sprint 3 stakeholder is a legitimate choice, and following up with a specific question is often easier than a first ask.
- They control or maintain the system your claim is about.

### 4. How the Dojo changed the plan

This is the part people skip, and it's the part that shows you directed the learning rather than outsourced it.

For each significant thing the Dojo offered, say what you did with it and why:

- **Kept.** What you took, and what it improved.
- **Rejected.** What you turned down, what was appealing about it, and what you gave up by rejecting it.
- **Still open.** What you can't settle yet, and what would settle it.

Compare these two:

> The Dojo's plan was too long so I shortened it.

> It wanted me to learn how service-level agreements are designed before looking at our own configuration. That's the right order for understanding the topic and the wrong order for my decision. I need to know what our instance does, and the general theory only matters if ours turns out to be standard. I dropped it. If our configuration is unusual I'll have no baseline to compare against, and I'll have to come back for it.

The second names the rejection, what it cost, and where it might bite. Write the second kind.

Then two or three sentences on how the plan differs from what you'd have written alone. If it doesn't differ, say why the alternatives didn't improve on it. Holding your ground is legitimate when you can defend it.

## Submission Format

Submit your gap list, what you already understand well enough, your committed gap, your learning path, and all four items from Part 2 as a text entry in Canvas.

## Portfolio Capture

Save this learning path with your portfolio, along with the AI suggestions you rejected or narrowed. Those are what show you directed the learning rather than outsourcing it. The path becomes the plan you run in Learn and Verify, and the two checks you designed here are the ones you'll log there.
