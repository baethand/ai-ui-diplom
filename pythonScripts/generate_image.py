import sys
from diffusers import StableDiffusionPipeline
import torch

def generate_image(prompt: str, output_path: str = "generated_image.png"):
    model_id = "stabilityai/stable-diffusion-2-1"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")  # Если у тебя есть GPU
    image = pipe(prompt, num_inference_steps=50, guidance_scale=10, height=512, width=512).images[0]  # По умолчанию 20-30 шагов
    image.save(output_path)
    return output_path

if __name__ == "__main__":
    prompt = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "generated_image.png"
    generate_image(prompt, output_path)
    print(output_path)  # Возвращаем путь к изображению
