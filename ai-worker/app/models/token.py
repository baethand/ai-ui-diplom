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