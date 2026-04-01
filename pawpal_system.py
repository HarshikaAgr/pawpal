# Simple PawPal+ System - Beginner Friendly

from datetime import datetime, timedelta

class Task:
    """One pet care activity (like feeding, walking, etc)"""

    def __init__(self, title, duration_minutes, priority, category, recurring="none", start_time="00:00", due_date=None):
        self.title = title
        self.duration_minutes = duration_minutes  # How long it takes
        self.priority = priority  # "high", "medium", or "low"
        self.category = category  # "feeding", "walking", "grooming", etc
        self.is_required = False  # Does the pet need this?
        self.completed = False  # Is it done?
        self.pet = None  # Which pet is this for?
        self.recurring = recurring  # "none", "daily", "weekly"
        self.start_time = start_time  # When task starts (HH:MM format)
        # If no due_date given, use today
        self.due_date = due_date if due_date else datetime.now().date()

    def mark_complete(self):
        """Mark this task as done"""
        self.completed = True

    def get_next_due_date(self):
        """Calculate when the next occurrence of this task is due"""
        if self.recurring == "none":
            return None  # Non-recurring task, no next date
        elif self.recurring == "daily":
            # Add 1 day to current due date
            next_date = self.due_date + timedelta(days=1)
            return next_date
        elif self.recurring == "weekly":
            # Add 7 days to current due date
            next_date = self.due_date + timedelta(days=7)
            return next_date
        return None

    def create_next_task(self):
        """Create a new task instance for the next occurrence

        Returns: New Task object (not added to pet yet)
        """
        if not self.is_recurring():
            return None  # Only recurring tasks can create next task

        next_date = self.get_next_due_date()

        # Create new task with same properties but new due date
        next_task = Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            recurring=self.recurring,
            start_time=self.start_time,
            due_date=next_date
        )

        # Copy pet reference
        next_task.pet = self.pet

        return next_task

    def get_task_details(self):
        """Show all info about this task"""
        pet_name = self.pet.name if self.pet else "No pet"
        status = "Done" if self.completed else "To Do"
        date_str = self.due_date.strftime("%Y-%m-%d") if self.due_date else "No date"

        return f"{self.title} [{self.start_time}] ({date_str}) ({self.duration_minutes}min, {self.priority}) - {status}"

    def update_task(self, title, duration_minutes, priority, category, is_required):
        """Change task details"""
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.is_required = is_required

    def is_recurring(self):
        """Check if this task repeats"""
        return self.recurring != "none"

    def get_recurrence_info(self):
        """Show if task is recurring"""
        if self.is_recurring():
            return f"(repeats {self.recurring})"
        return ""


class Pet:
    """A pet with its name, type, and care tasks"""

    def __init__(self, name, species, age):
        self.name = name  # "Buddy", "Whiskers", etc
        self.species = species  # "dog", "cat", "hamster", etc
        self.age = age  # How old (in years)
        self.tasks = []  # List of tasks for this pet

    def get_pet_info(self):
        """Show pet details"""
        return f"{self.name} is a {self.age} year old {self.species}"

    def update_pet_info(self, name, species, age):
        """Update pet details"""
        self.name = name
        self.species = species
        self.age = age

    def add_task(self, task):
        """Add a care task for this pet"""
        task.pet = self  # Link the task to this pet
        self.tasks.append(task)

    def get_all_tasks(self):
        """Get list of all tasks for this pet"""
        return self.tasks

    def filter_incomplete_tasks(self):
        """Get only incomplete (not done) tasks for this pet"""
        incomplete = []
        for task in self.tasks:
            if not task.completed:
                incomplete.append(task)
        return incomplete

    def filter_recurring_tasks(self):
        """Get only recurring tasks for this pet"""
        recurring = []
        for task in self.tasks:
            if task.is_recurring():
                recurring.append(task)
        return recurring

    def complete_task(self, task):
        """Mark a task complete and auto-create next task if recurring

        This is the smart version of mark_complete()
        - Marks task as done
        - If recurring, automatically creates next occurrence
        """
        # Mark as complete
        task.mark_complete()

        # If recurring, create next task
        if task.is_recurring():
            next_task = task.create_next_task()
            if next_task:
                self.add_task(next_task)
                return next_task  # Return the newly created task

        return None  # Non-recurring task, nothing new created


