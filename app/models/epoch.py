from datetime import datetime

from app import db
from app.models import associations
from app.utils.sanitisers import sanitise_input, sanitise_json


class Epoch(db.Model):
    __tablename__ = "epoch"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250), nullable=False)
    url_title = db.Column(db.String(250))
    has_events = db.Column(db.Boolean(), nullable=False, default=False)

    start_date = db.Column(db.String, nullable=False)
    start_year = db.Column(db.Integer)
    start_month = db.Column(db.Integer)
    start_day = db.Column(db.Integer)

    end_date = db.Column(db.String, nullable=False)
    end_year = db.Column(db.Integer)
    end_month = db.Column(db.Integer)
    end_day = db.Column(db.Integer)

    overview = db.Column(db.String(), nullable=True)
    dynamic_fields = db.Column(db.JSON, default={})

    # Database relationships
    # An epoch is part of a campaign, and may encapsulate multiple events.

    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    parent_campaign = db.relationship("Campaign",
                                      back_populates="epochs")

    events = db.relationship("Event",
                             secondary="epoch_events",
                             back_populates="epochs")
    
    sub_epochs = db.relationship("Epoch",
                                 secondary="epoch_sub_epochs",
                                 backref=db.backref("parent_epochs"),
                                 primaryjoin=(associations.epoch_sub_epochs.c.parent_epoch_id == id),
                                 secondaryjoin=(associations.epoch_sub_epochs.c.child_epoch_id == id))
    
    # Methods
    def update(self, form, parent_campaign, new=False):
        """ Method to populate and update self.
            Takes form data from request.form
            Set "new" to true if creating new entry.  """

        self.dynamic_fields = []
        for field, value in form.items():

            if value is not None or new:

                if field == "overview":
                    value = sanitise_input(value, allow_urls=False)
                    if value in ["<p><br/></p>", ""]:
                        value = None
                    self.overview = value
                elif field == "dynamic_fields":
                    data = self.map_dynamic_field_data(value)
                    self.dynamic_fields = data
                else:
                    setattr(self, field, value)

        self.start_date = self.set_date(self.start_year, self.start_month, self.start_day)
        self.end_date = self.set_date(self.end_year, self.end_month, self.end_day)
        self.parent_campaign = parent_campaign
        self.parent_campaign.last_edited = datetime.now()
        self.parent_campaign.clear_cache()
        self.set_url_title()
        
        if new:
            db.session.add(self)

        db.session.commit()

        self.populate_self()
        self.parent_campaign.check_epochs()

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

    def set_date(self, year, month, day):
        """ Method that formats date as string for template rendering """

        return f"{year}/{str(month).zfill(2)}/{str(day).zfill(2)}"

    def set_url_title(self):
        """ Method to set url safe version of title, replacing spaces
            with dashes '-'. """
        
        self.url_title = self.title.replace(" ", "-")

    def create_blank(self, date_values):
        """ Method to create a blank temporary pending epoch for pre-populating form.
            Takes a list of separated date values from formatters.split_date(). """

        self.title = ""
        self.type = ""
        self.start_year = date_values[0]
        self.start_month = date_values[1]
        self.start_day = date_values[2]
        self.end_year = date_values[0]
        self.end_month = date_values[1]
        self.end_day = date_values[2]

    def populate_self(self):
        """ Method to get all events in parent campaign that fall
        between the epochs start and end dates, and flag self
        if containing any events. """
        
        def is_in_epoch(item_to_check):

            def date_falls_between(year, month, day):
                if self.start_year <= year <= self.end_year:
                    if self.start_year == year and month < self.start_month:
                        return False
                    if self.end_year == year and month > self.end_month:
                        return False
                    if self.start_year == year and month == self.start_month and day < self.start_day:
                        return False
                    if self.end_year == year and month == self.end_month and day > self.end_day:
                        return False
                    return True
                return False

            # Handle epoch objects
            if isinstance(item_to_check, Epoch):
                item_start_year = item_to_check.start_year
                item_start_month = item_to_check.start_month
                item_start_day = item_to_check.start_day
                item_end_year = item_to_check.end_year
                item_end_month = item_to_check.end_month
                item_end_day = item_to_check.end_day

                # Return true if the checked epoch's start and end both fall within 
                # the start and end date values of the potential encapsulating epoch
                if date_falls_between(item_start_year, item_start_month, item_start_day):
                    if date_falls_between(item_end_year, item_end_month, item_end_day):
                        return True
                    else:
                        return False
                else:
                    return False

            # Handle event objects
            else:
                item_year = item_to_check.year
                item_month = item_to_check.month
                item_day = item_to_check.day

                # Return true if the event's date falls within the epoch
                if date_falls_between(item_year, item_month, item_day):
                    return True
                else:
                    return False

        self.events.clear()
        self.events = [event for event in self.parent_campaign.events if is_in_epoch(event)]
        self.sub_epochs.clear()
        self.sub_epochs = [epoch for epoch in self.parent_campaign.epochs 
                           if is_in_epoch(epoch) and epoch.id != self.id]

        if len(self.events) > 0:
            self.has_events = True
        else:
            self.has_events = False

        db.session.commit()
