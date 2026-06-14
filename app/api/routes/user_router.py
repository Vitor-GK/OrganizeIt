from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserRegister, UserResponse, UserUpdate
from service.service import Service
from repository.repository import Repository
from models.models import User

from api.deps import get_db, get_current_user

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/")
async def register_user(user_register: UserRegister, db: Session = Depends(get_db)):
    repo = Repository(db)
    service = Service(repo)
    return service.register_user(user_register)

@user_router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = Repository(db)
    service = Service(repo)
    return service.get_user_by_id(user_id, current_user)

@user_router.put("/{id}")
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = Repository(db)
    service = Service(repo)
    return service.update_user(user_id, user_update, current_user)

@user_router.delete("/{id}")
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = Repository(db)
    service = Service(repo)
    return service.delete_user(user_id, current_user)