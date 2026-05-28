from repository.repository import Repository
from schemas.user import UserRegister
from fastapi import HTTPException

class Service:
    def __init__(self, repo: Repository):
        self.repo = repo

    def register_user(self, user_register: UserRegister):
        user = self.repo.get_email(user_register.email)
        if user:
            raise HTTPException(status_code=409, detail="Email already registered")
        return self.repo.register_user(user_register)