import os
from datetime import datetime
from hashlib import md5
from xml.etree import ElementTree as ET

import boto3
from botocore.exceptions import NoCredentialsError, EndpointConnectionError
from flask import flash, redirect, render_template, session, url_for

from config import BaseConfig
from owl_mail.forms import ContentForm
from owl_mail.models import db, Docs


class Stamp():
    
    def save_data(self, content_dict):
        #create new xml file
        today = datetime.now().strftime('%d-%m-%Y')
        content_dict['Date_of_creation'] = today
        tree = ET.parse('profile/profile.xml')
        root = tree.getroot()
        for key in content_dict.keys():
            for tag in root.iter(key):
                tag.text = content_dict[key]
        xml_file = '{}_{}.xml'.format(root[1][0].text, root[1][1].text)
        tree.write(xml_file)
        # get file hash
        hasher = md5()
        with open(xml_file, 'rb') as f:
            hasher.update(f.read())
        file_hash = hasher.hexdigest()
        # data base insert
        db_set = Docs(content_dict['Name'],
            content_dict['Email'],
            file_hash,
            content_dict['Date_of_creation']
        )
        db.session.add(db_set)
        db.session.flush()
        # upload to cloud
        file_id = '{}.xml'.format(str(db_set.id))
        os.rename(xml_file, file_id)
        try:
            object_name = file_id
            s3 = boto3.client(
                's3',
                aws_access_key_id = BaseConfig.AWS_ACCESS_KEY_ID,
                aws_secret_access_key = BaseConfig.AWS_SECRET_ACCESS_KEY,
                region_name = BaseConfig.AWS_REGION,
            )
            respone = s3.upload_file(
                file_id,
                BaseConfig.AWS_BUCKET_NAME,
                object_name
            )
        except (NoCredentialsError, EndpointConnectionError):
            os.remove(file_id)
            raise s3_error('Something went wrong in working with the s3 service. The document was not saved')
        db.session.commit()
        os.remove(file_id)


    def stamp_processing(self):
        states = session['write_states']
        if not states['spelling']:
            return redirect(url_for('wrong'))

        form = ContentForm()
        content_dict = session['content']
        owls = {
            'Eared Owl': '/static/eared-owl.jpg',
            'White Owl': '/static/white-owl.jpg',
            'Barn Owl': '/static/barn-owl.jpg',
            'Tawny Owl': '/static/tawny-owl.jpg'
        }
        form.name.data = content_dict['Name']
        form.surname.data = content_dict['Surname']
        form.email.data = content_dict['Email']
        form.date_of_birth.data = content_dict['Date_of_birth']
        form.address.data = content_dict['Address']
        form.subaddress.data = content_dict['Subaddress']
        form.owl.data = content_dict['Owl']
        img = owls[form.owl.data]
            
        if form.submit.data:
            try:
                self.save_data(content_dict)
                states['view'] = True
                session['write_states'] = states
                print(session)
                return redirect(url_for('finish'))
            except Exception:
                flash(
                'Something went wrong in working with the s3 service.'
                'The document was not saved'
                )
        return render_template('show_data.html', form=form, img=img)
