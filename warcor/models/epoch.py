from datetime import datetime

from warcor.app import db
from warcor.utils.sanitisers import sanitise_input



class Epoch(db.Model):
    __tablename__ = "epoch"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250), nullable=False)

    start_date = db.Column(db.String, nullable=False)
    start_year = db.Column(db.Integer)
    start_month = db.Column(db.Integer)

    end_date = db.Column(db.String, nullable=False)
    end_year = db.Column(db.Integer)
    end_month = db.Column(db.Integer)

    description = db.Column(db.String(250), nullable=True)
    has_events = db.Column(db.Boolean(), nullable=False, default=False)

    # Database relationships
    # An epoch is part of a campaign, and may encapsulate multiple events.

    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))
    parent_campaign = db.relationship("Campaign", back_populates="epochs")

    # Many-to-many relationship to User, bypassing the `UserCampaign` class
    events = db.relationship("Event",
                              secondary="epoch_events",
                              back_populates="epochs")
    
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

                if field == "end_date":
                    self.end_date = value
                    self.end_year = self.split_date(value)[0]
                    self.end_month = self.split_date(value)[1]

                if field == "description":
                    value = sanitise_input(value)

                setattr(self, field, value)

        self.parent_campaign = parent_campaign
        self.parent_campaign.last_edited = datetime.now()
        
        if new:
            db.session.add(self)

        db.session.commit()

        self.populate_self()
        self.parent_campaign.check_epochs()


    def split_date(self, datestring):
        """ Method that splits a form datestring into individual integer values. """

        year = int(datestring.split("/")[0])
        month = int(datestring.split("/")[1])

        return [year, month]


    def populate_self(self):
        """ Method to get all events in parent campaign that fall
        between the epochs start and end dates, and flag self
        if containing any events. """
        
        def is_in_epoch(event, epoch):

            epoch_start_year = int(epoch.start_date.split("/")[:2][0])
            epoch_start_month = int(epoch.start_date.split("/")[:2][1])
            epoch_end_year = int(epoch.end_date.split("/")[:2][0])
            epoch_end_month = int(epoch.end_date.split("/")[:2][1])

            event_year = int(event.date.split("/")[:2][0])
            event_month = int(event.date.split("/")[:2][1])

            if epoch_start_year <= event_year <= epoch_end_year:
                if epoch_start_month <= event_month <= epoch_end_month:
                    return True
            else:
                return False
    
        self.events.clear()
        self.events = [event for event in self.parent_campaign.events if is_in_epoch(event, self)]

        if len(self.events) > 0:
            self.has_events = True
        else:
            self.has_events = False

        db.session.commit()
