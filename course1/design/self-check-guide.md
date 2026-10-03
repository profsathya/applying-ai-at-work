---
purpose: The one guide for writing and reviewing a Self-check for any 50-point item in CIS 501, agreed by Leslie and Melisa on 1 October 2026 from Sathya's Self-check model and grading rules; use it for each activity, alone or with a Claude session
status: v0.1, 1 October 2026
depends_on: course-wide-list.md (items 39, 41, 43, 46); Common-Curriculum skills/writing-assignments/references/rules.md (Criteria for success); cti-chief-of-staff skills/assignment-review/references/rules.md (Self-check items, 27 September); sprint-1-self-checks.md; sprint-3-stakeholder-map-rubric.md
---

# Self-check guide

A Self-check is the list of scored lines for a 50-point item. The same list serves the learner checking a draft, the grader scoring it, and the AI first pass Jeremy is building. One record per item, in `course1/design/`, holds everything; the page shows only the full-points lines.

## 1. The rules we agreed (Leslie and Melisa, 1 October)

1. **Five lines is the target, eight is allowed, ten is the ceiling.** More lines only when a line tests two things that can fail for different reasons.
2. **Each line is one observable statement of what full points looks like**, in the page's own words, with its points. Never "I wrote". The learner sees these lines and their points on the page. Nothing else from the record is on the page.
3. **Points per line are set by what the line carries and add up to 50.** The heaviest lines are the ones the next sprint depends on.
4. **Passing is 35 of 50.** Points are added across lines; 35 or more passes.
5. **Three rungs per line, no scores between them.** Full, 3, and 1. A 3 earns about 70 percent of the line, a 1 about 20 percent, rounded. Partial on every line lands at about 35, which passes by design.
6. **The 3 rung is the pass standard for the line.** Write it as the minimum a passing learner reaches. Anything below it scores the 1 rung. The 1 rung is the comment for the learner who did not reach the 3; it is short, and it names the common way of missing.
7. **Rung text is written for the learner.** It stays off the page but comes back in the grading comment, reworded. It names the thinking that fell short, not the box.
8. **Each line has a rank, 1 to N, no ties.** The grader comments on the top one or two missed lines by rank; the rest appear as one clause each in the grading line. Rank by what the next sprint depends on.
9. **Each line has a tag**: completeness, specificity, honesty, or judgment. One per line; it feeds the course's quality tracking, never the comment.
10. **A gate rule where the assignment's core thing can be absent.** Fewer than two frames, no pasted frame, fewer than two stakeholders: not a pass, whatever the other lines score. Points cannot do this alone; a rule does.
11. **"All" on the page, a count in the rungs.** The line says "all the people who feel this"; the 3 rung triggers on "only one named."
12. **Judged across the set.** Where a submission repeats a structure (frames, stakeholder tables), each quality line scores once over the whole set: full when every one passes, 3 when most do, 1 when few or none. Only the count line counts.
13. **Grader lines in every record.** Read for meaning: if the idea is there in the learner's own words, give the points. A blank part is a 1 on its line, not a 0 on the item. Every rung below full names the part, and the frame or table, it rests on.
14. **The rungs are a draft until the first batch.** Sathya sets his 3 and 1 rungs from the first real submissions. Write them now as a best guess, grade the first batch, revise, and share what you learned with the other sprint owners before their batch arrives.

