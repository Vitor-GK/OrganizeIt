from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Enum, Numeric, Boolean, Text
from sqlalchemy.sql import func
from app.enums import TaksEnum, PriorityEnum, RoleEnum

from app.core.db import Base

class User(Base):
    __tablename__="user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    birth_date = Column(Date, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum(RoleEnum, name="role_enum"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
    verification_token = Column(String(100), nullable=True, unique=True)
    token_expires_at = Column(DateTime, nullable=True)
    verified = Column(Boolean, nullable=False, default=False)


class Task(Base):
    __tablename__="task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(TaksEnum, name="task_enum"), nullable=False)
    priority = Column(Enum(PriorityEnum, name="priority_enum"), nullable=True)
    due_date = Column(Date, nullable=True)
    creator_id = Column(Integer, ForeignKey("user.id"), index=True)

