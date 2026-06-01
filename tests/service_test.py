import pytest
from service.service import Service
from schemas.user import UserRegister
from datetime import date
from fastapi import HTTPException
from models.models import User
from enums import RoleEnum


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
    
    def get_user_by_id(self, user_id: int):
        for user in self.users:
            if user["id"] == user_id:
                return user
        return None
    
def make_user_register(email="test@test.com"):
    return UserRegister(
        full_name="Test User",
        email=email,
        birth_date=date(2000, 1, 1),
        password="123456"
    )

def make_fake_user(role):
    user = User()
    user.role = role
    return user

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

def test_get_user_by_id_acess_denied():
    repo = FakeRepository()
    service = Service(repo)
    current_user = make_fake_user(RoleEnum.GUEST)
    
    with pytest.raises(HTTPException) as exc:
        service.get_user_by_id(1, current_user)
    assert exc.value.status_code == 403

def test_get_user_not_found():
    repo = FakeRepository()
    service = Service(repo)
    current_user = make_fake_user(RoleEnum.ADMIN)

    with pytest.raises(HTTPException) as exc:
        service.get_user_by_id(1, current_user)
    assert exc.value.status_code == 404

def test_get_user_success():
    repo = FakeRepository()
    service = Service(repo)
    service.register_user(make_user_register())
    current_user = make_fake_user(RoleEnum.ADMIN)

    result = service.get_user_by_id(1, current_user)
    assert result["email"] == "test@test.com"