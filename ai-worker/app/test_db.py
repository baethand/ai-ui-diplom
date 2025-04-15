import torch
from diffusers import StableDiffusionPipeline

def test_connection():
    pipe = StableDiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-2-1",
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
        )
    pipe = pipe.to("cuda")
    
    image = pipe(
            "rick grimes drinking coffee",
            num_inference_steps=75,
            guidance_scale=15,
            height=1024,
            width=1024
        ).images[0]
        
    image.save("aiaiaiaiai.png")

if __name__ == "__main__":
    test_connection()