import boto3
from botocore.exceptions import NoCredentialsError, EndpointConnectionError
from config import BaseConfig
from owl_mail.models import db, Docs

class Check:
    s3 = boto3.client(
            's3',
            aws_access_key_id = BaseConfig.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = BaseConfig.AWS_SECRET_ACCESS_KEY,
            region_name = BaseConfig.AWS_REGION,
            )

    def bucket_content_list(self):
        try:
            files = self.s3.list_objects(Bucket = BaseConfig.AWS_BUCKET_NAME)
        except (NoCredentialsError, EndpointConnectionError):
            raise s3_error("""
                            Something went wrong in working with the s3 service.
                            Failed to get information about stored files
                            """)    
        try:
            contents = files['Contents']
        except KeyError:
            return

        bucket_content_list = [key['Key'] for key in contents]
        return bucket_content_list


    def files_count_discrepancy(self):
        docs_record_count = db.session.query(Docs).count()
        if len(self.bucket_content_list()) != docs_record_count:
            return True


    def file_names_discrepancy(self):
        id_list = [str(r) for r, in db.session.query(Docs.id).all()]
        file_names = [el.split('.')[0] for el in self.bucket_content_list()]
        if set(id_list) != set(file_names):
            return True


    def hash_caompare(self, values_list):
        discrepancies = []
        for value in values_list:
            file_name = '{}.xml'.format(value)
            s3_file_md5 = self.s3.head_object(
                Bucket=BaseConfig.AWS_BUCKET_NAME,
                Key=file_name
            )['ETag'][1:-1]
            value = int(value)
            record = db.session.query(Docs).filter(Docs.id==value).first()
            db_md5 = record.file_hash
            if s3_file_md5 != db_md5:
                discrepancies.append(file_name)
        return discrepancies