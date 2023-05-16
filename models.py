from flask_login import UserMixin

from app import db

# Association table that defines user to campaign relationships
user_campaign = db.Table("user_campaign",
                         db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                         db.Column("campaign_id", db.Integer, db.ForeignKey("campaign.id")))

user_edit_permissions = db.Table("user_edit_permissions",
                                 db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                                 db.Column("campaign_id", db.Integer, db.ForeignKey("campaign.id")))


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    # Basic user data
    username = db.Column(db.String(30))
    password = db.Column(db.String(250))

    # Database relationships

    # A user takes part in a number of campaigns, may have editing permissions, and may be the author of many comments.

    campaigns = db.relationship("Campaign", secondary=user_campaign)
    permissions = db.relationship("Campaign", secondary=user_edit_permissions)

    comments = db.relationship("Comment", back_populates="author")


class Campaign(UserMixin, db.Model):
    __tablename__ = "campaign"

    id = db.Column(db.Integer, primary_key=True)

    # Basic campaign data
    title = db.Column(db.String(250))
    description = db.Column(db.String(250), nullable=False)

    # Database relationships

    # A campaign has a number of participating users, and is made up of a number of events. Users may have editing
    # permission.

    events = db.relationship("Event", back_populates="parent_campaign")


class Event(UserMixin, db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)

    # Events will either be defined as a "Conflict" or an "Event"
    type = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    belligerents = db.Column(db.String(250), nullable=True)
    body = db.Column(db.String(250), nullable=False)
    result = db.Column(db.String(250), nullable=False)

    # Database relationships
    # An event is part of a campaign, and may contain multiple comments.

    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    comments = db.relationship("Comment", back_populates="parent_event")

    parent_campaign = db.relationship("Campaign", back_populates="events")


class Comment(UserMixin, db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(250))

    # Database relationships

    # A comment is attached to an event, and has an author.

    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    parent_event = db.relationship("Event", back_populates="comments")

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="comments")
