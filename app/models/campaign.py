from datetime import datetime

from app import db
from app.utils.sanitisers import sanitise_input



class Campaign(db.Model):
    __tablename__ = "campaign"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250))
    description = db.Column(db.String(500), nullable=False)
    last_edited = db.Column(db.DateTime, nullable=False)
    date_suffix = db.Column(db.String(8), nullable=True)
    negative_date_suffix = db.Column(db.String(8), nullable=True)

    # Database relationships
    # A campaign has a number of participating users, and is made up of a number of events. Users may have editing
    # permission. 
    events = db.relationship("Event", 
                             back_populates="parent_campaign", 
                             cascade="delete, delete-orphan")
    epochs = db.relationship("Epoch", 
                             back_populates="parent_campaign", 
                             cascade="delete, delete-orphan")
    pending_invites = db.relationship("Message", 
                                      back_populates="target_campaign", 
                                      cascade="delete, delete-orphan")
    admins = db.relationship("User",
                             secondary="user_edit_permissions",
                             back_populates="permissions")
    # Many-to-many relationship to User, bypassing the `UserCampaign` class
    members = db.relationship("User",
                              secondary="user_campaign",
                              back_populates="campaigns",)
    # Association between Child -> Association -> Parent
    user_associations = db.relationship("UserCampaign",
                                        back_populates="campaign",
                                        cascade="delete, delete-orphan",
                                        viewonly=True)
    
    # Methods
    def update(self, form, new=False):
        """ Method to populate and update self.
            Takes form data from request.form.
            Set "new" to true if creating new entry. """
        
        for field, value in form.items():
            if value is not None:

                if field == "description":
                    value = sanitise_input(value)

                setattr(self, field, value)

        self.last_edited = datetime.now()

        if new:
            db.session.add(self)

        db.session.commit()

    
    def check_epochs(self):
        """ Method to clear and recheck all epochs for containing
            events. """
        
        for epoch in self.epochs:
            epoch.populate_self()


    def get_following_events(self):
        """ Method to iterate through all events, defining relationship to
            the event that immediately follows it. The backref can be used
            to access the preceding event. """

        sorted_campaign_events = sorted(self.events, key=lambda event: event.date)

        for index, event in enumerate(sorted_campaign_events):

            # Ignore last event in timeline as it has no following event
            if index != len(sorted_campaign_events) - 1:
                event.following_event = sorted_campaign_events[index + 1]

        db.session.commit()
