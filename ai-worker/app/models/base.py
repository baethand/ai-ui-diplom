from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.services.DBService import db_service

Base = db_service.Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    # Связь 1 ко многим (User → Images)
    images = relationship("Image", back_populates="user")

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Внешний ключ
    name = Column(String, index=True)
    width = Column(Integer, default=512)
    height = Column(Integer, default=512)
    model = Column(String, default="stable-diffusion-2.1")
    prompt = Column(String, nullable=True)
    negative_prompt = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    generated_at = Column(DateTime, nullable=True)
    status = Column(String, default="pending")  # pending, completed, failed

    # Связь многие к 1 (Image → User)
    user = relationship("User", back_populates="images")

    # Можно добавить методы для удобства
    def mark_as_completed(self):
        self.status = "completed"
        self.generated_at = datetime.utcnow()