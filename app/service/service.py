from repository.repository import Repository
from schemas.user import UserRegister, UserUpdate
from fastapi import HTTPException
from models.models import User
from enums import RoleEnum

class Service:
    def __init__(self, repo: Repository):
        self.repo = repo

    def register_user(self, user_register: UserRegister):
        user = self.repo.get_email(user_register.email)
        if user:
            raise HTTPException(status_code=409, detail="Email already registered")
        return self.repo.register_user(user_register)
    
    def get_user_by_id(self, user_id: int, current_user: User):
        if current_user.role !=  RoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Acess denied, you do not have authorization acesses this function")
        
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    
    def user_update(self, user_id: int, user_update: UserUpdate, current_user: User):
        user = self.repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User id not found")
        
        if current_user.id != user_id and current_user.role != RoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Acess denied, you do not have authorization acesses this function")
        
        if user_update.email:
            email = self.repo.get_email(user_update.email)
            if email:
                raise HTTPException(status_code=409, detail="This email is already registered")
            
        return self.repo.update_user(user_id, user_update)