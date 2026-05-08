---
type: assignment
title: "Libraries, Virtual Environments, and Project Operations CodeChecks"
slug: libraries-virtual-environments-and-project-operations-codechecks
artifact_id: course4-sprints-sprint-2-libraries-virtual-environments-and-project-operations-codechecks
sprint: 2
week: 3
module: "Module 3: Project Development, Git, Dependencies, Debugging, and Contribution"
position: 5
points: 25
submission_type: text_entry
publish: false
rubric:
  - description: "Completes assigned CodeChecks or equivalent local tasks"
    points: 8
  - description: "Uses at least one standard-library module appropriately"
    points: 5
  - description: "Explains the role of virtual environments or dependencies"
    points: 4
  - description: "Includes evidence from running code or tests"
    points: 4
  - description: "Reflects on AI use and verification"
    points: 4
---

# Libraries, Virtual Environments, and Project Operations CodeChecks

## Purpose

Practice small project operations that use Python's standard library and prepare you for the Flask application analysis.

These CodeChecks should be small enough to attempt independently. AI can help explain a library, but you should still run and inspect the code yourself.

## Virtual Environments

A virtual environment keeps project dependencies separate from the rest of your computer.

Common commands:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activation may use a different command. Follow your instructor's setup notes.

## CodeCheck Set

Complete the CodeChecks assigned by your instructor. If a CodeCheck link is not available, write local Python scripts for these prompts:

1. Use `pathlib` to list all `.txt` files in a folder.
2. Use `json` to read a small configuration file.
3. Use `csv` to count rows in a dataset.
4. Use `argparse` to accept a command line option.
5. Use `logging` to record an operation and an error.

## Required Reflection

Choose one task and explain:

- Which library you used.
- What problem the library solved.
- What input or file the script expected.
- What could go wrong in a real project.

## Submission

Submit:

- CodeCheck completion evidence or your local script.
- One command you ran.
- One output or test result.
- Your required reflection.
- A brief note on AI use.
