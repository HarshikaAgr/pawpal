#Tests for PawPal+ system
from pawpal_system import Task, Pet, Owner, Scheduler

# TEST 1: Task Completion
def test_mark_complete():
    """Check that mark_complete() changes task status"""
    # Create a task
    task = Task("Feed Buddy", 5, "high", "feeding")

    # Task should start as NOT completed
    assert task.completed == False

    # Mark it complete
    task.mark_complete()

    # Now it should be completed
    assert task.completed == True
    print("✓ Test 1 PASSED: Task completion works!")


# TEST 2: Pet Task Addition
def test_add_task_to_pet():
    """Check that adding a task increases pet's task count"""
    # Create a pet
    buddy = Pet("Buddy", "dog", 3)

    # Pet should start with 0 tasks
    assert len(buddy.tasks) == 0

    # Create and add a task
    task = Task("Morning Walk", 20, "high", "exercise")
    buddy.add_task(task)

    # Pet should now have 1 task
    assert len(buddy.tasks) == 1

    # Add another task
    task2 = Task("Feed Buddy", 5, "high", "feeding")
    buddy.add_task(task2)

    # Pet should now have 2 tasks
    assert len(buddy.tasks) == 2
    print("✓ Test 2 PASSED: Pet task addition works!")

#TEST 3: Owner Pet Addition
def test_add_pet_to_owner():
    """Check that adding a pet increases owner's pet count"""
    # Create an owner
    john = Owner("John", 60)

    # Owner should start with 0 pets
    assert len(john.pets) == 0

    # Add a pet
    buddy = Pet("Buddy", "dog", 3)
    john.add_pet(buddy)

    # Owner should now have 1 pet
    assert len(john.pets) == 1
    print("✓ Test 3 PASSED: Owner pet addition works!")


#TEST 4: Scheduler Plan Generation
def test_generate_plan():
    """Check that scheduler creates a plan"""
    # Create owner and pet
    john = Owner("John", 60)
    buddy = Pet("Buddy", "dog", 3)
    john.add_pet(buddy)

    # Add tasks
    walk = Task("Walk", 20, "high", "exercise")
    feed = Task("Feed", 5, "high", "feeding")
    buddy.add_task(walk)
    buddy.add_task(feed)

    # Create scheduler and generate plan
    scheduler = Scheduler(john)
    plan = scheduler.generate_plan()

    # Should have 2 tasks in plan (both fit in 60 minutes)
    assert len(plan) == 2
    print("✓ Test 4 PASSED: Scheduler plan generation works!")


#TEST 5: Sorting by Time (Chronological Order)
def test_sort_by_time():
    """Check that tasks are sorted chronologically by start_time"""
    # Create owner and pet
    john = Owner("John", 120)
    buddy = Pet("Buddy", "dog", 3)
    john.add_pet(buddy)

    # Add tasks in random order with different times
    task1 = Task("Afternoon Walk", 20, "high", "exercise", start_time="14:00")
    task2 = Task("Morning Feed", 5, "high", "feeding", start_time="08:00")
    task3 = Task("Evening Play", 15, "medium", "exercise", start_time="18:30")
    buddy.add_task(task1)
    buddy.add_task(task2)
    buddy.add_task(task3)

    # Sort by time
    scheduler = Scheduler(john)
    sorted_tasks = scheduler.sort_by_time()

    # Should be in order: 08:00, 14:00, 18:30
    assert sorted_tasks[0].start_time == "08:00"
    assert sorted_tasks[1].start_time == "14:00"
    assert sorted_tasks[2].start_time == "18:30"
    print("✓ Test 5 PASSED: Tasks sorted chronologically!")


#TEST 6: Recurrence Logic
def test_recurring_task_creates_next():
    """Check that completing a daily task creates the next task"""
    # Create owner and pet
    john = Owner("John", 120)
    buddy = Pet("Buddy", "dog", 3)
    john.add_pet(buddy)

    # Create a daily recurring task
    from datetime import date
    today = date.today()
    daily_feed = Task("Daily Feed", 5, "high", "feeding", recurring="daily", due_date=today)
    buddy.add_task(daily_feed)

    # Before completion: 1 task
    assert len(buddy.tasks) == 1

    # Complete the task (should auto-create next)
    next_task = buddy.complete_task(daily_feed)

    # After completion: 2 tasks (original + new one for tomorrow)
    assert len(buddy.tasks) == 2
    assert next_task is not None
    assert next_task.due_date == today + __import__('datetime').timedelta(days=1)
    print("✓ Test 6 PASSED: Recurring task creates next occurrence!")


#TEST 7: Conflict Detection
def test_detect_time_conflicts():
    """Check that scheduler detects tasks scheduled at the same time"""
    # Create owner and pet
    john = Owner("John", 120)
    buddy = Pet("Buddy", "dog", 3)
    john.add_pet(buddy)

    # Add two tasks at SAME time (conflict!)
    task1 = Task("Feed", 5, "high", "feeding", start_time="09:00")
    task2 = Task("Walk", 20, "high", "exercise", start_time="09:00")
    buddy.add_task(task1)
    buddy.add_task(task2)

    # Generate plan (will detect conflict)
    scheduler = Scheduler(john)
    scheduler.generate_plan()

    # Check for conflicts
    conflicts = scheduler.detect_all_conflicts()

    # Should have detected 1 conflict
    assert len(conflicts) == 1
    assert "CONFLICT" in conflicts[0]
    print("✓ Test 7 PASSED: Conflicts detected correctly!")


if __name__ == "__main__":
    test_mark_complete()
    test_add_task_to_pet()
    test_add_pet_to_owner()
    test_generate_plan()
    test_sort_by_time()
    test_recurring_task_creates_next()
    test_detect_time_conflicts()
    print("\nAll tests passed! ✓")
