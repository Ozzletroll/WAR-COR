from datetime import datetime
from sqlalchemy import select

from warcor import models
from warcor import db


def send_invite_message(sender, recipient, campaign):
    """ Function for creating and 'sending' a campaign invitation message.
    Messages are stored in the database, and accessed via the user.messages
    association. Takes a user object for both sender and recipient, and
    a campaign object."""

    # Check for existing pending invite
    message = db.session.execute(
        select(models.Message)
        .filter(models.Message.target_campaign.has(id=campaign.id))
        .filter(models.Message.target_user.has(id=recipient.id))
        .filter(models.Message.invite == True)
    ).scalar()

    # If invitation message already exists, update date
    # to push to top of notifications list
    if message:
        message.date = datetime.now()
        db.session.commit()

    # Otherwise, create a new message
    else:
        message = models.Message()

        message.author = sender
        message.invite = True
        message.body = f"{sender.username} has invited you to the campaign: {campaign.title}"
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

    # Check for existing pending request
    message = db.session.execute(
        select(models.Message)
        .filter(models.Message.target_campaign.has(id=campaign.id))
        .filter(models.Message.author.has(id=sender.id))
        .filter(models.Message.request == True)).scalar()

    # If invitation message already exists, update date
    # to push to top of notifications list
    if message:
        message.date = datetime.now()
        db.session.commit()

    # Otherwise, create a new message
    else:
        message = models.Message()

        message.author = sender
        message.request = True
        message.body = f"{sender.username} has requested to join the campaign: {campaign.title}"
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

    message = models.Message()

    message.author = sender
    message.notification = True
    message.body = f"{new_user_username} has joined the campaign: {campaign.title}"
    message.target_campaign = campaign
    message.date = datetime.now()

    db.session.add(message)

    for user in recipients:
        user.messages.append(message)

    db.session.commit()


def send_event_notification(sender, recipients, campaign, event):
    """Function for creating new event notifications. Takes a user model object as sender, and
    a list of user model objects as recipients, along with a campaign object, and an event object."""

    message = models.Message()

    message.author = sender
    message.notification = True
    message.body = f"The campaign: {campaign.title} has been updated with the new event: {event.title}"
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
        message.author = sender
        message.notification = True
        message.body = f"New comments for event: '{event.title}' in campaign: '{campaign.title}'."
        message.target_campaign = campaign
        message.target_event = event
        message.date = datetime.now()

        # Add message to all recipients messages list, unless they are already a recipient
        for user in recipients:
            if message not in user.messages and user.id != sender.id:
                user.messages.append(message)

    # Check for existing comment messages
    messages = db.session.execute(
        select(models.Message)
        .filter(models.Message.target_campaign.has(id=campaign.id))
        .filter(models.Message.target_event.has(id=event.id))
        .filter(models.Message.notification == True)
    ).scalars()

    # Convert the query result to a list to avoid ResourceClosedError
    messages_list = list(messages)

    if len(messages_list) > 0:
        for message in messages_list:
            format_message(message)

    else:
        # Otherwise, create new comment message
        message = models.Message()
        format_message(message)
        db.session.add(message)

    # Finally, commit all changes to db
    db.session.commit()


def send_recovery_email():

    # Email sending code goes here

    pass