classDiagram
    class Owner {
        +name: str
        +available_minutes: int
        +preferences: str
        +pets: list
        +set_available_time()
        +update_preferences()
        +view_plan()
        +add_pet()
        +get_all_tasks()
        +get_tasks_for_pet()
        +get_incomplete_tasks()
        +get_completed_tasks()
    }

    class Pet {
        +name: str
        +species: str
        +age: int
        +tasks: list
        +get_pet_info()
        +update_pet_info()
        +add_task()
        +get_all_tasks()
        +filter_incomplete_tasks()
        +filter_recurring_tasks()
        +complete_task()
    }

    class Task {
        +title: str
        +duration_minutes: int
        +priority: str
        +category: str
        +recurring: str
        +start_time: str
        +due_date: date
        +is_required: bool
        +completed: bool
        +pet: Pet
        +mark_complete()
        +get_next_due_date()
        +create_next_task()
        +get_task_details()
        +update_task()
        +is_recurring()
        +get_recurrence_info()
    }

    class Scheduler {
        +owner: Owner
        +planned_tasks: list
        +sort_tasks_by_priority()
        +sort_tasks_by_duration()
        +sort_by_time()
        +filter_by_completion()
        +filter_by_pet()
        +filter_by_category()
        +check_time_fit()
        +check_time_conflict()
        +detect_all_conflicts()
        +get_incomplete_tasks()
        +get_schedule_stats()
        +print_stats()
        +generate_plan()
        +explain_plan()
    }

    Owner --> Pet : owns multiple
    Pet --> Task : has multiple
    Scheduler --> Owner : schedules for
    Scheduler --> "planned_tasks" Task : plans with