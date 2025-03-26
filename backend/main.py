from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import Task
from schemas import TaskCreate, TaskResponse
from ai import recommend_tasks

app = FastAPI()
init_db()

@app.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(title=task.title, description=task.description, priority=task.priority)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get("/tasks/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@app.get("/tasks/recommendations/", response_model=list[TaskResponse])
def get_recommendations(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return recommend_tasks(tasks)
