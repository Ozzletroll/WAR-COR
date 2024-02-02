from app import db

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

# Association table that defines parent_epoch to child_epoch relationship
epoch_sub_epochs = db.Table("epoch_sub_epochs",
                            db.Column("parent_epoch_id", db.Integer, db.ForeignKey("epoch.id")),
                            db.Column("child_epoch_id", db.Integer, db.ForeignKey("epoch.id")))


# Association Object that defines user to campaign membership, and allows
# users to have a unique callsign for each campaign.
class UserCampaign(db.Model):
    __tablename__ = "user_campaign"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"), primary_key=True)
    callsign = db.Column(db.String(30))

    # Association between UserCampaign -> User
    user = db.relationship("User", back_populates="campaign_associations", viewonly=True)

    # Association between UserCampaign -> Campaign
    campaign = db.relationship("Campaign", back_populates="user_associations", viewonly=True)
