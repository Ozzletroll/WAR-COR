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
        "system": "Lancer",
        "image_url": "https://massifpress.com/_next/image?url=%2Fimages%2Flancer%2Flancer-carousel.webp&w=1920&q=75"
    }

    campaign_object.update(form=form_data)

    for field in form_data.keys():
        assert form_data[field] in getattr(campaign_object, field)


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


def test_set_url_title():

    campaign = models.Campaign()
    campaign.title = "Test Campaign Title"

    campaign.set_url_title()
    assert campaign.url_title == "Test-Campaign-Title"


def test_return_timeline_data(client, auth, campaign, event, epoch):

    auth.login()
    campaign.create(title="Timeline Test Campaign",
                    description="For use in testing campaign.return_timeline_data")

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Timeline Test Campaign")).scalar()

    # Year 5016
    # Create 10 event in months "01", "02", "03", "04"
    for value in range(1, 5):
        event.mass_create(campaign_object=campaign_object,
                          starting_date=f"5016/0{value}/01 00:00:00",
                          number=10,
                          increment="day")

    # Year 5017
    # Create 10 event in months "01", "02", "03", "04"
    for value in range(1, 5):
        event.mass_create(campaign_object=campaign_object,
                          starting_date=f"5017/0{value}/01 00:00:00",
                          number=10,
                          increment="day")

    epoch_data = {
        "title": "Epoch Title",
        "start_date": "5016/01/05",
        "end_date": "5016/02/01",
        "description": "A test epoch",
        "overview": "A test epoch"
    }
    epoch.create(campaign_object, data=epoch_data)

    timeline_data = campaign_object.return_timeline_data()

    # Check if all years were correctly returned
    years = [year.name for year in timeline_data]
    assert "5016" in years and "5017" in years
    assert len(years) == 2

    # Check if all months were correctly returned
    for year in timeline_data:
        assert len(year.months) == 4
        # Check days within month
        for index, month in enumerate(year.months):
            target_months = ["01", "02", "03", "04"]
            assert month.name == target_months[index]

            # Check concurrent months have been flagged
            if index != len(year.months) - 1:
                assert month.has_following_month
            else:
                assert not month.has_following_month

            for day_index, day in enumerate(month.days):

                # Check concurrent days have been flagged
                if day_index != len(month.days) - 1:
                    assert day.has_following_day
                else:
                    assert not day.has_following_day

                # Check that there is one event in each day
                assert len(day.events) == 1

                # Check that epoch properties have been correctly applied
                if year.name == "5016":
                    if month.name == "01" and day.name == "05":
                        assert day.has_epoch
                        assert day.epoch_has_events
                    else:
                        assert not day.has_epoch

                    if month.name == "02" and day.name == "01":
                        assert day.has_epoch_end
                    else:
                        assert not day.has_epoch_end


