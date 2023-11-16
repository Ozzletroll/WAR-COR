from flask_login import UserMixin
import werkzeug

from app import db
from models.associations import *



class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(250))
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

    permissions = db.relationship("Campaign", 
                                  secondary=user_edit_permissions, 
                                  back_populates="admins")
    
    comments = db.relationship("Comment", back_populates="author")
    messages = db.relationship("Message", 
                               secondary=user_messages, 
                               back_populates="recipients",
                               cascade="delete")
    sent_messages = db.relationship("Message", back_populates="author", foreign_keys="[Message.author_id]")
    open_invites = db.relationship("Message", back_populates="target_user", foreign_keys="[Message.target_user_id]")

    # Methods
    def update(self, form, new=False):
        """ Method to populate and update self.
            Takes form data from request.form.
            Email and username booleans
            Set "new" to true if creating new entry. """

        for field, value in form.items():
            if value is not None:

                if field == "email":
                    value.lower()

                setattr(self, field, value)

        if new:
            # Salt and hash password
            sh_password = werkzeug.security.generate_password_hash(
                form["password"],
                method="pbkdf2:sha256",
                salt_length=8
            )
            self.password = sh_password
            db.session.add(self)
        
        db.session.commit()


    def change_password(self, form):
        """ Method to change user's password. Returns false
            if given old password is incorrect. """

        old_password = form["old_password"]
        new_password = form["new_password"]

        # Check if the given old password matches the db password
        if werkzeug.security.check_password_hash(pwhash=self.password, password=old_password):
            
            # Salt and hash new password
            sh_password = werkzeug.security.generate_password_hash(
                new_password,
                method="pbkdf2:sha256",
                salt_length=8
            )
            self.password = sh_password
            db.session.commit()
            return True

        else:
            return False
        