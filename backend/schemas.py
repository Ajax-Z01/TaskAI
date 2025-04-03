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
    
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    task_id: int
    content: str

class CommentResponse(BaseModel):
    id: int
    task_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class AttachmentCreate(BaseModel):
    task_id: int
    file_name: str
    file_url: str

class AttachmentResponse(BaseModel):
    id: int
    task_id: int
    file_name: str
    file_url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True