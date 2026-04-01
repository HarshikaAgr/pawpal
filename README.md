# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## ✨ Core Features Implemented

### **Sorting & Organization**
- **By Priority**: High → Medium → Low
- **By Duration**: Shortest tasks first (fit more in limited time)
- **By Time**: Chronological order (08:00 → 09:00 → 18:30)

### **Smart Task Management**
- **Recurring Tasks**: Daily & weekly tasks auto-create next occurrence when completed
- **Task Filtering**: View by pet, by completion status, by category
- **Time Constraints**: Only schedule tasks that fit in available time

### **Scheduling Intelligence**
- **Conflict Detection**: ⚠️ Warns if tasks overlap (same start time)
- **Schedule Explanation**: Shows which tasks fit and why (priority-based)
- **Statistics Tracking**: Completed tasks, pending tasks, time breakdown

### **User Experience**
- Create owner profiles and manage multiple pets
- Add tasks with priority, duration, category, recurrence
- View organized task lists (sorted by user preference)
- Generate optimized daily schedules in one click

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
# Demo (CLI)
python main.py

# Interactive (Streamlit)
streamlit run app.py
```

---

## Smarter Scheduling Features

Your PawPal+ system now includes intelligent task management:

### 1. **Recurring Tasks**
- Tasks can repeat daily or weekly
- When completed, new instance auto-creates for next occurrence
- Daily: Creates task for tomorrow
- Weekly: Creates task for next week
- Smart completion: `pet.complete_task(task)` handles everything

### 2. **Sorting & Filtering**
- **Sort by Priority**: High → Medium → Low
- **Sort by Duration**: Shortest first (fit more tasks!)
- **Sort by Time**: Tasks ordered 08:00 → 09:00 → etc
- **Filter by Status**: Show completed or incomplete tasks
- **Filter by Pet**: Show tasks for one pet
- **Filter by Category**: Show feeding, exercise, grooming, etc

### 3. **Conflict Detection**
- Warns if two tasks start at same time (can't do both!)
- Non-blocking: Displays warnings but continues running
- Helps owners spot scheduling overlaps
- Example: Feed @ 08:00 + Play @ 08:00 = ⚠️ CONFLICT

### 4. **Schedule Explanation**
- Shows which tasks fit in available time
- Displays time used vs remaining
- Explains why tasks were chosen (priority-based greedy algorithm)
- Statistics: completed tasks, pending tasks, time breakdown

---

## Testing PawPal+
### Run Tests

```bash
python -m pytest tests/test_pawpal.py -v
```
### What's Tested

| Test | Coverage |
|------|----------|
| **Task Completion** | Mark tasks as done |
| **Pet Task Management** | Add/remove tasks from pets |
| **Owner Management** | Add pets to owner |
| **Scheduler Plan** | Generate feasible schedules |
| **Chronological Sorting** | Tasks ordered by time (08:00 → 14:00 → 18:30) |
| **Recurring Tasks** | Daily task completion auto-creates next occurrence |
| **Conflict Detection** | Warns when tasks overlap at same start time |

### Test Results
- **Total Tests**: 7
- **Passed**: 7 ✓
- **Failed**: 0

### Confidence Level: ⭐⭐⭐⭐⭐
All core behaviors validated:
- ✓ Happy paths (normal operation)
- ✓ Edge cases (conflicts, recurrence)
- ✓ Data integrity (proper sorting, creation)

---

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
