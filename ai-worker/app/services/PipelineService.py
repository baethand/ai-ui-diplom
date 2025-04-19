from functools import lru_cache
from diffusers import StableDiffusionPipeline
import torch

# Кэшируем уже загруженные пайплайны (по model_path)
@lru_cache(maxsize=5)
def get_pipeline(model_path: str):
    pipe = StableDiffusionPipeline.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
    )
    return pipe.to("cuda")
