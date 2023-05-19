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

TEST_CAMPAIGN_TITLE = "Test Campaign Title"
TEST_CAMPAIGN_DESCRIPTION = "Test Campaign Description"

TEST_EVENT_TITLE = "Test Event Title"
TEST_EVENT_TYPE = "Test Event Type"
TEST_EVENT_DATE = "5126-09-01 04:00:00"
TEST_EVENT_LOCATION = "Karaq Desert"
TEST_EVENT_BELLIGERENTS = "9th Armoured Cavalry, 12th Haqqarri Legion"
TEST_EVENT_BODY = "A description of the battle goes here."
TEST_EVENT_RESULT = "9th Armoured Cavalry victory."


# Function to log in test user
def example_login(client):
    client.post("/login", follow_redirects=True, data={
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
    })


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
    example_login(client)
    # Test if the user can be logged out
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert current_user.is_anonymous is True


def test_create_campaign(client, app):
    example_login(client)
    response = client.post("/create_campaign", follow_redirects=True, data={
        "title": TEST_CAMPAIGN_TITLE,
        "description": TEST_CAMPAIGN_DESCRIPTION,
    })
    assert response.status_code == 200
    campaign_query = db.session.execute(select(models.Campaign).filter_by(title=TEST_CAMPAIGN_TITLE)).scalar()
    assert campaign_query.description == TEST_CAMPAIGN_DESCRIPTION


def test_add_event(client, app):
    id_param = 1
    example_login(client)
    # The id of the campaign is passed as an url parameter
    response_1 = client.get(f"/{TEST_CAMPAIGN_TITLE}/new_event?id={id_param}", follow_redirects=True)
    assert response_1.status_code == 200

    response_2 = client.post(f"/{TEST_CAMPAIGN_TITLE}/new_event?id={id_param}", follow_redirects=True, data={
        "title": TEST_EVENT_TITLE,
        "type": TEST_EVENT_TYPE,
        "date": TEST_EVENT_DATE,
        "location": TEST_EVENT_LOCATION,
        "belligerents": TEST_EVENT_BELLIGERENTS,
        "body": TEST_EVENT_BODY,
        "result": TEST_EVENT_RESULT,
    })
    assert response_2.status_code == 200
    event_query = db.session.execute(select(models.Event).filter_by(id=id_param, title=TEST_EVENT_TITLE)).scalar()
    assert event_query.title == TEST_EVENT_TITLE
    assert event_query.date == TEST_EVENT_DATE


def test_show_timeline(client, app):
    id_param = 1

    response = client.get(f"/{TEST_CAMPAIGN_TITLE}?id={id_param}")
    assert response.status_code == 200
    assert b"<title>Test Campaign Title</title>" in response.data
