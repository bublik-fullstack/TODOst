from pydantic import BaseModel
from datetime import datetime
from app.models.task import PriorityEnum


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    column_id: str
    priority: PriorityEnum = PriorityEnum.medium
    deadline: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: PriorityEnum | None = None
    deadline: datetime | None = None


class TaskMove(BaseModel):
    column_id: str
    order_position: int


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str | None
    column_id: str
    order_position: int
    priority: PriorityEnum
    deadline: datetime | None
    author_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
