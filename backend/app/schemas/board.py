from pydantic import BaseModel
from datetime import datetime


class BoardCreate(BaseModel):
    title: str
    description: str | None = None


class BoardUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class BoardResponse(BaseModel):
    id: str
    title: str
    description: str | None
    owner_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BoardListResponse(BaseModel):
    boards: list[BoardResponse]
    total: int
