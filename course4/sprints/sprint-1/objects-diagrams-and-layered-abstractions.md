---
type: page
title: "Objects, Diagrams, and Layered Abstractions"
slug: objects-diagrams-and-layered-abstractions
artifact_id: course4-sprints-sprint-1-objects-diagrams-and-layered-abstractions
sprint: 1
week: 2
module: "Module 2: Data Models, Control Flow, Objects, Files, and Testing"
position: 4
points: null
submission_type: none
publish: false
---

# Objects, Diagrams, and Layered Abstractions

An object is a bundle of related information and behavior.

In Python, classes describe the shape and behavior of objects:

```python
class SupportTicket:
    def __init__(self, title, text, supportee, warning_level):
        self.title = title
        self.text = text
        self.supportee = supportee
        self.warning_level = warning_level
        self.status = "open"

    def close(self):
        self.status = "closed"
```

This class says a support ticket has data and behavior:

- Data: title, text, supportee, warning level, status.
- Behavior: close the ticket.

## Real-World Entities

Before writing a class, describe the real thing.

For a support ticket:

- Who creates it?
- Who reads it?
- What information must be stored?
- What changes over time?
- What decisions does the system make with it?

The answers tell you what belongs in the class.

## Inheritance

Inheritance lets one class build on another class.

```python
class Ticket:
    def __init__(self, title):
        self.title = title


class SecurityTicket(Ticket):
    def __init__(self, title, severity):
        super().__init__(title)
        self.severity = severity
```

Inheritance can be useful, but it can also make code harder to follow. Use it when one thing really is a more specific version of another thing. Do not use it just because it looks advanced.

## Simple UML-Style Sketch

You do not need a formal diagram tool to think clearly.

```text
SupportTicket
- title
- text
- supportee
- warning_level
- classification
- status

+ close()
+ assign_priority()
+ add_tag(tag)
```

This sketch shows fields with `-` and behavior with `+`.

## Workflow Sketch

A workflow diagram shows how information moves:

```text
Ticket submitted
  -> validate required fields
  -> classify ticket
  -> assign priority
  -> save ticket
  -> notify supportee
```

This is not code yet. It is a plan for what the code must represent.

## Layered Abstraction

A support ticket system has layers:

1. A ticket object stores information.
2. A classifier decides what kind of ticket it is.
3. A priority rule decides what should happen first.
4. A database stores tickets over time.
5. A user interface lets people create and read tickets.

When generated code feels overwhelming, identify the layer you are reading. Then ask what that layer owns.
