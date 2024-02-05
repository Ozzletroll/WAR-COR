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
