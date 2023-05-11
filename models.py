from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # Basic user data
    username = db.Column(db.String(30))
    password = db.Column(db.String(250))

    # Database relationships

    # A user takes part in a number of campaigns, and may be the author of many comments.

    # campaigns =
    # comments =


class Campaign(UserMixin, db.Model):
    __tablename__ = "campaign"

    id = db.Column(db.Integer, primary_key=True)

    # Basic campaign data
    title = db.Column(db.String(250))
    description = db.Column(db.String(250), nullable=False)

    # Database relationships

    # A campaign has a number of participating users, and is made up of a number of events. Users may have editing
    # permission.

    # participants =
    # edit_permission = 
    events = db.relationship("Event", backref="campaign")


class Event(UserMixin, db.Model):
    __tablename__ = "events"

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
    # comments =


class Comments(UserMixin, db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(250))

    # Database relationships

    # A comment is attached to an event, and has an author.

    # parent_event =
    # author =