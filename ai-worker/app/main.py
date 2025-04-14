from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import images
from app.routers import models
from app.routers import auth
import logging

# Настройка логирования перед созданием FastAPI app
logging.basicConfig(
    level=logging.DEBUG,  # или logging.DEBUG для более детальных логов
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="ai-worker generation image")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(images.router)
app.include_router(models.router)
app.include_router(auth.router)