# storage.py
import os
import uuid
import io
from django.core.files.uploadedfile import UploadedFile
from minio import Minio
import logging

# Logging konfiqurasiyası
logger = logging.getLogger(__name__)

# Contabo S3 parametrləri
CONTABO_ENDPOINT_URL = "https://usc1.contabostorage.com/a4def5a5d9f9427bbcca88f8a9503209:turing-academy"  # Düzəldilmiş endpoint
CONTABO_ACCESS_KEY = "turing2025"
CONTABO_SECRET_KEY = "turingacademy2025"
CONTABO_BUCKET_NAME = "turing-academy"

def upload_file_to_contabo_s3(file: UploadedFile) -> str:
    try:
        # MinIO client-i initialize et
        minio_client = Minio(
            CONTABO_ENDPOINT_URL,
            access_key=CONTABO_ACCESS_KEY,
            secret_key=CONTABO_SECRET_KEY,
            secure=True
        )

        # Fayl məzmununu oxu
        file.seek(0)
        file_bytes = file.read()

        # Fayl adını təmizlə
        clean_filename = "".join(c for c in file.name if c.isalnum() or c in ('-', '_', '.'))
        file_extension = os.path.splitext(clean_filename)[1] or '.jpg'

        # Unikal ad yarat
        unique_name = f"{uuid.uuid4()}{file_extension}"
        object_key = f"uploads/{unique_name}"

        # Bucket mövcudluğunu yoxla
        if not minio_client.bucket_exists(CONTABO_BUCKET_NAME):
            minio_client.make_bucket(CONTABO_BUCKET_NAME)

        # MinIO üçün data stream hazırla
        data_stream = io.BytesIO(file_bytes)
        data_length = len(file_bytes)

        # Faylı MinIO-ya yüklə
        minio_client.put_object(
            bucket_name=CONTABO_BUCKET_NAME,
            object_name=object_key,
            data=data_stream,
            length=data_length,
            content_type=file.content_type or "application/octet-stream",
        )

        # Public URL generate et
        public_url = f"https://{CONTABO_ENDPOINT_URL}/{CONTABO_BUCKET_NAME}/{object_key}"

        logger.info(f"File uploaded successfully: {public_url}")
        return public_url

    except Exception as e:
        logger.error(f"Upload error: {e}")
        # Lokalde test etmək üçün müvəqqəti həll
        return f"https://placeholder.com/image/{uuid.uuid4()}.jpg"