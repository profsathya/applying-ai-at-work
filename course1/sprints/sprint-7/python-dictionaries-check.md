---
type: quiz
title: Python Dictionaries Check
slug: python-dictionaries-check
artifact_id: course1-sprints-sprint-7-python-dictionaries-check
sprint: 7
week: null
module: Python Dictionaries
position: 4
publish: true
points: 5.0
submission_type: online_quiz
questions:
- type: multiple_choice
  prompt: 'Which Python syntax creates a dictionary?'
  points: 1.0
  answers:
  - text: 'employee = {"name": "Ava", "role": "analyst"}'
    correct: true
  - text: 'employee = ["name", "Ava", "role", "analyst"]'
    correct: false
  - text: 'employee = ("name", "Ava", "role", "analyst")'
    correct: false
  - text: 'employee = "name": "Ava", "role": "analyst"'
    correct: false
- type: multiple_choice
  prompt: 'In a dictionary, what is a key?'
  points: 1.0
  answers:
  - text: 'A label used to look up a value'
    correct: true
  - text: 'The position number of a value'
    correct: false
  - text: 'A required file name'
    correct: false
  - text: 'A command that sorts values'
    correct: false
- type: multiple_choice
  prompt: 'Given task = {"status": "open"}, what does task["status"] return?'
  points: 1.0
  answers:
  - text: 'open'
    correct: true
  - text: 'status'
    correct: false
  - text: 'task'
    correct: false
  - text: 'KeyError'
    correct: false
- type: multiple_choice
  prompt: 'Why might you use customer.get("phone", "no phone on file")?'
  points: 1.0
  answers:
  - text: 'To avoid an error when the phone key is missing and show a default value'
    correct: true
  - text: 'To remove the phone key from the dictionary'
    correct: false
  - text: 'To turn the dictionary into a list'
    correct: false
  - text: 'To rename every key in the dictionary'
    correct: false
- type: multiple_choice
  prompt: 'Which loop is best for printing both keys and values from a dictionary?'
  points: 1.0
  answers:
  - text: 'for key, value in inventory.items():'
    correct: true
  - text: 'for value in inventory.append():'
    correct: false
  - text: 'for key, value in inventory.sort():'
    correct: false
  - text: 'for index in inventory[0]:'
    correct: false
---

# Python Dictionaries Check

Use this short check to confirm that you understand dictionary syntax, keys, values, safe lookup with `.get()`, updates, and loops.
