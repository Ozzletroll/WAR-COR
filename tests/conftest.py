import pytest
from flask import url_for
from app import create_app
from app import db


@pytest.fixture(scope="package")
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


@pytest.fixture()
def campaign(client):
    return CampaignActions(client)


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


class CampaignActions(object):
    """ Class to facilitate common campaign actions """

    def __init__(self, client):
        self._client = client

    def create(self, title="Test Campaign", description="Test Description"):
        return self._client.post("/campaigns/create_campaign", follow_redirects=True, data={
            "title": title,
            "description": description,
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

    def delete(self, campaign_name, campaign_id, username="test", password="test"):
        url = url_for("campaign.delete_campaign",
                      campaign_name=campaign_name,
                      campaign_id=campaign_id)
        return self._client.post(url, follow_redirects=True, data={
            "username": username,
            "password": password
        })

    def add_user(self, campaign_name, campaign_id, username):
        url = url_for("membership.add_user",
                      campaign_name=campaign_name,
                      campaign_id=campaign_id,
                      username=username)
        return self._client.get(url, follow_redirects=True)
