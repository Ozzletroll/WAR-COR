from sqlalchemy import select

from app import db, models


def test_setup(client, auth, campaign, event):
    # Create a new campaign and populate it with events
    auth.register()
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")


def test_update(client):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    event = models.Event()
    event_form = {
        "type": "Test",
        "title": "Test Event",
        "date": "5016/01/01 09:00:00",
        "location": "Location",
        "belligerents": "Belligerent 1, Belligerent 2",
        "body": "Test Body Text",
        "result": "Test Result",
        "header": False,
        "hide_time": False,
    }
    event.update(form=event_form,
                 parent_campaign=campaign_object,
                 new=True)

    for field in event_form.keys():
        assert getattr(event, field) == event_form[field]


def test_create_blank(client):

    event = models.Event()
    event.create_blank(datestring="5016/01/01 12:00:00")

    assert event.title == ""
    assert event.type == ""
    assert event.body == ""
    assert event.date == "5016/01/01 12:00:00"


def test_split_date(client):

    event = models.Event()
    event.split_date(datestring="5016/01/01 12:00:00")

    assert event.year == 5016
    assert event.month == 1
    assert event.day == 1
    assert event.hour == 12
    assert event.minute == 0
    assert event.second == 0
