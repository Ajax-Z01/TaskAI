import os
import shutil
import uuid
import logging
import magic
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import Task, Comment, Attachment, User
from schemas import TaskCreate, TaskResponse, TaskUpdate, CommentCreate, CommentResponse, AttachmentResponse, UserCreate, UserResponse
from ai import recommend_tasks
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

logger = logging.getLogger("taskai")
logging.basicConfig(level=logging.INFO)

# ==========================
# ✅ USERS ENDPOINTS
# ==========================
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

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

    user = db.query(User).filter(User.id == comment.author_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_comment = Comment(
        task_id=task_id,
        content=comment.content,
        author_id=comment.author_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return CommentResponse(
        id=new_comment.id,
        task_id=new_comment.task_id,
        author=UserResponse.from_orm(user),
        content=new_comment.content,
        created_at=new_comment.created_at
    )

@app.get("/tasks/{task_id}/comments/", response_model=list[CommentResponse])
def get_comments(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    comments = db.query(Comment).filter(Comment.task_id == task_id).all()
    return comments

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

    file_extension = os.path.splitext(file.filename)[1].lower()
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".docx", ".xlsx", ".zip", ".txt", ".csv"}

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file_extension}' is not allowed."
        )

    MAX_FILE_SIZE_MB = 5
    MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds the limit of {MAX_FILE_SIZE_MB} MB."
        )

    mime = magic.from_buffer(file.file.read(2048), mime=True)
    file.file.seek(0)

    ALLOWED_MIME_TYPES = {
        "image/jpeg",
        "image/png",
        "image/gif",
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/zip",
        "text/plain",
        "text/csv",
        "application/vnd.ms-excel"
    }

    if mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"MIME type '{mime}' is not allowed."
        )

    unique_filename = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}{file_extension}"
    file_location = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_attachment = Attachment(
        task_id=task_id,
        original_name=file.filename,
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

    return db.query(Attachment).filter(
        Attachment.task_id == task_id,
        Attachment.is_deleted == False
    ).all()

@app.delete("/attachments/{attachment_id}")
def delete_attachment(attachment_id: int, db: Session = Depends(get_db)):
    attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    task = db.query(Task).filter(Task.id == attachment.task_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=400, detail="Cannot delete attachment from a deleted or missing task")

    upload_dir_abs = os.path.abspath(UPLOAD_DIR)
    file_path_abs = os.path.abspath(attachment.file_url)

    if not file_path_abs.startswith(upload_dir_abs):
        raise HTTPException(status_code=400, detail="Invalid file path")

    try:
        if os.path.exists(file_path_abs):
            os.remove(file_path_abs)
            logger.info(f"Attachment file deleted: {file_path_abs}")
        else:
            logger.warning(f"File not found: {file_path_abs}")
    except Exception as e:
        logger.error(f"Failed to delete file: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting file: {e}")

    attachment.is_deleted = True
    db.commit()

    return {"message": "Attachment soft-deleted successfully"}

@app.get("/tasks/{task_id}/attachments/all/", response_model=list[AttachmentResponse])
def get_all_attachments(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return db.query(Attachment).filter(Attachment.task_id == task_id).all()

@app.get("/uploads/{filename}")
def get_uploaded_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)