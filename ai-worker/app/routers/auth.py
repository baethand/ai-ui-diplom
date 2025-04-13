from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime
from app.services.AuthService import auth_service
from app.services.DBService import db_service
from app.models.user import UserCreate, Token, UserInDB
from app.models.base import User

router = APIRouter(prefix="/api/v1", tags=["auth"])

@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    with db_service.get_session() as session:
        # Проверка существующего пользователя
        if session.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Создание нового пользователя
        hashed_password = auth_service.get_password_hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            created_at=datetime.utcnow()
        )
        
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        # Генерация токенов
        user_dict = UserInDB.from_orm(new_user).dict()
        access_token = await auth_service.create_access_token(user_dict)
        refresh_token = await auth_service.create_refresh_token(user_dict)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Обновляем время последнего входа
    with db_service.get_session() as session:
        db_user = session.query(User).filter(User.username == user.username).first()
        db_user.last_login = datetime.utcnow()
        session.commit()

    # Генерация токенов
    user_dict = user.dict()
    access_token = await auth_service.create_access_token(user_dict)
    refresh_token = await auth_service.create_refresh_token(user_dict)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.get("/users/me", response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(auth_service.get_current_active_user)):
    return current_user