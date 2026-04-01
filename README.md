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

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
