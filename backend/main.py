from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import Task
from schemas import TaskCreate, TaskResponse, TaskUpdate
from ai import recommend_tasks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Retrieve all tasks that have not been deleted
@app.get("/tasks/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.is_deleted == False).all()

# ✅ Retrieve a single task by ID
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# ✅ Add a new task
@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(title=task.title, description=task.description, priority=task.priority)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# ✅ Update a task by ID
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task data
    task.title = task_update.title
    task.description = task_update.description
    task.priority = task_update.priority

    db.commit()
    db.refresh(task)
    return task

# ✅ Soft delete a task (not removed from the database)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.is_deleted = True
    db.commit()
    return {"message": "Task deleted successfully"}

# ✅ Get recommended tasks (ignoring deleted tasks)
@app.get("/tasks/recommendations/", response_model=list[TaskResponse])
def get_recommendations(db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.is_deleted == False).all()
    return recommend_tasks(tasks)
