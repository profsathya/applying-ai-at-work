---
type: page
title: Python Lists Exercises
slug: python-lists-exercises
sprint: 5
week: 10
module: Python Lists
position: 27
publish: true
---

# Python Lists Exercises

Use these exercises to practice Python lists before you complete the quiz and coding homework. You can work in any Python environment you already have available.

## Exercise 1: Create and Print a List

Create a list named `cities` with three city names.

Print the whole list.

Then print only the first city.

Starter code:
    
    
    cities = []
    
    print(cities)
    print()
    

Expected idea:

  * Your list should have three strings.
  * The first city should be printed by using index `0`.



## Exercise 2: Add Two Items

Create a list named `groceries` with two items.

Use `.append()` twice to add two more items.

Print the final list.

Starter code:
    
    
    groceries = ["apples", "rice"]
    
    # Add two more items here
    
    print(groceries)
    

## Exercise 3: Update an Item

Create this list:
    
    
    tasks = ["check email", "start project", "take break"]
    

Change `"start project"` to `"finish project"`.

Print the updated list.

Hint: `"start project"` is at index `1`.

## Exercise 4: Remove an Item

Create this list:
    
    
    playlist = ["song one", "song two", "song three", "song four"]
    

Remove `"song two"` from the list.

Then use `.pop()` to remove the last song.

Print the final list.

## Exercise 5: Loop Through a List

Create a list named `participants` with four names.

Use a `for` loop to print this message for each name:
    
    
    Welcome, NAME
    

Example output:
    
    
    Welcome, Maya
    Welcome, Luis
    

## Exercise 6: Count and Average

Create a list of five numbers named `scores`.

Print:

  * The number of scores.
  * The total of the scores.
  * The average score.



Starter code:
    
    
    scores = [80, 90, 75, 100, 85]
    
    total = sum(scores)
    count = len(scores)
    average = total / count
    
    print("Total:", total)
    print("Count:", count)
    print("Average:", average)
    

Change the scores and run the program again.

## Exercise 7: Slicing Practice

Create this list:
    
    
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    

Print:

  1. The first three days.
  2. The weekend days.
  3. Every day except Monday.



Hint: use slices like `days[:3]`.

## Check Your Understanding

Before moving on, make sure you can answer these questions:

  1. What index does Python use for the first item in a list?
  2. What is the difference between `.append()` and `.insert()`?
  3. What is the difference between `.remove()` and `.pop()`?
  4. Why is `len()` useful when working with lists?
  5. What does a `for` loop do with a list?
