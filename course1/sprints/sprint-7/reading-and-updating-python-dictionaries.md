---
type: page
title: Reading and Updating Python Dictionaries
slug: reading-and-updating-python-dictionaries
artifact_id: course1-sprints-sprint-7-reading-and-updating-python-dictionaries
sprint: 7
week: null
module: Python Dictionaries
position: 2
publish: true
---

# Reading and Updating Python Dictionaries

Once you can create a dictionary, the next step is to read, update, add, remove, and loop through its values.

## Read with square brackets

Use a key to retrieve its value.

```python
task = {
    "title": "prepare report",
    "status": "in progress",
    "hours": 3
}

print(task["title"])
print(task["status"])
```

Square brackets work well when you know the key exists.

## Read safely with `.get()`

If you try to read a missing key with square brackets, Python raises a `KeyError`.

```python
task = {
    "title": "prepare report",
    "status": "in progress"
}

print(task.get("owner"))
```

Output:

```text
None
```

You can also provide a default value.

```python
print(task.get("owner", "unassigned"))
```

Output:

```text
unassigned
```

Use `.get()` when a key might be missing.

## Update an existing value

Assign a new value to an existing key.

```python
task = {
    "title": "prepare report",
    "status": "in progress"
}

task["status"] = "complete"

print(task)
```

The key stays the same. The value changes.

## Add a new key-value pair

Assign a value to a new key.

```python
task = {
    "title": "prepare report",
    "status": "complete"
}

task["owner"] = "Jordan"

print(task)
```

Dictionaries can grow as you collect more information.

## Remove a key-value pair

Use `pop()` when you want to remove a key and keep the value that was removed.

```python
task = {
    "title": "prepare report",
    "status": "complete",
    "owner": "Jordan"
}

removed_owner = task.pop("owner")

print(removed_owner)
print(task)
```

Use `del` when you only want to delete the key-value pair.

```python
del task["status"]
```

## Loop through a dictionary

Use `.items()` when you need both the key and the value.

```python
task = {
    "title": "prepare report",
    "status": "complete",
    "hours": 3
}

for key, value in task.items():
    print(key, ":", value)
```

Output:

```text
title : prepare report
status : complete
hours : 3
```

Use `.keys()` if you only need keys. Use `.values()` if you only need values.

## Common beginner mistakes

- Forgetting quotation marks around string keys.
- Using a key that does not exist.
- Confusing a key with an index. Dictionaries are read by key, not by position.
- Repeating the same key and accidentally replacing a value.
- Printing the whole dictionary when the user only needs one value.

## A complete example

```python
contact = {
    "name": "Sam",
    "department": "Finance",
    "email": "sam@example.com"
}

contact["department"] = "Budget Office"
contact["phone"] = "555-0100"

for key, value in contact.items():
    print(key + ":", value)
```

This example creates a dictionary, updates one value, adds one new key-value pair, and prints a readable summary.
