from typing import Optional
from pydantic import BaseModel, EmailStr

# Модели данных
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: EmailStr 

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None