# PawPal+ Recurring Task Automation Guide

## Overview

When you mark a **recurring task as complete**, PawPal+ automatically creates a new instance for the next occurrence. No manual work needed!

---

## How It Works

### Step-by-Step Process

```
1. Task exists: "Feed Buddy" (daily, due 2026-04-01)
   ↓
2. Mark complete: pet.complete_task(feed_task)
   ↓
3. Check: Is recurring? YES → recurring="daily"
   ↓
4. Calculate next date: 2026-04-01 + 1 day = 2026-04-02
   ↓
5. Create new task: "Feed Buddy" (daily, due 2026-04-02)
   ↓
6. Add to pet: buddy.tasks.append(new_task)
   ↓
7. Result:
   - Old task: DONE (2026-04-01)
   - New task: TODO (2026-04-02)
```

---

## Key Methods

### 1. `Task.get_next_due_date()`

**What it does:** Calculate when next task should be due

```python
# For DAILY task:
next_date = today + timedelta(days=1)

# For WEEKLY task:
next_date = today + timedelta(days=7)
```

**Example:**
```python
task = Task("Feed", 5, "high", "feeding", recurring="daily", due_date=date(2026,4,1))
next_date = task.get_next_due_date()
# Returns: date(2026, 4, 2)
```

### 2. `Task.create_next_task()`

**What it does:** Create new Task instance for next occurrence

```python
next_task = task.create_next_task()
# Returns: New Task with same properties, different due_date
```

**Properties copied:**
- ✓ title
- ✓ duration_minutes
- ✓ priority
- ✓ category
- ✓ recurring
- ✓ start_time
- ✓ pet (reference)

**Properties new:**
- New due_date (tomorrow/next week)
- completed = False

### 3. `Pet.complete_task(task)`

**What it does:** Smart completion that auto-creates next task

```python
buddy = Pet("Buddy", "dog", 3)
feed_task = Task("Feed", 5, "high", "feeding", recurring="daily", due_date=today)
buddy.add_task(feed_task)

# Smart complete (instead of feed_task.mark_complete())
next_task = buddy.complete_task(feed_task)

# Result:
# - feed_task.completed = True
# - next_task created for tomorrow
# - next_task added to buddy.tasks
```

---

## Usage Examples

### Example 1: Daily Task Auto-Creation

```python
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Task

# Setup
john = Owner("John", 120)
buddy = Pet("Buddy", "dog", 3)
john.add_pet(buddy)

# Create daily task
today = datetime.now().date()
feed = Task("Feed Buddy", 5, "high", "feeding",
            recurring="daily", start_time="08:00", due_date=today)
buddy.add_task(feed)

print(f"Task created: {len(buddy.tasks)} task(s)")  # 1

# Complete the task
next_task = buddy.complete_task(feed)

print(f"After completion: {len(buddy.tasks)} task(s)")  # 2
print(f"Original: DONE (due {feed.due_date})")
print(f"Next: TODO (due {next_task.due_date})")
```

**Output:**
```
Task created: 1 task(s)
After completion: 2 task(s)
Original: DONE (due 2026-04-01)
Next: TODO (due 2026-04-02)
```

### Example 2: Weekly Task Auto-Creation

```python
# Create weekly grooming task
groom = Task("Groom Buddy", 30, "medium", "grooming",
             recurring="weekly", start_time="15:00", due_date=today)
buddy.add_task(groom)

# Complete it
next_groom = buddy.complete_task(groom)

# Next grooming scheduled 7 days later
print(f"Original grooming: {groom.due_date}")  # 2026-04-01
print(f"Next grooming: {next_groom.due_date}")  # 2026-04-08
```

### Example 3: Multiple Daily Tasks

```python
# Multiple daily tasks
walk = Task("Walk", 20, "high", "exercise",
            recurring="daily", due_date=today)
feed = Task("Feed", 5, "high", "feeding",
            recurring="daily", due_date=today)

buddy.add_task(walk)
buddy.add_task(feed)

print(f"Day 1: {len(buddy.tasks)} tasks")  # 2

buddy.complete_task(walk)
buddy.complete_task(feed)

print(f"After completion: {len(buddy.tasks)} tasks")  # 4
# walk (2026-04-01) DONE
# feed (2026-04-01) DONE
# walk (2026-04-02) TODO
# feed (2026-04-02) TODO
```

---

## Python Concepts Used

### 1. datetime and timedelta

```python
from datetime import datetime, timedelta

today = datetime.now().date()  # Get today's date
tomorrow = today + timedelta(days=1)  # Add 1 day
next_week = today + timedelta(days=7)  # Add 7 days
```

**Timedelta explained:**
```python
timedelta(days=1)   # 1 day
timedelta(days=7)   # 7 days
timedelta(hours=2)  # 2 hours
timedelta(weeks=1)  # 1 week (same as days=7)
```

### 2. Object Cloning

```python
# Create next task by copying properties
next_task = Task(
    title=self.title,
    duration_minutes=self.duration_minutes,
    priority=self.priority,
    # ... etc ...
    due_date=next_date  # New date only
)
```

### 3. Conditional Creation

```python
if task.is_recurring():
    next_task = task.create_next_task()
    if next_task:
        pet.add_task(next_task)
```

---

## Complete Workflow

### Model: Buddy's Daily Feeding Schedule

**Day 1 (April 1):**
```
Morning: Feed Buddy (due Apr 1) [TODO]
Evening: Mark as DONE
         → Auto-creates: Feed Buddy (due Apr 2)
```

**Day 2 (April 2):**
```
Morning: Feed Buddy (due Apr 2) [TODO]
Evening: Mark as DONE
         → Auto-creates: Feed Buddy (due Apr 3)
```

**Day 3 (April 3):**
```
Morning: Feed Buddy (due Apr 3) [TODO]
Evening: Mark as DONE
         → Auto-creates: Feed Buddy (due Apr 4)
```

**System Status:**
```
At any point, only ONE "Feed Buddy" task is incomplete:
- 3 completed from previous days
- 1 active for today
- Others auto-created as you complete
```

---

## Key Differences

### Old Way (Manual)
```python
# Day 1
feed1 = Task("Feed", 5, "high", "feeding", recurring="daily")
buddy.add_task(feed1)
feed1.mark_complete()  # Task done, but no next one created

# Day 2 - Need to manually create!
feed2 = Task("Feed", 5, "high", "feeding", recurring="daily")
buddy.add_task(feed2)
feed2.mark_complete()  # Again, no auto-creation
```

### New Way (Automatic)
```python
# Day 1
feed1 = Task("Feed", 5, "high", "feeding", recurring="daily")
buddy.add_task(feed1)
buddy.complete_task(feed1)  # Auto-creates feed2!

# Day 2
# feed2 already exists, just complete it
buddy.complete_task(feed2)  # Auto-creates feed3!
```

---

## Testing the Demo

Run the demo to see all features:
```bash
python main.py
```

Watch:
1. Tasks created (3 initial tasks)
2. Daily tasks auto-reproduce next day (+1 day)
3. Weekly task auto-reproduces next week (+7 days)
4. Tasks sorted by date in output

---

## Summary

| Feature | Status |
|---------|--------|
| Daily task repeat | ✓ Auto +1 day |
| Weekly task repeat | ✓ Auto +7 days |
| New task properties | ✓ Same as original |
| Task list growth | ✓ Smart management |
| No manual creation | ✓ Automatic |

**Result:** Your schedule stays fresh automatically!
