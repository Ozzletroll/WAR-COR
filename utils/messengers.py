from datetime import datetime

import models
from app import db

def send_invite_message(sender, recipient, campaign):
  """Function for creating and 'sending' a campaign invitation message.
  Messages are stored in the database, and accessed via the user.messages
  association. Takes a user object for both sender and recipient, and
  a campaign object."""

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


def send_event_notification(sender, recipients, campaign, event):
  """Function for creating new event notifications. Takes a user model object as sender, and
  a list of user model objects as recipients, along with a campaign object, and an event object."""

  message = models.Message()

  message.author = sender
  message.notification = True
  message.body = f"The campaign: {campaign.title} has been updated with the new event: {event.title}"
  message.target_campaign = campaign
  message.date = datetime.now()

  db.session.add(message)

  for user in recipients:
    user.messages.append(message)
    
  db.session.commit()
