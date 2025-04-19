from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
import torch
from app.models.schemas import ImageGenerationRequest
from diffusers import StableDiffusionPipeline
from fastapi import APIRouter
from datetime import datetime
from io import BytesIO
from PIL import Image
from app.services.MinioService import MinioService
from app.services.DBService import db_service
from app.services.AuthService import auth_service
from app.models.base import User, Image
from app.dependencies import get_current_user

import logging

router = APIRouter(prefix="/api/v1", tags=["image_generation"])
minio = MinioService()
log = logging.getLogger(__name__)

pipe = StableDiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-2-1",
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
pipe = pipe.to("cuda")

@router.post("/generate-image")
async def create_image( user: Annotated[str, Depends(auth_service.get_current_user)],
    request: ImageGenerationRequest
):
    try:
        generated_image = pipe(
            request.prompt,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
            height=request.height,
            width=request.width
        ).images[0]
        
        # 2. Конвертация в BytesIO (файлоподобный объект)
        img_byte_arr = BytesIO()
        generated_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)  # Важно: перемотка в начало!
        
        # 3. Сохранение в MinIO
        filename = f"generated_{datetime.now().timestamp()}.png"
        minio.client.put_object(
            bucket_name=minio.bucket,
            object_name=filename,
            data=img_byte_arr,  # Передаем BytesIO напрямую
            length=img_byte_arr.getbuffer().nbytes,
            content_type="image/png"
        )

        image_url = minio.get_image_url(filename)

        # 4. Запись в БД через контекстный менеджер
        with db_service.get_session() as session:
            db_image = Image(
                user_id=user.user_id,
                name=filename,
                width=request.width,
                height=request.height,
                model="stable-diffusion-2.1",
                prompt=request.prompt,
                status="completed",
                generated_at=datetime.utcnow(),
            )
            session.add(db_image)
            session.commit()

            # Получаем URL только после коммита (если нужен ID)
            image_url = minio.get_image_url(filename)
        
            return {
                "status": "success",
                "image_url": image_url,
                "image_id": db_image.id,
            }
        
    except Exception as e:
        if 'session' in locals():
            session.rollback()
        raise HTTPException(500, f"Error: {e}")