from sqlalchemy import select

from app import db, models


def test_setup(auth, client, campaign, event):

    auth.register()
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    event_data = {
        "title": "Event 1",
        "body": "Description",
        "date": "5016/02/15 09:00:00",
        "type": "Test",
    }

    event.create(campaign_object, data=event_data)


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
        .filter_by(body="Comment text goes here")).scalar()

    form = {"body": "Updated comment text"}
    comment.update(form=form,
                   parent_event=event_object,
                   author=user)

    assert comment.body == "Updated comment text"
