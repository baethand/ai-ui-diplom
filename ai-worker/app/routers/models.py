from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse  # Добавьте этот импорт
from pydantic import BaseModel, conint, confloat
from typing import Optional
import logging
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/v1", tags=["models"])

AVAILABLE_MODELS = [
    "stabilityai/stable-diffusion-2-1"
]

@router.get("/models")
async def create_image():
    """
    Возвращает список доступных моделей для генерации изображений
    
    Пример ответа:
    {
        "models": [
            "stabilityai/stable-diffusion-2-1",
            "stabilityai/stable-diffusion-xl-base-1.0",
            ...
        ]
    }
    """
    return JSONResponse({
        "models": AVAILABLE_MODELS
    })
