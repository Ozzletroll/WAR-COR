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


def test_add_user(client, auth, campaign):

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
                                   username=user_1.username,
                                   user_id=user_1.id)
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>' in response_1.data

    # Test admin can add user 1 to campaign
    auth.login(username="Admin", password="123")
    response_2 = campaign.add_user(campaign_name=campaign_object.title,
                                   campaign_id=campaign_object.id,
                                   username=user_1.username,
                                   user_id=user_1.id)
    assert response_2.status_code == 200

    # Test if pending invitation message created
    pending_invitation = db.session.query(models.Message)\
        .filter(models.Message.invite == 1,
                models.Message.target_campaign_id == campaign_object.id,
                models.Message.target_user_id == user_1.id).scalar()
    assert pending_invitation is not None
    assert user_1.id == pending_invitation.target_user_id


def test_remove_user(client, auth, campaign):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    # Manually add user_1 to campaign members
    campaign_object.members.append(user_1)
    db.session.commit()

    # Test unauthenticated user cannot remove campaign member
    response_1 = campaign.remove_user(campaign_name=campaign_object.title,
                                      campaign_id=campaign_object.id,
                                      username=user_1.username,
                                      user_id=user_1.id)
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>' in response_1.data

    # Test admin can remove user 1 to campaign
    auth.login(username="Admin", password="123")
    response_2 = campaign.remove_user(campaign_name=campaign_object.title,
                                      campaign_id=campaign_object.id,
                                      username=user_1.username,
                                      user_id=user_1.id)
    assert response_2.status_code == 200
    assert user_1 not in campaign_object.members


def test_join_campaign(client, auth, campaign):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    url = url_for("membership.join_campaign")

    # Test page is inaccessible as anonymous user
    response_1 = client.get(url, follow_redirects=True)
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>' in response_1.data

    # Test page accessible when logged in
    auth.login(username=user_1.username, password="123")
    response_2 = client.get(url, follow_redirects=True)
    assert response_2.status_code == 200
    assert b'<h3 class="campaigns-heading">Join Campaign</h3>' in response_2.data

    # Test if search fails when query less than 3 characters
    data = {
        "search": "aa",
    }
    response_3 = client.post(url, data=data, follow_redirects=True)
    assert response_3.status_code == 200
    assert b'<li>search: Field must be at least 3 characters long.</li>' in response_3.data

    # Test if search returns result when query is 3 or more characters
    data = {
        "search": "Test Campaign",
    }
    response_4 = client.post(url, data=data, follow_redirects=True)
    assert response_4.status_code == 200
    assert b'<h2 id="campaign-1" class="campaign-header">Test Campaign</h2>' in response_4.data

    # Test if search returns no results if query matches no campaign in database
    data = {
        "search": "Really Long Query That Will Return No Results",
    }
    response_5 = client.post(url, data=data, follow_redirects=True)
    assert response_5.status_code == 200
    assert b'<li>No campaigns matching query found</li>' in response_5.data


def test_request_membership(client, auth, campaign):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    url = url_for("membership.request_membership",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id)

    # Test if request fails if not authenticated
    response_1 = client.post(url, follow_redirects=True)
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>' in response_1.data

    # Test if user can request membership to campaign
    auth.login(username=user_1.username, password="123")
    response_2 = client.post(url, follow_redirects=True)
    assert response_2.status_code == 200

    # Test if membership request message created
    pending_request = db.session.query(models.Message) \
        .filter(models.Message.request == 1,
                models.Message.target_campaign_id == campaign_object.id,
                models.Message.target_user_id == user_1.id).scalar()
    assert pending_request is not None
    assert user_1.id == pending_request.target_user_id


def test_accept_invite(client, auth, campaign):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    user_2 = db.session.execute(
        select(models.User)
        .filter_by(username="User 2")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    pending_invitation = db.session.query(models.Message) \
        .filter(models.Message.invite == 1,
                models.Message.target_campaign_id == campaign_object.id,
                models.Message.target_user_id == user_1.id).scalar()

    url = url_for("membership.accept_invite")
    data = {
        "message_id": pending_invitation.id,
        "campaign_id": campaign_object.id,
    }

    # Test if accepting invite fails if not authenticated
    response_1 = client.post(url, data=data, follow_redirects=True)
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>' in response_1.data

    # Test if accepting invite fails if logged in as non-target user
    auth.login(username=user_2.username, password="123")
    response_2 = client.post(url, data=data, follow_redirects=True)
    assert response_2.status_code == 403
    auth.logout()

    # Test if accepting invite succeeds when logged in as correct target user
    auth.login(username=user_1.username, password="123")
    response_3 = client.post(url, data=data, follow_redirects=True)
    assert response_3.status_code == 200
    assert user_1 in campaign_object.members
