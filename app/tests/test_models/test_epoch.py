from sqlalchemy import select

from app import db, models


def test_epoch(client, auth, campaign, event, epoch):

    auth.register()
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()
