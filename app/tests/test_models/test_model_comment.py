from sqlalchemy import select
from werkzeug.datastructures import MultiDict

from app.forms.forms import CreateEventForm
from app import db, models


def test_setup(auth, client, campaign, event):

    auth.register()
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    event_form = CreateEventForm(
        MultiDict({
            "type": "Test",
            "title": "Event 1",
            "year": 5016,
            "month": 1,
            "day": 1,
            "hour": 9,
            "minute": 0,
            "second": 0,
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

    event.create(campaign_object, data=event_form)


def test_update(auth, client, event):

    auth.login()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    user = db.session.execute(
        select(models.User)
        .filter_by(username="test_username")).scalar()

    event_object = db.session.execute(
        select(models.Event)
        .filter_by(title="Event 1")).scalar()

    event.create_comment(campaign_object=campaign_object,
                         event_object=event_object,
                         data={"body": "Comment text goes here"})

    comment = db.session.execute(
        select(models.Comment)
        .filter_by(body="<p>Comment text goes here</p>")).scalar()

    form = {"body": "Updated comment text"}
    comment.update(form=form,
                   parent_event=event_object,
                   author=user)

    assert comment.body == "<p>Updated comment text</p>"
