---
type: page
title: Python Lists Explanation
slug: python-lists-explanation
artifact_id: course1-sprints-sprint-5-python-lists-explanation
sprint: 5
week: 10
module: Python Lists
position: 26
publish: true
---

# Python Lists Explanation

A Python list stores multiple values in one ordered collection. Instead of creating a separate variable for every item, you can put related items inside square brackets.
    
    
    favorite_foods = ["tacos", "sushi", "pasta"]
    scores = [84, 91, 78, 100]
    mixed_items = ["Alex", 42, True]
    

Lists are useful when you need to keep track of a group: names, prices, scores, tasks, ingredients, files, survey responses, or any other set of related values.

## Creating a List

Use square brackets, with commas between values.
    
    
    team_names = ["Warriors", "Lakers", "Kings"]
    

An empty list is also valid:
    
    
    shopping_list = []
    

You can add values later.

## Indexes

Each item in a list has a position called an index. Python starts counting at `0`, not `1`.
    
    
    colors = ["red", "blue", "green"]
    
    print(colors[0])  # red
    print(colors[1])  # blue
    print(colors[2])  # green
    

This is one of the first details that surprises beginners. The first item is index `0`.

You can also count from the end with negative indexes:
    
    
    print(colors[-1])  # green
    print(colors[-2])  # blue
    

## Changing a Value

Lists are mutable, which means you can change them after you create them.
    
    
    tasks = ["email client", "draft report", "review budget"]
    tasks[1] = "finish report"
    
    print(tasks)
    

The list now contains `"finish report"` instead of `"draft report"`.

## Adding Items

Use `.append()` to add one item to the end of a list.
    
    
    tasks = ["email client", "finish report"]
    tasks.append("schedule meeting")
    
    print(tasks)
    

Use `.insert()` when you want to place an item at a specific index.
    
    
    tasks.insert(1, "check calendar")
    

After this, `"check calendar"` appears at index `1`.

## Removing Items

Use `.remove()` when you know the value you want to remove.
    
    
    tasks = ["email client", "finish report", "schedule meeting"]
    tasks.remove("finish report")
    

Use `.pop()` when you want to remove an item by index. If you do not give an index, `.pop()` removes the last item.
    
    
    last_task = tasks.pop()
    first_task = tasks.pop(0)
    

The removed value can be stored in a variable, which is helpful when you still need to use it.

## List Length

Use `len()` to count how many items are in a list.
    
    
    scores = [84, 91, 78, 100]
    print(len(scores))  # 4
    

`len()` is especially useful before showing a count to a user or checking whether a list is empty.
    
    
    if len(scores) == 0:
        print("No scores yet.")
    else:
        print("Scores are ready.")
    

## Looping Through a List

A `for` loop lets you do the same action for every item in a list.
    
    
    names = ["Ava", "Jordan", "Miguel"]
    
    for name in names:
        print("Hello, " + name)
    

Read this as: for each `name` in the `names` list, run the indented code.

If you need both the index and the value, use `enumerate()`.
    
    
    names = ["Ava", "Jordan", "Miguel"]
    
    for index, name in enumerate(names):
        print(index, name)
    

## Slicing

A slice copies part of a list.
    
    
    numbers = [10, 20, 30, 40, 50]
    
    print(numbers[1:4])  # [20, 30, 40]
    print(numbers[:3])   # [10, 20, 30]
    print(numbers[3:])   # [40, 50]
    

In `numbers[1:4]`, Python starts at index `1` and stops before index `4`.

## Common Beginner Mistakes

  * Forgetting that the first index is `0`.
  * Trying to access an index that does not exist.
  * Writing `append` without parentheses.
  * Confusing the value in the list with the index of the value.
  * Changing a list while looping through it without thinking through the result.



## A Complete Example
    
    
    todo = ["read notes", "practice lists", "submit homework"]
    
    todo.append("review quiz")
    todo[0] = "reread notes"
    
    for item in todo:
        print("- " + item)
    
    print("Total tasks:", len(todo))
    

This example creates a list, adds an item, updates an item, loops through the list, and prints the total number of tasks.
