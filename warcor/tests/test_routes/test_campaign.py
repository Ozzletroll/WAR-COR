from sqlalchemy import select
from flask import url_for
from warcor.app import db
from warcor import models

TEST_CAMPAIGN_TITLE = "Test Campaign Title"
TEST_CAMPAIGN_DESCRIPTION = "Test Campaign Description"
TEST_PASSWORD = "12345678"


def test_view_campaigns_page(client, auth):

    url = url_for("campaign.campaigns")

    # Test page is inaccessible as anonymous user
    response_1 = client.get(url, follow_redirects=True)
    assert response_1.status_code == 200
    assert b"<li>Please log in to access this page</li>" in response_1.data

    # Create test user and login
    auth.register()
    response_2 = client.get(url, follow_redirects=True)
    assert response_2.status_code == 200
    assert b'<h3 class="campaigns-heading">Campaigns</h3>' in response_2.data
    auth.logout()


def test_create_campaign(client, auth, campaign):

    # Test campaign creation fails when not logged in
    response_1 = campaign.create(title=TEST_CAMPAIGN_TITLE,
                                 description=TEST_CAMPAIGN_DESCRIPTION)
    assert response_1.status_code == 200
    assert b"<li>Please log in to access this page</li>" in response_1.data
    campaign_query = db.session.execute(
        select(models.Campaign)
        .filter_by(title=TEST_CAMPAIGN_TITLE)).scalar()
    assert campaign_query is None

    # Test campaign creation succeeds when logged in
    auth.login()
    response_2 = campaign.create(title=TEST_CAMPAIGN_TITLE,
                                 description=TEST_CAMPAIGN_DESCRIPTION)

    assert response_2.status_code == 200
    campaign_query = db.session.execute(
        select(models.Campaign)
        .filter_by(title=TEST_CAMPAIGN_TITLE)).scalar()
    assert campaign_query is not None

    # Check if redirect to campaign timeline was successful
    string = f"<title>{TEST_CAMPAIGN_TITLE.upper()} | WAR/COR</title>".encode()
    assert string in response_2.data


def test_show_timeline(client, auth, campaign):

    campaign_query = db.session.execute(
        select(models.Campaign)
        .filter_by(title=TEST_CAMPAIGN_TITLE)).scalar()

    # Test if page accessible when logged out
    auth.logout()
    response_1 = campaign.view(campaign_name=TEST_CAMPAIGN_TITLE,
                               campaign_id=campaign_query.id)
    assert response_1.status_code == 200
    string = f"<title>{TEST_CAMPAIGN_TITLE.upper()} | WAR/COR</title>".encode()
    assert string in response_1.data

    # Test if page accessible when logged in
    auth.login()
    response_2 = campaign.view(campaign_name=TEST_CAMPAIGN_TITLE,
                               campaign_id=campaign_query.id)
    assert response_2.status_code == 200
    string = f"<title>{TEST_CAMPAIGN_TITLE.upper()} | WAR/COR</title>".encode()
    assert string in response_2.data


def test_show_timeline_editing_page(client, auth):

    campaign_query = db.session.execute(
        select(models.Campaign)
        .filter_by(title=TEST_CAMPAIGN_TITLE)).scalar()

    url = url_for("campaign.edit_timeline",
                  campaign_name=campaign_query.title,
                  campaign_id=campaign_query.id)

    # Test if access is denied to unauthenticated user
    response_1 = client.get(url, follow_redirects=True)
    assert response_1.status_code == 200
    assert b"<li>Please log in to access this page</li>" in response_1.data

    # Test if access is denied to user without editing permissions
    auth.register(email="testemail2@email.com",
                  username="User_2",
                  password=TEST_PASSWORD)
    response_2 = client.get(url, follow_redirects=True)
    assert response_2.status_code == 403
    auth.logout()

    # Test if original user with correct permissions can access editing page
    auth.login()
    response_3 = client.get(url, follow_redirects=True)
    assert response_3.status_code == 200
    assert b'editPage="true"' in response_3.data


def test_campaign_editing(client, auth, campaign):

    # Test campaign cannot be edited when logged out
    auth.logout()

    campaign_query = db.session.execute(
        select(models.Campaign)
        .filter_by(title=TEST_CAMPAIGN_TITLE)).scalar()

    response_1 = campaign.edit(campaign_name=TEST_CAMPAIGN_TITLE,
                               campaign_id=campaign_query.id,
                               new_title="Edited Title",
                               new_description="Edited Description")
    assert response_1.status_code == 200
    assert b"<li>Please log in to access this page</li>" in response_1.data

    new_campaign_query = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Edited Title")).scalar()

    assert new_campaign_query is None

    # Test campaign cannot be edited if logged in a non-admin user
    auth.register(email="testemail3@email.com",
                  username="User_3",
                  password=TEST_PASSWORD)
    response_2 = campaign.edit(campaign_name=TEST_CAMPAIGN_TITLE,
                               campaign_id=campaign_query.id,
                               new_title="Edited Title",
                               new_description="Edited Description")
    assert response_2.status_code == 403
    edited_campaign_query = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Edited Title")).scalar()
    assert edited_campaign_query is None
    auth.logout()

    # Test campaign can be edited by correctly authenticated admin user
    auth.login()
    response_3 = campaign.edit(campaign_name=TEST_CAMPAIGN_TITLE,
                               campaign_id=campaign_query.id,
                               new_title="Edited Title",
                               new_description="Edited Description")
    assert response_3.status_code == 200
    edited_campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Edited Title")).scalar()
    assert edited_campaign.title == "Edited Title"
    assert edited_campaign.description == "Edited Description"
    auth.logout()


def test_delete_campaign(client, auth, campaign):

    campaign_query = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Edited Title")).scalar()

    url = url_for("campaign.delete_campaign",
                  campaign_name=campaign_query.title,
                  campaign_id=campaign_query.id)

    # Test that unauthenticated user cannot access route
    response_1 = client.get(url, follow_redirects=True)
    assert response_1.status_code == 200
    assert b"<li>Please log in to access this page</li>" in response_1.data

    # Test that authenticated user without editing permissions cannot delete campaign
    auth.login(username="User_2", password=TEST_PASSWORD)
    response_2 = client.get(url, follow_redirects=True)
    assert response_2.status_code == 403
    auth.logout()

    # Test that authenticated user with editing permissions can delete campaign
    auth.login()
    response_3 = campaign.delete(campaign_name=campaign_query.title,
                                 campaign_id=campaign_query.id)
    assert response_3.status_code == 200

    campaign_query = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Edited Title")).scalar()
    assert campaign_query is None
