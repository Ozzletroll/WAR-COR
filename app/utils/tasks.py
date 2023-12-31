from sqlalchemy import select
from datetime import datetime, timedelta

from app import models
from app import scheduler, db
import os
from mailersend import emails



@scheduler.task("cron", id="1", week="*", day_of_week="mon", hour=3, misfire_grace_time=3600)
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


@scheduler.task('interval', id='2', seconds=10, misfire_grace_time=10)
def job1():

    email = os.environ.get("ADMIN")
    date = datetime.now()

    with scheduler.app.app_context():

        mailer = emails.NewEmail()

        mail_body = {}
        mail_from = {
            "name": "WAR/COR Scheduler Message",
            "email": "no-reply@war-cor.com",
        }
        recipients = [
            {
                "name": "Admin",
                "email": email,
            }
        ]
        reply_to = {
            "name": "Name",
            "email": "reply@domain.com",
        }

        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject("WAR/COR Scheduler Message", mail_body)
        mailer.set_html_content("This is the HTML content", mail_body)
        mailer.set_plaintext_content(f"Triggered at {date}", mail_body)
        mailer.set_reply_to(reply_to, mail_body)


        mailer.send(mail_body)

