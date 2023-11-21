from flask import url_for
from sqlalchemy import select
from flask_login import current_user
import werkzeug
from werkzeug.security import generate_password_hash

from app import models
from app import db

TEST_USERNAME = "test_user"
TEST_PASSWORD = "12345678"


def test_register(client, app, auth):
    # Test if a new user can be added
    response = auth.register(email="testemail1@email.com",
                             username=TEST_USERNAME,
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
    response = auth.register(email="testemail2@email.com",
                             username=TEST_USERNAME,
                             password=TEST_PASSWORD)
    assert response.status_code == 200
    # Test if user has been redirected due to username already being in use
    assert b"<li>Username already in use. Please choose a new username.</li>" in response.data

    # Test if only 1 user matching that user exists in database
    query = db.session.execute(select(models.User).filter_by(username=TEST_USERNAME)).all()
    assert len(query) == 1


def test_delete_user(client, app, auth):
    new_username = "Delete Me"
    new_password = TEST_PASSWORD

    response_1 = auth.register(email="testemail3@email.com",
                               username=new_username,
                               password=new_password)
    assert response_1.status_code == 200

    query = db.session.execute(select(models.User).filter_by(username=new_username)).scalar()
    assert query is not None

    # Test if incorrect username fails
    auth.login(username=new_username, password=new_password)
    response_2 = auth.delete(username=new_username,
                             given_username="Incorrect Username",
                             given_password=new_password)
    assert response_2.status_code == 200
    assert b"<li>Authentication failed. Incorrect username.</li>" in response_2.data

    # Test if incorrect password fails
    response_3 = auth.delete(username=new_username,
                             given_username=new_username,
                             given_password="Incorrect Password")
    assert response_3.status_code == 200
    assert b"<li>Authentication failed. Incorrect password.</li>" in response_3.data

    # Test if user can be deleted if logged in as another user
    auth.logout()
    auth.login(username=TEST_USERNAME,
               password=TEST_PASSWORD)
    response_4 = auth.delete(username=new_username,
                             given_username=new_username,
                             given_password=new_password)
    assert response_4.status_code == 403
    query_2 = db.session.execute(select(models.User).filter_by(username=new_username)).scalar()
    assert query_2 is not None

    # Test if correct credentials lead to user deletion
    auth.logout()
    auth.login(username=new_username,
               password=new_password)
    response_5 = auth.delete(username=new_username,
                             given_username=new_username,
                             given_password=new_password)
    assert response_5.status_code == 200
    query_3 = db.session.execute(select(models.User).filter_by(username=new_username)).scalar()
    assert query_3 is None


def test_update_callsign(client, auth, campaign):

    auth.register(email="testemail4@email.com",
                  username="New User",
                  password=TEST_PASSWORD)

    # Create test campaign to change callsign for
    campaign.create("Callsign Change Test",
                    description="A campaign to test user callsigns")

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Callsign Change Test")).scalar()

    url = url_for("user.update_callsign",
                  username=current_user.username,
                  user_id=current_user.id,
                  campaign_id=campaign_object.id)
    data = {
        "callsign": "NEW CALLSIGN",
    }

    # Test callsign can be updated
    response = client.post(url, data=data)
    assert response.status_code == 302

    user_campaign_association = [entry for entry in current_user.campaign_associations
                                 if entry.campaign_id == campaign_object.id]
    assert user_campaign_association[0].callsign == "NEW CALLSIGN"


def test_change_username(client, auth):

    auth.register(email="testemail5@email.com",
                  username="Username_1",
                  password=TEST_PASSWORD)
    auth.logout()
    auth.register(email="testemail6@email.com",
                  username="Username_2",
                  password=TEST_PASSWORD)

    url = url_for("user.change_username", username=current_user.username)

    # Test that username change fails if existing username is given
    data = {
        "username": "Username_1"
    }
    response_1 = client.post(url, data=data, follow_redirects=True)
    assert response_1.status_code == 200
    assert b'Username already in use, please choose another' in response_1.data
    assert current_user.username == "Username_2"

    # Test that username change fails if proposed username is less than 3 characters
    data = {
        "username": "a"
    }
    response_2 = client.post(url, data=data, follow_redirects=True)
    assert response_2.status_code == 200
    assert b'New username must be 3 or more characters' in response_2.data

    # Test that username change succeeds if unique username given
    data = {
        "username": "New_Username"
    }
    response_3 = client.post(url, data=data, follow_redirects=True)
    assert response_3.status_code == 200
    assert current_user.username == "New_Username"


def test_change_password(client, auth):

    auth.login(username="Username_1", password=TEST_PASSWORD)

    url = url_for("user.change_password", username=current_user.username)

    # Test password change fails if incorrect old password given
    data = {
        "old_password": "An Incorrect Password",
        "new_password": "New Password",
        "confirm_password": "New Password"
    }
    response_1 = client.post(url, data=data, follow_redirects=True)
    assert response_1.status_code == 200
    assert b'Incorrect password' in response_1.data

    # Test password change succeeds when correct authentication given
    data = {
        "old_password": TEST_PASSWORD,
        "new_password": "New Password",
        "confirm_password": "New Password"
    }
    response_2 = client.post(url, data=data, follow_redirects=True)
    assert response_2.status_code == 200
    assert b'Password updated' in response_2.data

    # Check user can log in with new details
    auth.logout()
    auth.login(username="Username_1", password="New Password")
    assert current_user.is_authenticated
    assert current_user.username == "Username_1"
