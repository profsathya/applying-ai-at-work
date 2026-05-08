---
type: page
title: "Code Reliability: Testing With Pytest"
slug: code-reliability-testing-with-pytest
artifact_id: course4-sprints-sprint-1-code-reliability-testing-with-pytest
sprint: 1
week: 2
module: "Module 2: Data Models, Control Flow, Objects, Files, and Testing"
position: 10
points: null
submission_type: none
publish: false
---

# Code Reliability: Testing With Pytest

Testing is how you turn expectations into executable checks.

When you write a test, you are saying: "For this input, I expect this behavior." That is useful when you write code yourself, and it is essential when AI helps produce code quickly.

## A First Test

Suppose you have this function:

```python
def assign_priority(warning_level):
    if warning_level >= 4:
        return "high"
    return "normal"
```

A `pytest` test might look like this:

```python
def test_high_warning_level_gets_high_priority():
    assert assign_priority(4) == "high"
```

The test names the behavior and checks the result.

## Multiple Cases

Parameterized tests let you check several cases:

```python
import pytest


@pytest.mark.parametrize(
    "warning_level, expected",
    [
        (1, "normal"),
        (3, "normal"),
        (4, "high"),
        (5, "high"),
    ],
)
def test_assign_priority(warning_level, expected):
    assert assign_priority(warning_level) == expected
```

This helps you see the rule more clearly.

## Fixtures

A fixture creates reusable test data:

```python
import pytest


@pytest.fixture
def sample_ticket():
    return {
        "title": "Cannot access email",
        "text": "My account login stopped working",
        "warning_level": 4,
    }


def test_sample_ticket_has_title(sample_ticket):
    assert sample_ticket["title"]
```

Use fixtures when several tests need the same setup.

## When To Use Tests

Use tests when:

- A function has rules or edge cases.
- A bug was fixed and should not return.
- AI generated code you do not fully trust yet.
- A feature affects existing behavior.
- You need evidence before changing a project.

## User-Defined Tests

Starter code may include tests, but you should still write your own.

User-defined tests are valuable because they show what you think matters. If the starter code does not check empty text, unusual warning levels, repeated tags, or bad file paths, your tests can reveal those gaps.

## Testing Habit

Before changing code, write down:

1. What should stay true?
2. What input might break it?
3. What output would prove the rule works?

Then write one small test.
