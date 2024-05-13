from flask import url_for
from datetime import datetime
from sqlalchemy import select
from mailersend import emails

from app.utils.sanitisers import sanitise_input
from app import models
from app import db



def send_invite_message(sender, recipient, campaign):
    """ Function for creating and 'sending' a campaign invitation message.
    Messages are stored in the database, and accessed via the user.messages
    association. Takes a user object for both sender and recipient, and
    a campaign object."""

    # Check for existing pending invite
    message = (db.session.execute(select(models.Message)
               .filter(models.Message.target_campaign.has(id=campaign.id))
               .filter(models.Message.target_user.has(id=recipient.id))
               .filter(models.Message.invite == True))
               .scalar())

    # If invitation message already exists, update date
    # to push to top of notifications list
    if message:
        message.date = datetime.now()
        db.session.commit()

    # Otherwise, create a new message
    else:
        message_text = f"<strong>{sender.username}</strong> has invited you to the campaign <strong>{campaign.title}</strong>"

        message = models.Message()

        message.author = sender
        message.invite = True
        message.body = sanitise_input(message_text, wrap=False)
        message.target_user = recipient
        message.target_campaign = campaign
        message.date = datetime.now()

        # Add message to user's message list
        db.session.add(message)
        recipient.messages.append(message)
        sender.sent_messages.append(message)
        db.session.commit()


def send_membership_request(sender, recipients, campaign):
    """Function for creating and 'sending' a campaign membership request message.
    Messages are stored in the database, and accessed via the user.messages
    association. Takes a user object for  sender, a list of admin users for recipients,
    and a campaign object."""

    # Get body values here rather than in f string to avoid SAWarning from autoflush process
    sender_username = sender.username
    campaign_title = campaign.title

    # Check for existing pending request
    message = (db.session.execute(select(models.Message)
               .filter(models.Message.target_campaign.has(id=campaign.id))
               .filter(models.Message.author.has(id=sender.id))
               .filter(models.Message.request == True))
               .scalar())

    # If invitation message already exists, update date
    # to push to top of notifications list
    if message:
        message.date = datetime.now()
        db.session.commit()

    # Otherwise, create a new message
    else:
        message_text = f"<strong>{sender_username}</strong> has requested to join the campaign <strong>{campaign_title}<strong>"

        message = models.Message()

        message.author = sender
        message.request = True
        message.body = sanitise_input(message_text, wrap=False)
        message.target_user = sender
        message.target_campaign = campaign
        message.date = datetime.now()

        db.session.add(message)

        # Add message to user's message list
        for user in recipients:
            user.messages.append(message)

        sender.sent_messages.append(message)
        db.session.commit()


def send_new_member_notification(sender, recipients, campaign, new_user_username):
    """Function called to create a new member notification"""

    # Get body values here rather than in f string to avoid SAWarning from autoflush process
    campaign_title = campaign.title
    message_text = f"<strong>{new_user_username}</strong> has joined the campaign <strong>{campaign_title}</strong>"

    message = models.Message()

    message.author = sender
    message.notification = True
    message.body = sanitise_input(message_text, wrap=False)
    message.target_campaign = campaign
    message.date = datetime.now()

    db.session.add(message)

    for user in recipients:
        user.messages.append(message)

    db.session.commit()


def send_event_notification(sender, recipients, campaign, event):
    """Function for creating new event notifications. Takes a user model object as sender, and
    a list of user model objects as recipients, along with a campaign object, and an event object."""

    # Get body values here rather than in f string to avoid SAWarning from autoflush process
    campaign_title = campaign.title
    event_title = event.title
    message_text = f"The campaign <strong>{campaign_title}</strong> has been updated with the new event <strong>{event_title}</strong>"

    message = models.Message()

    message.author = sender
    message.notification = True
    message.body = sanitise_input(message_text, wrap=False)
    message.target_campaign = campaign
    message.target_event = event
    message.date = datetime.now()

    db.session.add(message)

    for user in recipients:
        user.messages.append(message)

    db.session.commit()


def send_comment_notification(sender, recipients, campaign, event):
    """Function for creating new comment notifications. Creates a new message object
    if no message for the specific campaign and event exists, otherwise creates a new one.
    Message is added to all recipients messages list."""

    def format_message(message):
        message_text = f"New comments for event <strong>{event_title}</strong> in campaign <strong>{campaign_title}</strong>"
        message.author = sender
        message.notification = True
        message.body = sanitise_input(message_text, wrap=False)
        message.target_campaign = campaign
        message.target_event = event
        message.date = datetime.now()

        # Add message to all recipients messages list, unless they are already a recipient
        for user in recipients:
            if message not in user.messages and user.id != sender.id:
                user.messages.append(message)

    # Get body values here rather than in f string to avoid SAWarning from autoflush process
    event_title = event.title
    campaign_title = campaign.title

    # Check for existing comment messages
    messages = (db.session.execute(select(models.Message)
                .filter(models.Message.target_campaign.has(id=campaign.id))
                .filter(models.Message.target_event.has(id=event.id))
                .filter(models.Message.notification == True))
                .scalars())

    # Convert the query result to a list to avoid ResourceClosedError
    messages_list = list(messages)

    if len(messages_list) > 0:
        for message in messages_list:
            format_message(message)

    else:
        # Create new comment message, unless only recipient 
        # would be the original comment author
        if len(recipients) == 1 and recipients[0].id == sender.id:
            return
        else:
            message = models.Message()
            format_message(message)
            db.session.add(message)

    # Finally, commit all changes to db
    db.session.commit()


def send_recovery_email(recipient_email, user):
    """ Function to send emails via MailerSend """

    token = user.get_reset_password_token()
    reset_url = url_for("user.reset_password", token=token, _external=True)

    mailer = emails.NewEmail()

    mail_body = {}
    mail_from = {
        "name": "WAR/COR Password Reset",
        "email": "no-reply@war-cor.com",
    }
    recipients = [
        {
            "name": user.username,
            "email": recipient_email,
        }
    ]
    personalization = [
        {
            "email": recipient_email,
            "data": {
                "username": user.username,
                "reset_url": reset_url,
            }
        }
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject("WAR/COR Password Reset", mail_body)
    mailer.set_template("z86org880dkgew13", mail_body)
    mailer.set_advanced_personalization(personalization, mail_body)

    mailer.send(mail_body)
    