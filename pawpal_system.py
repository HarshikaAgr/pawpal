from datetime import datetime, timedelta


class Task:
    """One pet care activity (like feeding, walking, etc)."""

    def __init__(
        self,
        title,
        duration_minutes,
        priority,
        category,
        recurring="none",
        start_time="00:00",
        due_date=None,
    ):
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.is_required = False
        self.completed = False
        self.pet = None
        self.recurring = recurring
        self.start_time = start_time
        self.due_date = due_date if due_date else datetime.now().date()

    def mark_complete(self):
        """Mark this task as done."""
        self.completed = True

    def get_next_due_date(self):
        """Return the next due date for recurring tasks."""
        if self.recurring == "daily":
            return self.due_date + timedelta(days=1)
        if self.recurring == "weekly":
            return self.due_date + timedelta(days=7)
        return None

    def create_next_task(self):
        """Create the next recurring task instance."""
        if not self.is_recurring():
            return None

        next_date = self.get_next_due_date()

        next_task = Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            recurring=self.recurring,
            start_time=self.start_time,
            due_date=next_date,
        )
        next_task.pet = self.pet
        next_task.is_required = self.is_required
        return next_task

    def get_task_details(self):
        """Return a readable string for this task."""
        pet_name = self.pet.name if self.pet else "No pet"
        status = "Done" if self.completed else "To Do"
        date_str = self.due_date.strftime("%Y-%m-%d") if self.due_date else "No date"
        recurrence_text = f", {self.recurring}" if self.recurring != "none" else ""

        return (
            f"{self.title} | Pet: {pet_name} | Time: {self.start_time} | "
            f"Date: {date_str} | {self.duration_minutes} min | "
            f"{self.priority}{recurrence_text} | {status}"
        )

    def update_task(
        self,
        title,
        duration_minutes,
        priority,
        category,
        is_required=False,
        recurring="none",
        start_time="00:00",
    ):
        """Update task details."""
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.is_required = is_required
        self.recurring = recurring
        self.start_time = start_time

    def is_recurring(self):
        """Return True if the task repeats."""
        return self.recurring != "none"

    def get_recurrence_info(self):
        """Return readable recurrence text."""
        if self.is_recurring():
            return f"(repeats {self.recurring})"
        return ""


class Pet:
    """A pet with details and care tasks."""

    def __init__(self, name, species, age):
        self.name = name
        self.species = species
        self.age = age
        self.tasks = []

    def get_pet_info(self):
        """Return readable pet info."""
        return f"{self.name} is a {self.age} year old {self.species}"

    def update_pet_info(self, name, species, age):
        """Update pet details."""
        self.name = name
        self.species = species
        self.age = age

    def add_task(self, task):
        """Add a task to this pet."""
        task.pet = self
        self.tasks.append(task)

    def get_all_tasks(self):
        """Return all tasks for this pet."""
        return self.tasks

    def filter_incomplete_tasks(self):
        """Return incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]

    def filter_recurring_tasks(self):
        """Return recurring tasks for this pet."""
        return [task for task in self.tasks if task.is_recurring()]

    def complete_task(self, task):
        """Mark a task complete and auto-create the next one if recurring."""
        task.mark_complete()

        if task.is_recurring():
            next_task = task.create_next_task()
            if next_task:
                self.add_task(next_task)
                return next_task

        return None


class Owner:
    """A person who owns one or more pets."""

    def __init__(self, name, available_minutes):
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = ""
        self.pets = []

    def set_available_time(self, minutes):
        """Update available time."""
        self.available_minutes = minutes

    def update_preferences(self, preferences):
        """Update owner preferences."""
        self.preferences = preferences

    def view_plan(self):
        """Print owner information."""
        print(f"Owner: {self.name}")
        print(f"Available time: {self.available_minutes} minutes")
        print(f"Preferences: {self.preferences if self.preferences else 'None'}")

    def add_pet(self, pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_all_tasks())
        return all_tasks

    def get_tasks_for_pet(self, pet_name):
        """Return all tasks for a single pet."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet.get_all_tasks()
        return []

    def get_incomplete_tasks(self):
        """Return incomplete tasks across all pets."""
        return [task for task in self.get_all_tasks() if not task.completed]

    def get_completed_tasks(self):
        """Return completed tasks across all pets."""
        return [task for task in self.get_all_tasks() if task.completed]


