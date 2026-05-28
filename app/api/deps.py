from app.core.db import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.core.exceptions import ServiceError, InvalidCredentials, NotFound


from app.core.security import decode_access_token
from app.models.models import Member

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise ServiceError(detail="Error in the database service.")
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        member_id = int(payload.get("sub"))
    except JWTError:
        raise InvalidCredentials(detail="Invalid token.")
    
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise NotFound(detail="User was not found in database.")
    
    return member