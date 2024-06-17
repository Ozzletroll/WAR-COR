from datetime import datetime

from app import db
from app.utils.sanitisers import sanitise_input, sanitise_json


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

    dynamic_fields = db.Column(db.JSON, default={})

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

        self.dynamic_fields = []
        for field, value in form.items():

            if value is not None or new:

                if field == "dynamic_fields":
                    self.dynamic_fields = self.map_dynamic_field_data(value)
                else:
                    setattr(self, field, value)

        self.date = self.set_date()
        self.parent_campaign = parent_campaign
        self.parent_campaign.last_edited = datetime.now()
        self.parent_campaign.clear_cache()
        self.set_url_title()
        
        if new:
            db.session.add(self)

        db.session.commit()

    @staticmethod
    def map_dynamic_field_data(value):

        allowed_keys = ["title", "value", "field_type", "is_full_width"]
        allowed_field_types = ["html", "basic", "composite"]

        data = []
        for dynamic_field_data in value:
            dict = {}
            for key, dynamic_value in dynamic_field_data.items():
                
                if key == "value":
                    if dynamic_field_data["field_type"] == "html":
                        dynamic_value = sanitise_input(dynamic_value, wrap=True)
                    elif dynamic_field_data["field_type"] == "composite":
                        dynamic_value = sorted(sanitise_json(dynamic_value, "composite_field"),
                                               key=lambda x: int(x["position"]))
                if key == "field_type":
                    if dynamic_value not in allowed_field_types:
                        dynamic_value = "basic"
                if key == "is_full_width":
                    if not isinstance(dynamic_value, bool):
                        dynamic_value = False
                if key in allowed_keys:
                    dict[key] = dynamic_value
            data.append(dict)

        return data

    def create_blank(self, date_values):
        """ Method to create a blank temporary pending event for pre-populating form.
            Takes a dict of incremented date values from organisers.increment_date(). """

        self.title = ""
        self.type = ""
        self.year = date_values["year"]
        self.month = date_values["month"]
        self.day = date_values["day"]
        self.hour = date_values["hour"]
        self.minute = date_values["minute"]
        self.second = date_values["second"]

    def set_date(self):
        """ Method that formats date as string for template rendering """

        date = f"{self.year}/{str(self.month).zfill(2)}/{str(self.day).zfill(2)}"
        time = f"{str(self.hour).zfill(2)}:{str(self.minute).zfill(2)}:{str(self.second).zfill(2)}"

        return date + " " + time

    def set_url_title(self):
        """ Method to set url safe version of title, replacing spaces
            with dashes '-'. """

        self.url_title = self.title.replace(" ", "-")
