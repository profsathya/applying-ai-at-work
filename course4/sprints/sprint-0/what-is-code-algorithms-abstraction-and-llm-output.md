---
type: page
title: "What Is Code? Algorithms, Abstraction, and LLM Output"
slug: what-is-code-algorithms-abstraction-and-llm-output
artifact_id: course4-sprints-sprint-0-what-is-code-algorithms-abstraction-and-llm-output
sprint: 0
week: 1
module: "Module 1: Code, Abstraction, Functions, and Basic Reliability"
position: 4
points: null
submission_type: none
publish: false
---

# What Is Code? Algorithms, Abstraction, and LLM Output

Code is a written set of instructions that a computer can execute. Good code is also communication for people. It names ideas, records decisions, and makes behavior repeatable.

When you read code, ask three questions:

1. What information does this code use?
2. What steps does it follow?
3. What result or side effect does it produce?

Those questions matter more than memorizing every symbol.

## Algorithms

An algorithm is a sequence of steps for solving a problem.

Example:

```python
def total_price(price, tax_rate):
    tax = price * tax_rate
    return price + tax
```

This function has a small algorithm:

1. Take a price and a tax rate.
2. Multiply the price by the tax rate.
3. Add the tax to the original price.
4. Return the total.

The code is short, but the structure matters. Inputs enter. Steps happen. Output leaves.

## Abstraction

Abstraction means hiding details behind a simpler idea.

When you call `total_price(20, 0.095)`, you do not need to think about every arithmetic step each time. The function name lets you work at a higher level.

Programs use many layers of abstraction:

- Values: numbers, strings, booleans, tuples, lists, dictionaries.
- Operations: addition, comparison, membership checks, formatting.
- Functions: named procedures with inputs and outputs.
- Files: reusable scripts and modules.
- Applications: groups of files that work together.

AI tools often generate code at a high abstraction level. They may create functions, classes, imports, and helper files before you understand the layers. Your job is to bring the code back down to questions you can answer.

## Non-Deterministic Code Generation

Most programming code is deterministic: the same inputs should produce the same outputs when the environment is the same.

AI code generation is different. The same prompt can produce different code. A small change in wording can produce a different structure, a different library, or a different assumption about what you meant.

That is why understanding matters. If you only trust the output because it looks technical, you have not gained control. You have only moved the uncertainty somewhere harder to see.

## Reading Generated Code

When an AI tool produces code, read it in layers:

1. What files, libraries, or tools does it assume exist?
2. What inputs does the code expect?
3. What outputs or side effects does it produce?
4. What errors can happen?
5. What does the code not check?
6. What would you test before trusting it?

Use AI as a partner for explanation, but keep your own judgment active.

## Reflection Prompt

Before moving on, write a three-sentence note for yourself:

1. One thing code does for a computer.
2. One thing code communicates to a person.
3. One reason AI-generated code still needs a human reader.
