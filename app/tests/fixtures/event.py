from flask import url_for
from app.utils.formatters import increment_datestring


class EventActions(object):

    def __init__(self, client):
        self._client = client

    def create(self, campaign_object, data):

        url = url_for("event.add_event",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id)

        return self._client.post(url, data=data, follow_redirects=True)

    def edit(self, campaign_object, event_object, data):

        url = url_for("event.edit_event",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id,
                      event_name=event_object.title,
                      event_id=event_object.id)

        return self._client.post(url, data=data, follow_redirects=True)

    def create_comment(self, campaign_object, event_object, data):

        url = url_for("event.view_event",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id,
                      event_name=event_object.title,
                      event_id=event_object.id)

        return self._client.post(url, data=data, follow_redirects=True)

    def mass_create(self, campaign_object, number=1, increment="day"):

        all_events = []
        for index, value in enumerate(range(0, number)):
            if index == 0:
                new_event = EventFormat()
                all_events.append(new_event)
                self.create(campaign_object=campaign_object,
                            data=new_event.return_new_event_data())
            else:
                new_event = EventFormat(previous_event=all_events[index - 1],
                                        increment=increment)
                all_events.append(new_event)
                self.create(campaign_object=campaign_object,
                            data=new_event.return_new_event_data())


class EventFormat:
    """ Class for creating event model data, for easy mass event creation

            Methods:

                return_new_event_data(self, previous_event, increment):

                    Parameters:
                    ------------------------------------------------------------
                        previous_event : event model object
                            The event model of the event to increment over

                        increment: string
                            Either "month", "day" or "hour", to select at which
                            level of the date value to increment by 1
                    -------------------------------------------------------------

                    Returns a dict of event form data strings.
                    If given an event object as previous_event,
                    increments the title by 1, and the chosen date
                    unit by +1 day.

    """

    def __init__(self, previous_event=None, increment="day"):
        if previous_event:
            self.number = previous_event.number + 1
            self.title = f"Test Event {self.number}"
            if increment == "hour":
                self.date = increment_datestring(previous_event.date,
                                                 args={"new_hour": True})
            if increment == "day":
                self.date = increment_datestring(previous_event.date,
                                                 args={"new_day": True})
            elif increment == "month":
                self.date = increment_datestring(previous_event.date,
                                                 args={"new_month": True})
        else:
            self.number = 1
            self.title = f"Test Event {self.number}"
            self.date = "5016/01/01 00:00:00"
        self.type = "Test Event"
        self.location = "Location Name"
        self.belligerents = "Belligerent 1, Belligerent 2"
        self.body = "Example Description"
        self.result = "Result"
        self.header = False
        self.hide_time = False

    def return_new_event_data(self):
        return {
            attr: getattr(self, attr) for attr in dir(self)
            if not attr.startswith("__") and not attr.startswith("_")
            and not attr == "return_new_event_data"
            and not attr == "number"
        }
