# Copyright 2018 Geobeyond Srl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.utils.deconstruct import deconstructible
from minio_storage.storage import (
    MinioStorage,
    create_minio_client_from_settings,
    get_setting
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
