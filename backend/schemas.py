from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
        
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
    content: str
    author_id: int

class CommentResponse(BaseModel):
    id: int
    task_id: int
    author: UserResponse
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class AttachmentCreate(BaseModel):
    file_name: str
    file_url: str

class AttachmentResponse(BaseModel):
    id: int
    task_id: int
    original_name: str
    file_name: str
    file_url: str
    uploaded_at: datetime

    class Config:
        from_attributes = True