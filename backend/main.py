import os
import shutil
import uuid
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import Task, Comment, Attachment
from schemas import TaskCreate, TaskResponse, TaskUpdate, CommentCreate, CommentResponse, AttachmentResponse
from ai import recommend_tasks
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# ✅ TASKS ENDPOINTS
# ==========================

@app.get("/tasks/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.is_deleted == False).all()

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        progress=task.progress
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_update.title
    task.description = task_update.description
    task.priority = task_update.priority
    task.status = task_update.status
    task.progress = task_update.progress

    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.is_deleted = True
    db.commit()
    return {"message": "Task deleted successfully"}

@app.get("/tasks/recommendations/", response_model=list[TaskResponse])
def get_recommendations(mode: str = "urgent", db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.is_deleted == False).all()
    recommended_tasks = recommend_tasks(tasks, mode=mode)

    return [TaskResponse.from_orm(task) for task in recommended_tasks]

# ==========================
# ✅ COMMENTS ENDPOINTS
# ==========================

@app.post("/tasks/{task_id}/comments/", response_model=CommentResponse)
def add_comment(task_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    new_comment = Comment(task_id=task_id, content=comment.content)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@app.get("/tasks/{task_id}/comments/", response_model=list[CommentResponse])
def get_comments(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return db.query(Comment).filter(Comment.task_id == task_id).all()

# ==========================
# ✅ ATTACHMENTS ENDPOINTS
# ==========================

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/tasks/{task_id}/attachments/", response_model=AttachmentResponse)
def upload_attachment(task_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}{file_extension}"

    file_location = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_attachment = Attachment(
        task_id=task_id,
        file_name=unique_filename,
        file_url=file_location
    )
    db.add(new_attachment)
    db.commit()
    db.refresh(new_attachment)
    return new_attachment

@app.get("/tasks/{task_id}/attachments/", response_model=list[AttachmentResponse])
def get_attachments(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return db.query(Attachment).filter(Attachment.task_id == task_id).all()
