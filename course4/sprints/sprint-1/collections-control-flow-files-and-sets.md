---
type: page
title: "Collections, Control Flow, Files, and Sets"
slug: collections-control-flow-files-and-sets
artifact_id: course4-sprints-sprint-1-collections-control-flow-files-and-sets
sprint: 1
week: 2
module: "Module 2: Data Models, Control Flow, Objects, Files, and Testing"
position: 5
points: null
submission_type: none
publish: false
---

# Collections, Control Flow, Files, and Sets

Programs need ways to store and process groups of information.

This page introduces the collection and control-flow tools you will see in the support ticket system.

## Lists

A list stores an ordered group of values.

```python
tickets = ["printer broken", "password reset", "cannot access email"]

for ticket in tickets:
    print(ticket)
```

Use a list when order matters or when duplicates are allowed.

## Dictionaries

A dictionary stores key-value pairs.

```python
ticket = {
    "title": "Cannot access email",
    "supportee": "Jordan",
    "warning_level": 3,
}

print(ticket["title"])
```

Use a dictionary when you need to look up information by name.

## Sets

A set stores unique values.

```python
tags = {"password", "account", "urgent"}
tags.add("urgent")
print(tags)
```

The tag `"urgent"` appears only once because sets do not keep duplicates.

Use a set when you care about membership and uniqueness:

- Which tags are attached to this ticket?
- Has this word already appeared?
- Which classifications are present in the data?
- Do two groups share any values?

## Conditionals

Conditionals let code choose a path.

```python
if ticket["warning_level"] >= 4:
    priority = "high"
else:
    priority = "normal"
```

Read conditionals as decision rules. Ask whether the rule matches the real situation.

## Loops

A `for` loop processes each item in a known collection:

```python
for ticket in tickets:
    print(ticket["title"])
```

A `while` loop continues until a condition changes:

```python
command = ""

while command != "quit":
    command = input("Enter command: ")
```

Use `while` carefully. A condition that never changes can create an infinite loop.

## File Reading

Files let programs work with data beyond one run.

```python
with open("tickets.txt", "r") as file:
    for line in file:
        print(line.strip())
```

When reading files, ask:

- What path does the code expect?
- What format does the file use?
- What happens if the file is missing?
- What happens if one line has bad data?

## Choosing The Right Structure

Use this quick guide:

| Need | Structure |
|---|---|
| Ordered group | List |
| Unique values | Set |
| Named fields | Dictionary |
| Real-world entity with behavior | Object |
| Repeated action | Loop |
| Decision rule | Conditional |
| Data across runs | File or database |

Understanding these choices makes AI-generated code much easier to read.
