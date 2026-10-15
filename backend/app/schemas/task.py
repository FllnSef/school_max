from datetime import datetime
from pydantic import BaseModel

# Базовые поля задачи
class TaskBase(BaseModel):
    title: str
    description: str | None = None
    subject: str
    deadline: datetime

# Схема для создания задачи (учитель передает эти данные)
class TaskCreate(TaskBase):
    creator_id: int  # ID учителя, создающего задачу

# Схема ответа (то, что бэкенд возвращает на фронтенд)
class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    is_completed: bool
    creator_id: int

    class Config:
        from_attributes = True
