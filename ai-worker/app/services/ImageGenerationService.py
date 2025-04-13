import torch
from diffusers import StableDiffusionPipeline
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional
import logging
from pathlib import Path
from app.config import settings


logger = logging.getLogger(__name__)

class ImageGenerator:

    def __init__(self):
        self.device = self._get_device()
        self.model_path = settings.MODEL_PATH
        self.pipe = self._load_model()
        self.executor = ThreadPoolExecutor(max_workers=int(settings.MAX_WORKERS))
        self.save_dir = Path(settings.SAVE_DIR)
        self.save_dir.mkdir(exist_ok=True)
    
    def _get_device(self) -> str:
        if settings.DEVICE.lower() == "auto":
            if torch.cuda.is_available():
                return "cuda"
            elif torch.backends.mps.is_available():
                return "mps"
            return "cpu"
        return settings.DEVICE.lower()

    def _load_model(self):
        torch_dtype = {
            "float16": torch.float16,
            "float32": torch.float32
        }.get(settings.TORCH_DTYPE.lower(), torch.float16)

        pipe = StableDiffusionPipeline.from_pretrained(
            self.model_path,
            torch_dtype=torch_dtype,
            low_cpu_mem_usage=settings.LOW_CPU_MEM_USAGE == "true"
        ).to(self.device)

        if settings.ENABLE_ATTENTION_SLICING == "true":
            pipe.enable_attention_slicing()

        return pipe

    def _generate_single(
        self,
        prompt: str,
        output_path: str,
        num_steps: int = int(settings.DEFAULT_STEPS),
        guidance: float = float(settings.DEFAULT_GUIDANCE),
        height: int = int(settings.DEFAULT_HEIGHT),
        width: int = int(settings.DEFAULT_WIDTH)
    ) -> str:
        try:
            image = self.pipe(
                prompt,
                num_inference_steps=num_steps,
                guidance_scale=guidance,
                height=height,
                width=width
            ).images[0]
            
            image.save(output_path)
            return output_path
        except Exception as e:
            logger.error(f"Generation failed for '{prompt}': {e}")
            raise

    async def generate(
        self,
        prompts: List[str],
        num_steps: Optional[int] = None,
        guidance: Optional[float] = None,
        height: Optional[int] = None,
        width: Optional[int] = None
    ) -> List[str]:
        """Генерация изображений в многопоточном режиме"""
        futures = []
        results = []
        
        for i, prompt in enumerate(prompts):
            output_path = str(self.save_dir / f"generated_{i}.png")
            future = self.executor.submit(
                self._generate_single,
                prompt,
                output_path,
                num_steps or int(settings.DEFAULT_STEPS),
                guidance or float(settings.DEFAULT_GUIDANCE),
                height or int(settings.DEFAULT_HEIGHT),
                width or int(settings.DEFAULT_WIDTH)
            )
            futures.append(future)
        
        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                logger.error(f"Thread execution error: {e}")
        
        return results

# Глобальный инстанс генератора
image_generator = ImageGenerator()