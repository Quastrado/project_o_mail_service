import pytest
import boto3
from botocore.exceptions import EndpointConnectionError, NoCredentialsError
from owl_mail.save_data import upload_in_cloud

def test_upload_in_cloud():
    assert upload_in_cloud('profile/profile.xml', 'quastrdos-first-bucket') == 'Success'