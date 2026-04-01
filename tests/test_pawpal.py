# Simple tests for PawPal+ system

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


# BONUS TEST 3: Owner Pet Addition
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


# BONUS TEST 4: Scheduler Plan Generation
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


if __name__ == "__main__":
    test_mark_complete()
    test_add_task_to_pet()
    test_add_pet_to_owner()
    test_generate_plan()
    print("\nAll tests passed! ✓")
