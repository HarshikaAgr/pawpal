# PawPal+ Recurring Tasks - Step-by-Step Implementation Guide

## What Was Done (Summary)

You now have **automatic recurring task creation**. When you mark a daily/weekly task complete, a new task for the next occurrence is automatically created!

---

## STEP 1: Added Date Tracking to Tasks

**File:** `pawpal_system.py` (Task class)

**What changed:**
```python
# BEFORE:
def __init__(self, title, duration_minutes, priority, category, recurring="none"):

# AFTER:
def __init__(self, title, duration_minutes, priority, category, recurring="none",
             start_time="00:00", due_date=None):
    self.due_date = due_date if due_date else datetime.now().date()
```

**Why it matters:**
- Tasks now have a `due_date` (YYYY-MM-DD format)
- Tracks WHEN the task should be done
- Default is today if not specified

**Simple example:**
```python
from datetime import datetime

today = datetime.now().date()  #Get today: 2026-04-01

#Create task for today
feed = Task("Feed Buddy", 5, "high", "feeding",
            recurring="daily", due_date=today)
#Task due date: 2026-04-01
```

---

## STEP 2: Calculate Next Due Date

**File:** `pawpal_system.py` (Task class)

```python
def get_next_due_date(self):
    """Calculate when the next occurrence of this task is due"""
    if self.recurring == "none":
        return None  # Non-recurring task, no next date

    elif self.recurring == "daily":
        # Add 1 day to current due date
        next_date = self.due_date + timedelta(days=1)
        return next_date

    elif self.recurring == "weekly":
        # Add 7 days to current due date
        next_date = self.due_date + timedelta(days=7)
        return next_date

    return None
```

**What it does:**
- DAILY tasks: `today + 1 day`
- WEEKLY tasks: `today + 7 days`

**How timedelta works:**
```python
from datetime import timedelta

today = datetime.now().date()  # 2026-04-01

# Add 1 day
tomorrow = today + timedelta(days=1)  # 2026-04-02

# Add 7 days
next_week = today + timedelta(days=7)  # 2026-04-08

# Try it:
print(tomorrow)  # 2026-04-02
print(next_week)  # 2026-04-08
```

**Simple example:**
```python
feed = Task("Feed", 5, "high", "feeding", recurring="daily", due_date=date(2026,4,1))

next_date = feed.get_next_due_date()
print(next_date)  # 2026-04-02 (tomorrow!)
```

---

## STEP 3: Create Next Task Instance

**File:** `pawpal_system.py` (Task class)

**New method added:**
```python
def create_next_task(self):
    """Create a new task instance for the next occurrence

    Returns: New Task object (not added to pet yet)
    """
    if not self.is_recurring():
        return None  # Only recurring tasks can create next task

    next_date = self.get_next_due_date()

    # Create new task with same properties but new due date
    next_task = Task(
        title=self.title,
        duration_minutes=self.duration_minutes,
        priority=self.priority,
        category=self.category,
        recurring=self.recurring,
        start_time=self.start_time,
        due_date=next_date
    )

    # Copy pet reference
    next_task.pet = self.pet

    return next_task
```

**What it does:**
- Creates a **NEW** Task object
- Copies all properties (title, time, priority, etc.)
- Sets new due date (calculated in Step 2)
- **Does NOT add to pet yet** (you do that separately)

**Simple example:**
```python
feed = Task("Feed", 5, "high", "feeding", recurring="daily", due_date=today)

# Create next task
next_feed = feed.create_next_task()

# Check properties:
print(f"Original: {feed.title} due {feed.due_date}")  # 2026-04-01
print(f"Next: {next_feed.title} due {next_feed.due_date}")  # 2026-04-02
print(f"Completed? {next_feed.completed}")  # False (fresh task!)
```

---

## STEP 4: Smart Task Completion

**File:** `pawpal_system.py` (Pet class)

