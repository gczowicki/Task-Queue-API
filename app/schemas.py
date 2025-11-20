from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskCreate(BaseModel):
    task_type: str
    input_data: dict
    priority: int = Field(default=3, ge=1, le=5)


class TaskResponse(BaseModel):
    id: int
    task_type: str
    input_data: Optional[str]
    result: Optional[str]
    status: str
    priority: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
