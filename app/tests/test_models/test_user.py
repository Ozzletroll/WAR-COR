from sqlalchemy import select
import werkzeug

from app import db, models


def test_update(client):

    user = models.User()
    user_form = {
        "email": "email@testemail.com",
        "username": "New Username",
        "password": "Password"
    }
    user.update(user_form, new=True)

    assert user.email == "email@testemail.com"
    assert user.username == "New Username"
    assert werkzeug.security.check_password_hash(
        pwhash=user.password,
        password="Password")
