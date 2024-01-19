from datetime import datetime

from app import db
from app.models import associations
from app.utils.sanitisers import sanitise_input


class Epoch(db.Model):
    __tablename__ = "epoch"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250), nullable=False)
    url_title = db.Column(db.String(250))

    start_date = db.Column(db.String, nullable=False)
    start_year = db.Column(db.Integer)
    start_month = db.Column(db.Integer)
    start_day = db.Column(db.Integer)

    end_date = db.Column(db.String, nullable=False)
    end_year = db.Column(db.Integer)
    end_month = db.Column(db.Integer)
    end_day = db.Column(db.Integer)

    overview = db.Column(db.String(), nullable=True)
    description = db.Column(db.String(), nullable=True)
    has_events = db.Column(db.Boolean(), nullable=False, default=False)

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
                                 backref=db.backref("parent_epochs", lazy='dynamic'),
                                 primaryjoin=(associations.epoch_sub_epochs.c.parent_epoch_id == id),
                                 secondaryjoin=(associations.epoch_sub_epochs.c.child_epoch_id == id))
    
    # Methods
    def update(self, form, parent_campaign, new=False):
        """ Method to populate and update self.
            Takes form data from request.form
            Set "new" to true if creating new entry.  """

        for field, value in form.items():
            
            if value is not None:

                if field == "start_date":
                    self.start_date = value
                    self.start_year = self.split_date(value)[0]
                    self.start_month = self.split_date(value)[1]
                    self.start_day = self.split_date(value)[2]

                if field == "end_date":
                    self.end_date = value
                    self.end_year = self.split_date(value)[0]
                    self.end_month = self.split_date(value)[1]
                    self.end_day = self.split_date(value)[2]

                if field == "description" or field == "overview":
                    value = sanitise_input(value)
                    if value == "<p><br></p>":
                        value = None

                setattr(self, field, value)

        self.parent_campaign = parent_campaign
        self.parent_campaign.last_edited = datetime.now()
        self.set_url_title()
        
        if new:
            db.session.add(self)

        db.session.commit()

        self.populate_self()
        self.parent_campaign.check_epochs()

    @staticmethod
    def split_date(datestring):
        """ Method that splits a form datestring into individual integer values. """

        year = int(datestring.split("/")[0])
        month = int(datestring.split("/")[1])
        day = int(datestring.split("/")[2])

        return [year, month, day]
    
    def set_url_title(self):
        """ Method to set url safe version of title, replacing spaces
            with dashes '-'. """
        
        self.url_title = self.title.replace(" ", "-")
        
    def populate_self(self):
        """ Method to get all events in parent campaign that fall
        between the epochs start and end dates, and flag self
        if containing any events. """
        
        def is_in_epoch(event, epoch):

            epoch_start_year, epoch_start_month, epoch_start_day = self.split_date(epoch.start_date)
            epoch_end_year, epoch_end_month, epoch_end_day = self.split_date(epoch.end_date)

            event_year = int(event.date.split("/")[0])
            event_month = int(event.date.split("/")[1])
            event_day = int(event.date.split("/")[2][:2])

            if epoch_start_year <= event_year <= epoch_end_year:
                if epoch_start_year == event_year and event_month < epoch_start_month:
                    return False
                if epoch_end_year == event_year and event_month > epoch_end_month:
                    return False
                if epoch_start_year == event_year and event_month == epoch_start_month and event_day < epoch_start_day:
                    return False
                if epoch_end_year == event_year and event_month == epoch_end_month and event_day > epoch_end_day:
                    return False
                return True

            return False

        self.events.clear()
        self.events = [event for event in self.parent_campaign.events if is_in_epoch(event, self)]

        if len(self.events) > 0:
            self.has_events = True
        else:
            self.has_events = False

        db.session.commit()
