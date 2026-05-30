from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserRegister, UserResponse
from service.service import Service
from repository.repository import Repository
from models.models import User

from api.deps import get_db

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.post("/register")
async def register_user(user_register: UserRegister, db: Session = Depends(get_db)):
    repo =  Repository(db)
    service = Service(repo)
    return service.register_user(user_register)

@user_router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, current_user: User, db: Session = Depends(get_db)):
    repo = Repository(db)
    service = Service(repo)
    return service.get_user(user_id, current_user)