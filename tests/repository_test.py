import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User
from repository.repository import Repository
from schemas.user import UserRegister
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