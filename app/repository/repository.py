from sqlalchemy.orm import Session
from pydantic import EmailStr
from models.models import User
from schemas.user import UserRegister
from enums import RoleEnum
from schemas.user import UserUpdate

class Repository:
    def __init__(self, db: Session):
        self.db = db

    def get_email(self, email: EmailStr):
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        return user

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
    
    def update_user(self, user_id: int, user_update: UserUpdate):
        user  = self.db.query(User).filter(User.id  == user_id)

        if user_update.full_name:
            user.full_name = user_update.full_name
        if user_update.email:
            user.email = user_update.email
        if user_update.birth_date:
            user.birth_date = user_update.birth_date
        if user_update.password:
            user.password = user_update.password

        self.db.commit()
        self.db.refresh(user)
        return user