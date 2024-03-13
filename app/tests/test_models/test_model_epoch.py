from sqlalchemy import select

from app import db, models


def test_setup(client, auth, campaign, event):
    # Create a new campaign and populate it with events
    auth.register()
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    # Create 4 months with 10 events each, incremented by +1 day
    for value in range(1, 5):
        event.mass_create(campaign_object=campaign_object,
                          starting_date=f"5016/0{value}/01 00:00:00",
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
    epoch.update(form, 
                 parent_campaign=campaign_object, 
                 new=True)

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


def test_populate_self(client, auth, epoch):
    auth.login()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    data = {
        "title": "Valid Epoch",
        "start_date": "5016/01/05",
        "end_date": "5016/02/01",
        "description": "An epoch that should contain "
                       "the events found in valid_events",
        "overview": "Overview"
    }
    epoch.create(campaign_object, data)

    epoch_object = db.session.execute(
        select(models.Epoch)
        .filter_by(title="Valid Epoch")).scalar()

    # The test epoch starts on 5016/01/05 and ends on 5016/02/01
    for event in epoch_object.events:
        assert epoch_object.has_events is True
        assert event.date.startswith("5016/01") or event.date.startswith("5016/02")
        if event.date.startswith("5016/01"):
            assert event.day >= epoch_object.start_day
        elif event.date.startswith("5016/02"):
            assert event.day <= epoch_object.end_day
