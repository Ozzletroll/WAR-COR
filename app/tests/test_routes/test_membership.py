from sqlalchemy import select
from flask import url_for
from app import db
from app import models

TEST_PASSWORD = "12345678"


def test_setup(client, auth):
    # Create test users
    auth.register(email="testemail1@email.com",
                  username="Admin",
                  password=TEST_PASSWORD)
    auth.logout()
    auth.register(email="testemail2@email.com",
                  username="User 1",
                  password=TEST_PASSWORD)
    auth.logout()
    auth.register(email="testemail3@email.com",
                  username="User 2",
                  password=TEST_PASSWORD)
    auth.logout()


def test_edit_campaign_members(client, auth, campaign):

    # Create test campaign
    auth.login(username="Admin",
               password=TEST_PASSWORD)
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")
    auth.logout()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    campaign_object.accepting_applications = True
    db.session.commit()

    url = url_for("membership.edit_campaign_users",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id)

    # Test page is inaccessible as anonymous user
    response_1 = client.get(url, follow_redirects=True)
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>' in response_1.data

    # Test page is inaccessible as user without campaign permissions
    auth.login(username="User 1", password=TEST_PASSWORD)
    response_2 = client.get(url, follow_redirects=True)
    assert response_2.status_code == 403
    auth.logout()

    # Test page is accessible to authenticated user with campaign permissions
    auth.login(username="Admin", password=TEST_PASSWORD)
    response_3 = client.get(url, follow_redirects=True)
    assert response_3.status_code == 200
    assert b'<h3 class="campaigns-heading">Edit Members</h3>' in response_3.data


