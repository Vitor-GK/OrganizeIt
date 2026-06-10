from sqlalchemy.orm import Session
from pydantic import EmailStr
from models.models import User, Task, TaskAssigment
from schemas.user import UserRegister
from enums import RoleEnum, TaskEnum
from schemas.user import UserUpdate
from schemas.task import TaskCreater, TaskUpdate

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
        user  = self,self.get_user_by_id(user_id)
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
        task = self.db.query(Task).filter(Task.id == task_id).first()
        return task
    
    def get_assigned_tasks(self, user_id: int):
        tasks = self.db.query(Task).join(TaskAssigment, TaskAssigment.task_id == Task.id).filter(TaskAssigment.user_id == user_id).all()

        return tasks
    
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