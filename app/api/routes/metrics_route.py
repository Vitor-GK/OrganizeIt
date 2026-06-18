from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from service.service import Service
from repository.repository import Repository
from api.deps import get_db, get_current_user
from models.models import User
from schemas.task import TasksByUserResponse
from typing import List

metrics_router = APIRouter(prefix="/metrics", tags=["metrics"])

@metrics_router.get("/tasks-by-status")
async def get_tasks_by_status(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = Repository(db)
    service = Service(repo)
    return service.get_tasks_by_status()

@metrics_router.get("/tasks-by-user/{user_id}", response_model=List[TasksByUserResponse])
async def get_tasks_by_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = Repository(db)
    service = Service(repo)
    return service.get_tasks_by_user(user_id)