from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# filr_overwrite = False for static and media files to prevent overwriting if the file with the same name 
# already exists.

class StaticStorage(S3Boto3Storage):
    """
    Custom storage class for static files using S3.
    """
    location = settings.STATICFILES_LOCATION
    default_acl = 'public-read'
    file_overwrite = False
    
class MediaStorage(S3Boto3Storage):
    """
    Custom storage class for media files using S3.
    """
    location = settings.MEDIAFILES_LOCATION
    default_acl = 'public-read'
    file_overwrite = False