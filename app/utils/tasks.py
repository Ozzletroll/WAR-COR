from sqlalchemy import select
from datetime import datetime, timedelta

from app import models
from app import scheduler, db
import sys


@scheduler.task("cron", id="1", week="*", day_of_week="mon", hour=3)
def delete_old_messages():

    one_week_ago = datetime.now() - timedelta(days=7)

    with scheduler.app.app_context():

        messages = db.session.execute(
            select(models.Message)
            .filter(models.Message.date < one_week_ago)
            ).scalars()

        for message in messages:
            db.session.delete(message)

        db.session.commit()


@scheduler.task('interval', id='2', seconds=10, misfire_grace_time=900)
def job1():
    print(f'Job executed at {datetime.now}', file=sys.stdout)
