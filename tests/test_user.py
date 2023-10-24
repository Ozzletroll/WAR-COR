from sqlalchemy import select
from flask_login import current_user
import werkzeug
from werkzeug.security import generate_password_hash

import models
from app import db

TEST_USERNAME = "test_user"
TEST_PASSWORD = "123"


def test_register(client, app, auth):
    # Test if a new user can be added
    response = auth.register(username=TEST_USERNAME,
                             password=TEST_PASSWORD)
    assert response.status_code == 200

    # Check that the new user was added to the database
    user_query = db.session.execute(select(models.User).filter_by(username=TEST_USERNAME)).scalar()
    assert user_query.username == TEST_USERNAME
    assert werkzeug.security.check_password_hash(pwhash=user_query.password, password=TEST_PASSWORD)


def test_login(client, auth):
    response = auth.login(username=TEST_USERNAME,
                          password=TEST_PASSWORD)
    assert response.status_code == 200
    assert current_user.username == TEST_USERNAME


def test_logout(client, auth):
    # Login user
    auth.login(username=TEST_USERNAME,
               password=TEST_PASSWORD)

    # Test if the user can be logged out
    response = auth.logout()
    assert response.status_code == 200
    assert current_user.is_anonymous is True


def test_user_page(client, app, auth):
    # Login user
    auth.login(username=TEST_USERNAME,
               password=TEST_PASSWORD)

    # Test if the user page accessible
    response = client.get(f"/user/{TEST_USERNAME}", follow_redirects=True)
    assert b'<h3 class="user-heading heading-line-2">test_user</h3>' in response.data


def test_duplicate_user_registration(client, app, auth):
    # Test if another user with same credentials can be added
    response = auth.register(username=TEST_USERNAME,
                             password=TEST_PASSWORD)
    assert response.status_code == 200
    # Test if user has been redirected due to username already being in use
    assert b"<li>Username already in use. Please choose a new username.</li>" in response.data

    # Test if only 1 user matching that user exists in database
    query = db.session.execute(select(models.User).filter_by(username=TEST_USERNAME)).all()
    assert len(query) == 1
