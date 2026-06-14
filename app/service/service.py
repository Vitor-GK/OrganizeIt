from repository.repository import Repository
from schemas.user import UserRegister, UserUpdate
from schemas.task import TaskCreater, TaskUpdate
from fastapi import HTTPException
from models.models import User
from enums import RoleEnum
from core.security import verify_password, create_access_token
from schemas.auth import LoginRequest


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
            raise HTTPException(status_code=403, detail="Access denied, you do not have authorization to acess this function")
        
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    
    def update_user(self, user_id: int, user_update: UserUpdate, current_user: User):
        user = self.repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User id not found")
        
        if current_user.id != user_id and current_user.role != RoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Access denied, you do not have authorization to acess this function")
        
        if user_update.email:
            email = self.repo.get_email(user_update.email)
            if email:
                raise HTTPException(status_code=409, detail="This email is already registered")
            
        return self.repo.update_user(user_id, user_update)
    
    def delete_user(self, user_id: int, current_user: User):
        user = self.repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User id not found")
        
        if current_user.id != user_id and current_user.role != RoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Access denied, you do not have authorization to acess this function")
        
        if user.is_active == 0:
            raise HTTPException(status_code=400, detail="This user is already inactive")
        
        return self.repo.delete_user(user_id)
    
    def create_task(self, task_creater: TaskCreater, current_user: User):
        if current_user.role != RoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Access denied, you do not have authorization to acess this function")
        
        return self.repo.create_task(task_creater, current_user.id)
    
    def get_task_by_id(self, task_id: int):
        task = self.repo.get_task_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return task
    
    def get_assigned_tasks(self, user_id: int):
        user = self.repo.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return self.repo.get_assigned_tasks(user_id)
    
    def update_task(self, task_id: int, task_update: TaskUpdate, current_user: User):
        task = self.get_task_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if current_user.role != RoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Access denied, you do not have authorization to acess this function")
        
        return self.repo.update_task(task_id, task_update)
    
    def delete_task(self, task_id: int, current_user: User):
        task = self.get_task_by_id(task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if current_user.role != RoleEnum.ADMIN:
            raise HTTPException(status_code=403, detail="Access denied, you do not have authorization to acess this function")
        
        return self.repo.delete_task(task_id)
    
    def login(self, login_request: LoginRequest):
        user = self.repo.get_email(login_request.email)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not verify_password(login_request.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}

    def get_tasks_by_status(self):
        return self.repo.get_tasks_by_status()

    def get_tasks_by_user(self, user_id: int | None = None):
        return self.repo.get_tasks_by_user(user_id)