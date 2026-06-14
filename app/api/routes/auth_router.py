from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from service.service import Service
from repository.repository import Repository
from schemas.auth import LoginRequest
from api.deps import get_db, get_current_user, oauth2_scheme
from models.models import User
from fastapi.security import OAuth2PasswordBearer

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login")
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    repo =  Repository(db)
    service = Service(repo)
    return service.login(login_request)

@auth_router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo =  Repository(db)
    service = Service(repo)
    return service.logout(current_user, token)
    

    