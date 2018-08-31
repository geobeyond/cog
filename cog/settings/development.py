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

from cog.settings.base import *

if os.getenv('SECRET_KEY'):
    SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = bool(int(os.getenv('DEBUG', True)))

if os.getenv('ALLOWED_HOSTS'):
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
else:
    ALLOWED_HOSTS = ['*']

SQLITE = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

PG = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'HOST': os.getenv('POSTGRES_HOST'),
    'PORT': os.getenv('POSTGRES_PORT'),
    'USER': os.getenv('POSTGRES_USER'),
    'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
    'NAME': os.getenv('POSTGRES_DB'),
}

if os.getenv("DOCKER", default=False):
    DB = PG
else:
    DB = SQLITE

# Database
DATABASES = {
    'default': DB
}

INSTALLED_APPS += (
    # other apps for local development
    'rest_framework',
    'minio_storage',
)

# Minio server
STATIC_URL = '/static/'
STATIC_ROOT = './static_files/'

DEFAULT_FILE_STORAGE = "minio_storage.storage.MinioMediaStorage"
STATICFILES_STORAGE = "minio_storage.storage.MinioStaticStorage"
if os.getenv("DOCKER", default=False):
    MINIO_STORAGE_ENDPOINT = os.getenv("MINIO_STORAGE_ENDPOINT", "minio:9000")
    MINIO_STORAGE_ACCESS_KEY = os.getenv("MINIO_STORAGE_ACCESS_KEY")
    MINIO_STORAGE_SECRET_KEY = os.getenv("MINIO_STORAGE_SECRET_KEY")
else:
    MINIO_STORAGE_ENDPOINT = 'localhost:9000'
    MINIO_STORAGE_ACCESS_KEY = 'geobeyond'
    MINIO_STORAGE_SECRET_KEY = 'geobeyond'
MINIO_STORAGE_USE_HTTPS = False
MINIO_STORAGE_MEDIA_BUCKET_NAME = 'local-media'
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
MINIO_STORAGE_STATIC_BUCKET_NAME = 'local-static'
MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True
MINIO_STORAGE_AUTO_CREATE_STATIC_POLICY = True

# These settings should generally not be used:
# MINIO_STORAGE_MEDIA_URL = 'http://localhost:9000/local-media'
# MINIO_STORAGE_STATIC_URL = 'http://localhost:9000/local-static'

# COG
MINIO_STORAGE_COG_BUCKET_NAME = "cog"
if os.getenv("DOCKER", default=False):
    MINIO_STORAGE_COG_URL = os.getenv("MINIO_STORAGE_COG_URL")
else:
    MINIO_STORAGE_COG_URL = "http://localhost:9000"
MINIO_STORAGE_AUTO_CREATE_COG_BUCKET = True
MINIO_STORAGE_AUTO_CREATE_COG_POLICY = True
MINIO_STORAGE_COG_USE_PRESIGNED = False
MINIO_STORAGE_COG_BACKUP_FORMAT = False
MINIO_STORAGE_COG_BACKUP_BUCKET = False

# RASTERIO
# It could be one of ycbcr,zstd,lzw,deflate,packbits,raw
RASTERIO_COGEO_PROFILE = "ycbcr"
