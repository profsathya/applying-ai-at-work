---
type: page
title: "Functions, Documentation, and Your First Program"
slug: functions-documentation-and-your-first-program
artifact_id: course4-sprints-sprint-0-functions-documentation-and-your-first-program
sprint: 0
week: 1
module: "Module 1: Code, Abstraction, Functions, and Basic Reliability"
position: 5
points: null
submission_type: none
publish: false
---

# Functions, Documentation, and Your First Program

A function is a named block of code that performs a task.

Functions are useful because they let you:

- Give a name to a process.
- Reuse logic without rewriting it.
- Separate inputs, behavior, and output.
- Test one small piece of a program.

## A First Function

```python
def greet(name):
    message = "Hello, " + name
    return message
```

Read this function slowly:

- `def` starts a function definition.
- `greet` is the function name.
- `name` is an input.
- `message` stores a string.
- `return` sends a result back to whoever called the function.

You can call it like this:

```python
print(greet("Ari"))
```

The output is:

```text
Hello, Ari
```

## Running A Program

Create a file named `hello.py`:

```python
def greet(name):
    message = "Hello, " + name
    return message


print(greet("Ari"))
```

Run it from your terminal:

```bash
python hello.py
```

If your system uses `python3`, run:

```bash
python3 hello.py
```

## Basic Input And Output

Input is information a program receives. Output is information it gives back.

```python
name = input("What is your name? ")
print(greet(name))
```

The `input` function asks the user for text. The `print` function displays output.

## Documentation

Documentation explains what code is for, how to use it, and what assumptions it makes.

A Python docstring is one way to document a function:

```python
def calculate_tip(meal_cost, tip_rate):
    """Return the tip amount for a meal cost and tip rate."""
    return meal_cost * tip_rate
```

Useful function documentation should answer:

1. What does this function do?
2. What inputs does it expect?
3. What does it return?
4. What errors or limits should the caller know about?

## Tuples

A tuple stores multiple values together and keeps their order.

```python
def split_name(full_name):
    parts = full_name.split(" ")
    return (parts[0], parts[-1])


first, last = split_name("Ada Lovelace")
print(first)
print(last)
```

Tuples are useful when a function naturally returns a small fixed group of values.

## First Program Checklist

Before submitting any code this week, check:

- Can I explain each function in a sentence?
- Do function names describe what they do?
- Do inputs and outputs make sense?
- Is there a short docstring for non-obvious behavior?
- Did I run the file myself?
