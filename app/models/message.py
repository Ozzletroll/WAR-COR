from sqlalchemy import select
from app import db
from app.models.associations import user_messages


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

    def dismiss(self, user):
        if self in user.messages:
            user.messages.remove(self)
            db.session.commit()

            # Check if message is still in any user's messages list
            # by querying association table
            message_query = (db.session.execute(
                             select(user_messages.c.user_id)
                             .where(user_messages.c.message_id == self.id))
                             .scalar())

            # If message is no longer needed, delete it
            if not message_query:
                db.session.delete(self)
                db.session.commit()
