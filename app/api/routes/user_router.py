from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserRegister
from service.service import Service
from repository.repository import Repository

from api.deps import get_db

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.post("/register")
async def register_user(user_register: UserRegister, db: Session = Depends(get_db)):
    repo =  Repository(db)
    service = Service(repo)
    return service.register_user(user_register)