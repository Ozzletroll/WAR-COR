from sqlalchemy import select
from flask import url_for
from app import db
import models


def test_setup(client, auth, campaign):
    # Create test users
    auth.register(username="Admin",
                  password="123")
    auth.logout()
    auth.register(username="User 1",
                  password="123")
    auth.logout()
    auth.register(username="User 2",
                  password="123")
    auth.logout()

    # Create test campaign and add user_1 as member
    auth.login(username="Admin", password="123")
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    campaign_object.members.append(user_1)
    db.session.commit()


def test_add_event(client, auth, campaign, event):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    event_data = {
        "type": "Test",
        "title": "Test Event",
        "date": "5016/01/01 09:00:00",
        "location": "Test Location",
        "belligerents": "Belligerent 1, Belligerent 2",
        "body": "Test Body Text",
        "result": "Test Result",
        "header": False,
        "hide_time": False,
    }

    url = url_for("event.add_event",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id)

    # Test that page is not reachable when unauthenticated
    response_1 = client.get(url, follow_redirects=True)
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>' in response_1.data

    # Test that post request fails if logged in as non admin user
    auth.login(username=user_1.username, password="123")
    response_2 = event.create(campaign_object=campaign_object, data=event_data)
    assert response_2.status_code == 403
    auth.logout()

    # Test that event can be created when logged in as campaign admin
    auth.login(username="Admin", password="123")
    response_3 = event.create(campaign_object=campaign_object, data=event_data)
    assert response_3.status_code == 200

    event_object = db.session.execute(
        select(models.Event)
        .filter_by(title="Test Event")).scalar()

    assert event_object in campaign_object.events
    assert event_object.belligerents == "Belligerent 1, Belligerent 2"


def test_view_event(client, auth, campaign):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    event_object = db.session.execute(
        select(models.Event)
        .filter_by(title="Test Event")).scalar()

    url = url_for("event.view_event",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id,
                  event_name=event_object.title,
                  event_id=event_object.id)

    # Test if event route is reachable
    response = client.get(url)
    assert response.status_code == 200
    