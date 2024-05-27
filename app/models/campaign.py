from datetime import datetime

from app import db, cache
from app.utils.sanitisers import sanitise_input
import app.utils.organisers as organisers


class Campaign(db.Model):
    __tablename__ = "campaign"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(250))
    url_title = db.Column(db.String(250))
    image_url = db.Column(db.String(), nullable=True)
    description = db.Column(db.String(), nullable=False)
    last_edited = db.Column(db.DateTime, nullable=False)
    date_suffix = db.Column(db.String(8), nullable=True)
    negative_date_suffix = db.Column(db.String(8), nullable=True)
    system = db.Column(db.String(40), nullable=True)
    private = db.Column(db.Boolean(), default=False)
    accepting_applications = db.Column(db.Boolean(), default=False)
    comments = db.Column(db.String(), default="private")

    # Relationships
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
    templates = db.relationship("Template",
                                back_populates="parent_campaign",
                                cascade="delete, delete-orphan")
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
                    value = sanitise_input(value, allow_images=False)

                if field in ["image_url", "system"]:
                    if value == "":
                        value = None

                setattr(self, field, value)

        self.last_edited = datetime.now()
        self.clear_cache()
        self.set_url_title()

        if new:
            db.session.add(self)

        db.session.commit()

    def clear_cache(self):
        """ Method to clear any out of date cached data. """
    
        cache.delete_memoized(self.return_timeline_data)

    def remove_user(self, user):
        """ Method to remove a given user from campaign """

        if user in self.members:
            self.members.remove(user)
        if user in self.admins:
            self.admins.remove(user)
        # If campaign left with no admins, upgrade all user to admin status
        if len(self.admins) == 0:
            for user in self.members:
                user.permissions.append(self)
            db.session.commit()
        #  Delete campaign if left with no members
        if len(self.members) == 0:
            db.session.delete(self)
            db.session.commit()

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

        # Clear old relationships
        for event in self.events:
            event.following_event = None
            
        db.session.commit()

        sorted_campaign_events = sorted(self.events, key=lambda event: event.date)

        for index, event in enumerate(sorted_campaign_events):

            # Ignore last event in timeline as it has no following event
            if index != len(sorted_campaign_events) - 1:
                event.following_event = sorted_campaign_events[index + 1]

        db.session.commit()

    def set_url_title(self):
        """ Method to set url safe version of title, replacing spaces
            with dashes '-'. """
        
        self.url_title = self.title.replace(" ", "-")

    @cache.memoize(900)
    def return_timeline_data(self, epoch=None):
        """ Method to return campaign timeline data """
        
        return organisers.campaign_sort(self, epoch)
