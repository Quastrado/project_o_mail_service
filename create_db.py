from owl_mail import create_app
from owl_mail.models import db

db.create_all(app=create_app())