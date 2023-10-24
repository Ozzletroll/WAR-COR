import pytest
from flask import url_for
from app import create_app
from app import db


@pytest.fixture(scope="module")
def app():
    app = create_app(database_uri="sqlite:///test.db")
    yield app

    # Teardown
    with app.app_context():
        db.session.close()
        db.drop_all()


@pytest.fixture()
def client(app):
    app.config["TESTING"] = True
    app.config['SECRET_KEY'] = "TESTING_KEY"
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


@pytest.fixture()
def auth(client):
    return AuthActions(client)


class AuthActions(object):
    """ Class to facilitate common user auth functions during testing """

    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post("/login", follow_redirects=True, data={
            "username": username,
            "password": password,
        })

    def register(self, username='test', password='test'):
        return self._client.post("/register", follow_redirects=True, data={
            "username": username,
            "password": password,
            "confirm_password": password,
        })

    def logout(self):
        return self._client.get("/logout", follow_redirects=True)

    def delete(self, username, given_username, given_password):
        url = url_for("user.delete_user", username=username)
        return self._client.post(url, follow_redirects=True, data={
            "username": given_username,
            "password": given_password,
        })


