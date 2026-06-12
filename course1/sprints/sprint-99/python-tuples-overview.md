---
type: page
title: "Python Tuples Overview"
slug: python-tuples-overview
artifact_id: course1-sprints-sprint-99-python-tuples-overview
sprint: 99
module: "Hosted HTML Pilot: Python Tuples"
position: 1
points: null
submission_type: none
publish: false
---

# Python Tuples Overview

Tuples are one of Python's simplest ways to keep related values together. A tuple is ordered, can hold different kinds of values, and is immutable after it is created.

## Why tuples matter

Use a tuple when a small group of values belongs together and should not be changed by accident. Common examples include coordinates, status pairs, database rows, and function results that return more than one value.

```python
employee = ("Maya", "Operations", 42)
point = (10, 20)
status = ("approved", 202)
```

Lists are better when the collection needs to grow, shrink, or change. Tuples are better when the grouping itself should stay stable.

## Creating tuples

Most tuples are created with parentheses and commas.

```python
colors = ("red", "green", "blue")
single_value = ("ready",)
```

The comma is what makes a one-item tuple. Without it, Python treats the value as a plain string, number, or object in parentheses.

## Reading tuple values

Tuples use zero-based indexes, just like lists.

```python
status = ("approved", 202)

label = status[0]
code = status[1]
```

You can also loop through a tuple when each value should be handled in order.

## Immutability

Once a tuple is created, you cannot replace one of its positions.

```python
status = ("approved", 202)
status[0] = "pending"  # TypeError
```

This is useful because it makes intent clear. A tuple tells future readers that these values are meant to travel together without being edited in place.

## Next step

Move to the indexing and unpacking page to practice reading tuple values in a more direct way.
