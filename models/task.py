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
