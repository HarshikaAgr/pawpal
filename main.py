# Demo script - Test PawPal+ system

from pawpal_system import Owner, Pet, Task, Scheduler

# Step 1: Create an owner
print("=== Creating Owner ===")
john = Owner("John", 60)  # John has 60 minutes available today
print(f"Owner created: {john.name} with {john.available_minutes} minutes")

# Step 2: Create pets
print("\n=== Creating Pets ===")
buddy = Pet("Buddy", "dog", 3)
whiskers = Pet("Whiskers", "cat", 2)
print(f"Pet 1: {buddy.get_pet_info()}")
print(f"Pet 2: {whiskers.get_pet_info()}")

# Step 3: Add pets to owner
john.add_pet(buddy)
john.add_pet(whiskers)
print(f"Added 2 pets to {john.name}")

# Step 4: Create tasks for each pet
print("\n=== Creating Tasks ===")

# Tasks for Buddy (dog)
walk = Task("Morning Walk", 20, "high", "exercise")
feed_buddy = Task("Feed Buddy", 5, "high", "feeding")
buddy.add_task(walk)
buddy.add_task(feed_buddy)

# Tasks for Whiskers (cat)
feed_whiskers = Task("Feed Whiskers", 5, "high", "feeding")
playtime = Task("Playtime with Whiskers", 15, "medium", "exercise")
grooming = Task("Groom Whiskers", 10, "low", "grooming")
whiskers.add_task(feed_whiskers)
whiskers.add_task(playtime)
whiskers.add_task(grooming)

print(f"Created 3 tasks for {buddy.name}")
print(f"Created 3 tasks for {whiskers.name}")

# Step 5: Create scheduler
print("\n=== Creating Schedule ===")
scheduler = Scheduler(john)
scheduled_tasks = scheduler.generate_plan()

# Step 6: Print the schedule
print("\n" + "="*50)
print(scheduler.explain_plan())
print("="*50)

# Step 7: Show what didn't fit
print("\n=== All Available Tasks ===")
all_tasks = john.get_all_tasks()
print(f"Total tasks available: {len(all_tasks)}\n")

for task in all_tasks:
    status = "[SCHEDULED]" if task in scheduled_tasks else "[NO TIME]"
    print(f"{status}: {task.get_task_details()}")
