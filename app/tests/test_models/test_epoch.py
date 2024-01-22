from sqlalchemy import select

from app import db, models
from app.utils.formatters import increment_datestring


class EventFormat:

    def __init__(self, previous_event=None):
        if previous_event:
            self.number = previous_event.number + 1
            self.title = f"Test Event {self.number}"
            self.date = increment_datestring(previous_event.date,
                                             args={"new_day": True})
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


def test_epoch(client, auth, campaign, event, epoch):

    auth.register()
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    all_events = []
    for index, value in enumerate(range(0, 20)):
        if index == 0:
            new_event = EventFormat()
            all_events.append(new_event)
            event.create(campaign_object=campaign_object,
                         data=new_event.return_new_event_data())
        else:
            new_event = EventFormat(previous_event=all_events[index - 1])
            all_events.append(new_event)
            event.create(campaign_object=campaign_object,
                         data=new_event.return_new_event_data())

    event_query = db.session.execute(
        select(models.Event)
        .filter_by(campaign_id=campaign_object.id)).scalars()

    asd = list(event_query)

    assert len(list(event_query)) == 20
