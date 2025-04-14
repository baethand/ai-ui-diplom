from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    disabled:bool
    created_at: datetime
    last_login: datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str]

class TokenData(BaseModel):
    username: Optional[str] = None