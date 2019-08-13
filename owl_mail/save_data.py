import os
from datetime import datetime
from hashlib import md5
from xml.etree import ElementTree as ET

import boto3
from botocore.exceptions import NoCredentialsError, EndpointConnectionError

from config import BaseConfig
from owl_mail.models import db, Docs


def to_xml(dict_of_data):
    
    dict_of_data['Date_of_creation'] = datetime.now().strftime("%d/%m/%Y")
    
    tree = ET.parse('profile/profile.xml')
    root = tree.getroot()
    for key in dict_of_data.keys():
        for tag in root.iter(key):
            tag.text = dict_of_data[key]

    xml_file = '{}_{}.xml'.format(root[1][0].text, root[1][1].text)
    tree.write(xml_file)
    return xml_file


def hash_receiver(xml):
    file_name = xml
    hasher = md5()

    with open(file_name, 'rb') as f:
        hasher.update(f.read())

    f_hash = hasher.hexdigest()
    return f_hash


def db_insert(db_dict):
    db_set = Docs(db_dict['Name'], db_dict['Email'], db_dict['Hash'], db_dict['Date_of_creation'])
    db.session.add(db_set)
    db.session.flush()
    f_id = db_set.id
    return f_id


def upload_in_cloud(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    s3 = boto3.client(
        's3',
        aws_access_key_id = BaseConfig.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = BaseConfig.AWS_SECRET_ACCESS_KEY,
        region_name = BaseConfig.AWS_REGION,
        )
    respone = s3.upload_file(file_name, bucket, object_name)
            

def execute_save(c_dict):
    xml = to_xml(c_dict)
    f_hash = hash_receiver(xml)
    db_dict = {
        'Name': c_dict['Name'], 
        'Email': c_dict['Email'], 
        'Hash': f_hash, 
        'Date_of_creation': c_dict['Date_of_creation']
        }
    f_id = db_insert(db_dict)
    f_id = '{}.xml'.format(str(f_id))
    os.rename(xml, str(f_id))
    try:
        upload_in_cloud(str(f_id), BaseConfig.AWS_BUCKET_NAME)
    except (NoCredentialsError, EndpointConnectionError):
        os.remove(f_id)
        raise s3_error('Something went wrong in working with the s3 service. The document was not saved')
    db.session.commit()
    os.remove(f_id)
    
    