def test_add_user(client, auth, campaign):

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
    auth.login(username="Admin", password=TEST_PASSWORD)
    response_2 = campaign.add_user(campaign_name=campaign_object.title,
                                   campaign_id=campaign_object.id,
                                   username=user_1.username,
                                   user_id=user_1.id)
    assert response_2.status_code == 200

    # Test if pending invitation message created
    pending_invitation = db.session.query(models.Message)\
        .filter(models.Message.invite == True,
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

    # Test admin can remove user 1 from campaign
    auth.login(username="Admin", password=TEST_PASSWORD)
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
    auth.login(username=user_1.username, password=TEST_PASSWORD)
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


def test_leave_campaign(client, auth, campaign):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    # Manually add user_1 to campaign members
    campaign_object.members.append(user_1)
    db.session.commit()

    assert user_1 in campaign_object.members

    auth.login(username=user_1.username,
               password=TEST_PASSWORD)

    url = url_for("membership.leave_campaign",
                  campaign_name=campaign_object.url_title,
                  campaign_id=campaign_object.id)

    form = {
        "username": user_1.username,
        "user_id": user_1.id,
    }

    response = client.post(url, data=form, follow_redirects=True)
    assert response.status_code == 200
    assert user_1 not in campaign_object.members


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
    auth.login(username=user_1.username, password=TEST_PASSWORD)
    response_2 = client.post(url, follow_redirects=True)
    assert response_2.status_code == 200

    # Test if membership request message created
    pending_request = db.session.query(models.Message) \
        .filter(models.Message.request == True,
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
        .filter(models.Message.invite == True,
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
    auth.login(username=user_2.username, password=TEST_PASSWORD)
    response_2 = client.post(url, data=data, follow_redirects=True)
    assert response_2.status_code == 403
    auth.logout()

    # Test if accepting invite succeeds when logged in as correct target user
    auth.login(username=user_1.username, password=TEST_PASSWORD)
    response_3 = client.post(url, data=data, follow_redirects=True)
    assert response_3.status_code == 200
    assert user_1 in campaign_object.members


def test_decline_invite(client, auth, campaign):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    user_2 = db.session.execute(
        select(models.User)
        .filter_by(username="User 2")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    # Create pending campaign invitation for user_2
    auth.login(username="Admin", password=TEST_PASSWORD)
    campaign.add_user(campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id,
                      username=user_2.username,
                      user_id=user_2.id)

    pending_invitation = db.session.query(models.Message) \
        .filter(models.Message.invite == True,
                models.Message.target_campaign_id == campaign_object.id,
                models.Message.target_user_id == user_2.id).scalar()

    auth.logout()

    url = url_for("membership.decline_invite")
    data = {
        "message_id": pending_invitation.id,
        "campaign_id": campaign_object.id,
    }

    # Test that declining invite fails if user is not authenticated
    response_1 = client.post(url, data=data, follow_redirects=True)
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>'

    # Test that declining invite fails if user is not the messages target user
    auth.login(username=user_1.username, password=TEST_PASSWORD)
    response_2 = client.post(url, data=data, follow_redirects=True)
    assert response_2.status_code == 403
    auth.logout()

    # Test that declining the invite succeeds if logged in as target user
    auth.login(username=user_2.username, password=TEST_PASSWORD)
    response_3 = client.post(url, data=data)
    assert response_3.status_code == 200

    pending_invitation = db.session.query(models.Message) \
        .filter(models.Message.invite == True,
                models.Message.target_campaign_id == campaign_object.id,
                models.Message.target_user_id == user_2.id).scalar()

    assert user_2 not in campaign_object.members
    assert pending_invitation is None


def test_confirm_request(client, auth, campaign):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    user_2 = db.session.execute(
        select(models.User)
        .filter_by(username="User 2")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    create_request_url = url_for("membership.request_membership",
                                 campaign_name=campaign_object.title,
                                 campaign_id=campaign_object.id)

    # Create membership request for user_2
    auth.login(username=user_2.username, password=TEST_PASSWORD)
    client.post(create_request_url)

    pending_request = db.session.query(models.Message) \
        .filter(models.Message.request == True,
                models.Message.target_campaign_id == campaign_object.id,
                models.Message.target_user_id == user_2.id).scalar()

    auth.logout()

    # Test that non-admin user cannot accept request
    auth.login(username=user_1.username, password=TEST_PASSWORD)

    url = url_for("membership.confirm_request")
    data = {
        "campaign_id": campaign_object.id,
        "message_id": pending_request.id,
    }

    response_1 = client.post(url, data=data, follow_redirects=True)
    assert response_1.status_code == 403
    auth.logout()

    # Test that admin can confirm request
    auth.login(username="Admin", password=TEST_PASSWORD)
    response_2 = client.post(url, data=data)
    assert response_2.status_code == 302
    assert user_2 in campaign_object.members


def test_deny_request(client, auth, campaign):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    user_2 = db.session.execute(
        select(models.User)
        .filter_by(username="User 2")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    # Remove user_2 from campaign
    campaign_object.members.remove(user_2)

    create_request_url = url_for("membership.request_membership",
                                 campaign_name=campaign_object.title,
                                 campaign_id=campaign_object.id)

    # Create new membership request for user_2
    auth.login(username=user_2.username, password=TEST_PASSWORD)
    client.post(create_request_url)

    pending_request = db.session.query(models.Message) \
        .filter(models.Message.request == True,
                models.Message.target_campaign_id == campaign_object.id,
                models.Message.target_user_id == user_2.id).scalar()

    auth.logout()

    url = url_for("membership.deny_request")
    data = {
        "campaign_id": campaign_object.id,
        "message_id": pending_request.id,
    }

    # Test that non-admin user cannot deny request
    auth.login(username=user_1.username, password=TEST_PASSWORD)
    response_1 = client.post(url, data=data, follow_redirects=True)
    assert response_1.status_code == 403
    assert pending_request is not None
    auth.logout()

    # Test that admin can deny request
    auth.login(username="Admin", password=TEST_PASSWORD)
    response_2 = client.post(url, data=data)
    assert response_2.status_code == 200
    assert user_2 not in campaign_object.members

    pending_request = db.session.query(models.Message) \
        .filter(models.Message.request == True,
                models.Message.target_campaign_id == campaign_object.id,
                models.Message.target_user_id == user_2.id).scalar()

    assert pending_request is None


def test_add_permission(client, auth, campaign):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    user_2 = db.session.execute(
        select(models.User)
        .filter_by(username="User 2")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    # Add new user as member (user_1 is already a member from earlier test in module)
    campaign_object.members.append(user_2)
    db.session.commit()

    url = url_for("membership.add_permission",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id)
    data = {
        "username": user_2.username,
        "user_id": user_2.id,
    }

    # Test if non-admin user can add permission
    auth.login(username=user_1.username, password=TEST_PASSWORD)
    response_1 = client.post(url, data=data, follow_redirects=True)
    assert response_1.status_code == 403
    assert user_2 not in campaign_object.admins
    auth.logout()

    # Test if admin can grant editing permission
    auth.login(username="Admin", password=TEST_PASSWORD)
    response_1 = client.post(url, data=data, follow_redirects=True)
    assert response_1.status_code == 200
    assert user_2 in campaign_object.admins
