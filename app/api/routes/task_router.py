from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.task import TaskCreater, TaskResponse, TaskUpdate
from service.service import Service
from repository.repository import Repository
from models.models import User
from typing import List

from api.deps import get_db

task_router = APIRouter(prefix="/task", tags=["task"])

@task_router.post("/")
async def create_task(task_creater: TaskCreater, current_user: User, db: Session = Depends(get_db)):
    repo =  Repository(db)
    service = Service(repo)
    return service.create_task(task_creater, current_user)

@task_router.get("/{id}", response_model=TaskResponse)
async def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    repo =  Repository(db)
    service = Service(repo)
    return service.get_task_by_id(task_id)
 
@task_router.get("/assigned/To{id}", response_model=List[TaskResponse])
async def get_assigned_tasks(user_id: int, db: Session = Depends(get_db)):
    repo =  Repository(db)
    service = Service(repo)
    return service.get_assigned_tasks(user_id)

@task_router.put("/{id}")
async def update_task(task_id: int, task_update: TaskUpdate, current_user: User, db: Session = Depends(get_db)):
    repo =  Repository(db)
    service = Service(repo)
    return service.update_task(task_id, task_update, current_user)

@task_router.delete("/{id}")
async def delete_task(task_id: int, current_user: User, db: Session = Depends(get_db)):
    repo =  Repository(db)
    service = Service(repo)
    return service.delete_task(task_id, current_user)