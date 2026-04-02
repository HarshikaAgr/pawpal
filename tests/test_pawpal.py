from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete():
    task = Task("Feed Buddy", 5, "high", "feeding")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_to_pet():
    buddy = Pet("Buddy", "dog", 3)
    assert len(buddy.tasks) == 0

    task1 = Task("Morning Walk", 20, "high", "exercise")
    task2 = Task("Feed Buddy", 5, "high", "feeding")

    buddy.add_task(task1)
    buddy.add_task(task2)

    assert len(buddy.tasks) == 2


def test_add_pet_to_owner():
    john = Owner("John", 60)
    assert len(john.pets) == 0

    buddy = Pet("Buddy", "dog", 3)
    john.add_pet(buddy)

    assert len(john.pets) == 1


def test_generate_plan():
    john = Owner("John", 60)
    buddy = Pet("Buddy", "dog", 3)
    john.add_pet(buddy)

    walk = Task("Walk", 20, "high", "exercise")
    feed = Task("Feed", 5, "high", "feeding")
    buddy.add_task(walk)
    buddy.add_task(feed)

    scheduler = Scheduler(john)
    plan = scheduler.generate_plan()

    assert len(plan) == 2


def test_sort_by_time():
    john = Owner("John", 120)
    buddy = Pet("Buddy", "dog", 3)
    john.add_pet(buddy)

    task1 = Task("Afternoon Walk", 20, "high", "exercise", start_time="14:00")
    task2 = Task("Morning Feed", 5, "high", "feeding", start_time="08:00")
    task3 = Task("Evening Play", 15, "medium", "play", start_time="18:30")

    buddy.add_task(task1)
    buddy.add_task(task2)
    buddy.add_task(task3)

    scheduler = Scheduler(john)
    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks[0].start_time == "08:00"
    assert sorted_tasks[1].start_time == "14:00"
    assert sorted_tasks[2].start_time == "18:30"


def test_recurring_task_creates_next():
    john = Owner("John", 120)
    buddy = Pet("Buddy", "dog", 3)
    john.add_pet(buddy)

    today = date.today()
    daily_feed = Task(
        "Daily Feed",
        5,
        "high",
        "feeding",
        recurring="daily",
        due_date=today,
    )
    buddy.add_task(daily_feed)

    next_task = buddy.complete_task(daily_feed)

    assert len(buddy.tasks) == 2
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)


def test_detect_time_conflicts():
    john = Owner("John", 120)
    buddy = Pet("Buddy", "dog", 3)
    john.add_pet(buddy)

    task1 = Task("Feed", 5, "high", "feeding", start_time="09:00")
    task2 = Task("Walk", 20, "high", "exercise", start_time="09:00")

    buddy.add_task(task1)
    buddy.add_task(task2)

    scheduler = Scheduler(john)
    scheduler.generate_plan()
    conflicts = scheduler.detect_all_conflicts()

    assert len(conflicts) == 1
    assert "CONFLICT" in conflicts[0]


def test_no_task_fits_in_available_time():
    john = Owner("John", 5)
    buddy = Pet("Buddy", "dog", 3)
    john.add_pet(buddy)

    long_task = Task("Long Walk", 30, "high", "exercise")
    buddy.add_task(long_task)

    scheduler = Scheduler(john)
    plan = scheduler.generate_plan()

    assert plan == []