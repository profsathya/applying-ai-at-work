---
type: assignment
title: "LLM Analysis: A Basic Calculator"
slug: llm-analysis-basic-calculator
artifact_id: course4-sprints-sprint-0-llm-analysis-basic-calculator
sprint: 0
week: 1
module: "Module 1: Code, Abstraction, Functions, and Basic Reliability"
position: 8
points: 25
submission_type: text_entry
publish: false
rubric:
  - description: "Explains the starter calculator structure and major functions"
    points: 6
  - description: "Identifies at least three assumptions, risks, or missing checks"
    points: 6
  - description: "Improves or proposes improvements with clear reasoning"
    points: 6
  - description: "Uses AI as an explanation and debugging partner without outsourcing judgment"
    points: 4
  - description: "Includes evidence from running or testing the code"
    points: 3
---

# LLM Analysis: A Basic Calculator

## Purpose

Analyze a pre-generated calculator program so you can practice reading generated code without having to compare different AI outputs.

Everyone will use the same starter code. The point is not whether AI can create a calculator. The point is whether you can understand what the calculator does, where it can fail, and how to improve it.

## Starter Code

Use the calculator code provided by your instructor. Do not generate a new calculator from scratch for this assignment.

The starter should include:

- Functions for addition, subtraction, multiplication, and division.
- A simple command line interface.
- User input.
- At least one place where input can fail or behave unexpectedly.

## Part 1: Read The Code

Write a short explanation of:

1. What each function does.
2. What inputs each function expects.
3. What output each function returns or prints.
4. Where the command line interface starts.
5. What happens if the user enters unexpected input.

## Part 2: Use AI For Explanation

Ask Copilot or the approved AI assistant to explain one part of the calculator.

Use a prompt like:

```text
Explain this calculator code for a beginner. Focus on inputs, outputs, functions, and places where it could fail. Do not rewrite the code yet.
```

Then compare the AI explanation with your own reading.

## Part 3: Refine And Debug

Choose two improvements:

- Better error handling for division by zero.
- Better handling when the user types text instead of a number.
- Clearer function names.
- A docstring for each function.
- A loop that lets the user keep calculating until they quit.
- A clearer message for invalid operations.

Run the code after each improvement.

## Submission

Submit:

- Your explanation of the original calculator.
- The AI prompt you used and the most useful part of the response.
- The two improvements you made or proposed.
- Evidence that you ran the program, such as example inputs and outputs.
- One paragraph explaining what you trust about the final code and what you would still test.

## Review Question

What did the AI explanation make easier to understand, and what did you still need to verify yourself?
