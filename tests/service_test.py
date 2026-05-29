import pytest
from service.service import Service
from schemas.user import UserRegister
from datetime import date
from fastapi import HTTPException


class FakeRepository:
    def __init__(self):
        self.users = []

    def get_email(self, email):
        for user in self.users:
            if user["email"] == email:
                return user
        return None
    
    def register_user(self, user_register: UserRegister):
        user = {"id": 1, "full_name": user_register.full_name, "email": user_register.email}
        self.users.append(user)
        return user
    
def make_user_register(email="test@test.com"):
    return UserRegister(
        full_name="Test User",
        email=email,
        birth_date=date(2000, 1, 1),
        password="123456"
    )

def test_register_user_sucess():
    repo = FakeRepository()
    service = Service(repo)
    result = service.register_user(make_user_register())
    assert result["email"] == "test@test.com"

def test_register_user_email_already_exist():
    repo = FakeRepository()
    service = Service(repo)
    service.register_user(make_user_register())


    with pytest.raises(HTTPException) as exc:
        service.register_user(make_user_register())
    assert exc.value.status_code == 409