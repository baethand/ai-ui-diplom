from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLoginRequest(BaseModel):
    usernameOrEmail: str
    password: str

class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]

    class Config:
        orm_mode = True
