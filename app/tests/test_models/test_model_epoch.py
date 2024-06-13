from sqlalchemy import select
from werkzeug.datastructures import MultiDict

from app import db, models
from app.forms.forms import CreateEpochForm


def test_setup(client, auth, campaign, event):
    # Create a new campaign and populate it with events
    auth.register()
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    # Create 4 months with 10 events each, incremented by +1 day
    for value in range(1, 5):
        event.mass_create(campaign_object=campaign_object,
                          starting_date=f"5016/0{value}/01 00:00:00",
                          number=10,
                          increment="day")


def test_update(client):
    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    # Create a new epoch
    epoch = models.Epoch()

    # Update the epoch
    epoch_form = CreateEpochForm(
        MultiDict({
            "title": "Updated Epoch",
            "start_year": 5016,
            "start_month": 1,
            "start_day": 2,
            "end_year": 5016,
            "end_month": 2,
            "end_day": 2,
            "overview": "Overview Text",
            "dynamic_fields-0-title": "Title 1",
            "dynamic_fields-0-value": "Value 1",
            "dynamic_fields-0-is_full_width": False,
            "dynamic_fields-0-field_type": "basic",
            "dynamic_fields-1-title": "Title 2",
            "dynamic_fields-1-value": "Value 2",
            "dynamic_fields-1-is_full_width": False,
            "dynamic_fields-1-field_type": "basic",
        })).data

    epoch.update(epoch_form,
                 parent_campaign=campaign_object,
                 new=True)

    for field in epoch_form:
        if field == "overview":
            assert getattr(epoch, field) == "<p>Overview Text</p>"
        else:
            assert getattr(epoch, field) == epoch_form[field]


def test_map_dynamic_fields():
    epoch = models.Epoch()

    input_value = [
        {
            "title": "Test Title",
            "value": "<script>virus.exe</script> Text that needs to be sanitised and wrapped in p tags",
            "field_type": "html",
            "is_full_width": "incorrect data type"
        },
        {
            "title": "Test Title 2",
            "value": [
                {
                    "entries": [
                        "ENTRY 1",
                    ],
                    "position": "1",
                    "title": "Allies"
                },
                {
                    "entries": [
                        "ENTRY 1",
                    ],
                    "position": "2",
                    "title": "Enemies"
                }
            ],
            "field_type": "composite",
            "is_full_width": True
        }
    ]

    expected_output = [
        {
            "title": "Test Title",
            "value": "<p> Text that needs to be sanitised and wrapped in p tags</p>",
            "field_type": "html",
            "is_full_width": False
        },
        {
            "title": "Test Title 2",
            "value": [
                {
                    "entries": [
                        "ENTRY 1",
                    ],
                    "position": "1",
                    "title": "Allies"
                },
                {
                    "entries": [
                        "ENTRY 1",
                    ],
                    "position": "2",
                    "title": "Enemies"
                }
            ],
            "field_type": "composite",
            "is_full_width": True
        }
    ]
    output = epoch.map_dynamic_field_data(input_value)
    assert output == expected_output


def test_set_date():

    epoch = models.Epoch()
    output = epoch.set_date(5016, 1, 5)
    assert output == "5016/01/05"


def test_set_url_title():
    # Create a new epoch
    epoch = models.Epoch()
    epoch.title = "Test Epoch"
    epoch.set_url_title()

    # Verify the url_title has been set correctly
    assert epoch.url_title == "Test-Epoch"


def test_create_blank():

    date_values = [5016, 1, 1]

    epoch = models.Epoch()
    epoch.create_blank(date_values)

    assert epoch.start_year == 5016
    assert epoch.start_month == 1
    assert epoch.start_day == 1
    assert epoch.end_year == 5016
    assert epoch.end_month == 1
    assert epoch.end_day == 1


def test_populate_self(client, auth, epoch):
    auth.login()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    epoch_form = CreateEpochForm(
        MultiDict({
            "title": "Valid Epoch",
            "start_year": 5016,
            "start_month": 1,
            "start_day": 5,
            "end_year": 5016,
            "end_month": 2,
            "end_day": 1,
            "overview": "Overview Text",
        })).data
    epoch.create(campaign_object, epoch_form)

    epoch_object = db.session.execute(
        select(models.Epoch)
        .filter_by(title="Valid Epoch")).scalar()

    for event in epoch_object.events:
        assert epoch_object.has_events is True
        assert event.date.startswith("5016/01") or event.date.startswith("5016/02")
        if event.date.startswith("5016/01"):
            assert event.day >= epoch_object.start_day
        elif event.date.startswith("5016/02"):
            assert event.day <= epoch_object.end_day
