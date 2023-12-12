import pytest
from flask import url_for, template_rendered
from app import create_app
from app import db
from config import TestingConfig, TestingPostgresConfig


@pytest.fixture(scope="module")
def app():
    """ 
        Main app fixture for pytest.
        Either pass TestingConfig to test on SQlite db,
        or TestingPostgres Config to test on local Postgres db.
        
    """

    app = create_app(config_class=TestingPostgresConfig)
    yield app

    # Teardown
    with app.app_context():
        db.session.close()
        db.drop_all()


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture()
def auth(client):
    return AuthActions(client)


@pytest.fixture()
def campaign(client):
    return CampaignActions(client)


@pytest.fixture()
def event(client):
    return EventActions(client)


@pytest.fixture()
def epoch(client):
    return EpochActions(client)


class AuthActions(object):
    """ Class to facilitate common user auth functions during testing """

    def __init__(self, client):
        self._client = client

    def login(self, username="test_username", password="12345678"):
        return self._client.post("/login", follow_redirects=True, data={
            "username": username,
            "password": password,
        })

    def register(self, email='test@testemail.com', username='test_username', password='12345678'):
        return self._client.post("/register", follow_redirects=True, data={
            "email": email,
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

    def accept_invite(self, campaign_name, campaign_id, message_id):
        url = url_for("membership.accept_invite",
                      campaign_name=campaign_name,
                      campaign_id=campaign_id,
                      message_id=message_id)
        return self._client.get(url, follow_redirects=True)


class CampaignActions(object):
    """ Class to facilitate common campaign actions """

    def __init__(self, client):
        self._client = client

    def create(self, title="Test Campaign", description="Test Description"):
        url = url_for("campaign.create_campaign")
        return self._client.post(url, follow_redirects=True, data={
            "title": title,
            "description": description,
            "date_suffix": "",
            "negative_date_suffix": "",
        })

    def edit(self, campaign_name, campaign_id, new_title="Edited Title", new_description="Edited Description"):
        url = url_for("campaign.edit_campaign",
                      campaign_name=campaign_name,
                      campaign_id=campaign_id)
        return self._client.post(url, follow_redirects=True, data={
            "title": new_title,
            "description": new_description,
        })

    def view(self, campaign_name, campaign_id):
        url = url_for("campaign.show_timeline", campaign_name=campaign_name, campaign_id=campaign_id)
        return self._client.get(url, follow_redirects=True)

    def delete(self, campaign_name, campaign_id, username="test_username", password="12345678"):
        url = url_for("campaign.delete_campaign",
                      campaign_name=campaign_name,
                      campaign_id=campaign_id)
        return self._client.post(url, follow_redirects=True, data={
            "username": username,
            "password": password
        })

    def add_user(self, campaign_name, campaign_id, username, user_id):
        url = url_for("membership.add_user",
                      campaign_name=campaign_name,
                      campaign_id=campaign_id)
        data = {
            "username": username,
            "user_id": user_id,
        }
        return self._client.post(url, data=data, follow_redirects=True)

    def remove_user(self, campaign_name, campaign_id, username, user_id):
        url = url_for("membership.remove_user",
                      campaign_name=campaign_name,
                      campaign_id=campaign_id)
        data = {
            "username": username,
            "user_id": user_id,
        }
        return self._client.post(url, data=data, follow_redirects=True)


class EventActions(object):

    def __init__(self, client):
        self._client = client

    def create(self, campaign_object, data):

        url = url_for("event.add_event",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id)

        return self._client.post(url, data=data, follow_redirects=True)

    def edit(self, campaign_object, event_object, data):

        url = url_for("event.edit_event",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id,
                      event_name=event_object.title,
                      event_id=event_object.id)

        return self._client.post(url, data=data, follow_redirects=True)

    def create_comment(self, campaign_object, event_object, data):

        url = url_for("event.view_event",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id,
                      event_name=event_object.title,
                      event_id=event_object.id)

        return self._client.post(url, data=data, follow_redirects=True)


class EpochActions(object):

    def __init__(self, client):
        self._client = client

    def create(self, campaign_object, data):

        url = url_for("epoch.new_epoch",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id)

        return self._client.post(url, data=data, follow_redirects=True)

    def edit(self, campaign_object, epoch_object, data):

        url = url_for("epoch.edit_epoch",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id,
                      epoch_id=epoch_object.id,
                      epoch_title=epoch_object.title)

        return self._client.post(url, data=data, follow_redirects=True)


@pytest.fixture
def captured_templates(app):
    """ Captures the template and context of the app.
        Pass the fixture to the test function, and the
        templates and contexts can be accessed with:

        template, context = captured_templates[index]
    """

    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
