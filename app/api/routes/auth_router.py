from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from service.service import Service
from repository.repository import Repository
from app.api.deps import get_db
from app.schemas.auth import LoginRequest

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login")
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    repo =  Repository(db)
    service = Service(repo)
    return service.login(login_request)

@auth_router.post("/logout")
async def logout(db: Session = Depends(get_db)):
    repo =  Repository(db)
    service = Service(repo)
    return service.logout()
    

    