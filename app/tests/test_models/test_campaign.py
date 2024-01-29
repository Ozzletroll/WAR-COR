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

    # Create 2 months with 5 events each, incremented by +1 day
    for value in range(1, 3):
        event.mass_create(campaign_object=campaign_object,
                          starting_date=f"5016/0{value}/01 00:00:00",
                          number=5,
                          increment="day")


def test_update(client):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    form_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "date_suffix": "ACE",
        "negative_date_suffix": "BCE",
    }

    campaign_object.update(form=form_data)

    for field in form_data.keys():
        assert getattr(campaign_object, field) == form_data[field]
