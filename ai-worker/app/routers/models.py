from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.config import ALLOWED_MODELS

router = APIRouter(prefix="/api/v1", tags=["models"])

@router.get("/models")
async def create_image():
    return JSONResponse({
        "models": list(ALLOWED_MODELS)
    })
