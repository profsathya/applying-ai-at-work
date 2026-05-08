---
type: quiz
title: "Week 1 Code Reading Quiz"
slug: week-1-code-reading-quiz
artifact_id: course4-sprints-sprint-0-week-1-code-reading-quiz
sprint: 0
week: 1
module: "Module 1: Code, Abstraction, Functions, and Basic Reliability"
position: 13
points: 10
submission_type: online_quiz
publish: false
questions:
  - type: multiple_choice
    prompt: "What is the main purpose of a function?"
    points: 1
    answers:
      - text: "To give a reusable name to a block of behavior"
        correct: true
      - text: "To make code impossible to change"
        correct: false
      - text: "To remove the need for inputs"
        correct: false
      - text: "To hide all errors from the user"
        correct: false
  - type: multiple_choice
    prompt: "In the expression total = price + tax, what is total?"
    points: 1
    answers:
      - text: "A variable storing the result of adding price and tax"
        correct: true
      - text: "A function definition"
        correct: false
      - text: "An exception"
        correct: false
      - text: "A command line argument"
        correct: false
  - type: true_false
    prompt: "The same AI coding prompt is guaranteed to produce the same code every time."
    points: 1
    answers:
      - text: "True"
        correct: false
      - text: "False"
        correct: true
  - type: multiple_choice
    prompt: "Why are docstrings useful?"
    points: 1
    answers:
      - text: "They explain what a function does and how it should be used"
        correct: true
      - text: "They make Python ignore all errors"
        correct: false
      - text: "They replace the need to run the program"
        correct: false
      - text: "They turn strings into numbers automatically"
        correct: false
  - type: multiple_choice
    prompt: "Which Python error is most directly related to dividing by zero?"
    points: 1
    answers:
      - text: "ZeroDivisionError"
        correct: true
      - text: "NameError"
        correct: false
      - text: "IndentationError"
        correct: false
      - text: "FileNotFoundError"
        correct: false
  - type: short_answer
    prompt: "In one or two sentences, explain the difference between input and output in a program."
    points: 1
  - type: short_answer
    prompt: "Name one thing you should check before trusting AI-generated code."
    points: 1
  - type: essay
    prompt: "Read this function: def double(x): return x * 2. Explain the input, the operation, and the output."
    points: 1
  - type: essay
    prompt: "Explain why a useful error message can make a program more reliable."
    points: 1
  - type: essay
    prompt: "Describe one way the calculator analysis lab helped you understand code reading."
    points: 1
---

# Week 1 Code Reading Quiz

Use this quiz to check whether you can read basic Python structure and explain what small pieces of code do.

Focus on behavior. Do not rush through the questions as vocabulary recall.

## Answer Key

1. A function gives a reusable name to a block of behavior.
2. `total` stores the result of adding `price` and `tax`.
3. False.
4. Docstrings explain what a function does and how it should be used.
5. `ZeroDivisionError`.
6. Strong answers explain that input is information received by the program and output is information returned, printed, or otherwise produced.
7. Strong answers include inputs, outputs, errors, assumptions, libraries, tests, or whether the code solves the intended problem.
8. Strong answers identify `x` as input, multiplication by 2 as the operation, and the doubled value as output.
9. Strong answers explain that error messages help people diagnose and recover from failure.
10. Strong answers connect the lab to reading functions, tracing input/output, checking assumptions, or debugging generated code.
