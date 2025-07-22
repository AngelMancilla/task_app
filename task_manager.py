import json
import os
from dataclasses import dataclass, field
from typing import Optional
import datetime
from enum import Enum

class Status(Enum):
    ACTIVA = "Activa"
    EN_PROGRESO = "En progreso"
    COMPLETADA = "Completada"


@dataclass
class Task:
    id: int
    title: str
    description: str
    status: Status = Status.ACTIVA
    priority: int = 2
    limit_date: Optional[datetime.datetime] = None
    created_time: datetime.datetime = field(default_factory=datetime.datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value, 
            "priority": self.priority,
            "limit_date": self.limit_date.isoformat() if self.limit_date else None,
            "created_time": self.created_time.isoformat()
        }
        
    @staticmethod
    def from_dict(data: dict) -> "Task":
        return Task(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            status=Status(data["status"]),
            priority=data["priority"],
            limit_date=datetime.fromisoformat(data["limit_date"]) if data["limit_date"] else None
        )



class TaskManager:
    def __init__(self, storage_file='tasks.json'):
        self.storage_file = storage_file
        self.tasks = []
        self.next_id = 1
        self.load_tasks_from_file()

    def load_tasks_from_file(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                for task_data in data:
                    task = Task.from_dict(task_data)
                    self.tasks.append(task)
                if self.tasks:
                    self.next_id = max(task.id for task in self.tasks) + 1

    def save_tasks_to_file(self):
        with open(self.storage_file, 'w') as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

    def add_task(self, title: str, description: str, priority: int = 2, limit_date: Optional[datetime] = None) -> Task:
        task = Task(id=self.next_id, title=title, description=description, priority=priority, limit_date=limit_date)
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks_to_file()
        return task

    def get_tasks(self):
        return [task.to_dict() for task in self.tasks]

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
                    status: Optional[Status] = None, priority: Optional[int] = None,
                    limit_date: Optional[datetime] = None):
        for task in self.tasks:
            if task.id == task_id:
                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description
                if status is not None:
                    task.status = status
                if priority is not None:
                    task.priority = priority
                if limit_date is not None:
                    task.limit_date = limit_date
                self.save_tasks_to_file()
                return task.to_dict()
        return None

    def delete_task(self, task_id: int):
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_tasks_to_file()
                return True
        return False

    def search_by_title_or_description(self, query: str):
        results = []
        for task in self.tasks:
            if query.lower() in task.title.lower() or query.lower() in task.description.lower():
                results.append(task.to_dict())
        return results

    def filter_by_status(self, status: Status):
        results = []
        for task in self.tasks:
            if task.status == status:
                results.append(task.to_dict())
        return results

    def filter_by_priority(self, priority: int):
        results = []
        for task in self.tasks:
            if task.priority == priority:
                results.append(task.to_dict())
        return results
    
    