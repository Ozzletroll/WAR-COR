from sqlalchemy import select
import json
from werkzeug.datastructures import MultiDict

from app import db, models
from app.forms.forms import CreateEventForm


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

    event_form = CreateEventForm(
        MultiDict({
            "type": "Test",
            "title": "Test Event",
            "year": 5016,
            "month": 1,
            "day": 2,
            "hour": 9,
            "minute": 0,
            "second": 0,
            "dynamic_fields-0-title": "Title 1",
            "dynamic_fields-0-value": "Value 1",
            "dynamic_fields-0-is_full_width": False,
            "dynamic_fields-0-field_type": "basic",
            "dynamic_fields-1-title": "Title 2",
            "dynamic_fields-1-value": "Value 2",
            "dynamic_fields-1-is_full_width": False,
            "dynamic_fields-1-field_type": "basic",
            "hide_time": False,
        })).data

    event.update(form=event_form,
                 parent_campaign=campaign_object,
                 new=True)

    for field in event_form:
        assert getattr(event, field) == event_form[field]


def test_map_dynamic_field_data(client):
    # Case 1, correct data
    test_data_1 = [{"title": "Title 1",
                    "value": "Value 1",
                    "is_full_width": False,
                    "field_type": "basic"}]

    event = models.Event()

    test_1 = event.map_dynamic_field_data(test_data_1)
    assert test_1 == test_data_1

    # Case 2, disallowed html in value
    test_data_2 = [{"title": "Title 2",
                    "value": "<script>install_virus.exe</script>",
                    "is_full_width": False,
                    "field_type": "html"}]

    test_2 = event.map_dynamic_field_data(test_data_2)
    assert test_2 == [{"title": "Title 2",
                       "value": "",
                       "is_full_width": False,
                       "field_type": "html"}]

    # Case 3, correct composite field format
    composite_data = json.dumps(
        [{"entries": ["Entry 1", "Entry 2"],
          "position": "1",
          "title": "Group 1"}])

    test_data_3 = [{"title": "Title 3",
                    "value": composite_data,
                    "is_full_width": False,
                    "field_type": "composite"}]

    test_3 = event.map_dynamic_field_data(test_data_3)
    assert test_3 == [{"title": "Title 3",
                       "value": [{"entries": ["Entry 1", "Entry 2"],
                                  "position": "1",
                                  "title": "Group 1"}],
                       "is_full_width": False,
                       "field_type": "composite"}]

    # Case 4, incorrect composite field format
    composite_data = json.dumps(
        [{"entries": ["Entry 1", "Entry 2"],
          "incorrect name": "1",
          "title": "Group 1"}])

    test_data_4 = [{"title": "Title 3",
                    "value": composite_data,
                    "is_full_width": False,
                    "field_type": "composite"}]

    test_4 = event.map_dynamic_field_data(test_data_4)
    assert test_4 == [{"title": "Title 3",
                       "value": [],
                       "is_full_width": False,
                       "field_type": "composite"}]


def test_create_blank(client):

    data = {
        "year": 5016,
        "month": 1,
        "day": 1,
        "hour": 12,
        "minute": 0,
        "second": 0
    }

    event = models.Event()
    event.create_blank(date_values=data)

    assert event.title == ""
    assert event.type == ""
    for attribute, value in data.items():
        assert getattr(event, attribute) == value


def test_set_date(client):

    event = models.Event()
    event.year = 5016
    event.month = 1
    event.day = 1
    event.hour = 12
    event.minute = 0
    event.second = 0

    output = event.set_date()
    assert output == "5016/01/01 12:00:00"


def test_set_url_title(client):
    event = models.Event()
    event.title = "Event Title"
    event.set_url_title()

    assert event.url_title == "Event-Title"
