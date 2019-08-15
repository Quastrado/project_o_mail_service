from xml.etree import ElementTree as ET
import boto3
from config import BaseConfig

def s3_files():
    s3 = boto3.client(
        's3',
        aws_access_key_id = BaseConfig.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = BaseConfig.AWS_SECRET_ACCESS_KEY,
        region_name = BaseConfig.AWS_REGION,
        )
    
    files = s3.list_objects(Bucket = BaseConfig.AWS_BUCKET_NAME)['Contents']
    
    for key in files:
        tree = ET.parse(key)
        root = tree.getroot() 
    
    return files