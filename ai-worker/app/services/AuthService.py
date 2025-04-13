from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.models.user import UserInDB, TokenData
from app.services.DBService import db_service
from app.models.base import User
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=[settings.PWD_SCHEMES],
            deprecated=settings.PWD_DEPRECATED
        )
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        self.refresh_token_expire = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def get_user(self, username: str) -> Optional[UserInDB]:
        with db_service.get_session() as session:
            user = session.query(User).filter(User.username == username).first()
            return UserInDB.from_orm(user) if user else None

    async def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        user = await self.get_user(username)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    def create_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or self.access_token_expire)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def create_access_token(self, user_data: dict) -> str:
        return self.create_token(
            data={"sub": user_data.username, "isUser": True},
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

    async def get_current_user(self, token: str = Depends(lambda: self.oauth2_scheme)) -> UserInDB:
        token_data = await self.decode_token(token)
        user = await self.get_user(token_data.username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_current_active_user(self, current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

auth_service = AuthService()