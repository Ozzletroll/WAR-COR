from datetime import datetime

from app import db



class Epoch(db.Model):
    __tablename__ = "epoch"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250), nullable=False)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
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
                setattr(self, field, value)

        self.parent_campaign = parent_campaign
        self.parent_campaign.last_edited = datetime.now()
        
        if new:
            db.session.add(self)

        db.session.commit()

        self.populate_self()
        self.parent_campaign.check_epochs()


    def populate_self(self):
        """ Method to get all events in parent campaign that fall
        between the epochs start and end dates, and flag self
        if containing any events. """
        
        def is_in_epoch(event, epoch):

            epoch_start = float(epoch.start_date.replace("-", "."))
            epoch_end = float(epoch.end_date.replace("-", "."))

            event_year, event_month = event.date.split("-")[:2]
            event_combined = event_year + "-" + event_month
            event_date = float(event_combined.replace("-", "."))

            if epoch_start <= event_date <= epoch_end:
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
