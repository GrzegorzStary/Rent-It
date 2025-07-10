from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    """
    Custom storage class for static files using S3.
    """
    location = settings.STATICFILES_LOCATION

    
class MediaStorage(S3Boto3Storage):
    """
    Custom storage class for media files using S3.
    """
    location = settings.MEDIAFILES_LOCATION
