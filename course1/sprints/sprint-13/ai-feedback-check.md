---
type: quiz
title: 'AI Feedback: What Changed and Try It'
slug: ai-feedback-check
artifact_id: course1-sprint-13-ai-feedback-check
sprint: 13
week: 1
module: AI Feedback Check
position: 1
points: 0
submission_type: file_upload
delivery_mode: ai_activity
publish: true
learner_labels: true
omit_from_final_grade: true
completion_requirement: none
ai_activity:
  activity_id: course1-sprint-13-ai-feedback-check
  version: "1.0"
  title: 'AI Feedback: What Changed and Try It'
  description: >-
    Optional, ungraded service check. The previous AI connection failed the
    Sprint 4 request with "Empty response from AI service." A CTI-owned
    replacement now handles requests, and updated configuration links prevent
    browsers from retaining the old connection. Try generating three questions,
    saving a response, and exporting it. No Canvas submission is required.
  questions:
    - id: q1-feedback-check
      type: ai-discussion
      prompt: >-
        Copy this fictional diagnostic sample into the response box, then select
        Get Follow-up Questions: "I need to learn whether handover delays come
        from missing information or unclear ownership. Until I know this, I
        cannot choose between a checklist and an assigned owner. The gap is
        closed when five recent handovers show where each delay began and who
        could resolve it." This checks the service using sample text; no prior
        coursework is needed. After three questions appear, write a brief
        response of at least 30 characters explaining one useful challenge or
        something you would question. Select Save Response, enter "Demo Check" in the name field, then use the export
        control to inspect your JSON. You can stop there without submitting to
        Canvas. The AI does not grade or submit your work.
      placeholder: Paste the fictional handover sample above (at least 120 characters).
      minLength: 120
      numQuestions: 3
      aiContext: >-
        This is an optional diagnostic check of the course AI feedback service
        using a clearly fictional handover example. Generate three focused
        questions that challenge the connection between the missing knowledge
        and the decision, whether closing the gap would be observable, and
        whether a different answer would change the proposed action. Keep the
        questions concrete and answerable from this example. Do not invent
        stakeholder evidence or treat the example as a participant's actual
        workplace. The participant retains judgment about the questions.
      generateButtonText: Get Follow-up Questions
      loadingText: Generating follow-up questions...
      discussionPrompt: >-
        Read the three questions. In at least 30 characters, explain one useful
        challenge or something you would question. Save your response, then
        export the JSON to check that it contains the sample, questions, and
        your response. This optional check ends there; no Canvas upload is needed.
      summaryLabel: Your Check of the Feedback
      summaryPlaceholder: Explain one useful challenge or something you would question (at least 30 characters).
      saveButtonText: Save Response
      updateButtonText: Update Response
      digDeeperText: Try another round of questions
---

# AI Feedback: What Changed and Try It

Try the repaired AI connection with the sample below. This optional, ungraded check needs no prior coursework or Canvas submission. It is excluded from the final grade.

## What Was Broken

The previous connection between the activity and the AI provider returned **“Empty response from AI service”** for the Sprint 4 request. A tiny test request worked, so the service was not completely offline. The underlying cause was not confirmed.

## What Changed

The activities now use a CTI-owned replacement service. Updated configuration links also prevent browsers from holding onto the old connection. The repaired flow generates questions, saves your response, and exports it. AI does not grade or submit your work.

## Try It

Open the interactive activity and paste this **fictional diagnostic sample** into the response box:

> I need to learn whether handover delays come from missing information or unclear ownership. Until I know this, I cannot choose between a checklist and an assigned owner. The gap is closed when five recent handovers show where each delay began and who could resolve it.

1. Select **Get Follow-up Questions**. Three questions should appear about the gap, the decision, and what evidence would close it. Wording can vary.
2. In **Your Check of the Feedback**, explain one useful challenge or something you would question. Use at least 30 characters so the response can be saved.
3. Select **Save Response**, enter **Demo Check** in the name field, then use the export control to inspect the JSON containing the sample, generated questions, and your response.

You have checked generation, saving, and export when all three are present. You can stop without uploading anything to Canvas. This checks the service; it does not establish that every AI suggestion is sound.