**New method added:**
```python
def complete_task(self, task):
    """Mark a task complete and auto-create next task if recurring

    This is the smart version of mark_complete()
    - Marks task as done
    - If recurring, automatically creates next occurrence
    """
    # Mark as complete
    task.mark_complete()

    # If recurring, create next task
    if task.is_recurring():
        next_task = task.create_next_task()
        if next_task:
            self.add_task(next_task)
            return next_task  # Return the newly created task

    return None  # Non-recurring task, nothing new created
```

**What it does (step by step):**
1. Mark current task as DONE
2. Check: Is task recurring? (daily/weekly)
3. If YES: Create next task
4. If YES: Add it to pet's task list
5. Return the new task (or None if not recurring)

**Simple example:**
```python
buddy = Pet("Buddy", "dog", 3)
feed = Task("Feed", 5, "high", "feeding", recurring="daily", due_date=today)
buddy.add_task(feed)

print(f"Before: {len(buddy.tasks)} tasks")  # 1

# Use smart complete (NOT task.mark_complete())
next_feed = buddy.complete_task(feed)

print(f"After: {len(buddy.tasks)} tasks")  # 2
print(f"Original: {feed.completed}")  # True (DONE)
print(f"Next: {next_feed.completed}")  # False (TODO)
print(f"Next due: {next_feed.due_date}")  # Tomorrow!
```

---

## STEP 5: Updated Task Details

**File:** `pawpal_system.py` (Task class)

**What changed:**
```python
# BEFORE:
return f"{self.title} ({self.duration_minutes}min, {self.priority})"

# AFTER:
date_str = self.due_date.strftime("%Y-%m-%d") if self.due_date else "No date"
return f"{self.title} [{self.start_time}] ({date_str}) ({self.duration_minutes}min) - {status}"
```

**Now shows:**
- Task title
- Start time (HH:MM)
- Due date (YYYY-MM-DD)
- Duration
- Status (Done/To Do)

**Example output:**
```
Feed Buddy [08:00] (2026-04-01) (5min, high) - To Do
Feed Buddy [08:00] (2026-04-02) (5min, high) - To Do
```

---

## COMPLETE WORKFLOW

### Scenario: Buddy's Daily Feeding

**Day 1 (April 1):**
```python
today = date(2026, 4, 1)

# Create daily feeding task
feed = Task("Feed Buddy", 5, "high", "feeding",
            recurring="daily", due_date=today)
buddy.add_task(feed)

print(f"Tasks: {len(buddy.tasks)}")  # 1

# Later in the day: Complete the task
next_task = buddy.complete_task(feed)

print(f"Tasks: {len(buddy.tasks)}")  # 2!
print(f"Task 1: {feed.title} - DONE (due {feed.due_date})")
# Feed Buddy - DONE (due 2026-04-01)

print(f"Task 2: {next_task.title} - TODO (due {next_task.due_date})")
# Feed Buddy - TODO (due 2026-04-02)
```

**Day 2 (April 2):**
```python
# The next task already exists!
# Just complete it

next_task.mark_complete()  # Or buddy.complete_task(next_task)
# Another task created for April 3

print(f"Tasks: {len(buddy.tasks)}")  # 3
```

---

## STEP-BY-STEP USAGE GUIDE

### Task 1: Create Recurring Task

```python
from datetime import datetime
from pawpal_system import Pet, Task

# Get today
today = datetime.now().date()

# Create pet
buddy = Pet("Buddy", "dog", 3)

# Create DAILY task
feed = Task(
    title="Feed Buddy",
    duration_minutes=5,
    priority="high",
    category="feeding",
    recurring="daily",  # KEY: Set to daily!
    start_time="08:00",
    due_date=today
)

buddy.add_task(feed)
```

### Task 2: Complete Task (Smart Way)

```python
# Use buddy.complete_task() instead of task.mark_complete()
next_task = buddy.complete_task(feed)

# Result:
# - feed is DONE
# - next_task is created for tomorrow
# - next_task is already added to buddy.tasks
```

