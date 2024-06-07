from sqlalchemy import select
from werkzeug.datastructures import MultiDict

from app import db, models
from app.forms.forms import CreateEpochForm


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

    # Update the epoch
    epoch_form = CreateEpochForm(
        MultiDict({
            "title": "Updated Epoch",
            "start_date": "5016/01/02",
            "end_date": "5016/02/02",
            "overview": "Updated overview",
            "dynamic_fields-0-title": "Title 1",
            "dynamic_fields-0-value": "Value 1",
            "dynamic_fields-0-is_full_width": False,
            "dynamic_fields-0-field_type": "basic",
            "dynamic_fields-1-title": "Title 2",
            "dynamic_fields-1-value": "Value 2",
            "dynamic_fields-1-is_full_width": False,
            "dynamic_fields-1-field_type": "basic",
            "hide_time": False,
        })).data

    epoch.update(epoch_form,
                 parent_campaign=campaign_object,
                 new=True)

    for field in epoch_form:
        if field == "overview":
            assert getattr(epoch, field) == "<p>Updated overview</p>"
        else:
            assert getattr(epoch, field) == epoch_form[field]


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
