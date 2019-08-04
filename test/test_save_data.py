import pytest

from owl_mail import create_app

@pytest.fixture
def app():
    app=create_app()
    return app


def test_app(client):
    response = client.get('/login')
    assert response.status_code == 200
