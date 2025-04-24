from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from sqlalchemy import or_
from app.services.AuthService import auth_service
from app.services.DBService import db_service
from app.models.user import UserCreateRequest, UserLoginRequest
from app.models.base import User
from app.models.token import *

router = APIRouter(prefix="/api/v1", tags=["auth"])

@router.post("/register", response_model=Token)
async def register(
    # user_data: Annotated[UserCreateRequest, Depends()],
    user_data: UserCreateRequest,
):
    with db_service.get_session() as session:
        existing_user = session.query(User).filter(
            or_(
                User.username == user_data.username,
                User.email == user_data.email
            )
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )

        hashed_password = auth_service.get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_login=datetime.now()
        )
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        access_token = await auth_service.create_access_token(new_user)
        refresh_token = await auth_service.create_refresh_token(new_user)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

@router.post("/login", response_model=Token)
async def login(
    # user_data: Annotated[UserLoginRequest, Depends()],
    user_data: UserLoginRequest,
):
    with db_service.get_session() as session:
        user = session.query(User).filter(
            or_(
                User.username == user_data.usernameOrEmail,
                User.email == user_data.usernameOrEmail
            )
        ).first()

        if not user or not auth_service.verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username/email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )

        user.last_login = datetime.utcnow()
        session.commit()

        access_token = await auth_service.create_access_token(user)
        refresh_token = await auth_service.create_refresh_token(user)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
