"""
Cloudflare R2 storage backends (S3-compatible), used only in production —
see the USE_R2 flag in settings.py. Static and media files are split into
two "folders" (location=...) inside the same bucket.
"""
from storages.backends.s3 import S3Storage


class StaticStorage(S3Storage):
    location = 'static'
    default_acl = None
    file_overwrite = True


class MediaStorage(S3Storage):
    location = 'media'
    default_acl = None
    file_overwrite = False
