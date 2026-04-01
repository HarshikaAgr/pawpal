# PawPal+ Sorting & Filtering Guide

## Overview

PawPal+ now supports **4 powerful sorting and filtering methods** to organize tasks in different ways.

---

## 1. SORTING BY TIME

**Method:** `Scheduler.sort_by_time()`

**What it does:**
- Sorts all tasks by start time (early to late)
- Uses HH:MM format (24-hour time)

**How it works:**
```python
scheduler = Scheduler(owner)
sorted_tasks = scheduler.sort_by_time()

# Lambda function converts "14:30" to 1430 (comparable number)
# key=lambda task: int(task.start_time.replace(":", ""))
```

**Example Output:**
```
Tasks sorted BY TIME (early to late):
  08:00 - Feed Buddy (Morning)
  08:30 - Feed Whiskers
  10:00 - Grooming
  14:00 - Afternoon Walk
  16:00 - Playtime
```

**Why useful:**
- See chronological schedule
- Plan tasks in order they'll happen
- Avoid scheduling conflicts

---

## 2. FILTER BY COMPLETION STATUS

**Method:** `Scheduler.filter_by_completion(completed_only=True/False)`

**What it does:**
- Shows only completed tasks (DONE)
- Shows only incomplete tasks (TODO)

**How to use:**
```python
scheduler = Scheduler(owner)

# Get incomplete tasks
todos = scheduler.filter_by_completion(completed_only=False)

# Get completed tasks
done = scheduler.filter_by_completion(completed_only=True)
```

**Example Output:**
```
Incomplete tasks (TODO): 3
  - 14:00: Afternoon Walk
  - 10:00: Grooming
  - 08:30: Feed Whiskers

Completed tasks (DONE): 2
  - 08:00: Feed Buddy (Morning)
  - 16:00: Playtime
```

**Why useful:**
- Track what's done vs what's left
- Focus on remaining work
- See progress at a glance

---

## 3. FILTER BY PET

**Method:** `Scheduler.filter_by_pet(pet_name)`

**What it does:**
- Shows only tasks for one specific pet

**How to use:**
```python
scheduler = Scheduler(owner)

buddy_tasks = scheduler.filter_by_pet("Buddy")
whiskers_tasks = scheduler.filter_by_pet("Whiskers")
```

**Example Output:**
```
Tasks for Buddy: 3
  14:00 - Afternoon Walk [TODO]
  08:00 - Feed Buddy (Morning) [DONE]
  10:00 - Grooming [TODO]

Tasks for Whiskers: 2
  08:30 - Feed Whiskers [TODO]
  16:00 - Playtime [DONE]
```

**Why useful:**
- Focus on one pet's schedule
- Plan individual pet care
- See pet-specific workload

---

## 4. FILTER BY CATEGORY

**Method:** `Scheduler.filter_by_category(category_name)`

**What it does:**
- Shows only tasks of one type (feeding, exercise, grooming, etc)

**How to use:**
```python
scheduler = Scheduler(owner)

feeding_tasks = scheduler.filter_by_category("feeding")
exercise_tasks = scheduler.filter_by_category("exercise")
grooming_tasks = scheduler.filter_by_category("grooming")
```

**Example Output:**
```
Feeding tasks: 2
  08:00 - Feed Buddy (Morning) (Buddy) [DONE]
  08:30 - Feed Whiskers (Whiskers) [TODO]

Exercise tasks: 2
  14:00 - Afternoon Walk (Buddy) [TODO]
  16:00 - Playtime (Whiskers) [DONE]

Grooming tasks: 1
  10:00 - Grooming (Buddy) [TODO]
```

**Why useful:**
- Group similar care activities
- See what category takes most time
- Plan by type of activity

---

## 5. COMBINE FILTERS (Advanced)

You can combine filters for powerful results:

```python
# Get Buddy's incomplete tasks sorted by time
buddy_incomplete = [t for t in scheduler.filter_by_completion(False)
                    if t.pet.name == "Buddy"]
sorted_buddy = sorted(buddy_incomplete,
                      key=lambda t: int(t.start_time.replace(":", "")))

# Get feeding tasks that are not done
feeding_incomplete = [t for t in scheduler.filter_by_category("feeding")
                      if not t.completed]
```

---

## Key Concepts Explained

### Time Sorting (Lambda Magic)

```python
# Original time string: "14:30"
# Remove colon: "1430"
# Convert to int: 1430

key=lambda task: int(task.start_time.replace(":", ""))

# This makes times sortable:
# 08:00 (800) < 10:00 (1000) < 14:30 (1430) < 16:00 (1600)
```

### List Comprehension (Filtering Magic)

```python
# Get tasks that meet a condition
incomplete = [task for task in all_tasks if not task.completed]

# English: "Make a list of tasks WHERE task is not completed"
```

---

## Complete Example

```python
from pawpal_system import Owner, Pet, Task, Scheduler

# Setup
john = Owner("John", 120)
buddy = Pet("Buddy", "dog", 3)
john.add_pet(buddy)

# Add tasks with different times
task1 = Task("Afternoon Walk", 20, "high", "exercise", "daily", "14:00")
task2 = Task("Feed Buddy", 5, "high", "feeding", "daily", "08:00")
buddy.add_task(task1)
buddy.add_task(task2)
task2.mark_complete()

# Create scheduler
scheduler = Scheduler(john)

# SORT by time
sorted_tasks = scheduler.sort_by_time()
for task in sorted_tasks:
    print(f"{task.start_time}: {task.title}")

# FILTER by status
todos = scheduler.filter_by_completion(completed_only=False)
print(f"\nTodos: {len(todos)}")

# FILTER by pet
buddy_tasks = scheduler.filter_by_pet("Buddy")
print(f"\nBuddy's tasks: {len(buddy_tasks)}")

# FILTER by category
feeding = scheduler.filter_by_category("feeding")
print(f"\nFeeding tasks: {len(feeding)}")
```

---

## Summary Table

| Method | Sorts? | Filters? | Input | Output |
|--------|--------|----------|-------|--------|
| `sort_by_time()` | ✓ | - | Scheduler | List (early→late) |
| `filter_by_completion()` | - | ✓ | Boolean | Done or TODO tasks |
| `filter_by_pet()` | - | ✓ | Pet name | One pet's tasks |
| `filter_by_category()` | - | ✓ | Category | Tasks by type |

---

## Quick Cheat Sheet

```python
# Sort by time (early to late)
scheduler.sort_by_time()

# Show only incomplete tasks
scheduler.filter_by_completion(completed_only=False)

# Show only completed tasks
scheduler.filter_by_completion(completed_only=True)

# Show Buddy's tasks only
scheduler.filter_by_pet("Buddy")

# Show all feeding tasks
scheduler.filter_by_category("feeding")

# Combine: Buddy's incomplete tasks sorted by time
buddy_todos = [t for t in scheduler.filter_by_completion(False)
               if t.pet.name == "Buddy"]
sorted_todos = sorted(buddy_todos,
                      key=lambda t: int(t.start_time.replace(":", "")))
```

---

## Running the Demo

```bash
python main.py
```

See all sorting and filtering features in action with example output!
