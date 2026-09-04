from pydantic import BaseModel
from datetime import datetime


class ColumnCreate(BaseModel):
    title: str
    order_position: int | None = None


class ColumnUpdate(BaseModel):
    title: str | None = None
    order_position: int | None = None


class ColumnResponse(BaseModel):
    id: str
    title: str
    board_id: str
    order_position: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
