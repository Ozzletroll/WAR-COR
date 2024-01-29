from sqlalchemy import select
from unittest.mock import MagicMock


from app import db, models


def test_setup(client, auth, campaign, event, epoch):
    # Create a new campaign and populate it with events
    auth.register()
    campaign.create(title="Model Test Campaign",
                    description="A campaign for testing purposes")


def test_update(client):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Model Test Campaign")).scalar()

    form_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "date_suffix": "ACE",
        "negative_date_suffix": "BCE",
    }

    campaign_object.update(form=form_data)

    for field in form_data.keys():
        assert getattr(campaign_object, field) == form_data[field]


def test_check_epochs(client):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Updated Title")).scalar()

    epoch = MagicMock(spec=models.Epoch)
    epoch._sa_instance_state = MagicMock()
    campaign.epochs.append(epoch)
    epoch.populate_self = MagicMock()

    campaign.check_epochs()
    epoch.populate_self.assert_called_once()


def test_get_following_events(client):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Updated Title")).scalar()

    # Create test events
    event_1 = models.Event()
    data_1 = {
        "title": "Event 1",
        "body": "Description",
        "date": "5016/02/15 09:00:00",
        "type": "Test",
    }
    event_1.update(data_1, campaign, new=True)

    event_2 = models.Event()
    data_2 = {
        "title": "Event 2",
        "body": "Description",
        "date": "5016/05/21 14:30:00",
        "type": "Test",
    }
    event_2.update(data_2, campaign, new=True)

    campaign.get_following_events()

    assert event_1.following_event is event_2
    assert event_1.preceding_event is None

    assert event_2.following_event is None
    assert event_2.preceding_event is event_1
