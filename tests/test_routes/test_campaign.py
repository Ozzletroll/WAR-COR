from sqlalchemy import select
from app import db
import models

TEST_CAMPAIGN_TITLE = "Test Campaign Title"
TEST_CAMPAIGN_DESCRIPTION = "Test Campaign Description"


def test_create_campaign(client, app, auth, campaign):

    # Create test user
    auth.register()

    response = campaign.create(title=TEST_CAMPAIGN_TITLE,
                               description=TEST_CAMPAIGN_DESCRIPTION)

    assert response.status_code == 200
    campaign_query = db.session.execute(
        select(models.Campaign)
        .filter_by(title=TEST_CAMPAIGN_TITLE)).scalar()
    assert campaign_query is not None

    # Check if redirect to campaign timeline was successful
    string = f"<title>{TEST_CAMPAIGN_TITLE.upper()} | WAR/COR</title>".encode()
    assert string in response.data


def test_show_timeline(client, app, auth, campaign):

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


def test_campaign_editing(client, app, auth, campaign):

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
    auth.register(username="user_2", password="123")
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
