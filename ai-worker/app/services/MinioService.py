from minio import Minio
from minio.error import S3Error
from datetime import timedelta
from app.config import settings

class MinioService:
    
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket = settings.MINIO_BUCKET
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def upload_image(self, file_data: bytes, filename: str, content_type: str) -> None:
        try:
            self.client.put_object(
                self.bucket,
                filename,
                file_data,
                length=len(file_data),
                content_type=content_type
            )
        except S3Error as e:
            raise ValueError(f"MinIO upload error: {e}")

    def get_image_url(self, filename: str, expires: int = 3600) -> str:
        try:
            return self.client.presigned_get_object(
                self.bucket,
                filename,
                expires=timedelta(seconds=expires)
            )
        except S3Error:
            raise FileNotFoundError(f"Image {filename} not found")

    def list_images(self) -> list[str]:
        try:
            objects = self.client.list_objects(self.bucket)
            return [obj.object_name for obj in objects]
        except S3Error as e:
            raise ValueError(f"MinIO list error: {e}")