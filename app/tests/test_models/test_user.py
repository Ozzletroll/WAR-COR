import werkzeug
from datetime import datetime
import jwt
from flask import current_app

from app import models


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


def test_change_password(client):

    user = models.User()
    user_form = {
        "email": "email@testemail.com",
        "username": "New Username",
        "password": "Password"
    }
    user.update(user_form, new=True)

    change_password_form = {
        "old_password": "Password",
        "new_password": "NewPassword"
    }
    user.change_password(change_password_form)
    assert werkzeug.security.check_password_hash(
        pwhash=user.password,
        password="NewPassword")

    change_password_form_reset = {
        "new_password": "ResetPassword"
    }
    user.change_password(change_password_form_reset, reset=True)
    assert werkzeug.security.check_password_hash(
        pwhash=user.password,
        password="ResetPassword")


def test_get_reset_password_token(client):

    user = models.User()
    user_form = {
        "email": "email@testemail.com",
        "username": "New Username",
        "password": "Password"
    }
    user.update(user_form, new=True)

    token = user.get_reset_password_token()

    assert token is not None
    assert isinstance(token, str)

    # Decode the token to check its contents
    decoded = jwt.decode(
        token,
        current_app.config["SECRET_KEY"],
        algorithms=["HS256"]
    )

    # Verify that the decoded token contains expected data
    assert "reset_password" in decoded
    assert decoded["reset_password"] == user.id

    expiry = datetime.now().timestamp() + 600
    assert "exp" in decoded
    assert decoded["exp"] == expiry


def test_verify_password_reset_token(client):

    user = models.User()
    user_form = {
        "email": "email@testemail.com",
        "username": "New Username",
        "password": "Password"
    }
    user.update(user_form, new=True)

    token = user.get_reset_password_token()
    decoded_user = user.verify_password_reset_token(token)
    assert decoded_user.id == user.id
