from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel
from app.config import settings

security = HTTPBearer()

class TokenData(BaseModel):
    username: str | None = None
    user_id: str | None = None

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Декодируем и проверяем токен
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        isUser: bool = payload.get("isUser")
        if username is None or isUser is False:
            raise credentials_exception
        
        # Проверяем срок действия токена
        expire = payload.get("exp")
        if expire is None or datetime.utcnow() > datetime.fromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return TokenData(username=username, user_id=user_id)
        
    except JWTError:
        raise credentials_exception