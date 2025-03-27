from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    priority: int

class TaskUpdate(BaseModel):
    title: str
    description: str
    priority: int

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
