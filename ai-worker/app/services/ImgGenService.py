import torch 
from diffusers import StableDiffusionPipeline
from PIL.Image import Image
from pydantic import BaseModel
from typing import Optional
import io

class ImageGenerationRequest(BaseModel):
    seed: Optional[int] = 42
    prompt: str
    output_path: str = "generated_image.png"
    model_path: str = "stabilityai/stable-diffusion-2-1"
    num_inference_steps: int = 50
    guidance_scale: float = 12.0
    height: int = 512
    width: int = 512
    device: str = "auto"

pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1",
    torch_dtype=torch.float16
    )

if torch.backends.mps.is_available():
    device = "mps"
else: 
    device = "cuda" if torch.cuda.is_available() else "cpu"

pipe.to(device)


def generate_image(imgPrompt: ImageGenerationRequest) -> Image: 
    generator = None if imgPrompt.seed is None else torch.Generator().manual_seed(int(imgPrompt.seed))

    image: Image = pipe(imgPrompt.prompt,
                        guidance_scale=imgPrompt.guidance_scale, 
                        num_inference_steps=imgPrompt.num_inference_steps, 
                        generator = generator, 
                    ).images[0]
    
    return image

 
reqqq = ImageGenerationRequest(prompt = "The walking dead",
guidance_scale = 12,
num_inference_steps = 50) 
    
image = generate_image(reqqq)
memory_stream = io.BytesIO()
image.save(memory_stream, format="PNG")