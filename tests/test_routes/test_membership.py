from sqlalchemy import select
from flask import url_for
from app import db
import models


def test_setup(client, auth):
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


def test_edit_campaign_members(client, auth, campaign):

    # Create test campaign
    auth.login(username="Admin",
               password="123")
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")
    auth.logout()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    url = url_for("membership.edit_campaign_users",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id)

    # Test page is inaccessible as anonymous user
    response_1 = client.get(url, follow_redirects=True)
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>' in response_1.data

    # Test page is inaccessible as user without campaign permissions
    auth.login(username="User 1", password="123")
    response_2 = client.get(url, follow_redirects=True)
    assert response_2.status_code == 403
    auth.logout()

    # Test page is accessible to authenticated user with campaign permissions
    auth.login(username="Admin", password="123")
    response_3 = client.get(url, follow_redirects=True)
    assert response_3.status_code == 200
    assert b'<h3 class="campaigns-heading">Edit Members</h3>' in response_3.data


def test_add_campaign_members(client, auth, campaign):

    admin = db.session.execute(
        select(models.User)
        .filter_by(username="Admin")).scalar()
    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    # Test unauthenticated user cannot add to campaign
    response_1 = campaign.add_user(campaign_name=campaign_object.title,
                                   campaign_id=campaign_object.id,
                                   username="User 1")
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>' in response_1.data

    # Test admin can add user 1 to campaign
    auth.login(username="Admin", password="123")
    response_2 = campaign.add_user(campaign_name=campaign_object.title,
                                   campaign_id=campaign_object.id,
                                   username="User 1")
    assert response_2.status_code == 200

    # Test if pending invitation message created
    pending_invitation = db.session.query(models.Message)\
        .filter(models.Message.invite == 1,
                models.Message.target_campaign_id == campaign_object.id,
                models.Message.target_user_id == user_1.id).scalar()
    assert pending_invitation is not None
    assert user_1.id == pending_invitation.target_user_id