class Owner:
    """A person who owns one or more pets"""

    def __init__(self, name, available_minutes):
        self.name = name  # Owner's name
        self.available_minutes = available_minutes  # How much time they have today
        self.preferences = ""  # What they like/dislike
        self.pets = []  # List of pets they own

    def set_available_time(self, minutes):
        """Update how much time the owner has"""
        self.available_minutes = minutes

    def update_preferences(self, preferences):
        """Update owner's preferences"""
        self.preferences = preferences

    def view_plan(self):
        """Show owner info"""
        print(f"Owner: {self.name}")
        print(f"Available time: {self.available_minutes} minutes")
        print(f"Preferences: {self.preferences if self.preferences else 'None'}")

    def add_pet(self, pet):
        """Add a pet to this owner's list"""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Get ALL tasks from ALL pets (as one big list)"""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_all_tasks())
        return all_tasks

    def get_tasks_for_pet(self, pet_name):
        """Get tasks for only ONE specific pet"""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet.get_all_tasks()
        return []  # Pet not found

    def get_incomplete_tasks(self):
        """Get all incomplete tasks across ALL pets"""
        incomplete = []
        for task in self.get_all_tasks():
            if not task.completed:
                incomplete.append(task)
        return incomplete

    def get_completed_tasks(self):
        """Get all completed tasks across ALL pets"""
        completed = []
        for task in self.get_all_tasks():
            if task.completed:
                completed.append(task)
        return completed


class Scheduler:
    """The brain that decides which tasks to do and in what order"""

    def __init__(self, owner):
        self.owner = owner
        self.planned_tasks = []  # Tasks that fit in the time available

    def sort_tasks_by_priority(self):
        """Put high priority tasks first, then medium, then low"""
        all_tasks = self.owner.get_all_tasks()

        # Separate tasks by priority
        high_priority = []
        medium_priority = []
        low_priority = []

        for task in all_tasks:
            if task.priority == "high":
                high_priority.append(task)
            elif task.priority == "medium":
                medium_priority.append(task)
            else:
                low_priority.append(task)

        # Return high first, then medium, then low
        return high_priority + medium_priority + low_priority

    def sort_tasks_by_duration(self):
        """Sort tasks from shortest to longest duration

        Useful for fitting more tasks in limited time.
        Returns: List of tasks sorted by duration (ascending)
        """
        all_tasks = self.owner.get_all_tasks()
        # Sort by duration (shortest first)
        return sorted(all_tasks, key=lambda task: task.duration_minutes)

    def sort_by_time(self):
        """Sort tasks by start time in chronological order

        Converts HH:MM format to comparable numbers (e.g., 09:30 → 930).
        Returns: List of tasks sorted by start time (early to late)
        """
        all_tasks = self.owner.get_all_tasks()
        # Sort by time using lambda: converts HH:MM to comparable number
        # Example: "09:30" -> 930 (9*60+30)
        return sorted(all_tasks, key=lambda task: int(task.start_time.replace(":", "")))

    def filter_by_completion(self, completed_only=False):
        """Filter tasks by completion status

        completed_only=True: Show only completed tasks
        completed_only=False: Show only incomplete tasks
        """
        all_tasks = self.owner.get_all_tasks()
        if completed_only:
            return [task for task in all_tasks if task.completed]
        else:
            return [task for task in all_tasks if not task.completed]

    def filter_by_pet(self, pet_name):
        """Get all tasks for one specific pet by name

        Returns: List of tasks belonging to the named pet (empty if pet not found)
        """
        all_tasks = self.owner.get_all_tasks()
        return [task for task in all_tasks if task.pet and task.pet.name == pet_name]

    def filter_by_category(self, category):
        """Filter tasks by category (feeding, exercise, grooming, etc)"""
        all_tasks = self.owner.get_all_tasks()
        return [task for task in all_tasks if task.category == category]

    def check_time_fit(self, task, remaining_time):
        """Does this task fit in the time we have left?"""
        return task.duration_minutes <= remaining_time

    def get_incomplete_tasks(self):
        """Get only tasks that are NOT done yet"""
        all_tasks = self.owner.get_all_tasks()
        incomplete = []
        for task in all_tasks:
            if not task.completed:
                incomplete.append(task)
        return incomplete

    def check_time_conflict(self, task1, task2):
        """Check if two tasks start at the same time"""
        return task1.start_time == task2.start_time

    def detect_all_conflicts(self):
        """Find ALL tasks scheduled at the same time in the plan

        Returns: List of conflict warning messages
        """
        conflicts = []

        # Compare each pair of tasks in the plan
        for i in range(len(self.planned_tasks)):
            for j in range(i + 1, len(self.planned_tasks)):
                task1 = self.planned_tasks[i]
                task2 = self.planned_tasks[j]

                # Same start time = CONFLICT!
                if task1.start_time == task2.start_time:
                    msg = f"⚠️ CONFLICT: '{task1.title}' and '{task2.title}' both at {task1.start_time}"
                    conflicts.append(msg)

        return conflicts

    def get_schedule_stats(self):
        """Show statistics about the schedule"""
        all_tasks = self.owner.get_all_tasks()
        completed_list = [task for task in all_tasks if task.completed]
        incomplete_list = [task for task in all_tasks if not task.completed]

        completed = len(completed_list)
        incomplete = len(incomplete_list)
        total_time_needed = sum(task.duration_minutes for task in incomplete_list)
        total_time_scheduled = sum(task.duration_minutes for task in self.planned_tasks)

        stats = {
            "total_tasks": len(all_tasks),
            "completed_tasks": completed,
            "incomplete_tasks": incomplete,
            "total_time_needed": total_time_needed,
            "available_time": self.owner.available_minutes,
            "total_time_scheduled": total_time_scheduled,
            "time_remaining": self.owner.available_minutes - total_time_scheduled
        }
        return stats

    def print_stats(self):
        """Print schedule statistics in readable format"""
        stats = self.get_schedule_stats()

        stats_text = "\n=== SCHEDULE STATISTICS ===\n"
        stats_text += f"Total tasks: {stats['total_tasks']}\n"
        stats_text += f"[DONE] Completed: {stats['completed_tasks']}\n"
        stats_text += f"[TODO] Incomplete: {stats['incomplete_tasks']}\n"
        stats_text += f"Total time needed: {stats['total_time_needed']} minutes\n"
        stats_text += f"Available time: {stats['available_time']} minutes\n"
        stats_text += f"Time scheduled: {stats['total_time_scheduled']} minutes\n"
        stats_text += f"Time remaining: {stats['time_remaining']} minutes\n"

        return stats_text

    def generate_plan(self):
        """Create a schedule with the tasks that fit"""
        sorted_tasks = self.sort_tasks_by_priority()
        remaining_time = self.owner.available_minutes
        self.planned_tasks = []

        # Go through tasks in order, add if they fit
        for task in sorted_tasks:
            if self.check_time_fit(task, remaining_time):
                self.planned_tasks.append(task)
                remaining_time -= task.duration_minutes  # Use up that time

        # Detect conflicts (but don't crash!)
        conflicts = self.detect_all_conflicts()
        if conflicts:
            print("\n" + "="*60)
            print("⚠️  WARNING: SCHEDULE CONFLICTS DETECTED!")
            print("="*60)
            for conflict in conflicts:
                print(f"{conflict}")
            print("="*60 + "\n")

        return self.planned_tasks

    def explain_plan(self):
        """Show why we picked these tasks"""
        if not self.planned_tasks:
            return f"No tasks fit in {self.owner.available_minutes} minutes. Need more time!"

        explanation = f"\n=== Schedule for {self.owner.name} ===\n"
        explanation += f"Available time: {self.owner.available_minutes} minutes\n"
        explanation += f"Tasks to do: {len(self.planned_tasks)}\n\n"

        total_time = 0
        for task in self.planned_tasks:
            explanation += f"  - {task.title} ({task.duration_minutes}min - {task.priority})\n"
            total_time += task.duration_minutes

        leftover = self.owner.available_minutes - total_time
        explanation += f"\nTime used: {total_time} minutes"
        explanation += f"\nTime left: {leftover} minutes\n"

        return explanation
