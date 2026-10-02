---
type: quiz
title: Directing AI Check
slug: directing-ai-check
artifact_id: course1-sprints-sprint-2-directing-ai-check
sprint: 2
week: 3
module: 'Sprint 2: Direct AI Deliberately'
position: 8
points: 5
submission_type: file_upload
delivery_mode: ai_activity
publish: false
ai_activity:
  activity_id: course1-directing-ai-check
  version: "1.0"
  title: Directing AI Check
  description: Use AI follow-up questions to check how well you provided context, considered choices, and planned confirmation.
  questions:
    - id: q1-context-choices-confirmation
      type: ai-discussion
      prompt: >
        Describe one recent AI interaction from this sprint. What context did you
        provide, what choices or tradeoffs did you ask AI to surface, and what
        still needs confirmation outside AI?
      placeholder: >
        Use a real prompt or output. Name the context you gave, the options AI
        returned, and the evidence you would need before acting on the output.
      minLength: 110
      numQuestions: 3
      aiContext: >
        This is a Sprint 2 concept check on directing AI deliberately. The
        participant should show context, choices, and confirmation in a real AI
        interaction. Push vague answers toward specific constraints, audience,
        purpose, tradeoffs, assumptions, and external verification. Challenge any
        claim that confidence from AI is the same as confirmed evidence.
      generateButtonText: Get Follow-up Questions
      loadingText: Generating follow-up questions...
      discussionPrompt: >
        Use the follow-up questions to revise your answer. Your refined response
        should show how your judgment improved or limited the AI output.
      summaryLabel: Your Refined Check Response
      summaryPlaceholder: >
        Rewrite your answer with concrete context, the choices or tradeoffs AI
        surfaced, and the confirmation step needed before using the output.
      saveButtonText: Save Response
      updateButtonText: Update Response
      digDeeperText: Dig deeper with AI guidance
---

# Directing AI Check

## Purpose

Check whether you can direct AI deliberately instead of accepting the first fluent answer. This is an applied AI-guided check on context, choices, confirmation, prompt iteration, and output assessment.

## How It Works

1. Write about one real AI interaction from this sprint.
2. Generate AI follow-up questions.
3. Revise your answer so it shows the context you provided, the choices you considered, and what still needs confirmation.
4. Use the deeper AI guidance button if the answer does not yet show your judgment.
5. Save the refined response in the activity.

## What To Submit

Download the JSON response file from the activity and upload it to Canvas. Your final response should show how your judgment changed the AI output or limited what you were willing to trust.
