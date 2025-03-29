from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    priority: int
    status: str
    progress: int

class TaskUpdate(BaseModel):
    title: str
    description: str
    priority: int
    status: str
    progress: int

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    status: str
    progress: int
    created_at: datetime
    updated_at: datetime
