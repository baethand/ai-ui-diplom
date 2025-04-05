from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import images
from app.routers import models
from app.routers import auth

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