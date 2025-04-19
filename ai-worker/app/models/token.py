from typing import Optional
from pydantic import BaseModel



class TokenRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str]

class TokenData(BaseModel):
    username: Optional[str] = None

class TokenPayload(BaseModel):
    username: str
    user_id: int
    email: str
    is_active: bool
    is_superuser: bool
