import base64
import os
from sqlalchemy.exc import IntegrityError

from app import db


class Template(db.Model):
    __tablename__ = "template"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(250), nullable=False)
    share_code = db.Column(db.String(30), nullable=False, unique=True)
    format = db.Column(db.JSON, default={})

    parent_campaign = db.relationship("Campaign", back_populates="templates")
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.share_code = self.generate_share_code()

        while True:
            try:
                db.session.add(self)
                db.session.commit()
                break
            except IntegrityError:
                db.session.rollback()
                self.share_code = self.generate_share_code()

    @staticmethod
    def generate_share_code():
        return base64.urlsafe_b64encode(os.urandom(9)).decode("utf-8").rstrip("==")
    
    def duplicate(self, new_campaign):

        new_template = Template(name=self.name,
                                format=self.format,
                                parent_campaign=new_campaign)

        return new_template
    