Still open: where the lines render on the page (Jeremy's renderer, list item 39), and how Jeremy's grader reads the record (item 46).

## 2. The record shape

One section per item:

```
## <Item title>, 50 points

Submission: <what the learner hands in>. <Judged across the set, if it applies.>

| # | On the page (the full-points line) | Pts | 3 rung (pts) | 1 rung (pts) | Rank | Tag |

Total: 50. Passing: 35.

Gate: <rule, if any>.

Grading note. <set judgment; cite the part; read for meaning; blank is a 1>.

What makes it strong. <how the parts connect, so a learner can test a draft against it; not a sixth line>.

Open. <questions for the first-batch revision>.
```

## 3. The review pass, line by line

Do these in order, for each item. Each is a question you answer by looking at the page and the draft.

1. **Read the full-points lines as the learner will.** One cell or box per line, in the page's words. Could you check it against a draft by looking? If a line checks two cells, split it. If it paraphrases the page, use the page's words.
2. **Ask what the real test is.** The common failure is not the test. "No fix in it" was a symptom; "names a gap" was the test. Write the line as the test; the failure goes in the 1 rung.
3. **Check the points.** Add to 50. Heaviest where the next sprint depends on it. Partial everywhere should land at or just above 35.
4. **Write the 3 rung as the pass standard.** What is the least a passing learner has on this line? One sentence, to the learner.
5. **Write the 1 rung as the comment.** The common way of missing, and what to do instead. Short.
6. **Ask what the grader would quote.** Every rung below full must rest on something in the submission text, with the part and the frame or table named.
7. **Rank the lines, no ties.** If a learner misses several, which fix unlocks the most? Order by what the next sprint depends on.
8. **Tag each line.** One of four.
9. **Set the gate, if the core thing can be absent.**
10. **Decide set versus per-table** where the submission repeats a structure.
11. **Write "what makes it strong"** as connections between parts.
12. **Note the open questions** for the first-batch revision.

## 4. A worked example

First frames, 50 points, as settled on 1 October; on-the-page lines in plain language, 3 October. Six lines; lines 2 to 6 judged across every frame submitted; gate: fewer than two frames does not pass.

| # | On the page | Pts | 3 rung (pts) | 1 rung (pts) | Rank | Tag |
|---|---|---|---|---|---|---|
| 1 | You submitted at least three frames, and every part of each one is filled in or says, "I do not know yet." | 10 | Two frames, every part filled or marked. Two gives you a runner-up; three gives the Dojo Lab a real choice. (7) | One frame, or frames with most parts blank. (2) | 6 | completeness |
| 2 | In each frame, Part 2 says what is going wrong and who it is going wrong for, in one or two sentences. | 8 | A gap is named, but either who it happens to or what goes wrong is unclear. Say both. (6) | Part 2 is a task, a complaint, or a solution, not a gap. Go back to your table and start from the gap. (2) | 1 | judgment |
| 3 | In each frame, Part 5 describes what it would look like if the problem in Part 2 were solved, without saying how to solve it. | 8 | A changed situation is described, even if a fix is named with it or it does not fully match Part 2. Describe the day after this gap is closed. (6) | Part 5 is a solution, such as "build an app," or is missing. Describe what would be different, not how. (2) | 3 | judgment |
| 4 | In each frame, Part 3a names everyone who feels this problem, and Part 3b says what it costs each of them: time, money, mistakes, or stress. | 8 | Only one person or role is named, or some named people have no cost. A gap usually touches more than one person: who else feels it, and what does it cost them? (6) | One vague group, such as "everyone," or a cost with nobody attached. Start from who feels this and say what each one loses. (2) | 4 | specificity |
| 5 | In each frame, Part 4 says how people deal with this problem now and where that stops working. | 6 | The current habit, process, or workaround is there, but not where it falls short. Say what it does not cover. (4) | A fix or a "should" instead of what people do today. Describe the current habit first. (1) | 5 | specificity |
| 6 | In each frame, Part 6 lists at least four assumptions, and each one says which part of the frame it comes from and who could tell you whether it is true. | 10 | Four assumptions, but some do not say which part or who could tell you. Each line needs both: that is how Sprint 2 knows where to look. (7) | Fewer than four, or none names who could tell you. Reread parts 2 to 5 and mark every sentence you have not seen yourself. (2) | 2 | honesty |

Total 50. Passing 35. Partial on every line gives 36.

## 5. Working through an item with Claude

Paste this into a Claude session that can read the repo, with the item's file path:

> Read `course1/design/self-check-guide.md` and the page at `<path to the item's .md file>`. Draft the Self-check record for this item in the guide's record shape, following section 1's rules. Use the page's own words for each full-points line. Then walk me through section 3 one question at a time, line by line, and wait for my answer before moving on. When we finish, write the record to `course1/design/<sprint>-self-checks.md` and open a pull request for me to merge.

Answer each question as you would in conversation; the session applies the change and shows the revised line. Expect to disagree with a few lines: that is the review working.
