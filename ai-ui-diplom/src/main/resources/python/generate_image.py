import sys
from diffusers import StableDiffusionPipeline
import torch

def generate_image(
    prompt: str,
    output_path: str = "generated_image.png",
    model_path: str = "./models",  # Путь к локальной модели
    num_inference_steps: int = 50,
    guidance_scale: float = 12.0,
    height: int = 512,
    width: int = 512,
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
) -> str:
    """
    Генерация изображения с использованием Stable Diffusion.

    :param prompt: Текстовый запрос для генерации изображения.
    :param output_path: Путь для сохранения изображения.
    :param model_path: Путь к локальной модели.
    :param num_inference_steps: Количество шагов генерации.
    :param guidance_scale: Параметр guidance scale.
    :param height: Высота изображения.
    :param width: Ширина изображения.
    :param device: Устройство для выполнения ("cuda" или "cpu").
    :return: Путь к сохранённому изображению.
    """
    # Загрузка модели из локальной директории
    pipe = StableDiffusionPipeline.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True  # Используем accelerate для оптимизации
    )
    pipe = pipe.to(device)

    # Генерация изображения
    image = pipe(
        prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        height=height,
        width=width
    ).images[0]

    # Сохранение изображения
    image.save(output_path)
    return output_path

if __name__ == "__main__":
    # Парсинг аргументов командной строки
    prompt = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "generated_image.png"
    model_path = sys.argv[3] if len(sys.argv) > 3 else "./models"
    num_inference_steps = int(sys.argv[4]) if len(sys.argv) > 4 else 50
    guidance_scale = float(sys.argv[5]) if len(sys.argv) > 5 else 12.0
    height = int(sys.argv[6]) if len(sys.argv) > 6 else 512
    width = int(sys.argv[7]) if len(sys.argv) > 7 else 512
    device = sys.argv[8] if len(sys.argv) > 8 else ("cuda" if torch.cuda.is_available() else "cpu")

    # Генерация изображения
    result_path = generate_image(
        prompt=prompt,
        output_path=output_path,
        model_path=model_path,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        height=height,
        width=width,
        device=device
    )

    # Вывод пути к изображению
    print(result_path)