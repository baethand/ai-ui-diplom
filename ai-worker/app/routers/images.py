from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
import torch
from app.services.ImageGenerationService import image_generator
from app.dependencies import get_current_user
from app.models.schemas import ImageGenerationRequest

router = APIRouter(prefix="/api/v1", tags=["image_generation"])

@router.post("/generate-image")
async def create_image(
    request: ImageGenerationRequest,
    # background_tasks: BackgroundTasks,
    user: str = Depends(get_current_user)
):
    try:
        device = request.device
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
            


        result = image_generator._generate_single(
            prompt=request.prompt,
            output_path=request.output_path,
            num_steps=request.num_inference_steps,
            guidance=request.guidance_scale,
            height=request.height,
            width=request.width
        )
        
        return {"status": "success", "result": result}

        # if request.background:
        #     background_tasks.add_task(
        #         image_generator.generate,
        #         request.prompts,
        #         request.num_steps,
        #         request.guidance,
        #         request.height,
        #         request.width
        #     )
        #     return {"message": "Generation started in background"}
    
        # results = await image_generator.generate(
        #     request.prompts,
        #     request.num_steps,
        #     request.guidance,
        #     request.height,
        #     request.width
        # )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {str(e)}"
        )