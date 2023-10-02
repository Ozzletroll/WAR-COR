from app import db



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
