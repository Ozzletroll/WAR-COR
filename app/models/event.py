from datetime import datetime

from app import db
from app.utils.sanitisers import sanitise_input


class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    url_title = db.Column(db.String(250))
    hide_time = db.Column(db.Boolean(), nullable=False, default=False)

    date = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)
    second = db.Column(db.Integer)

    data = db.Column(db.JSON, default={})

    # Database relationships
    # An event is part of a campaign, and may contain multiple comments. 
    # Events have both following and preceding events.

    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    parent_campaign = db.relationship("Campaign", 
                                      back_populates="events")
    
    following_event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    following_event = db.relationship("Event",
                                      backref=db.backref("preceding_event", uselist=False),
                                      remote_side=[id])
    epochs = db.relationship("Epoch",
                             secondary="epoch_events",
                             back_populates="events")
    comments = db.relationship("Comment", 
                               back_populates="parent_event",
                               cascade="delete, delete-orphan")
    targeting_messages = db.relationship("Message",
                                         back_populates="target_event",
                                         cascade="delete, delete-orphan")

    # Methods
    def update(self, form, parent_campaign, new=False):
        """ Method to populate and update self.
            Set "new" to true if creating new entry.  """
        
        for field, value in form.items():

            if value or new:

                if field == "date":
                    self.date = value
                    self.split_date(value)

                elif field == "dynamic_fields":

                    data = []
                    for dynamic_field_data in value:
                        dict = {}
                        for key, dynamic_value in dynamic_field_data.items():
                            if key == "value":
                                dynamic_value = sanitise_input(dynamic_value)
                            if key != "edited":
                                dict[key] = dynamic_value
                            data.append(dict)

                    self.data = data
                        
                else:
                    setattr(self, field, value)

        self.parent_campaign = parent_campaign
        self.parent_campaign.last_edited = datetime.now()
        self.parent_campaign.clear_cache()
        self.set_url_title()
        
        if new:
            db.session.add(self)

        db.session.commit()

    def create_blank(self, datestring):
        """ Method to create a blank temporary pending event for pre-populating form.
            Takes an incremented date-string from organisers.format_event_datestring(). """

        self.title = ""
        self.type = ""
        self.body = ""
        self.date = datestring

    def split_date(self, datestring):
        """ Method that splits a form date string into individual integer values. """

        self.year = int(datestring.split("/")[0])
        self.month = int(datestring.split("/")[1])
        self.day = int(datestring.split("/")[2].split()[0])
        self.hour = int(datestring.split("/")[2].split()[1].split(":")[0])
        self.minute = int(datestring.split("/")[2].split()[1].split(":")[1])
        self.second = int(datestring.split("/")[2].split()[1].split(":")[2])

    def separate_belligerents(self):
        """ Method to separate the belligerents into groups for rendering. """

        if self.belligerents == "":
            return []

        separated_belligerents = self.belligerents.split(",")
        groups = []

        for group in separated_belligerents:
            allied_belligerents = []
            for element in group.split("&"):
                allied_belligerents.append(element.strip())
            groups.append(allied_belligerents)
            
        return groups

    def set_url_title(self):
        """ Method to set url safe version of title, replacing spaces
            with dashes '-'. """

        self.url_title = self.title.replace(" ", "-")
