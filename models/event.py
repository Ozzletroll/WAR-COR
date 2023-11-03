from datetime import datetime
import bleach
from bleach.css_sanitizer import CSSSanitizer

from app import db



class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)

    date = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)
    second = db.Column(db.Integer)

    location = db.Column(db.String(250), nullable=True)
    belligerents = db.Column(db.String(250), nullable=True)
    body = db.Column(db.String(250), nullable=False)
    result = db.Column(db.String(250), nullable=True)
    header = db.Column(db.Boolean(), nullable=False, default=False)
    hide_time = db.Column(db.Boolean(), nullable=False, default=False)

    # Database relationships
    # An event is part of a campaign, and may contain multiple comments. 
    # Events have both following and preceding events.

    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    parent_campaign = db.relationship("Campaign", 
                                      back_populates="events")
    
    following_event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    following_event = db.relationship('Event', 
                                      backref=db.backref('preceding_event', 
                                                         uselist=False), 
                                                         remote_side=[id])
    epochs = db.relationship("Epoch",
                              secondary="epoch_events",
                              back_populates="events")
    comments = db.relationship("Comment", 
                               back_populates="parent_event",
                               cascade="delete, delete-orphan")

    # Methods
    def update(self, form, parent_campaign, new=False):
        """ Method to populate and update self.
            Takes form data from form.data
            Set "new" to true if creating new entry  """

        for field, value in form.items():
            if field == "date" and value is not None:
                self.date = value
                self.split_date(value)
                continue

            if field == "body":
                allowed_tags = ["p", "b", "em", "h1", "h2", "h3", "a", "br", "u", "img", "ul", "ol"]
                allowed_attrs = {
                    "*": ["class"],
                    "a": ["href", "rel"],
                    "img": ["alt", "src", "style"],
                    }
                allowed_styles = ["height", "width"]
                css_santizer = CSSSanitizer(allowed_css_properties=allowed_styles)
                value = bleach.clean(value, 
                                     tags=allowed_tags,
                                     attributes=allowed_attrs,
                                     css_sanitizer=css_santizer)

            if value is not None:
                setattr(self, field, value)

        self.parent_campaign = parent_campaign
        self.parent_campaign.last_edited = datetime.now()
        
        if new:
            db.session.add(self)

        db.session.commit()


    def create_blank(self, datestring):
        """ Method to create a blank temporary pending event for prepopulating form.
            Takes an incremented datestring from organisers.format_event_datestring(). """

        self.title = ""
        self.type = ""
        self.body = ""
        self.date = datestring


    def split_date(self, datestring):
        """ Method that splits a form datestring into individual integer values. """

        self.year = int(datestring.split("/")[0])
        self.month = int(datestring.split("/")[1])
        self.day = int(datestring.split("/")[2].split()[0])
        self.hour = int(datestring.split("/")[2].split()[1].split(":")[0])
        self.minute = int(datestring.split("/")[2].split()[1].split(":")[1])
        self.second = int(datestring.split("/")[2].split()[1].split(":")[2])


    def separate_belligerents(self):
        """ Method to seperate the belligerents into groups for rendering. """

        separated_belligerents = self.belligerents.split(",")
        groups = []

        for group in separated_belligerents:
            allied_belligerents = []
            for element in group.split("&"):
                allied_belligerents.append(element)
            groups.append(allied_belligerents)
            
        return groups
