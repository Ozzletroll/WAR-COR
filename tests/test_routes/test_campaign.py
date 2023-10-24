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
    string = f"<title>{TEST_CAMPAIGN_TITLE.upper()} | WAR/COR</title>".encode()
    assert string in response_1.data

    # Test if page accessible when logged in
    auth.login()
    response_2 = campaign.view(campaign_name=TEST_CAMPAIGN_TITLE,
                               campaign_id=campaign_query.id)
    string = f"<title>{TEST_CAMPAIGN_TITLE.upper()} | WAR/COR</title>".encode()
    assert string in response_2.data
