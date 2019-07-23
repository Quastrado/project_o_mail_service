from flask import Flask, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, logout_user
from owl_mail.models import db, User

def create_app(test_config = False):
    app = Flask(__name__)
    Bootstrap(app)
    if test_config:
        app.config.from_object('config.TestConfig')
    else:
        app.config.from_object('config.BaseConfig')
        db.init_app(app)
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    with app.app_context():
        from owl_mail import routes

    return app