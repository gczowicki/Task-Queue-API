import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Task, TaskStatus
from app.schemas import TaskCreate, TaskResponse
from app.redis_client import push_task
from app.tasks.registry import TASK_REGISTRY


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    if task_data.task_type not in TASK_REGISTRY:
        raise HTTPException(
            status_code=400, 
            detail=f"Unknown task_type. Available: {list(TASK_REGISTRY.keys())}"
        )
            
    task = Task(
        task_type=task_data.task_type,
        input_data=json.dumps(task_data.input_data),
        priority=task_data.priority,
        status=TaskStatus.PENDING
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    push_task(task.id, task.priority)
    
    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task