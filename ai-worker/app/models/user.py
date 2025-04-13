from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    hashed_password: str
    disabled: bool = False
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str]

class TokenData(BaseModel):
    username: Optional[str] = None