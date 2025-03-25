from diffusers import StableDiffusionPipeline
import torch

def generate_image(
    prompt: str,
    output_path: str = "generated_image.png",
    model_path: str = "stabilityai/stable-diffusion-2-1",
    num_inference_steps: int = 50,
    guidance_scale: float = 12.0,
    height: int = 512,
    width: int = 512,
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
) -> str:
    pipe = StableDiffusionPipeline.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
    )
    pipe = pipe.to(device)
    
    image = pipe(
        prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        height=height,
        width=width
    ).images[0]
    
    image.save(output_path)
    return output_path