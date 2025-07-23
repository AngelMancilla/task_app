import json
import os
from dataclasses import dataclass, field
from typing import Optional
import datetime
from enum import Enum
from .task import Task, Status

class TaskManager:
    TASKS_FILE = os.path.join('data', 'tasks.json')

    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self._ensure_data_directory()
        self.load_tasks_from_file()

    def _ensure_data_directory(self):
        os.makedirs(os.path.dirname(self.TASKS_FILE), exist_ok=True)

    def load_tasks_from_file(self):
        if os.path.exists(self.TASKS_FILE):
            with open(self.TASKS_FILE, 'r') as f:
                try:
                    data = json.load(f)
                    for task_data in data:
                        task = Task.from_dict(task_data)
                        self.tasks.append(task)
                    if self.tasks:
                        self.next_id = max(task.id for task in self.tasks) + 1
                except json.JSONDecodeError:
                    print("Archivo JSON dañado o vacío. Se cargará sin tareas.")

    def save_tasks_to_file(self):
        with open(self.TASKS_FILE, 'w') as f:
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
        return [task.to_dict() for task in self.tasks
                if query.lower() in task.title.lower() or query.lower() in task.description.lower()]

    def filter_by_status(self, status: Status):
        return [task.to_dict() for task in self.tasks if task.status == status]

    def filter_by_priority(self, priority: int):
        return [task.to_dict() for task in self.tasks if task.priority == priority]
    
if __name__ == "__main__":
    tm = TaskManager()

    # Agregar tarea
    task = tm.add_task("Estudiar Python", "Repasar dataclasses y json", priority=1)
    print("Tarea agregada:", task.to_dict())

    # Listar todas
    print("Todas las tareas:", tm.get_tasks())

    # Buscar por palabra clave
    print("Buscar 'python':", tm.search_by_title_or_description("python"))

    # Actualizar tarea
    updated = tm.update_task(task.id, status=Status.COMPLETADA)
    print("Tarea actualizada:", updated)

    # Filtrar completadas
    print("Filtrar completadas:", tm.filter_by_status(Status.COMPLETADA))

    # Listar todas después de eliminar
    print("Tareas:", tm.get_tasks())

    

