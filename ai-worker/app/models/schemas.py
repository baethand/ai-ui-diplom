from pydantic import BaseModel

class ImageGenerationRequest(BaseModel):
    prompt: str
    output_path: str = "generated_image.png"
    model_path: str = "./models"
    num_inference_steps: int = 50
    guidance_scale: float = 12.0
    height: int = 512
    width: int = 512
    device: str = "auto"