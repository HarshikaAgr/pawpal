classDiagram
    class Owner {
        +name: str
        +available_minutes: int
        +preferences: str
        +update_preferences()
        +set_available_time()
        +view_plan()
    }

    class Pet {
        +name: str
        +species: str
        +age: int
        +get_pet_info()
        +update_pet_info()
    }

    class Task {
        +title: str
        +duration_minutes: int
        +priority: str
        +category: str
        +is_required: bool
        +update_task()
        +mark_complete()
        +get_task_details()
    }

    class Scheduler {
        +tasks: list
        +available_time: int
        +owner_preferences: str
        +generate_plan()
        +sort_tasks_by_priority()
        +check_time_fit()
        +explain_plan()
    }

    Owner --> Pet : owns
    Pet --> Task : has
    Scheduler --> Task : schedules
    Scheduler --> Owner : uses info
    Scheduler --> Pet : uses info