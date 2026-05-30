from sqlalchemy.orm import Session
from pydantic import EmailStr
from models.models import User
from schemas.user import UserRegister
from enums import RoleEnum

class Repository:
    def __init__(self, db: Session):
        self.db = db

    def get_email(self, email: EmailStr):
        return self.db.query(User).filter(User.email == email).first()

    def register_user(self, user_register: UserRegister):
        new_user = User(full_name=user_register.full_name,
                        email=user_register.email,
                        birth_date=user_register.birth_date,
                        password=user_register.password,
                        role=RoleEnum.GUEST
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def get_user_by_id(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        return user