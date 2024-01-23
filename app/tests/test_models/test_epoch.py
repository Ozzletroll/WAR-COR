from sqlalchemy import select

from app import db, models


def test_setup(client, auth, campaign, event):
    # Create a new campaign and populate it with 10 events
    # beginning at 5016/01/01 00:00:00 and incrementing by +1 day
    auth.register()
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    event.mass_create(campaign_object=campaign_object,
                      number=10,
                      increment="day")


def test_update(client):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    # Create a new epoch
    epoch = models.Epoch()
    epoch.title = "Epoch 1"
    epoch.start_date = "5016/01/01"
    epoch.end_date = "5016/02/01"
    db.session.add(epoch)
    db.session.commit()

    # Update the epoch
    form = {
        "title": "Updated Epoch",
        "start_date": "5016/01/02",
        "end_date": "5016/02/02",
        "description": "Updated description",
        "overview": "Updated overview"
    }
    epoch.update(form, parent_campaign=campaign_object, new=False)

    # Verify the changes
    updated_epoch = db.session.execute(
        select(models.Epoch)
        .filter_by(id=epoch.id)).scalar()

    assert updated_epoch.title == "Updated Epoch"
    assert updated_epoch.start_date == "5016/01/02"
    assert updated_epoch.end_date == "5016/02/02"
    assert updated_epoch.description == "Updated description"
    assert updated_epoch.overview == "Updated overview"


def test_set_url_title():

    # Create a new epoch
    epoch = models.Epoch()
    epoch.title = "Test Epoch"
    epoch.set_url_title()

    # Verify the url_title has been set correctly
    assert epoch.url_title == "Test-Epoch"
