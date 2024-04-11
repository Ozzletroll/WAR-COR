from app.forms.validators import *
from app.forms import forms
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def validate_fixture():
    def _validate(validator, form_class, form_data, field_data):

        form = MagicMock(spec=form_class)
        for value in form_data:
            field = MagicMock()
            field.data = form_data[value]
            setattr(form, value, field)

        current_field = MagicMock()
        current_field.data = field_data

        validator(form, current_field)

    return _validate


def test_date_format(validate_fixture):
    correct_event_format = "5016/01/01 12:00:00"
    correct_epoch_format = "5016/01/01"
    incorrect_event_format = "5016/1/01 12:00:00"
    incorrect_epoch_format = "5016/0101"

    # Test that incorrect formats raise ValidationErrors
    with pytest.raises(ValidationError):
        validate_fixture(date_format("event"),
                         forms.CreateEventForm,
                         {"date": incorrect_event_format},
                         incorrect_event_format)

    with pytest.raises(ValidationError):
        validate_fixture(date_format("epoch"),
                         forms.CreateEventForm,
                         {"date": incorrect_epoch_format},
                         incorrect_epoch_format)

    # Test correct format passes
    validate_fixture(date_format("event"),
                     forms.CreateEventForm,
                     {"date": correct_event_format},
                     correct_event_format)

    validate_fixture(date_format("epoch"),
                     forms.CreateEventForm,
                     {"date": correct_epoch_format},
                     correct_epoch_format)


def test_file_format(validate_fixture):
    # Test that 6MB file raises ValidationError
    with pytest.raises(ValidationError):
        validate_fixture(file_format(),
                         forms.UploadJsonForm,
                         {},
                         type("obj", (object,), {"content_length": 6 * 1024 * 1024}))

    # Test that 3MB file passes
    validate_fixture(file_format(),
                     forms.UploadJsonForm,
                     {},
                     type("obj", (object,), {"content_length": 3 * 1024 * 1024}))


def test_image_url(validate_fixture):
    no_image_url = ""
    broken_image_url = "asd"
    non_image_url = "https://www.google.com/"
    correct_image_url = "https://massifpress.com/_next/image?url=%2Fimages%2Flancer%2Flancer-carousel.webp&w=1920&q=75"

    validate_fixture(image_url(),
                     forms.CreateCampaignForm,
                     {},
                     no_image_url)

    with pytest.raises(ValidationError):
        validate_fixture(image_url(),
                         forms.CreateCampaignForm,
                         {},
                         broken_image_url)

    with pytest.raises(ValidationError):
        validate_fixture(image_url(),
                         forms.CreateCampaignForm,
                         {},
                         non_image_url)

    validate_fixture(image_url(),
                     forms.CreateCampaignForm,
                     {},
                     correct_image_url)


def test_date_is_after(validate_fixture):
    with pytest.raises(ValidationError):
        validate_fixture(date_is_after(),
                         forms.CreateEpochForm,
                         form_data={"start_date": "5016/01/05",
                                    "end_date": "5015/12/04"},
                         field_data="5015/12/04")

    validate_fixture(date_is_after(),
                     forms.CreateEpochForm,
                     form_data={"start_date": "5016/01/05",
                                "end_date": "5016/02/11"},
                     field_data="5016/02/11")


def test_plain_text_length(validate_fixture):

    with pytest.raises(ValidationError):
        validate_fixture(plain_text_length(),
                         forms.CreateCampaignForm,
                         form_data={"description": "A" * 601},
                         field_data="A" * 601)

    validate_fixture(plain_text_length(),
                     forms.CreateCampaignForm,
                     form_data={"description": "A" * 480},
                     field_data="A" * 480)