class Scheduler:
    """The brain that selects and organizes tasks."""

    def __init__(self, owner):
        self.owner = owner
        self.planned_tasks = []

    def sort_tasks_by_priority(self):
        """Sort incomplete tasks by priority."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        tasks = self.get_incomplete_tasks()
        return sorted(tasks, key=lambda task: (priority_order.get(task.priority, 3), task.duration_minutes))

    def sort_tasks_by_duration(self):
        """Sort incomplete tasks from shortest to longest."""
        tasks = self.get_incomplete_tasks()
        return sorted(tasks, key=lambda task: task.duration_minutes)

    def sort_by_time(self):
        """Sort incomplete tasks by HH:MM start time."""
        tasks = self.get_incomplete_tasks()
        return sorted(tasks, key=lambda task: int(task.start_time.replace(":", "")))

    def filter_by_completion(self, completed_only=False):
        """Filter tasks by completion."""
        all_tasks = self.owner.get_all_tasks()
        if completed_only:
            return [task for task in all_tasks if task.completed]
        return [task for task in all_tasks if not task.completed]

    def filter_by_pet(self, pet_name):
        """Return incomplete tasks for one pet."""
        tasks = self.get_incomplete_tasks()
        return [task for task in tasks if task.pet and task.pet.name == pet_name]

    def filter_by_category(self, category):
        """Return incomplete tasks in one category."""
        tasks = self.get_incomplete_tasks()
        return [task for task in tasks if task.category == category]

    def check_time_fit(self, task, remaining_time):
        """Return True if the task fits in the remaining time."""
        return task.duration_minutes <= remaining_time

    def get_incomplete_tasks(self):
        """Return only incomplete tasks."""
        return self.owner.get_incomplete_tasks()

    def check_time_conflict(self, task1, task2):
        """Return True if two tasks start at the same time."""
        return task1.start_time == task2.start_time

    def detect_all_conflicts(self):
        """Return conflict warning messages for planned tasks."""
        conflicts = []

        for i in range(len(self.planned_tasks)):
            for j in range(i + 1, len(self.planned_tasks)):
                task1 = self.planned_tasks[i]
                task2 = self.planned_tasks[j]

                if self.check_time_conflict(task1, task2):
                    conflicts.append(
                        f"⚠️ CONFLICT: '{task1.title}' and '{task2.title}' both start at {task1.start_time}"
                    )

        return conflicts

    def get_schedule_stats(self):
        """Return basic schedule statistics."""
        all_tasks = self.owner.get_all_tasks()
        completed_list = [task for task in all_tasks if task.completed]
        incomplete_list = [task for task in all_tasks if not task.completed]
        total_time_scheduled = sum(task.duration_minutes for task in self.planned_tasks)

        return {
            "total_tasks": len(all_tasks),
            "completed_tasks": len(completed_list),
            "incomplete_tasks": len(incomplete_list),
            "total_time_needed": sum(task.duration_minutes for task in incomplete_list),
            "available_time": self.owner.available_minutes,
            "total_time_scheduled": total_time_scheduled,
            "time_remaining": self.owner.available_minutes - total_time_scheduled,
        }

    def print_stats(self):
        """Return readable stats text."""
        stats = self.get_schedule_stats()
        stats_text = "\n=== SCHEDULE STATISTICS ===\n"
        stats_text += f"Total tasks: {stats['total_tasks']}\n"
        stats_text += f"Completed: {stats['completed_tasks']}\n"
        stats_text += f"Incomplete: {stats['incomplete_tasks']}\n"
        stats_text += f"Total time needed: {stats['total_time_needed']} minutes\n"
        stats_text += f"Available time: {stats['available_time']} minutes\n"
        stats_text += f"Time scheduled: {stats['total_time_scheduled']} minutes\n"
        stats_text += f"Time remaining: {stats['time_remaining']} minutes\n"
        return stats_text

    def generate_plan(self):
        """Build the final schedule using priority first, then time fit."""
        sorted_tasks = self.sort_tasks_by_priority()
        remaining_time = self.owner.available_minutes
        self.planned_tasks = []

        for task in sorted_tasks:
            if self.check_time_fit(task, remaining_time):
                self.planned_tasks.append(task)
                remaining_time -= task.duration_minutes

        return self.planned_tasks

    def explain_plan(self):
        """Explain why these tasks were chosen."""
        if not self.planned_tasks:
            return f"No tasks fit in {self.owner.available_minutes} minutes. Need more time!"

        explanation = f"\n=== Schedule for {self.owner.name} ===\n"
        explanation += f"Available time: {self.owner.available_minutes} minutes\n"
        explanation += f"Tasks selected: {len(self.planned_tasks)}\n\n"

        total_time = 0
        for task in self.planned_tasks:
            pet_name = task.pet.name if task.pet else "No pet"
            explanation += (
                f"- {task.title} for {pet_name} at {task.start_time} "
                f"({task.duration_minutes} min, {task.priority})\n"
            )
            total_time += task.duration_minutes

        leftover = self.owner.available_minutes - total_time
        explanation += f"\nTime used: {total_time} minutes"
        explanation += f"\nTime left: {leftover} minutes\n"
        explanation += "\nTasks were chosen by priority first, then by whether they fit in the time available."

        return explanation