import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
import torch
from app.models.schemas import ImageGenerationRequest
from fastapi import APIRouter
from datetime import datetime
from io import BytesIO
from PIL import Image
from app.services.MinioService import MinioService
from app.services.DBService import db_service
from app.services.AuthService import auth_service
from app.models.base import Image
from app.services.PipelineService import get_pipeline
from app.config import ALLOWED_MODELS, settings
from app.models.images import ImageResponse

import logging

executor = ThreadPoolExecutor(settings.MAX_WORKERS)

def generate_image_sync(request, user):
    if request.model_path not in ALLOWED_MODELS:
        raise HTTPException(status_code=400, detail=f"Модель '{request.model_path}' не поддерживается")

    pipe = get_pipeline(request.model_path)
    generator = torch.manual_seed(request.seed)

    generated_image = pipe(
        request.prompt,
        num_inference_steps=request.num_inference_steps,
        guidance_scale=request.guidance_scale,
        height=request.height,
        width=request.width,
        # generator=generator
    ).images[0]

    img_byte_arr = BytesIO()
    generated_image.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    filename = f"generated_{datetime.now().timestamp()}.png"
    minio.client.put_object(
        bucket_name=minio.bucket,
        object_name=filename,
        data=img_byte_arr,
        length=img_byte_arr.getbuffer().nbytes,
        content_type="image/png"
    )
    image_url = minio.get_image_url(filename)
    with db_service.get_session() as session:
        image = Image(
            user_id=user.user_id,
            name=filename,
            width=request.width,
            height=request.height,
            model="stable-diffusion-2.1",
            prompt=request.prompt,
            status="completed",
            generated_at=datetime.utcnow(),
            image_url=image_url
        )
        session.add(image)
        session.commit()
        
        return { "status": "success",
            "image": ImageResponse(
                        id=image.id,
                        image_url=image.image_url,
                        name=image.name,
                        width=image.width,
                        height=image.height,
                        model=image.model,
                        prompt=image.prompt,
                        created_at=image.created_at,
                        status=image.status
                    )
        }

router = APIRouter(prefix="/api/v1", tags=["image_generation"])
minio = MinioService()
log = logging.getLogger(__name__)

@router.post("/generate-image")
async def create_image(
    user: Annotated[str, Depends(auth_service.get_current_user)],
    request: ImageGenerationRequest
):
    try:
        # Выполняем sync-функцию в отдельном потоке
        result = await asyncio.get_event_loop().run_in_executor(
            executor, generate_image_sync, request, user
        )
        return result
    except Exception as e:
        raise HTTPException(500, f"Error: {e}")
    
@router.get("/images")
async def get_images_by_user(
    user: Annotated[str, Depends(auth_service.get_current_user)],
    limit: int = Query(20, description="Количество изображений", ge=1, le=100),
    offset: int = Query(0, description="Смещение", ge=0),
):
    with db_service.get_session() as session:
        

        # Получаем изображения из БД
        images = session.query(Image)\
            .filter(Image.user_id == user.user_id)\
            .offset(offset)\
            .limit(limit)\
            .all()
        
        # Преобразуем в response model
        return { "images": [
                    ImageResponse(
                        id=image.id,
                        image_url=image.image_url,
                        name=image.name,
                        width=image.width,
                        height=image.height,
                        model=image.model,
                        prompt=image.prompt,
                        created_at=image.created_at,
                        status=image.status
                    )
                    for image in images
                ]}
