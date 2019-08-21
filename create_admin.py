from getpass import getpass
import sys

from owl_mail import create_app
from owl_mail.models import db, User

app = create_app()

with app.app_context():
    username = input('Enter your name: ')

    if User.query.filter(User.username == username).count():
        print('This user already exist: ')
        sys.exit(0)

    password1 = getpass('Enter your password: ')
    password2 = getpass('Repeat your password: ')

    if not password1 == password2:
        print('Passwords do not match')
        sys.exit(0)

    new_user = User(username=username, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('Created user, id={}, {}, {}'.format(new_user.id, new_user.username, new_user.password))