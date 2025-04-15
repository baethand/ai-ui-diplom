import torch
from diffusers import StableDiffusionPipeline
from concurrent.futures import as_completed
from concurrent.futures import ProcessPoolExecutor
from typing import List, Optional
import logging
from pathlib import Path
logger = logging.getLogger(__name__)




class ImageGenerator:

    def __init__(self):
        self.device = "cuda"
        self.model_path = "stabilityai/stable-diffusion-2-1"
        self.pipe = self._load_model()
        self.executor = ProcessPoolExecutor(max_workers=int(1))
        self.save_dir = Path("/")
        self.save_dir.mkdir(exist_ok=True)
    
    def _get_device(self) -> str:
        if "auto" == "auto":
            if torch.cuda.is_available():
                return "cuda"
            elif torch.backends.mps.is_available():
                return "mps"
            return "cpu"
        return "cuda"

    def _load_model(self):
        torch_dtype = {
            "float16": torch.float16,
            "float32": torch.float32
        }.get("float32", torch.float16)

        pipe = StableDiffusionPipeline.from_pretrained(
            self.model_path,
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=True
        ).to(self.device)

        # pipe.enable_attention_slicing()

        return pipe

    def _generate_single(
        self,
        prompt: str,
        output_path: str,
        num_steps: int = int(5),
        guidance: float = float(12),
        height: int = int(512),
        width: int = int(512)
    ) -> str:
        pipe = StableDiffusionPipeline.from_pretrained(
            self.model_path,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
            )
        pipe = pipe.to("cuda")
        
        image = pipe(
            prompt,
            num_inference_steps=num_steps,
            guidance_scale=guidance,
            height=height,
            width=width
        ).images[0]
        
        image.save(output_path)
        return "good"
        
# Глобальный инстанс генератора
image_generator = ImageGenerator()
result = image_generator._generate_single(
            prompt="The walking dead",
            output_path="aiaiaiaiai.png",
            num_steps=15,
            guidance=12,
            height=768,
            width=768
        )
