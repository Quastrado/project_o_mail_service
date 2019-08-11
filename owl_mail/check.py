import boto3
from config import BaseConfig

def s3_files():
    s3 = boto3.client(
        's3',
        aws_access_key_id = BaseConfig.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = BaseConfig.AWS_SECRET_ACCESS_KEY,
        region_name = BaseConfig.AWS_REGION,
    )

    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(BaseConfig.AWS_BUCKET_NAME)
    summaries = my_bucket.objects.all()
    s3_files_dict = {
        'bucket': my_bucket,
        'files': summaries
    }
    return s3_files_dict