from sqlalchemy import select
import base64
import binascii
from unittest.mock import Mock

from app import db, models


def test_setup(client, auth, campaign):

    auth.register()
    campaign.create(title="Template Test Campaign",
                    description="A campaign for testing purposes")


def test_update(client):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Template Test Campaign")).scalar()

    template = models.Template(name="New Template",
                               parent_campaign=campaign_object,
                               share_code="Test Share Code")

    # Mock the generate_share_code method to return a fixed value
    template.generate_share_code = lambda: "New Share Code"

    db.session.add(template)
    db.session.commit()

    # Update the template, generating new share code
    template.update()
    assert template.share_code == "New Share Code"

    # Create a second template with a duplicate share code,
    # expecting an IntegrityError
    template_2 = models.Template(name="Second Template",
                                 parent_campaign=campaign_object)

    # Create a mock for the generate_share_code method
    mock_generate_share_code = Mock()
    # Set the mock to return "New Share Code" on the first call,
    # and "Unique Share Code" on the second call
    mock_generate_share_code.side_effect = ["New Share Code", "Unique Share Code"]
    template_2.generate_share_code = mock_generate_share_code

    # Call update, assert that the duplicate share code causes it to
    # generate the second value
    template_2.update()
    assert template_2.share_code == "Unique Share Code"


def test_generate_share_code(client):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Template Test Campaign")).scalar()

    template = models.Template(name="Test Template",
                               parent_campaign=campaign_object,
                               share_code="Test Share Code")

    share_code = template.generate_share_code()
    assert len(share_code) == 12

    try:
        base64.urlsafe_b64decode(share_code)
    except binascii.Error:
        assert False
