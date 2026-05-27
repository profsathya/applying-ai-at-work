---
type: page
title: Python Dictionaries Exercises
slug: python-dictionaries-exercises
artifact_id: course1-sprints-sprint-7-python-dictionaries-exercises
sprint: 7
week: null
module: Python Dictionaries
position: 3
publish: true
---

# Python Dictionaries Exercises

Use these five exercises to practice creating, reading, updating, and looping through dictionaries. You can work in any Python environment you already have available.

## Exercise 1: Create a Profile Dictionary

Create a dictionary named `employee` with these keys:

- `"name"`
- `"role"`
- `"department"`

Give each key a realistic value. Print the whole dictionary. Then print only the employee name.

Starter code:

```python
employee = {
    "name": "",
    "role": "",
    "department": ""
}

print(employee)
print(employee["name"])
```

Expected idea:

- The dictionary should use string keys.
- The name should be read by using the `"name"` key.

## Exercise 2: Update a Ticket Status

Create this dictionary:

```python
ticket = {
    "id": 305,
    "status": "open",
    "priority": "medium"
}
```

Change the status from `"open"` to `"resolved"`. Print the updated dictionary.

Hint: assign a new value to `ticket["status"]`.

## Exercise 3: Add and Remove Information

Create this dictionary:

```python
project = {
    "name": "website refresh",
    "owner": "Luis",
    "phase": "planning"
}
```

Add a new key named `"deadline"` with any date string as the value.

Then remove the `"phase"` key with `.pop()`.

Print the final dictionary.

## Exercise 4: Use `.get()` for Missing Data

Create this dictionary:

```python
customer = {
    "name": "Mina",
    "email": "mina@example.com"
}
```

Print the customer's phone number by using `.get("phone", "no phone on file")`.

Then add a `"phone"` key and print the phone number again with `.get()`.

Expected idea:

- The first print should show the default message.
- The second print should show the phone number you added.

## Exercise 5: Loop Through Key-Value Pairs

Create a dictionary named `inventory` with at least four items and counts.

Example:

```python
inventory = {
    "laptops": 12,
    "monitors": 8,
    "keyboards": 20,
    "headsets": 15
}
```

Use a `for` loop with `.items()` to print each item and count in this format:

```text
laptops: 12
monitors: 8
```

Then print the total number of different item types by using `len(inventory)`.

## Check Your Understanding

Before moving on, make sure you can answer these questions:

1. What symbol does Python use to create a dictionary?
2. What is the difference between a key and a value?
3. Why might `.get()` be safer than square brackets?
4. How do you add a new key-value pair?
5. What does `.items()` give you in a loop?
