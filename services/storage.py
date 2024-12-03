from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class S3Storage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket_name'] = settings.AWS_BUCKET
        kwargs['access_key'] = settings.AWS_ACCESS_KEY
        kwargs['secret_key'] = settings.AWS_SECRET
        kwargs['region_name'] = settings.AWS_REGION
        # print(f"Initializing S3Storage with bucket: {kwargs['bucket_name']}")
        super().__init__(*args, **kwargs)

    def _save(self, name, content):
        # print(f"Saving file '{name}' to bucket '{self.bucket_name}'")  # Debugging
        return super()._save(name, content)
