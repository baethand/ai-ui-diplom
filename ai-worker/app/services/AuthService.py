from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from app.config import settings
from app.models.base import User
from app.models.token import TokenData
import logging

logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=[settings.PWD_SCHEMES],
            deprecated=settings.PWD_DEPRECATED
        )
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        self.refresh_token_expire = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    # Подтверждение пароля (Пароль == Хэшированный пароль (В БД))
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    # Хэширует пароль
    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or self.access_token_expire)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def create_access_token(self, user_data: User) -> str:
        return self.create_token(
            data={
                "sub": user_data.username,
                "user_id": user_data.id,
                "email": user_data.email,
                "is_active": user_data.is_active,
                "is_superuser": user_data.is_superuser
            },
            expires_delta=self.access_token_expire
        )

    async def create_refresh_token(self, user_data: dict) -> str:
        return self.create_token(
            data={"sub": user_data.username, "refresh": True},
            expires_delta=self.refresh_token_expire
        )

    async def decode_token(self, token: str) -> TokenData:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            return TokenData(username=username)
        except JWTError as e:
            logger.error(f"JWT Error: {e}")
            raise credentials_exception
    
    async def authenticate_user(self, token: str = Depends(oauth2_scheme)) -> str:
        token_data = await self.decode_token(token)
        if not token_data.username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data.username

auth_service = AuthService()