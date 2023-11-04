from datetime import datetime

from app import db
from utils.sanitisers import sanitise_input



class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(250), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    # Database relationships
    # A comment is attached to an event, and has an author.

    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    parent_event = db.relationship("Event", back_populates="comments")

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="comments")

    # Methods
    def update(self, form, parent_event, author):
        """ Method to populate and update self.
            Takes form data from request.form. """

        for field, value in form.items():

            if field == "body":
                value = sanitise_input(value)

            setattr(self, field, value)

        self.parent_event = parent_event
        self.author = author
        self.date = datetime.now()

        db.session.add(self)
        db.session.commit()
