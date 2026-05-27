---
type: page
title: Python Dictionaries Overview
slug: python-dictionaries-overview
artifact_id: course1-sprints-sprint-7-python-dictionaries-overview
sprint: 7
week: null
module: Python Dictionaries
position: 1
publish: true
---

# Python Dictionaries Overview

A Python dictionary stores related information as key-value pairs. Use a dictionary when each piece of data has a label.

```python
profile = {
    "name": "Ava",
    "role": "analyst",
    "team": "operations"
}
```

In this example, `"name"`, `"role"`, and `"team"` are keys. `"Ava"`, `"analyst"`, and `"operations"` are values.

Dictionaries are useful when a list is not specific enough. A list can store values in order, but a dictionary can describe what each value means.

## When a dictionary helps

Use a dictionary when you want to track facts about one thing.

```python
ticket = {
    "id": 1042,
    "status": "open",
    "priority": "high",
    "owner": "Maya"
}
```

This is easier to read than a list like this:

```python
ticket = [1042, "open", "high", "Maya"]
```

The list has the same values, but the meaning depends on remembering the order. The dictionary names each value.

## Dictionary syntax

A dictionary uses curly braces. Each key is followed by a colon and a value. Each key-value pair is separated by a comma.

```python
settings = {
    "notifications": True,
    "theme": "light",
    "items_per_page": 25
}
```

Keys are often strings. Values can be strings, numbers, booleans, lists, or even other dictionaries.

## Reading one value

Use the key inside square brackets to read a value.

```python
profile = {
    "name": "Ava",
    "role": "analyst"
}

print(profile["name"])
print(profile["role"])
```

Output:

```text
Ava
analyst
```

Python looks up the value connected to that key.

## Keys should be unique

Each key in a dictionary should appear once. If you repeat a key, Python keeps the latest value.

```python
record = {
    "status": "open",
    "status": "closed"
}

print(record["status"])
```

Output:

```text
closed
```

Use clear, unique keys so the dictionary stays readable.

## A practical mental model

Think of a dictionary as a small labeled record.

- The key answers: What piece of information is this?
- The value answers: What is the current information?

That makes dictionaries useful for profiles, settings, inventory counts, survey responses, support tickets, project tasks, and many other workplace records.
