---
type: quiz
title: "Week 2 Code Reading Quiz"
slug: week-2-code-reading-quiz
artifact_id: course4-sprints-sprint-1-week-2-code-reading-quiz
sprint: 1
week: 2
module: "Module 2: Data Models, Control Flow, Objects, Files, and Testing"
position: 12
points: 10
submission_type: online_quiz
publish: false
questions:
  - type: multiple_choice
    prompt: "When is a set a better choice than a list?"
    points: 1
    answers:
      - text: "When uniqueness and membership checks matter most"
        correct: true
      - text: "When duplicate order must be preserved"
        correct: false
      - text: "When every value needs a named key"
        correct: false
      - text: "When code should never loop"
        correct: false
  - type: multiple_choice
    prompt: "What is an object useful for?"
    points: 1
    answers:
      - text: "Grouping related data and behavior"
        correct: true
      - text: "Avoiding all tests"
        correct: false
      - text: "Replacing every dictionary automatically"
        correct: false
      - text: "Running code without Python"
        correct: false
  - type: true_false
    prompt: "A support ticket system should be defined before asking AI to generate or extend it."
    points: 1
    answers:
      - text: "True"
        correct: true
      - text: "False"
        correct: false
  - type: multiple_choice
    prompt: "What does a pytest assertion check?"
    points: 1
    answers:
      - text: "Whether an expected condition is true"
        correct: true
      - text: "Whether the code uses inheritance"
        correct: false
      - text: "Whether AI wrote the code"
        correct: false
      - text: "Whether a file is published to Canvas"
        correct: false
  - type: multiple_choice
    prompt: "Which structure best represents named fields like title, supportee, and warning_level?"
    points: 1
    answers:
      - text: "Dictionary"
        correct: true
      - text: "Set"
        correct: false
      - text: "While loop"
        correct: false
      - text: "Exception"
        correct: false
  - type: short_answer
    prompt: "Name one field that belongs in the support ticket system and explain why it matters."
    points: 1
  - type: short_answer
    prompt: "What is one reason to write your own test even when starter code is provided?"
    points: 1
  - type: essay
    prompt: "Explain the difference between a for loop and a while loop in your own words."
    points: 1
  - type: essay
    prompt: "Describe one feature you might use to predict phone price and why it could matter."
    points: 1
  - type: essay
    prompt: "Explain why defining a system before prompting AI can improve the result."
    points: 1
---

# Week 2 Code Reading Quiz

Use this quiz to check whether you can read and reason about objects, collections, control flow, and tests.

## Answer Key

1. A set is useful when uniqueness and membership checks matter most.
2. Objects group related data and behavior.
3. True.
4. A pytest assertion checks whether an expected condition is true.
5. A dictionary represents named fields well.
6. Strong answers name a field such as title, text, supportee, warning level, classification, or status and connect it to system behavior.
7. Strong answers mention checking assumptions, edge cases, bugs, AI-generated code, or behavior that starter tests omit.
8. Strong answers explain that a `for` loop processes items in a collection, while a `while` loop continues until a condition changes.
9. Strong answers connect a feature to plausible price difference and acknowledge that it still needs testing.
10. Strong answers explain that clear definitions keep AI from inventing the system's meaning.
