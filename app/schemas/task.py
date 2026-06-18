from pydantic import BaseModel, ConfigDict
from datetime import date
from enums import TaskEnum, PriorityEnum

class TaskCreater(BaseModel):
    name: str
    description: str
    priority: PriorityEnum | None = None
    due_date: date | None = None

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    priority: PriorityEnum | None = None
    due_date: date | None = None

class TaskUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: TaskEnum | None = None

class TasksByUserResponse(BaseModel):
    user_id: int
    full_name: str
    total_tasks: int