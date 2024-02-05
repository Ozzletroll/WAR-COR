from sqlalchemy import select

from app import db, models


def test_setup(client, auth, campaign, event):
    # Create a new campaign and populate it with events
    auth.register()
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")


def test_update(client):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    event = models.Event()
    event_form = {
        "type": "Test",
        "title": "Test Event",
        "date": "5016/01/01 09:00:00",
        "location": "Location",
        "belligerents": "Belligerent 1, Belligerent 2",
        "body": "Test Body Text",
        "result": "Test Result",
        "header": False,
        "hide_time": False,
    }
    event.update(form=event_form,
                 parent_campaign=campaign_object,
                 new=True)

    for field in event_form.keys():
        assert getattr(event, field) == event_form[field]


def test_create_blank(client):

    event = models.Event()
    event.create_blank(datestring="5016/01/01 12:00:00")

    assert event.title == ""
    assert event.type == ""
    assert event.body == ""
    assert event.date == "5016/01/01 12:00:00"


def test_split_date(client):

    event = models.Event()
    event.split_date(datestring="5016/01/01 12:00:00")

    assert event.year == 5016
    assert event.month == 1
    assert event.day == 1
    assert event.hour == 12
    assert event.minute == 0
    assert event.second == 0


def test_separate_belligerents(client):

    event_1 = models.Event()
    event_1.belligerents = "Group 1 & Group 2, Group 3"

    belligerents_1 = event_1.separate_belligerents()
    # Assert two vs groups
    assert len(belligerents_1) == 2
    # Assert group's 1 and 2 in first list
    assert len(belligerents_1[0]) == 2
    assert belligerents_1[0][0] == "Group 1"
    assert belligerents_1[0][1] == "Group 2"
    # Assert group 2 in second list
    assert len(belligerents_1[1]) == 1
    assert belligerents_1[1][0] == "Group 3"

    event_2 = models.Event()
    event_2.belligerents = "Group 1, Group 2, Group 3, Group 4"
    belligerents_2 = event_2.separate_belligerents()
    # Assert four vs groups of 1 belligerent
    assert len(belligerents_2) == 4
    for group in belligerents_2:
        assert len(group) == 1
    assert belligerents_2[0][0] == "Group 1"
    assert belligerents_2[1][0] == "Group 2"
    assert belligerents_2[2][0] == "Group 3"
    assert belligerents_2[3][0] == "Group 4"


def test_set_url_title(client):

    event = models.Event()
    event.title = "Event Title"
    event.set_url_title()

    assert event.url_title == "Event-Title"
