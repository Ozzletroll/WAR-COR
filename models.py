from flask_login import UserMixin
from datetime import datetime

from app import db

import utils.organisers as organisers



# Association table that defines user to campaign editing permissions.
user_edit_permissions = db.Table("user_edit_permissions",
                                 db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                                 db.Column("campaign_id", db.Integer, db.ForeignKey("campaign.id")))


# Association table that defines user to message relationship.
user_messages = db.Table("user_messages",
                         db.Column("user_id", db.Integer, db.ForeignKey("user.id", ondelete="CASCADE")),
                         db.Column("message_id", db.Integer, db.ForeignKey("message.id", ondelete="CASCADE")))


# Association table that defines event to epoch relationship
epoch_events = db.Table("epoch_events",
                        db.Column("epoch_id", db.Integer, db.ForeignKey("epoch.id")),
                        db.Column("event_id", db.Integer, db.ForeignKey("event.id")))


# Association Object that defines user to campaign membership, and allows
# users to have a unique callsign for each campaign.
class UserCampaign(db.Model):
    __tablename__ = 'user_campaign'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), primary_key=True)
    callsign = db.Column(db.String(30))

    # Association between UserCampaign -> User
    user = db.relationship('User', back_populates="campaign_associations", viewonly=True)

    # Association between UserCampaign -> Campaign
    campaign = db.relationship('Campaign', back_populates="user_associations", viewonly=True)



class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(30))
    password = db.Column(db.String(250))

    # Database relationships
    # A user takes part in a number of campaigns, may have editing permissions, and may be the author of many comments.

    # Many-to-many relationship to Campaign, bypassing the `UserCampaign` class
    campaigns = db.relationship("Campaign",
                                secondary="user_campaign",
                                back_populates="members")
    
    # Association between User -> UserCampaign -> Campaign
    campaign_associations = db.relationship("UserCampaign",
                                            back_populates="user",
                                            cascade="delete, delete-orphan",
                                            viewonly=True)

    permissions = db.relationship("Campaign", secondary=user_edit_permissions)
    comments = db.relationship("Comment", back_populates="author")
    messages = db.relationship("Message", 
                               secondary=user_messages, 
                               back_populates="recipients",
                               cascade="delete")
    sent_messages = db.relationship("Message", back_populates="author", foreign_keys="[Message.author_id]")
    open_invites = db.relationship("Message", back_populates="target_user", foreign_keys="[Message.target_user_id]")



class Campaign(db.Model):
    __tablename__ = "campaign"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250))
    description = db.Column(db.String(250), nullable=False)
    last_edited = db.Column(db.DateTime, nullable=False)
    date_suffix = db.Column(db.String(8), nullable=True)

    # Database relationships
    # A campaign has a number of participating users, and is made up of a number of events. Users may have editing
    # permission. 
    events = db.relationship("Event", 
                             back_populates="parent_campaign", 
                             cascade="delete, delete-orphan")
    epochs = db.relationship("Epoch", 
                             back_populates="parent_campaign", 
                             cascade="delete, delete-orphan")
    pending_invites = db.relationship("Message", 
                                      back_populates="target_campaign", 
                                      cascade="delete, delete-orphan")
    # Many-to-many relationship to User, bypassing the `UserCampaign` class
    members = db.relationship("User",
                              secondary="user_campaign",
                              back_populates="campaigns")
    # Association between Child -> Association -> Parent
    user_associations = db.relationship("UserCampaign",
                                        back_populates="campaign",
                                        cascade="delete, delete-orphan",
                                        viewonly=True)
    

    # Methods
    def update(self, form, new=False):
        """ Method to populate and update self.
            Takes form data from request.form.
            Set "new" to true if creating new entry. """

        for field, value in form.items():
            if value is not None:
                setattr(self, field, value)

        self.last_edited = datetime.now()

        if new:
            db.session.add(self)

        db.session.commit()

    
    def check_epochs(self):
        """ Method to clear and recheck all epochs for containing
            events. """
        
        for epoch in self.epochs:
            epoch.populate_self()



