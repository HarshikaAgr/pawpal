from dataclasses import dataclass, field
from typing import List


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: str = ""

    def update_preferences(self, new_preferences: str) -> None:
        pass

    def set_available_time(self, minutes: int) -> None:
        pass

    def view_plan(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0

    def get_pet_info(self) -> str:
        pass

    def update_pet_info(self, name: str, species: str, age: int) -> None:
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    category: str
    is_required: bool = False
    completed: bool = False

    def update_task(
        self,
        title: str,
        duration_minutes: int,
        priority: str,
        category: str,
        is_required: bool
    ) -> None:
        pass

    def mark_complete(self) -> None:
        pass

    def get_task_details(self) -> str:
        pass


class Scheduler:
    def __init__(self, tasks: List[Task], available_time: int, owner_preferences: str = ""):
        self.tasks = tasks
        self.available_time = available_time
        self.owner_preferences = owner_preferences

    def generate_plan(self) -> List[Task]:
        pass

    def sort_tasks_by_priority(self) -> List[Task]:
        pass

    def check_time_fit(self, task: Task) -> bool:
        pass

    def explain_plan(self) -> str:
        pass