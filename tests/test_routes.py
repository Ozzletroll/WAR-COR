from sqlalchemy import select
from flask_login import current_user
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash

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

EDITED_EVENT_TITLE = "Edited Event Title"
EDITED_EVENT_DATE = "5127-11-01 07:01:13"
EDITED_EVENT_BELLIGERENTS = "Edited Belligerents"


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
        "confirm_password": TEST_PASSWORD,
    })
    assert response_2.status_code == 200

    # Check that the new user was added to the database
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
    campaign_query = db.session.execute(select(models.Campaign).filter_by(title=TEST_CAMPAIGN_TITLE, id=1)).scalar()
    assert campaign_query.description == TEST_CAMPAIGN_DESCRIPTION
    # Check if redirect to campaign timeline was successful
    assert b"<title>Test Campaign Title</title>" in response.data


def test_add_event(client, app):

    with client.session_transaction() as session:
        session["campaign_id"] = 1

    example_login(client)
    # The id of the campaign is passed as an url parameter
    response_1 = client.get(f"/{TEST_CAMPAIGN_TITLE}/new_event", follow_redirects=True)
    assert response_1.status_code == 200

    response_2 = client.post(f"/{TEST_CAMPAIGN_TITLE}/new_event", follow_redirects=True, data={
        "title": TEST_EVENT_TITLE,
        "type": TEST_EVENT_TYPE,
        "date": TEST_EVENT_DATE,
        "location": TEST_EVENT_LOCATION,
        "belligerents": TEST_EVENT_BELLIGERENTS,
        "body": TEST_EVENT_BODY,
        "result": TEST_EVENT_RESULT,
    })
    assert response_2.status_code == 200
    event_query = db.session.execute(select(models.Event).filter_by(id=1, title=TEST_EVENT_TITLE)).scalar()
    assert event_query.title == TEST_EVENT_TITLE
    assert event_query.date == TEST_EVENT_DATE


def test_show_timeline(client, app):

    with client.session_transaction() as session:
        session["campaign_id"] = 1

    response = client.get(f"/{TEST_CAMPAIGN_TITLE}")
    assert response.status_code == 200
    assert b"<title>Test Campaign Title</title>" in response.data
    assert b"<li>Test Event Title</li>" in response.data


def test_edit_campaign(client, app):

    with client.session_transaction() as session:
        session["campaign_id"] = 1

    example_login(client)
    response_1 = client.post(f"/edit_campaign/{TEST_CAMPAIGN_TITLE}", follow_redirects=True, data={
        "title": "Edited Campaign Title",
        "description": "An edited campaign description.",
    })
    assert response_1.status_code == 200
    campaign_query = db.session.execute(select(models.Campaign).filter_by(id=1)).scalar()
    assert campaign_query.title == "Edited Campaign Title"
    assert campaign_query.description == "An edited campaign description."


def test_edit_event(client, app):

    with client.session_transaction() as session:
        session["campaign_id"] = 1
        session["event_id"] = 1

    example_login(client)
    response_1 = client.get(f"/{TEST_CAMPAIGN_TITLE}/{TEST_EVENT_TITLE}/edit")
    assert response_1.status_code == 200
    response_2 = client.post(f"/{TEST_CAMPAIGN_TITLE}/{TEST_EVENT_TITLE}/edit", follow_redirects=True, data={
        "title": EDITED_EVENT_TITLE,
        "type": TEST_EVENT_TYPE,
        "date": EDITED_EVENT_DATE,
        "location": TEST_EVENT_LOCATION,
        "belligerents": EDITED_EVENT_BELLIGERENTS,
        "body": TEST_EVENT_BODY,
        "result": TEST_EVENT_RESULT,
    })
    event_query = db.session.execute(select(models.Event).filter_by(id=1)).scalar()
    assert event_query.title == EDITED_EVENT_TITLE
    assert event_query.date == EDITED_EVENT_DATE
    assert event_query.belligerents == EDITED_EVENT_BELLIGERENTS


def test_view_event(client, app):

    with client.session_transaction() as session:
        session["event_id"] = 1

    response = client.get(f"/{TEST_CAMPAIGN_TITLE}/{TEST_EVENT_TITLE}")
    assert b"<title>Edited Event Title</title>" in response.data
    assert b"Edited Belligerents" in response.data


def test_add_campaign_users(client, app):
    response_1 = client.post("/register", follow_redirects=True, data={
        "username": "Ozzletroll",
        "password": TEST_PASSWORD,
        "confirm_password": TEST_PASSWORD,
    })

    test_logout(client)

    example_login(client)
    with client.session_transaction() as session:
        session["campaign_id"] = 1

    response_2 = client.get(f"/edit_campaign/{TEST_CAMPAIGN_TITLE}/add_users")
    assert response_2.status_code == 200

    response_3 = client.post(f"/edit_campaign/{TEST_CAMPAIGN_TITLE}/add_users", follow_redirects=True, data={
        "username": "Ozzletroll",
    })
    # Test if the campaign is in the user.campaigns
    campaign_query = db.session.execute(select(models.Campaign).filter_by(id=1)).scalar()
    user_query = db.session.execute(select(models.User).filter_by(username="Ozzletroll")).scalar()
    assert campaign_query in user_query.campaigns


def test_remove_campaign_users(client, app):

    with client.session_transaction() as session:
        session["campaign_id"] = 1

    example_login(client)

    response_1 = client.get(f"/edit_campaign/{TEST_CAMPAIGN_TITLE}/remove_users/Ozzletroll", follow_redirects=True)
    assert response_1.status_code == 200
    campaign_query = db.session.execute(select(models.Campaign).filter_by(id=1)).scalar()
    user_query = db.session.execute(select(models.User).filter_by(username="Ozzletroll")).scalar()
    assert campaign_query not in user_query.campaigns


def test_delete_event(client, app):

    example_login(client)

    with client.session_transaction() as session:
        session["campaign_id"] = 1
        session["event_id"] = 1

    response = client.get(f"/{TEST_CAMPAIGN_TITLE}/{EDITED_EVENT_TITLE}/delete", follow_redirects=True)
    assert response.status_code == 200
    event_query = db.session.execute(select(models.Event).filter_by(id=1)).scalar()
    assert event_query is None


def test_delete_user(client, app):

    # First test without logging in
    response_1 = client.get(f"/user/{TEST_USERNAME}/delete", follow_redirects=True)
    assert response_1.status_code == 401

    example_login(client)
    response_2 = client.post(f"/user/{TEST_USERNAME}/delete", follow_redirects=True, data={
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
    })
    user_query = db.session.execute(select(models.User).filter_by(username=TEST_USERNAME)).scalar()
    assert user_query is None
