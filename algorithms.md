# PawPal+ Smart Algorithms

This document describes the 6 smart algorithms implemented in Phase 3.

---

## Algorithm 1: Filter Recurring Tasks

**Location:** `Pet.filter_recurring_tasks()`

**What it does:**
- Shows only tasks that repeat daily or weekly
- Helps identify which tasks need to be done regularly

**Example:**
```python
buddy = Pet("Buddy", "dog", 3)
walk = Task("Morning Walk", 20, "high", "exercise", recurring="daily")
buddy.add_task(walk)

recurring = buddy.filter_recurring_tasks()  # Returns [walk]
```

**Why it's useful:**
- Quickly see which tasks repeat
- Plan recurring care routines
- Easier scheduling for repeated tasks

---

## Algorithm 2: Filter Incomplete Tasks

**Location:** `Pet.filter_incomplete_tasks()` and `Owner.get_incomplete_tasks()`

**What it does:**
- Returns only tasks that haven't been marked complete
- Filters out done tasks from the list

**Example:**
```python
whiskers = Pet("Whiskers", "cat", 2)
feed = Task("Feed", 5, "high", "feeding")
whiskers.add_task(feed)

incomplete = whiskers.filter_incomplete_tasks()  # Returns [feed]
feed.mark_complete()
incomplete = whiskers.filter_incomplete_tasks()  # Returns []
```

**Why it's useful:**
- See what still needs to be done
- Separate completed vs pending tasks
- Focus on remaining work

---

## Algorithm 3: Sort Tasks by Duration

**Location:** `Scheduler.sort_tasks_by_duration()`

**What it does:**
- Sorts all tasks from shortest to longest time
- Allows fitting more tasks into limited time

**Example:**
```python
scheduler = Scheduler(owner)
sorted_tasks = scheduler.sort_tasks_by_duration()
# Result: [5min, 5min, 10min, 15min, 20min]
```

**Why it's useful:**
- "Fit more tasks in less time" strategy
- Alternative to priority-based sorting
- Better for owners with very limited time

---

## Algorithm 4: Task Statistics

**Location:** `Scheduler.get_schedule_stats()` and `Scheduler.print_stats()`

**What it does:**
- Counts total tasks, completed, and incomplete tasks
- Calculates time needed vs time available
- Shows remaining time after scheduling

**Example:**
```python
scheduler = Scheduler(owner)
scheduler.generate_plan()
stats = scheduler.get_schedule_stats()

# Returns:
# {
#   "total_tasks": 5,
#   "completed_tasks": 0,
#   "incomplete_tasks": 5,
#   "total_time_needed": 55,
#   "available_time": 60,
#   "total_time_scheduled": 55,
#   "time_remaining": 5
# }
```

**Why it's useful:**
- See overall schedule health
- Identify if owner has enough time
- Track progress (completed vs remaining)
- Plan ahead for future tasks

---

## Algorithm 5: Generate Smart Schedule

**Location:** `Scheduler.generate_plan()`

**What it does:**
- Combines priority sorting with time checking
- Picks the best tasks that fit in available time
- Uses greedy algorithm (high priority first, check time fit)

**Example:**
```python
scheduler = Scheduler(owner)  # Owner has 60 minutes
planned = scheduler.generate_plan()

# With tasks: [5min, 5min, 10min, 15min, 20min] (by priority)
# Result: All 5 tasks fit (55 minutes total, 5 remaining)
```

**Why it's useful:**
- Automatically creates daily schedule
- Respects priority AND time constraints
- Explains what fits and what doesn't

---

## Algorithm 6: Conflict Detection

**Location:** `Scheduler.check_time_conflict(task1, task2)`

**What it does:**
- Detects if two tasks are both in the same schedule
- Simple overlap detection

**Example:**
```python
walk = Task("Walk", 20, "high", "exercise")
feed = Task("Feed", 5, "high", "feeding")

scheduler.planned_tasks = [walk, feed]
conflict = scheduler.check_time_conflict(walk, feed)  # Returns True
```

**Why it's useful:**
- Warn about scheduling conflicts
- Prevent double-booking
- Ensures tasks don't overlap

---

## Algorithm 7: Filter Tasks by Pet (Bonus)

**Location:** `Owner.get_tasks_for_pet(pet_name)`

**What it does:**
- Gets all tasks for one specific pet
- Filters across all owner's pets

**Example:**
```python
john = Owner("John", 60)
buddy = Pet("Buddy", "dog", 3)
john.add_pet(buddy)
# ... add tasks ...

buddy_tasks = john.get_tasks_for_pet("Buddy")  # Only Buddy's tasks
```

**Why it's useful:**
- Focus on one pet at a time
- Manage individual pet schedules
- See pet-specific tasks

---

## Summary Table

| # | Algorithm | Key Method | Input | Output |
|---|-----------|-----------|-------|--------|
| 1 | Filter Recurring | `filter_recurring_tasks()` | Pet | List of recurring tasks |
| 2 | Filter Incomplete | `filter_incomplete_tasks()` | Pet/Owner | List of incomplete tasks |
| 3 | Sort by Duration | `sort_tasks_by_duration()` | Scheduler | Tasks sorted short→long |
| 4 | Task Statistics | `get_schedule_stats()` | Scheduler | Dict with stats |
| 5 | Smart Schedule | `generate_plan()` | Scheduler | List of scheduled tasks |
| 6 | Conflict Detection | `check_time_conflict()` | 2 Tasks | True/False |
| 7 | Filter by Pet | `get_tasks_for_pet()` | Owner + pet name | List of pet's tasks |

---

## Demo Output

Run `python main.py` to see all algorithms in action:
```
ALGORITHM 1: Filter Recurring Tasks
Recurring tasks for Buddy: 2

ALGORITHM 2: Filter Incomplete Tasks
Incomplete tasks for Whiskers: 3

ALGORITHM 3: Sort Tasks by Duration
Tasks sorted by duration: 5min, 5min, 10min, 15min, 20min

ALGORITHM 4: Task Statistics (Before)
Total tasks: 5, Incomplete: 5, Time needed: 55min

ALGORITHM 5: Generate Smart Schedule
Schedule for John: 5 tasks fit (55/60 min)

ALGORITHM 6: Conflict Detection
No conflicts detected

ALGORITHM 4: Task Statistics (After)
Time scheduled: 55 min, Time remaining: 5 min
```

---

## Next Steps (Phase 4)

Future improvements could include:
- Sort by category (group similar tasks)
- Sort by pet (group by pet owner)
- Advanced conflict detection (time slots)
- AI-powered task recommendations
- One-click task completion tracking
