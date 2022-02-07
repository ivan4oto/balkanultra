import os


AWS_S3_REGION_NAME = 'fra1'
AWS_S3_ENDPOINT_URL = 'https://{r}.digitaloceanspaces.com'.format(r=AWS_S3_REGION_NAME)

AWS_STORAGE_BUCKET_NAME = 'balkanultra'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

AWS_LOCATION = "https://balkanultra.fra1.digitaloceanspaces.com"

DEFAULT_FILE_STORAGE = "balkanultra.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "balkanultra.cdn.backends.StaticRootS3Boto3Storage"
