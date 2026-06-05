from pydantic import BaseModel, ConfigDict
from datetime import date
from enums import TaksEnum

class TaskCreater(BaseModel):
    name: str
    description: str
    priority: TaksEnum | None = None
    due_date: date | None = None

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    priority: TaksEnum | None = None
    due_date: date | None = None