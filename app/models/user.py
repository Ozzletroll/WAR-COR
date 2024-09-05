from flask import current_app
from flask_login import UserMixin
import werkzeug
import jwt
from datetime import datetime
from sqlalchemy import select, join, asc, desc

from app.models.associations import *
from app.models import Campaign


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
    def check_password(self, password):
        return werkzeug.security.check_password_hash(pwhash=self.password, 
                                                     password=password)

    def update(self, form, new=False):
        """ Method to populate and update self.
            Takes form data from request.form.
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

    def change_password(self, form, reset=False):
        """ Method to change user's password. Returns false
            if given old password is incorrect. Set Reset param when
            resetting password via recovery email. """

        if reset:
            new_password = form["new_password"]
            sh_password = werkzeug.security.generate_password_hash(
                new_password,
                method="pbkdf2:sha256",
                salt_length=8
            )
            self.password = sh_password
            db.session.commit()
            return True

        else:
            old_password = form["old_password"]
            new_password = form["new_password"]

            if self.check_password(password=old_password):
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

    def get_reset_password_token(self, expiration=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": datetime.now().timestamp() + expiration},
            current_app.config["SECRET_KEY"], 
            algorithm="HS256")

    @staticmethod
    def verify_password_reset_token(token):

        try:
            id = jwt.decode(token,
                            current_app.config["SECRET_KEY"],
                            algorithms=["HS256"])["reset_password"]
        except:
            return
        
        return db.session.get(User, id)
    
    def return_paginated_campaigns(self, page, sort_by):

        if sort_by == "alphabetical":
            order_by = asc(Campaign.title)
        else:
            order_by = desc(Campaign.last_edited)

        user_campaigns = (select(Campaign)
                          .select_from(join(UserCampaign, Campaign, UserCampaign.campaign_id == Campaign.id))
                          .where(UserCampaign.user_id == self.id)
                          .order_by(order_by))
    
        paginated_campaigns = db.paginate(user_campaigns, page=page, per_page=6, error_out=False)
        
        return paginated_campaigns
    