from flask_login import UserMixin

from app import db

# Association table that defines user to campaign editing permissions.
user_edit_permissions = db.Table("user_edit_permissions",
                                 db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                                 db.Column("campaign_id", db.Integer, db.ForeignKey("campaign.id")))


# Association table that defines user to message relationship.
user_messages = db.Table("user_messages",
                         db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                         db.Column("message_id", db.Integer, db.ForeignKey("message.id")))


# Association Object that defines user to campaign membership, and allows
# users to have a unique callsign for each campaign.
class UserCampaign(db.Model):
    __tablename__ = 'user_campaign'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), primary_key=True)
    callsign = db.Column(db.String(50))

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
    messages = db.relationship("Message", secondary=user_messages)
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

    events = db.relationship("Event", back_populates="parent_campaign")
    pending_invites = db.relationship("Message", back_populates="target_campaign")

    # Many-to-many relationship to User, bypassing the `UserCampaign` class
    members = db.relationship("User",
                              secondary="user_campaign",
                              back_populates="campaigns")

    # Association between Child -> Association -> Parent
    user_associations = db.relationship("UserCampaign",
                                        back_populates="campaign",
                                        cascade="delete, delete-orphan",
                                        viewonly=True)


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

    # Database relationships
    # An event is part of a campaign, and may contain multiple comments.

    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    parent_campaign = db.relationship("Campaign", back_populates="events")
    comments = db.relationship("Comment", back_populates="parent_event")



class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(250))

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
    body = db.Column(db.String(250))
    date = db.Column(db.DateTime, nullable=False)


    # Database relationships
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="sent_messages", foreign_keys=[author_id])

    target_campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    target_campaign = db.relationship("Campaign", back_populates="pending_invites")

    target_event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    target_event = db.relationship("Event", back_populates="")

    target_user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    target_user = db.relationship("User", back_populates="open_invites", foreign_keys=[target_user_id])
