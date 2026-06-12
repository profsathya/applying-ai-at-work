---
type: page
title: "Tuple Indexing and Unpacking"
slug: tuple-indexing-and-unpacking
artifact_id: course1-sprints-sprint-99-tuple-indexing-and-unpacking
sprint: 99
module: "Hosted HTML Pilot: Python Tuples"
position: 2
points: null
submission_type: none
publish: false
---

# Tuple Indexing and Unpacking

Indexing and unpacking are the two most common ways to pull useful values out of a tuple.

## Indexing by position

Use an index when you need one value from a tuple.

```python
ticket = ("A-104", "billing", "open")

ticket_id = ticket[0]
category = ticket[1]
status = ticket[2]
```

Python starts counting at zero. The first item is index `0`, the second item is index `1`, and so on.

## Unpacking into names

Unpacking lets you assign each tuple value to a clear variable name in one line.

```python
ticket = ("A-104", "billing", "open")

ticket_id, category, status = ticket
```

This is often easier to read than repeated indexing, especially when every value in the tuple has a specific meaning.

## Returning more than one value

Functions often use tuples to return multiple values.

```python
def summarize_order(quantity, unit_price):
    subtotal = quantity * unit_price
    tax = subtotal * 0.09
    total = subtotal + tax
    return subtotal, tax, total

subtotal, tax, total = summarize_order(5, 12)
```

Python packs the returned values into a tuple, then unpacks them into the variable names on the left.

## When unpacking fails

The number of names must match the number of tuple values.

```python
status = ("approved", 202)

label, code, owner = status  # ValueError
```

This error is helpful. It usually means the shape of your data is not what your code expected.

## Practice prompt

Before moving on, write a tuple that represents a real work item you recognize, such as a support ticket, schedule block, inventory item, or approval record. Then unpack it into named variables.
