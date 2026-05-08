---
type: page
title: "Code Reliability: Errors, Exceptions, and Logging"
slug: code-reliability-errors-exceptions-and-logging
artifact_id: course4-sprints-sprint-0-code-reliability-errors-exceptions-and-logging
sprint: 0
week: 1
module: "Module 1: Code, Abstraction, Functions, and Basic Reliability"
position: 10
points: null
submission_type: none
publish: false
---

# Code Reliability: Errors, Exceptions, and Logging

Reliable code is not code that never fails. Reliable code makes failure understandable.

When a program breaks, the error message is information. It tells you where Python stopped and what kind of problem it found.

## Exceptions

An exception is Python's way of saying something prevented normal execution.

Example:

```python
def divide(a, b):
    return a / b


print(divide(10, 0))
```

This raises a `ZeroDivisionError` because division by zero is not allowed.

## Handling An Exception

You can handle expected failure:

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero."
```

This does not hide the problem. It turns a known failure into a useful message.

## Raising Your Own Error

Sometimes the function should reject an input clearly:

```python
def encrypt_message(message):
    if not message:
        raise ValueError("Message must not be empty.")
    return "encrypted text goes here"
```

Raise an error when the program cannot continue honestly with the input it received.

## Where To Place Error Messages

Place error handling close to the decision that can fail.

- Validate user input before using it.
- Check file paths before reading files.
- Check whether a number can be used before dividing.
- Convert AI-generated assumptions into explicit checks.

Good error messages say what happened and what the user can do next.

## Logging

Printing is useful while learning, but logs are better when a program grows.

```python
import logging

logging.basicConfig(level=logging.INFO)


def decrypt_sample(sample_id):
    logging.info("Decrypting sample %s", sample_id)
    return "hidden message"
```

Logs help you understand what happened without turning every message into user-facing output.

## Debugging Habit

When something fails:

1. Read the full error message.
2. Find the line number.
3. Identify the variable or operation involved.
4. Reproduce the issue with the smallest input possible.
5. Add a check, test, or clearer message.

AI tools can help explain a stack trace, but they should not skip your own reading. Ask: "What does this error mean?" before asking: "Fix this."
