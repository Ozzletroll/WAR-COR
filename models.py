from flask_login import UserMixin

from app import db

# Association table that defines user to campaign editing permissions.
user_edit_permissions = db.Table("user_edit_permissions",
                                 db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
                                 db.Column("campaign_id", db.Integer, db.ForeignKey("campaign.id")))


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


class Campaign(db.Model):
    __tablename__ = "campaign"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250))
    description = db.Column(db.String(250), nullable=False)
    last_edited = db.Column(db.DateTime, nullable=False)

    # Database relationships
    # A campaign has a number of participating users, and is made up of a number of events. Users may have editing
    # permission.

    events = db.relationship("Event", back_populates="parent_campaign")

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
    location = db.Column(db.String(250), nullable=False)
    belligerents = db.Column(db.String(250), nullable=True)
    body = db.Column(db.String(250), nullable=False)
    result = db.Column(db.String(250), nullable=False)

    # Database relationships
    # An event is part of a campaign, and may contain multiple comments.

    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    comments = db.relationship("Comment", back_populates="parent_event")
    parent_campaign = db.relationship("Campaign", back_populates="events")


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
