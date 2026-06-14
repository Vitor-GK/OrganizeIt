import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User
from repository.repository import Repository
from schemas.user import UserRegister, UserUpdate
from schemas.task import TaskCreater, TaskUpdate
from datetime import date

engine = create_engine("sqlite:///:memory:")
TestingSession = sessionmaker(bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(engine)
    session = TestingSession()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def make_user_register(email="test@test.com"):
    return UserRegister(
        full_name="Test User",
        email=email,
        birth_date=date(2000, 1, 1),
        password="123456"
    )

def make_task_creater():
    return TaskCreater(
        name="Test Task",
        description="Test Description"
    )

def test_register_user(db):
    repo = Repository(db)
    result = repo.register_user(make_user_register())
    assert result.email == "test@test.com"

def test_get_email_exists(db):
    repo = Repository(db)
    repo.register_user(make_user_register())
    result = repo.get_email("test@test.com")
    assert result is not None

def test_get_email_not_exists(db):
    repo = Repository(db)
    result = repo.get_email("naoexiste@test.com")
    assert result is None

def test_get_user_by_id_sucess(db):
    repo = Repository(db)
    repo.register_user(make_user_register())
    result = repo.get_user_by_id(1)
    assert result is not None

def test_get_user_by_id_not_exist(db):
    repo = Repository(db)
    result = repo.get_user_by_id(999)
    assert result is None

def test_update_user(db):
    repo = Repository(db)
    repo.register_user(make_user_register())
    user_update = UserUpdate(full_name="New Name")
    result = repo.update_user(1, user_update)
    assert result.full_name == "New Name"

def test_update_user_email(db):
    repo = Repository(db)
    repo.register_user(make_user_register())
    user_update = UserUpdate(email="new@test.com")
    result = repo.update_user(1, user_update)
    assert result.email == "new@test.com"

def test_update_user_partial(db):
    repo = Repository(db)
    repo.register_user(make_user_register())
    user_update = UserUpdate(full_name="New Name")
    result = repo.update_user(1, user_update)
    assert result.email == "test@test.com"

def test_delete_user(db):
    repo = Repository(db)
    repo.register_user(make_user_register())
    result = repo.delete_user(1)
    assert result.is_active == False

def test_delete_user_not_found(db):
    repo = Repository(db)
    result = repo.delete_user(999)
    assert result is None

def test_create_task(db):
    repo = Repository(db)
    repo.register_user(make_user_register())
    result = repo.create_task(make_task_creater(), 1)
    assert result.name == "Test Task"

def test_get_task_by_id(db):
    repo = Repository(db)
    repo.register_user(make_user_register())
    repo.create_task(make_task_creater(), 1)
    result = repo.get_task_by_id(1)
    assert result is not None

def test_get_task_by_id_not_found(db):
    repo = Repository(db)
    result = repo.get_task_by_id(999)
    assert result is None

def test_update_task(db):
    repo = Repository(db)
    repo.register_user(make_user_register())
    repo.create_task(make_task_creater(), 1)
    task_update = TaskUpdate(name="Updated Task")
    result = repo.update_task(1, task_update)
    assert result.name == "Updated Task"

def test_delete_task(db):
    repo = Repository(db)
    repo.register_user(make_user_register())
    repo.create_task(make_task_creater(), 1)
    result = repo.delete_task(1)
    assert result is not None

def test_get_tasks_by_status(db):
    repo = Repository(db)
    repo.register_user(make_user_register())
    repo.create_task(make_task_creater(), 1)
    result = repo.get_tasks_by_status()
    assert isinstance(result, dict)

def test_get_tasks_by_user(db):
    repo = Repository(db)
    repo.register_user(make_user_register())
    repo.create_task(make_task_creater(), 1)
    result = repo.get_tasks_by_user()
    assert isinstance(result, list)

def test_get_tasks_by_user_with_id(db):
    repo = Repository(db)
    repo.register_user(make_user_register())
    repo.create_task(make_task_creater(), 1)
    result = repo.get_tasks_by_user(1)
    assert isinstance(result, list)