class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String, nullable=False)
    location = db.Column(db.String(250), nullable=True)
    belligerents = db.Column(db.String(250), nullable=True)
    body = db.Column(db.String(250), nullable=False)
    result = db.Column(db.String(250), nullable=True)
    header = db.Column(db.Boolean(), nullable=False, default=False)
    hide_time = db.Column(db.Boolean(), nullable=False, default=False)

    # Database relationships
    # An event is part of a campaign, and may contain multiple comments. 
    # Events have both following and preceding events.

    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    parent_campaign = db.relationship("Campaign", 
                                      back_populates="events")
    following_event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    following_event = db.relationship('Event', 
                                      backref=db.backref('preceding_event', 
                                                         uselist=False), 
                                                         remote_side=[id])
    epochs = db.relationship("Epoch",
                              secondary="epoch_events",
                              back_populates="events")
    comments = db.relationship("Comment", 
                               back_populates="parent_event",
                               cascade="delete, delete-orphan")

    # Methods
    def update(self, form, parent_campaign, new=False):
        """ Method to populate and update self.
            Takes form data from form.data
            Set "new" to true if creating new entry
            Set "date" to true if event's date has been specified by ui.  """

        for field, value in form.items():
            if value is not None:
                setattr(self, field, value)

        self.parent_campaign = parent_campaign
        self.parent_campaign.last_edited = datetime.now()
        
        if new:
            db.session.add(self)

        db.session.commit()


    def create_blank(self, datestring):
        """ Method to create a blank temporary pending event for prepopulating form.
            Takes an incremented datestring from organisers.format_event_datestring(). """

        self.title = ""
        self.type = ""
        self.body = ""
        self.date = datestring




class Epoch(db.Model):
    __tablename__ = "epoch"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250), nullable=False)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
    description = db.Column(db.String(250), nullable=True)
    has_events = db.Column(db.Boolean(), nullable=False, default=False)

    # Database relationships
    # An epoch is part of a campaign, and may encapsulate multiple events.

    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    parent_campaign = db.relationship("Campaign", back_populates="epochs")

    # Many-to-many relationship to User, bypassing the `UserCampaign` class
    events = db.relationship("Event",
                              secondary="epoch_events",
                              back_populates="epochs")
    

    # Methods
    def update(self, form, parent_campaign, new=False):
        """ Method to populate and update self.
            Takes form data from request.form
            Set "new" to true if creating new entry.  """

        for field, value in form.items():
            if value is not None:
                setattr(self, field, value)

        self.parent_campaign = parent_campaign
        self.parent_campaign.last_edited = datetime.now()
        
        if new:
            db.session.add(self)

        db.session.commit()

        self.populate_self()
        self.parent_campaign.check_epochs()


    def populate_self(self):
        """ Method to get all events in parent campaign that fall
        between the epochs start and end dates, and flag self
        if containing any events. """
        
        def is_in_epoch(event, epoch):

            epoch_start = float(epoch.start_date.replace("-", "."))
            epoch_end = float(epoch.end_date.replace("-", "."))

            event_year, event_month = event.date.split("-")[:2]
            event_combined = event_year + "-" + event_month
            event_date = float(event_combined.replace("-", "."))

            if epoch_start <= event_date <= epoch_end:
                return True
            else:
                return False
    
        self.events.clear()
        self.events = [event for event in self.parent_campaign.events if is_in_epoch(event, self)]

        if len(self.events) > 0:
            self.has_events = True
        else:
            self.has_events = False

        db.session.commit()



class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    new = db.Column(db.Boolean(), default=False)

    # Database relationships
    # A comment is attached to an event, and has an author.

    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    parent_event = db.relationship("Event", back_populates="comments")

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="comments")


class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    invite = db.Column(db.Boolean(), default=False)
    notification = db.Column(db.Boolean(), default=False)
    request = db.Column(db.Boolean(), default=False)
    body = db.Column(db.String(250))
    date = db.Column(db.DateTime, nullable=False)
    

    # Database relationships
    recipients = db.relationship("User",
                                secondary="user_messages",
                                back_populates="messages")

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="sent_messages", foreign_keys=[author_id])

    target_campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    target_campaign = db.relationship("Campaign", back_populates="pending_invites")

    target_event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    target_event = db.relationship("Event")

    target_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    target_user = db.relationship("User", back_populates="open_invites", foreign_keys=[target_user_id])
