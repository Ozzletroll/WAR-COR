from flask import Flask, render_template, redirect, request, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_login import UserMixin, login_user, login_required, current_user, logout_user
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash

import forms
import models
from app import db

TEST_USERNAME = "test_user"
TEST_PASSWORD = "123"


# Test if the home page is reachable
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>WAR/COR</title>" in response.data


# Test if a new user can be added
def test_register(client, app):
    # Check the route actually works
    response_1 = client.get("/register")
    assert response_1.status_code == 200

    # Check that the post response is correct
    response_2 = client.post("/register", follow_redirects=True, data={
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
        "confirm_password": "123",
    })
    assert response_2.status_code == 200

    # Check that the new user was added to the database
    with app.app_context():
        user_query = db.session.execute(select(models.User).filter_by(username=TEST_USERNAME)).scalar()
        assert user_query.username == TEST_USERNAME
        assert werkzeug.security.check_password_hash(pwhash=user_query.password, password=TEST_PASSWORD)


def test_login(client):
    # Test if the page is reachable
    response_1 = client.get("/login")
    assert response_1.status_code == 200

    # Test if the test user can log in successfully
    response_2 = client.post("/login", follow_redirects=True, data={
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
    })
    assert response_2.status_code == 200
    assert current_user.username == TEST_USERNAME


def test_logout(client):
    # Login user
    response_1 = client.post("/login", follow_redirects=True, data={
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
    })
    # Test if the user can be logged out
    response_2 = client.get("/logout", follow_redirects=True)
    assert response_2.status_code == 200
    assert current_user.is_anonymous is True
