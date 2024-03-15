from sqlalchemy import select
from app import db, models, scheduler
from datetime import datetime, timedelta
from app.utils.tasks import delete_old_messages


def test_delete_old_messages(client, auth, campaign):

    # Test that job is correctly added to job store
    assert scheduler.get_job("weekly_message_delete")

    # Test that job correctly deletes events older than a week
    auth.register(email="testemail1@email.com",
                  username="Admin",
                  password="12345678")
    campaign.create(title="Test Campaign",
                    description="Test campaign for task test")
    auth.logout()
    auth.register(email="testemail2@email.com",
                  username="User 1",
                  password="12345678")
    auth.logout()

    campaign_query = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    sender = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    recipient = db.session.execute(
        select(models.User)
        .filter_by(username="User 2")).scalar()

    one_week_ago = datetime.now() - timedelta(days=7, minutes=1)

    message_1 = models.Message()
    message_1.author = sender
    message_1.invite = True
    message_1.body = "Message older than 1 week"
    message_1.target_user = recipient
    message_1.target_campaign = campaign_query
    message_1.date = one_week_ago

    message_2 = models.Message()
    message_2.author = sender
    message_2.invite = True
    message_2.body = "Message not older than 1 week"
    message_2.target_user = recipient
    message_2.target_campaign = campaign_query
    message_2.date = datetime.now()

    db.session.add(message_1)
    db.session.add(message_2)
    db.session.commit()

    delete_old_messages()

    message_1_query = (db.session.execute(
                       select(models.Message)
                       .filter_by(body="Message older than 1 week"))
                       .scalar())

    message_2_query = (db.session.execute(
                       select(models.Message)
                       .filter_by(body="Message not older than 1 week"))
                       .scalar())

    assert message_1_query is None
    assert message_2_query
