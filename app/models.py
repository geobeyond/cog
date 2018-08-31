# -*- coding: utf-8 -*-

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

from django.db import models
from django.db.models.signals import post_save, post_delete
from app.storage import MinioCogStorage
from cog.settings import development, production
from PIL import Image
from urllib.parse import urljoin
import uuid
import os


class PrimaryKeyAsUUIDModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class COG(PrimaryKeyAsUUIDModel):
    """Model for the Cloud Optimized Geotiff objects
    """

    length = 100

    name = models.CharField(max_length=length, blank=False, null=False)
    image = models.FileField(
        storage=MinioCogStorage(),
        blank=True, null=True
    )
    thumbnail = models.FileField(
        storage=MinioCogStorage(),
        blank=True, null=True
    )
    bucket_name = models.CharField(max_length=length, blank=True, null=True)
    resource_uri = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{0}:{1}".format(self.bucket_name, self.name)

    class Meta:
        db_table = 'COG'
        managed = True
        verbose_name = 'COG'
        verbose_name_plural = 'COGs'


    def set_thumbnail(self):
        # generate thumbnail
        thumb_name = "{0}-thumb.png".format(
            self.name
        )
        max_size = (250, 250)
        try:
            if self.image:
                thumb_img = Image.open(self.image)
                # see issue https://github.com/python-pillow/Pillow/issues/3044
                # thumb_img.tile = [
                #     e for e in thumb_img.tile if e[1][2] < 2181 and e[1][3]<1294
                # ]
                thumb_img.load()
                thumb_img.verify()
                thumb_img.thumbnail(max_size, Image.ANTIALIAS)
                thumb_img.save(thumb_name)
        except:
            raise IOError("Unsupported image type")

        COG.objects.filter(
            id=self.id
        ).update(thumbnail=thumb_img)

    def set_bucket_name_and_resource_uri(self):
        # generate bucket_name
        if 'development' in os.getenv('DJANGO_SETTINGS_MODULE'):
            bucketname = development.MINIO_STORAGE_COG_BUCKET_NAME
        else:
            bucketname = production.MINIO_STORAGE_COG_BUCKET_NAME
        # generate uri from minio
        if 'development' in os.getenv('DJANGO_SETTINGS_MODULE'):
            minio_baseurl = development.MINIO_STORAGE_COG_URL
        else:
            minio_baseurl = production.MINIO_STORAGE_COG_URL
        uri = urljoin(
            minio_baseurl,
            os.path.join(bucketname, self.name)
        )
        COG.objects.filter(
            id=self.id
        ).update(
            bucket_name=bucketname,
            resource_uri=uri
        )

    def delete_file_from_minio_storage(self):
        try:
            MinioCogStorage().delete(self.name)
        except:
            raise IOError("Resource not deleted from Minio Server.")


def cog_changed(instance, *args, **kwargs):
# Comment until issue with Pillow is resolved
#     instance.set_thumbnail()
    instance.set_bucket_name_and_resource_uri()

def cog_deleted(instance, *args, **kwargs):
    instance.delete_file_from_minio_storage()


post_save.connect(cog_changed, sender=COG)
post_delete.connect(cog_deleted, sender=COG)
