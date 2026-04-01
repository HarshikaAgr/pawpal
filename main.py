# Demo: Recurring Tasks Automation + Conflict Detection

from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime, timedelta

print("="*70)
print("PAWPAL+ RECURRING TASKS + CONFLICT DETECTION DEMO")
print("="*70)

# Step 1: Create owner and pet
print("\n[SETUP] Creating owner and pet...")
john = Owner("John", 120)
buddy = Pet("Buddy", "dog", 3)
john.add_pet(buddy)

print(f"Owner: {john.name}")
print(f"Pet: {buddy.name}")

# Step 2: Create recurring tasks with SOME AT SAME TIME (conflicts!)
print("\n[TASKS] Creating tasks (some with SAME start time to demonstrate conflicts)...")

today = datetime.now().date()

# Feed task at 08:00
feed = Task("Feed Buddy", 5, "high", "feeding", recurring="daily", start_time="08:00", due_date=today)
buddy.add_task(feed)

# CONFLICT! Play task ALSO at 08:00
play = Task("Play with Buddy", 15, "high", "exercise", start_time="08:00", due_date=today)
buddy.add_task(play)

# Walk task at 09:00 (no conflict)
walk = Task("Morning Walk", 20, "high", "exercise", recurring="daily", start_time="09:00", due_date=today)
buddy.add_task(walk)

# Grooming task at 15:00 (weekly)
grooming = Task("Groom Buddy", 30, "medium", "grooming", recurring="weekly", start_time="15:00", due_date=today)
buddy.add_task(grooming)

print(f"Created 4 tasks:")
print(f"  - Feed Buddy @ 08:00")
print(f"  - Play with Buddy @ 08:00  ← CONFLICTS WITH FEED!")
print(f"  - Morning Walk @ 09:00")
print(f"  - Groom Buddy @ 15:00")

# Step 3: Show initial tasks
print("\n" + "="*70)
print("BEFORE: All tasks in system")
print("="*70)
print(f"\nTotal tasks: {len(buddy.tasks)}\n")

for i, task in enumerate(buddy.tasks, 1):
    print(f"{i}. {task.get_task_details()}")

# Step 4: Generate schedule (will show CONFLICTS!)
print("\n" + "="*70)
print("GENERATING SCHEDULE (will detect conflicts automatically)")
print("="*70)

scheduler = Scheduler(john)
planned = scheduler.generate_plan()

print(f"\n✓ Schedule generated with {len(planned)} tasks")

# Step 5: Show explanation
print("\n" + "="*70)
print("SCHEDULE EXPLANATION")
print("="*70)
print(scheduler.explain_plan())

# Step 6: Complete a daily task (auto-creates next)
print("\n" + "="*70)
print("ACTION: Complete daily task (Feed Buddy)")
print("="*70)

print(f"\nBefore: {len(buddy.tasks)} tasks")
print(f"Completing: '{feed.title}'...")

next_feed = buddy.complete_task(feed)

print(f"After: {len(buddy.tasks)} tasks")
print(f"Status: Task marked as DONE")
if next_feed:
    print(f"Auto-created next: '{next_feed.title}' due {next_feed.due_date.strftime('%Y-%m-%d')}")

# Step 7: Show final status
print("\n" + "="*70)
print("FINAL: All tasks after completion and auto-creation")
print("="*70)
print(f"\nTotal tasks: {len(buddy.tasks)}\n")

for i, task in enumerate(buddy.tasks, 1):
    status = "DONE" if task.completed else "TODO"
    print(f"{i}. [{status}] {task.title}")
    print(f"   Time: {task.start_time} | Due: {task.due_date.strftime('%Y-%m-%d')}")

# Step 8: Summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)

completed = [t for t in buddy.tasks if t.completed]
incomplete = [t for t in buddy.tasks if not t.completed]

print(f"\n✓ Completed: {len(completed)} tasks")
print(f"✓ Incomplete: {len(incomplete)} tasks")
print(f"✓ Recurring tasks auto-create next occurrence!")
print(f"✓ Conflicts detected and displayed as warnings (no crash!)")

print("\n" + "="*70)
print("DEMO COMPLETE!")
print("="*70)
