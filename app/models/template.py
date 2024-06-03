import base64
import os
from sqlalchemy.exc import IntegrityError
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


from app import db


class Template(db.Model):
    __tablename__ = "template"

    id = db.Column(db.Integer, primary_key=True)

    origin_id = db.Column(db.Integer)
    name = db.Column(db.String(250), nullable=False)
    share_code = db.Column(db.String(30), nullable=False, unique=True)
    field_format = db.Column(db.JSON, default={})

    parent_campaign = db.relationship("Campaign", back_populates="templates")
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    
    def update(self):
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
                                field_format=self.field_format,
                                parent_campaign=new_campaign,
                                origin_id=self.id)

        return new_template
    
    def build_redirect_url(self, previous_url):
        """ Method to return redirect url when loading template """

        # Parse the previous url and its parameters
        url_parts = list(urlparse(previous_url))
        query = dict(parse_qs(url_parts[4]))
        query.update({"template_id": self.id})

        # Build the new url
        url_parts[4] = urlencode(query, doseq=True)
        redirect_url = urlunparse(url_parts)

        return redirect_url
    