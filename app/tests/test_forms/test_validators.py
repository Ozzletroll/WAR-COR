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


def test_date_is_after(client, validate_fixture):

    valid_data = {
        "start_year": 5016,
        "start_month": 1,
        "start_day": 5,
        "end_year": 5016,
        "end_month": 2,
        "end_day": 1,
    }

    invalid_data = {
        "start_year": 5016,
        "start_month": 1,
        "start_day": 5,
        "end_year": 5015,
        "end_month": 5,
        "end_day": 2,
    }

    valid_form = forms.CreateEpochForm()
    for key, value in valid_data.items():
        getattr(valid_form, key).data = value

    invalid_form = forms.CreateEpochForm()
    for key, value in invalid_data.items():
        getattr(invalid_form, key).data = value

    assert date_is_after(valid_form)
    assert not date_is_after(invalid_form)


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
