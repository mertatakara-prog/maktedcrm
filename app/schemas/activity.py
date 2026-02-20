from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ActivityCreate(BaseModel):
    customer_id: int
    user_id: int
    activity_type: str
    notes: str | None = None


class ActivityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    user_id: int
    activity_type: str
    notes: str | None
    created_at: datetime
