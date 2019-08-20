import pytest

from flask_sqlalchemy import SQLAlchemy

from owl_mail import create_app
from owl_mail.models import User

@pytest.fixture
def app():
    app=create_app()
    return app


def test_app(client):
    response = client.get('/menu')
    assert response.status_code == 200


@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    user1 = User('Ghost', 'invisible', 'admin')
    user2 = User('Vagabound', 'danger', 'user')
    db.session.add(user1)
    db.session.add(user2)

    yield db

    db.drop_all() 