from fastapi import APIRouter, Depends, HTTPException
import torch
from app.services.image_service import generate_image
from app.dependencies import get_current_user
from app.models.schemas import ImageGenerationRequest

router = APIRouter(prefix="/api/v1", tags=["image_generation"])

@router.post("/generate-image")
async def create_image(
    request: ImageGenerationRequest,
    user: str = Depends(get_current_user)
):
    try:
        device = request.device
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
        # output_path = generate_image(
        #     prompt=request.prompt,
        #     output_path=request.output_path,
        #     model_path=request.model_path,
        #     num_inference_steps=request.num_inference_steps,
        #     guidance_scale=request.guidance_scale,
        #     height=request.height,
        #     width=request.width,
        #     device=device
        # )
        
        return {
            "status": "success",
            "image_path": output_path
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {str(e)}"
        )