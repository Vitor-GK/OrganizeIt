from pydantic import BaseModel, EmailStr
from datetime import date

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    birth_date: date
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True