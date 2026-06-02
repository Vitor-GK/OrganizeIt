import pytest
from service.service import Service
from schemas.user import UserRegister, UserUpdate
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
    
    def update_user(self, user_id: int, user_update: UserUpdate):
        for user in self.users:
            if user["id"] == user_id:
                if user_update.full_name:
                    user["full_name"] = user_update.full_name
                if user_update.email:
                    user["email"] = user_update.email
        return user
        
    
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

def test_update_user_not_found():
    repo = FakeRepository()
    service = Service(repo)
    current_user = make_fake_user(RoleEnum.ADMIN)
    user_update = UserUpdate(full_name="New Name")

    with pytest.raises(HTTPException) as exc:
        service.user_update(999, user_update, current_user)
    assert exc.value.status_code == 404

def test_update_user_access_denied():
    repo = FakeRepository()
    service = Service(repo)
    service.register_user(make_user_register())
    current_user = make_fake_user(RoleEnum.GUEST)
    current_user.id = 99
    user_update = UserUpdate(full_name="New Name")

    with pytest.raises(HTTPException) as exc:
        service.user_update(1, user_update, current_user)
    assert exc.value.status_code == 403

def test_update_user_email_already_registered():
    repo = FakeRepository()
    service = Service(repo)
    service.register_user(make_user_register())
    service.register_user(make_user_register(email="other@test.com"))
    current_user = make_fake_user(RoleEnum.ADMIN)
    user_update = UserUpdate(email="other@test.com")

    with pytest.raises(HTTPException) as exc:
        service.user_update(1, user_update, current_user)
    assert exc.value.status_code == 409

def test_update_user_success():
    repo = FakeRepository()
    service = Service(repo)
    service.register_user(make_user_register())
    current_user = make_fake_user(RoleEnum.ADMIN)
    user_update = UserUpdate(full_name="New Name")

    result = service.user_update(1, user_update, current_user)
    assert result["full_name"] == "New Name"