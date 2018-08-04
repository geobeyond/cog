from django.utils.deconstruct import deconstructible
from minio_storage.storage import (
    MinioStorage,
    create_minio_client_from_settings
)


@deconstructible
class MinioCogStorage(MinioStorage):
    def __init__(self):
        client = create_minio_client_from_settings()
        bucket_name = get_setting("MINIO_STORAGE_COG_BUCKET_NAME")
        base_url = get_setting("MINIO_STORAGE_COG_URL", None)
        auto_create_bucket = get_setting(
            "MINIO_STORAGE_AUTO_CREATE_COG_BUCKET", False)
        auto_create_policy = get_setting(
            "MINIO_STORAGE_AUTO_CREATE_COG_POLICY", False)
        presign_urls = get_setting(
            'MINIO_STORAGE_COG_USE_PRESIGNED', False)
        backup_format = get_setting(
            "MINIO_STORAGE_COG_BACKUP_FORMAT", False)
        backup_bucket = get_setting(
            "MINIO_STORAGE_COG_BACKUP_BUCKET", False)

        super(MinioCogStorage, self).__init__(
            client, bucket_name,
            auto_create_bucket=auto_create_bucket,
            auto_create_policy=auto_create_policy,
            base_url=base_url,
            presign_urls=presign_urls,
            backup_format=backup_format,
            backup_bucket=backup_bucket)