### Task 3: Check Results

```python
# Print all tasks
for task in buddy.tasks:
    status = "DONE" if task.completed else "TODO"
    print(f"[{status}] {task.title} (due {task.due_date})")

# Output:
# [DONE] Feed Buddy (due 2026-04-01)
# [TODO] Feed Buddy (due 2026-04-02)
```

---

## DEMO

**Run this to see everything working:**
```bash
python main.py
```

**Expected output:**
```
BEFORE: 3 tasks

ACTION 1: Complete daily task
After: 4 tasks (1 done, 1 new created for tomorrow)

ACTION 2: Complete another daily task
After: 5 tasks (2 done, 2 new created)

ACTION 3: Complete weekly task
After: 6 tasks (3 done, 3 new created)

SUMMARY:
- Original tasks (Daily, Weekly): 3 DONE
- Auto-created tasks: 3 TODO
  - Dailies: Due tomorrow
  - Weekly: Due next week
```

---

## KEY CONCEPTS

### 1. Date Math with timedelta

```python
from datetime import datetime, timedelta

today = datetime.now().date()

# Add 1 day
tomorrow = today + timedelta(days=1)

# Add 7 days
next_week = today + timedelta(days=7)

# Subtract 1 day
yesterday = today - timedelta(days=1)
```

### 2. Object Cloning

```python
# Create new task with same properties
next_task = Task(
    title=original_task.title,           # Copy
    duration_minutes=original_task.duration_minutes,  # Copy
    # ... etc ...
    due_date=next_date  # NEW value only
)
```

### 3. When to Use Each Method

```python
# OLD WAY (Simple, but no auto-creation)
task.mark_complete()

# NEW WAY (Smart, auto-creates next task)
pet.complete_task(task)

# Use the NEW way for recurring tasks!
```

---

## TESTING CHECKLIST

Run these tests to verify everything works:

✅ Test 1: Daily task auto-creates for tomorrow
```python
feed_today = Task("Feed", 5, "high", "feeding", recurring="daily", due_date=today)
buddy.add_task(feed_today)
next_feed = buddy.complete_task(feed_today)
assert next_feed.due_date == today + timedelta(days=1)  # Tomorrow!
```

✅ Test 2: Weekly task auto-creates for next week
```python
groom_today = Task("Groom", 30, "medium", "grooming", recurring="weekly", due_date=today)
buddy.add_task(groom_today)
next_groom = buddy.complete_task(groom_today)
assert next_groom.due_date == today + timedelta(days=7)  # Next week!
```

✅ Test 3: Non-recurring task doesn't auto-create
```python
bath = Task("Bath", 20, "high", "grooming", recurring="none", due_date=today)
buddy.add_task(bath)
result = buddy.complete_task(bath)
assert result is None  # Nothing created
```

✅ Test 4: New task is NOT completed
```python
feed_today = Task("Feed", 5, "high", "feeding", recurring="daily", due_date=today)
buddy.add_task(feed_today)
next_feed = buddy.complete_task(feed_today)
assert feed_today.completed == True   # Original is DONE
assert next_feed.completed == False   # Next is TODO
```

---

## FILES CHANGED

| File | Changes |
|------|---------|
| `pawpal_system.py` | Added date tracking, date math, auto-creation |
| `main.py` | Full demo showing all features |
| `RECURRING_TASKS.md` | Complete documentation |

---

## SUMMARY

**What you can do now:**

1. ✅ Create daily/weekly tasks
2. ✅ Mark them complete with `pet.complete_task()`
3. ✅ New task auto-created for next occurrence
4. ✅ Daily: Due date is +1 day
5. ✅ Weekly: Due date is +7 days
6. ✅ Original task marked DONE, new task is TODO
7. ✅ Never manually create recurring tasks again!

**Result:** Automatic scheduling system that works!
