from app.utils.sanitisers import sanitise_input, sanitise_json, sanitise_share_code
from app.models import Template


def test_sanitise_input():

    value = '<img src="image.jpg"/>'
    expected_output = '<img src="image.jpg"/>'
    assert sanitise_input(value, allow_images=True) == expected_output

    value = '<img src="image.jpg"/>'
    expected_output = ''
    assert sanitise_input(value, allow_images=False) == expected_output

    value = '<script>Text with disallowed tag</script>'
    expected_output = ''
    assert sanitise_input(value) == expected_output

    value = "Text without tags"
    expected_output = "<p>Text without tags</p>"
    assert sanitise_input(value) == expected_output

    value = "Message body that shouldn't have p tags"
    expected_output = "Message body that shouldn't have p tags"
    assert sanitise_input(value, wrap=False) == expected_output

    value = '<a href="http://www.google.com">LINK TEXT</a>'
    expected_output = '<a href="http://www.google.com" rel="noopener noreferrer nofollow">LINK TEXT</a>'
    assert sanitise_input(value, wrap=False) == expected_output


def test_sanitise_json():

    composite_field_valid_test_data = [
        {
            "title": "Test Title 1",
            "position": "Test Position 1",
            "entries": ["Entry 1", "Entry 2"]
        },
        {
            "title": "Test Title 2",
            "position": "Test Position 2",
            "entries": ["Entry 3", "Entry 4"]
        }
    ]
    composite_field_invalid_test_data = [
        {
            "title": "Test Title 1",
            "entries": ["Entry 1", "Entry 2"]
        },
        {
            "title": "Test Title 2",
            "position": "Test Position 2",
            "entries": ["Entry 3", "Entry 4"]
        }
    ]
    # Check test data validates
    # Invalid json data is replaced with an empty string
    assert sanitise_json(composite_field_valid_test_data, "composite_field") != ""
    assert sanitise_json(composite_field_invalid_test_data, "composite_field") == ""

    template_valid_test_data = [
        {
            "title": "Test Title 1",
            "value": "Test Value 1",
            "field_type": "Test Field Type 1",
            "is_full_width": True
        },
        {
            "title": "Test Title 2",
            "value": None,
            "field_type": "Test Field Type 2",
            "is_full_width": False
        },
        {
            "title": "Test Title 3",
            "value": "Test Value 3",
            "field_type": "Test Field Type 3",
            "is_full_width": None
        }
    ]
    template_invalid_test_data = [
        {
            "title": "Test Title 1",
            "value": "Test Value 1",
            "field_type": "Test Field Type 1",
            "is_full_width": "True"
        },
        {
            "title": "Test Title 2",
            "value": None,
            "field_type": "Test Field Type 2",
            "is_full_width": False
        },
        {
            "title": "Test Title 3",
            "field_type": "Test Field Type 3",
            "is_full_width": None
        }
    ]
    assert sanitise_json(template_valid_test_data, "template") != ""
    assert sanitise_json(template_invalid_test_data, "template") == ""

    dynamic_field_valid_test_data = [
        {
            "title": "Test Title",
            "value": "Test Value",
            "field_type": "Test Field Type",
            "is_full_width": True
        }
    ]
    dynamic_field_invalid_test_data = [
        {
            "title": "Test Title",
            "field_type": "Test Field Type",
            "is_full_width": True
        }
    ]

    backup_valid_test_data = {
        "campaign_data": {
            "title": "Campaign Title",
            "description": "Campaign Description",
            "image_url": "https://example.com/image.jpg",
            "date_suffix": "st",
            "negative_date_suffix": "nd",
            "system": "Test System"
        },
        "events": [
            {
                "type": "Event Type",
                "title": "Event Title",
                "date": {
                    "year": 2024,
                    "month": 6,
                    "day": 7,
                    "hour": 0,
                    "minute": 0,
                    "second": 0,
                },
                "hide_time": False,
                "dynamic_fields": dynamic_field_valid_test_data
            }
        ],
        "epochs": [
            {
                "title": "Epoch Title",
                "start_date": {
                    "start_year": 2024,
                    "start_month": 6,
                    "start_day": 1,
                },
                "end_date": {
                    "end_year": 2024,
                    "end_month": 6,
                    "end_day": 30,
                },
                "overview": "Epoch Overview",
                "dynamic_fields": dynamic_field_valid_test_data
            }
        ]
    }
    backup_invalid_test_data = {
        "campaign_data": {
            "title": "Campaign Title",
            "description": "Campaign Description",
            "image_url": "https://example.com/image.jpg",
            "date_suffix": "st",
            "negative_date_suffix": "nd",
            "system": "Test System"
        },
        "events": [
            {
                "type": "Event Type",
                "title": "Event Title",
                "date": "2024-06-07",
                "hide_time": False,
                "dynamic_fields": dynamic_field_invalid_test_data
            }
        ],
        "epochs": [
            {
                "title": "Epoch Title",
                "start_date": "2024-06-01",
                "end_date": "2024-06-30",
                "overview": "Epoch Overview",
                "dynamic_fields": dynamic_field_invalid_test_data
            }
        ]
    }

    assert sanitise_json(backup_valid_test_data, "backup") != ""
    assert sanitise_json(backup_invalid_test_data, "backup") == ""


def test_sanitise_share_code():

    valid_share_code = Template().generate_share_code()
    invalid_share_code = "An invalid share code"

    assert sanitise_share_code(valid_share_code) != ""
    assert sanitise_share_code(invalid_share_code) == ""
