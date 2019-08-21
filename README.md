# Owl Mail

This is a simple web application for a staff member at Hogwarts School. It allows you to create and store documents and necessary records.

# Technologies

- python 3.6.8
- bootstrap 4
- PostgreSQL 11.4
- Amazon S3 - AWS

# Installation

First, you need to clone the repository using git

```bash
$ git clone https://github.com/Quastrado/project_o_mail_service.git
```
Then create a virtual environment in the project folder using the venv tool
```bash
$ python3 -m venv env
```
And activate the virtual environment
```bash
$ source env/bin/activate
```
Using file requirements.txt, install neсessary modules and packages
```bash
$ pip install -r requirements.txt
```
Add to the root of application folder file config.py, which will contain:
- Secret key
- PostgreSQL parameters
- AWS keys, region, bucket name

Something like:
```python
class BaseConfig:
    SECRET_KEY = "your secret key"
    DEBUG = True
    AWS_ACCESS_KEY_ID = 'your aws_access_key_id'
    AWS_SECRET_ACCESS_KEY = 'your aws_secret_access_key' 
    AWS_REGION = 'your aws region'
    AWS_BUCKET_NAME = 'your bucket name'
    
    POSTGRES = {
        'user':  'xxx', 
        'password':  'xxx', 
        'host':  'localhost', 
        'database':  'xxx'
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(password)s@%(host)s/%(database)s' % POSTGRES
```
Create tables in your database
```bash
$ python create_db.py
```
Create user for application
```bash
$ python create_admin.py
```

# Launch

Open the terminal in the application folder and aсctivate virtual environment
```bash
$ source env/bin/activate
```
Launch the application
```bash
$ sh run.sh
```
And just click on the link terminal

# Usage

Log in using login and password which you that you specified when creating the user.
This project still in development. But you can create documents now. Choose "Write" in menu and start create a document

# Status

In development


