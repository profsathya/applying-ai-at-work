---
type: assignment
title: "Project 1: CLI Encryption and Decryption Tool"
slug: project-1-cli-encryption-and-decryption-tool
artifact_id: course4-sprints-sprint-0-project-1-cli-encryption-and-decryption-tool
sprint: 0
week: 1
module: "Module 1: Code, Abstraction, Functions, and Basic Reliability"
position: 11
points: 40
submission_type: text_entry
publish: false
rubric:
  - description: "CLI accepts clear user input for encrypting or decrypting"
    points: 8
  - description: "Provided RSA function is used correctly without rewriting the algorithm unnecessarily"
    points: 8
  - description: "Five encrypted samples are decrypted and hidden text is reported"
    points: 8
  - description: "Program includes documentation and useful error handling"
    points: 8
  - description: "Reflection explains development choices and AI usage"
    points: 8
---

# Project 1: CLI Encryption and Decryption Tool

## Purpose

Build a small command line tool that uses a provided RSA function to encrypt and decrypt messages.

You are not expected to implement the RSA algorithm from scratch. The learning target is using a provided function, building a command line interface, documenting the program, and handling errors clearly.

## Provided Materials

Your instructor will provide:

- A Python function or module that performs the RSA operation.
- Five encrypted samples.
- Keys needed to decrypt the samples.
- Any setup notes required for your environment.

## Required Features

Your tool should:

1. Let the user choose whether to encrypt or decrypt.
2. Accept a message or sample identifier.
3. Accept the required key values.
4. Call the provided RSA function.
5. Print a readable result.
6. Display a useful message when input is missing or invalid.
7. Include docstrings for your own functions.

## Suggested Structure

Start with small functions:

```python
def get_user_choice():
    """Ask whether the user wants to encrypt or decrypt."""
    pass


def display_result(result):
    """Print a readable result for the user."""
    pass
```

Then connect those functions to the provided RSA function.

## Development Steps

1. Run the provided RSA function exactly as given.
2. Write one wrapper function that calls it with known values.
3. Add a command line prompt for the user's choice.
4. Add input prompts for the message and key values.
5. Test the five encrypted samples.
6. Add docstrings and error messages.
7. Run the tool one final time from the terminal.

## Deliverable

Submit a text entry with:

- Your code or a link to your repository if your instructor provides that option.
- The decrypted hidden text for all five samples.
- Two example command line runs.
- One error case you handled.
- One paragraph explaining where you used AI, if anywhere, and how you checked the result.

## Bonus

Create a short hidden message for someone else in the course. If the instructor opens the bonus discussion, share the encrypted message and the required public information there.
