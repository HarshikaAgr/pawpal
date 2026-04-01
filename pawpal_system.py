# Simple PawPal+ System - Beginner Friendly

class Task:
    """One pet care activity (like feeding, walking, etc)"""

    def __init__(self, title, duration_minutes, priority, category):
        self.title = title
        self.duration_minutes = duration_minutes  # How long it takes
        self.priority = priority  # "high", "medium", or "low"
        self.category = category  # "feeding", "walking", "grooming", etc
        self.is_required = False  # Does the pet need this?
        self.completed = False  # Is it done?
        self.pet = None  # Which pet is this for?

    def mark_complete(self):
        """Mark this task as done"""
        self.completed = True

    def get_task_details(self):
        """Show all info about this task"""
        pet_name = self.pet.name if self.pet else "No pet"
        status = "Done" if self.completed else "To Do"

        return f"{self.title} ({self.duration_minutes}min, {self.priority}) - {status}"

    def update_task(self, title, duration_minutes, priority, category, is_required):
        """Change task details"""
        self.title = title
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.category = category
        self.is_required = is_required


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

    def check_time_fit(self, task, remaining_time):
        """Does this task fit in the time we have left?"""
        return task.duration_minutes <= remaining_time

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
