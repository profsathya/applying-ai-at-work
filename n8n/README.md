# Grading Automation (n8n)

Grading lives in n8n, not in this repo's runtime. The repo is course-content; the n8n workflow is a separate service that reads canvas submissions, drafts feedback and scores, routes to a HITL review queue, and posts approved grades back to canvas.

## Why n8n and not GitHub Actions

- Already in the CTI stack.
- Webhook-shaped flows are n8n's sweet spot.
- Existing SRL-grounded prompt templates live in n8n.
- Iterating on grading prompts is easier in n8n's UI than editing YAML.

GHA still has a role (see `.github/workflows/`), but for schema validation on PRs, not grading.

## Workflow overview

```
Canvas submission webhook
        |
        v
Fetch submission + rubric + assignment body
        |
        v
Build grading prompt (rubric + SRL framing + student submission)
        |
        v
Claude API call -> {score, rubric_breakdown, feedback_comment, flags}
        |
        v
Write to review queue (Google Sheet or Notion DB)
        |
        v
Notify instructor on Slack
        |
        v
(HITL gate: instructor approves, edits, or rejects)
        |
        v
On approve: Canvas API PUT grade + comment
        |
        v
Log to audit sheet
```

## Import the workflow

1. In n8n, go to Workflows > Import from File.
2. Import `grading-workflow.json`.
3. Set these credentials:
   - Canvas OAuth2 or personal access token (same as the one in this repo's `.env`)
   - Anthropic API key
   - Google Sheets or Notion (for the review queue)
   - Slack webhook or bot token
4. Configure the webhook URL in canvas: Course > Settings > Webhooks > Add webhook for `submission_created` and `submission_updated` events.

## The grading prompt

See `grading-prompt-template.md`. The template uses these variables:

- `{{ rubric }}` - rubric from the assignment's MD frontmatter (pulled via GitHub API or a local repo clone)
- `{{ assignment_body }}` - the assignment prose as shown to students
- `{{ submission }}` - the student's submission text
- `{{ student_context }}` - optional: prior SRL-O data, prior reflections (Jeremy's research context)

The prompt is SRL-grounded: it explicitly asks for feedback that supports self-regulated learning phases (forethought, performance, self-reflection) rather than just evaluative feedback.

## HITL gate

Two options for the approval step:

### Option A: n8n's built-in human-approval node (recommended)

n8n v1.50+ has a "Wait" node with human-approval semantics. The workflow pauses, the instructor gets a link to a hosted approval UI, and clicks approve / edit / reject.

### Option B: Google Sheet with Apps Script

Each row is a pending submission with drafted score and comment. Instructor clicks an "Approve" checkbox; an Apps Script onEdit trigger fires a second n8n webhook with the row data to resume the workflow.

Option A is cleaner if you're on n8n v1.50+. Option B works anywhere and gives you an audit trail in the sheet itself.

## What gets logged

For every submission, the audit log captures:

- Student ID
- Assignment ID and title
- AI-drafted score
- AI-drafted feedback
- Instructor-edited score (if any)
- Instructor-edited feedback (if any)
- Final posted score
- Timestamp of each stage

This is research-grade data. For a dissertation examining AI-enhanced feedback (like Jeremy's), it's the same audit trail needed to analyze "AI draft vs instructor final" gaps as a signal of feedback quality.

## Security notes

- The Canvas API token in n8n should be scoped to grading-only if possible.
- The Anthropic API key should be project-scoped with usage limits.
- Review queue data contains student PII; follow your institution's FERPA guidance on storage.
