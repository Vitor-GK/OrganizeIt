from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date

class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    birth_date: date
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr