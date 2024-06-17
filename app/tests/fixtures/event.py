from flask import url_for
from app.utils.formatters import increment_date, split_date
from app.forms.forms import CreateEventForm


class EventActions(object):

    def __init__(self, client):
        self._client = client

    def create(self, campaign_object, data, no_redirect=False):

        url = url_for("event.add_event",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id)

        event_form = CreateEventForm()
        for field in event_form:
            if field.name not in data:
                data[field.name] = ""

        if no_redirect:
            return self._client.post(url, data=data, follow_redirects=False)
        else:
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

    def mass_create(self,
                    campaign_object,
                    number=1,
                    starting_date="5016/01/01 00:00:00",
                    increment="day"):

        all_events = []
        for index, value in enumerate(range(0, number)):
            if index == 0:
                new_event = EventFormat(starting_date=starting_date)
                all_events.append(new_event)
                self.create(campaign_object=campaign_object,
                            data=new_event.return_new_event_data(),
                            no_redirect=True)
            else:
                new_event = EventFormat(previous_event=all_events[index - 1],
                                        starting_date=starting_date,
                                        increment=increment)
                all_events.append(new_event)
                self.create(campaign_object=campaign_object,
                            data=new_event.return_new_event_data(),
                            no_redirect=True)


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

    def __init__(self,
                 previous_event=None,
                 starting_date="5016/01/01 00:00:00",
                 increment="day"):

        if previous_event:
            self.number = previous_event.number + 1
            self.title = f"Test Event {self.number}"

            if increment == "hour":
                new_date = increment_date(datestring=previous_event.date,
                                          args={"new_hour": True})
                for attribute, value in new_date.items():
                    setattr(self, attribute, value)
                self.date = self.set_date(new_date)
            if increment == "day":
                new_date = increment_date(datestring=previous_event.date,
                                          args={"new_day": True})
                for attribute, value in new_date.items():
                    setattr(self, attribute, value)
                self.date = self.set_date(new_date)
            elif increment == "month":
                new_date = increment_date(datestring=previous_event.date,
                                          args={"new_month": True})
                for attribute, value in new_date.items():
                    setattr(self, attribute, value)
                self.date = self.set_date(new_date)
        else:
            self.number = 1
            self.title = f"Test Event {self.number}"

            attribute_names = ["year", "month", "day", "hour", "minute", "second"]
            date_parts = dict(zip(attribute_names, split_date(starting_date)))
            for attribute, value in date_parts.items():
                setattr(self, attribute, value)
            self.date = self.set_date(date_parts)

        self.type = "Test Event"
        self.header = False
        self.hide_time = False

    @staticmethod
    def set_date(date_parts):
        """ Method that formats date as string """

        date = f"{date_parts['year']}/{str(date_parts['month']).zfill(2)}/{str(date_parts['day']).zfill(2)}"
        time = f"{str(date_parts['hour']).zfill(2)}:{str(date_parts['minute']).zfill(2)}:{str(date_parts['second']).zfill(2)}"

        return date + " " + time

    def return_new_event_data(self):
        return {
            attr: getattr(self, attr) for attr in dir(self)
            if not attr.startswith("__") and not attr.startswith("_")
               and not attr == "return_new_event_data"
               and not attr == "number"
        }
