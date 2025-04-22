from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):

    # MinIO
    MINIO_ENDPOINT: str = Field("localhost:9000", env="MINIO_ENDPOINT")
    MINIO_ACCESS_KEY: str = Field(..., env="MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = Field(..., env="MINIO_SECRET_KEY")
    MINIO_SECURE: bool = Field(False, env="MINIO_SECURE")
    MINIO_BUCKET: str = Field("my-bucket", env="MINIO_BUCKET")
    
    DEBUG: bool = Field(False, env="DEBUG")

    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(180, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    PWD_SCHEMES: str = Field("bcrypt", env="PWD_SCHEMES")
    PWD_DEPRECATED: str = Field("auto", env="PWD_DEPRECATED")

    # Database
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(5432, env="POSTGRES_PORT")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Image Generation
    MODEL_PATH: str = Field("stabilityai/stable-diffusion-2-1", env="MODEL_PATH")
    DEFAULT_STEPS: int = Field(50, env="DEFAULT_STEPS")
    DEFAULT_GUIDANCE: float = Field(12.0, env="DEFAULT_GUIDANCE")
    DEFAULT_HEIGHT: int = Field(512, env="DEFAULT_HEIGHT")
    DEFAULT_WIDTH: int = Field(512, env="DEFAULT_WIDTH")
    SAVE_DIR: str = Field("./generated_images", env="SAVE_DIR")
    DEVICE: str = Field("auto", env="DEVICE")
    
    # Performance
    TORCH_DTYPE: str = Field("float16", env="TORCH_DTYPE")
    MAX_WORKERS: int = Field(2, env="MAX_WORKERS")
    LOW_CPU_MEM_USAGE: bool = Field(True, env="LOW_CPU_MEM_USAGE")
    ENABLE_ATTENTION_SLICING: bool = Field(True, env="ENABLE_ATTENTION_SLICING")
    

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

ALLOWED_MODELS = {
        "stabilityai/stable-diffusion-2-1"
    }

settings = Settings()