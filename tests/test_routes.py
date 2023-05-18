from flask import Flask, render_template, redirect, request, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_login import UserMixin, login_user, login_required, current_user, logout_user
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash

import forms
import models
from app import db


# Test if the home page is reachable
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>WAR/COR</title>" in response.data


# Test if a new user can be added
def test_register(client, app):

    test_username = "test_user"
    test_password = "123"

    # Check the route actually works
    response_1 = client.get("/register")
    assert response_1.status_code == 200

    # TODO: This is not submitted a form properly, so the form.validate_on_submit condition is never met.
    # Check that the post response is correct
    response_2 = client.post("/register", follow_redirects=True, data={
        "username": test_username,
        "password": test_password,
        "confirm_password": "123",
    })
    assert response_2.status_code == 200

    # Check that the new user was added to the database
    with app.app_context():
        user_query = db.session.execute(select(models.User).filter_by(username=test_username)).scalar()
        assert user_query.username == test_username
        assert werkzeug.security.check_password_hash(pwhash=user_query.password, password=test_password)


def test_logout(client, app):
    response_1 = client.get("/register")
    assert response_1.status_code == 200


def test_login(client):
    response = client.get("/login")
    assert response.status_code == 200



#
# # Test if the newly created user can be logged in.
# def test_login(client, app):
#     # The register path automatically logs in the newly created user,
#     # so they must be logged out here.
#     with app.test_request_context():
#         logout_user()
#
#     response = client.post("/login", data={
#         "username": "test_user",
#         "password": "123",
#     })
#
#     assert response.status_code == 200

