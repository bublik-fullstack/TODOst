from pydantic import BaseModel
from datetime import datetime


class CommentCreate(BaseModel):
    content: str


class CommentUpdate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: str
    content: str
    task_id: str
    author_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
