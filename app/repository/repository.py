from sqlalchemy.orm import Session
from pydantic import EmailStr
from models.models import User, Task, TaskAssigment
from schemas.user import UserRegister
from enums import RoleEnum, TaskEnum
from schemas.user import UserUpdate
from schemas.task import TaskCreater, TaskUpdate
from sqlalchemy import func


class Repository:
    def __init__(self, db: Session):
        self.db = db

    def get_email(self, email: EmailStr):
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

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
        user  = self.db.query(User).filter(User.id  == user_id).first()

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
    
    def delete_user(self, user_id: int):
        user  = self.get_user_by_id(user_id)
        if not user:
            return None
        user.is_active = 0

        self.db.commit()
        self.db.refresh(user)
        return user
    
    def create_task(self, task_creater: TaskCreater, user_id: int):
        new_task = Task(name=task_creater.name, description=task_creater.description, status=TaskEnum.PENDING, priority=task_creater.priority, due_date=task_creater.due_date, creator_id=user_id)
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)

        return new_task

    def get_task_by_id(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def get_assigned_tasks(self, user_id: int):
        return self.db.query(Task).join(TaskAssigment, TaskAssigment.task_id == Task.id).filter(TaskAssigment.user_id == user_id).all()
    
    def update_task(self, task_id: int, task_update: TaskUpdate):
        task = self.get_task_by_id(task_id)

        if task_update.name != None:
            task.name = task_update.name
        if task_update.description != None:
            task.description = task_update.description
        if task_update.status != None:
            task.status = task_update.status

        self.db.commit()
        self.db.refresh(task)
        return task
    
    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)

        self.db.delete(task)
        self.db.commit()
        return task
    
    def get_tasks_by_status(self):
        results = self.db.query(Task.status, func.count(Task.id))\
            .group_by(Task.status)\
            .all()
        return {status.value: count for status, count in results}

    def get_tasks_by_user(self, user_id: int | None = None):
        query = self.db.query(User.id, User.full_name, func.count(Task.id).label("total_tasks"))\
            .join(Task, Task.creator_id == User.id)\
            .group_by(User.id, User.full_name)
        
        if user_id:
            query = query.filter(User.id == user_id)
        
        results = query.all()
        return [{"user_id": user_id, "full_name": full_name, "total_tasks": total} for user_id, full_name, total in results]
    
    def logout(self, user_id: int, token: str):
        user = self.get_user_by_id(user_id)
        user.banned_token = token
        self.db.commit()
        self.db.refresh(user)
        return {"message": "Logged out successfully"}

    def assign_task(self, task_id: int, user_id: int):
        assignment = TaskAssigment(task_id=task_id, user_id=user_id)
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment
    
    def get_assigned_users(self, task_id: int):
        return self.db.query(User)\
            .join(TaskAssigment, TaskAssigment.user_id == User.id)\
            .filter(TaskAssigment.task_id == task_id)\
            .all()