from sqlalchemy import select
import json

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
        "dynamic_fields": [{"title": "Title 1",
                            "value": "Value 1",
                            "is_full_width": False,
                            "field_type": "basic"}],
        "hide_time": False,
    }
    event.update(form=event_form,
                 parent_campaign=campaign_object,
                 new=True)

    for field in event_form.keys():
        if field == "body":
            assert event_form[field] in getattr(event, field)
        else:
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
    event = models.Event()
    event.create_blank(datestring="5016/01/01 12:00:00")

    assert event.title == ""
    assert event.type == ""
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


def test_set_url_title(client):
    event = models.Event()
    event.title = "Event Title"
    event.set_url_title()

    assert event.url_title == "Event-Title"
