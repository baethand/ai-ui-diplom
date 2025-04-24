from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ImageResponse(BaseModel):
    id: int
    image_url: str
    name: str
    width: int
    height: int
    model: str
    prompt: Optional[str]
    created_at: datetime
    status: str