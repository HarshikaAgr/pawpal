from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


def print_task_list(title, tasks):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    if not tasks:
        print("No tasks.")
        return

    for i, task in enumerate(tasks, start=1):
        pet_name = task.pet.name if task.pet else "No pet"
        status = "DONE" if task.completed else "TODO"
        print(
            f"{i}. [{status}] {task.title} | Pet: {pet_name} | "
            f"Time: {task.start_time} | Duration: {task.duration_minutes} min | "
            f"Priority: {task.priority}"
        )


print("=" * 70)
print("PAWPAL+ CLI DEMO")
print("=" * 70)

# 1. Create owner and two pets
john = Owner("John", 120)
buddy = Pet("Buddy", "dog", 3)
luna = Pet("Luna", "cat", 2)

john.add_pet(buddy)
john.add_pet(luna)

print("\nCreated owner and pets:")
print(f"- Owner: {john.name}")
print(f"- Pet 1: {buddy.get_pet_info()}")
print(f"- Pet 2: {luna.get_pet_info()}")

# 2. Add tasks with different times
today = datetime.now().date()

feed_buddy = Task("Feed Buddy", 5, "high", "feeding", recurring="daily", start_time="08:00", due_date=today)
walk_buddy = Task("Morning Walk", 20, "high", "exercise", recurring="daily", start_time="09:00", due_date=today)
groom_buddy = Task("Groom Buddy", 25, "medium", "grooming", recurring="weekly", start_time="15:00", due_date=today)

feed_luna = Task("Feed Luna", 5, "high", "feeding", recurring="daily", start_time="08:00", due_date=today)
play_luna = Task("Play with Luna", 15, "medium", "play", start_time="18:30", due_date=today)

buddy.add_task(feed_buddy)
buddy.add_task(walk_buddy)
buddy.add_task(groom_buddy)

luna.add_task(feed_luna)
luna.add_task(play_luna)

print_task_list("ALL TASKS BEFORE SCHEDULING", john.get_all_tasks())

# 3. Show chronological order
scheduler = Scheduler(john)
time_sorted_tasks = scheduler.sort_by_time()
print_task_list("TASKS SORTED BY TIME", time_sorted_tasks)

# 4. Generate plan
planned_tasks = scheduler.generate_plan()
print_task_list("TODAY'S SCHEDULE", planned_tasks)

# 5. Show conflict warnings
conflicts = scheduler.detect_all_conflicts()
print("\n" + "=" * 70)
print("CONFLICT CHECK")
print("=" * 70)

if conflicts:
    for conflict in conflicts:
        print(conflict)
else:
    print("No conflicts detected.")

# 6. Explain the plan
print("\n" + "=" * 70)
print("PLAN EXPLANATION")
print("=" * 70)
print(scheduler.explain_plan())

# 7. Complete one recurring task
print("\n" + "=" * 70)
print("RECURRING TASK DEMO")
print("=" * 70)
print(f"Before completion, Buddy has {len(buddy.tasks)} tasks.")

next_task = buddy.complete_task(feed_buddy)

print(f"After completion, Buddy has {len(buddy.tasks)} tasks.")
print(f"Completed task: {feed_buddy.title}")

if next_task:
    print(
        f"New recurring task created: {next_task.title} "
        f"for {next_task.due_date.strftime('%Y-%m-%d')}"
    )

print_task_list("FINAL TASK LIST AFTER COMPLETION", john.get_all_tasks())

print("\n" + "=" * 70)
print("DEMO COMPLETE")
print("=" * 70)