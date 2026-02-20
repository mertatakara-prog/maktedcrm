from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskEventCreate(BaseModel):
    customer_id: int
    user_id: int
    title: str
    status: str = 'open'
    due_date: datetime | None = None


class TaskEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    user_id: int
    title: str
    status: str
    due_date: datetime | None
    created_at: datetime
