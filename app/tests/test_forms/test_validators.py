from app.forms.validators import *
import pytest


@pytest.fixture
def validate_fixture():
    def _validate(validator, form_data, field_data):
        class MockForm:
            data = form_data

        class MockField:
            data = field_data

        form = MockForm()
        field = MockField()

        validator(form, field)

    return _validate


def test_date_format(validate_fixture):

    correct_event_format = "5016/01/01 12:00:00"
    correct_epoch_format = "5016/01/01"
    incorrect_event_format = "5016/1/01 12:00:00"
    incorrect_epoch_format = "5016/0101"

    # Test that incorrect formats raise ValidationErrors
    with pytest.raises(ValidationError):
        validate_fixture(date_format("event"),
                         {"date": incorrect_event_format},
                         incorrect_event_format)

    with pytest.raises(ValidationError):
        validate_fixture(date_format("epoch"),
                         {"date": incorrect_epoch_format},
                         incorrect_epoch_format)

    # Test correct format passes
    validate_fixture(date_format("event"),
                     {"date": correct_event_format},
                     correct_event_format)

    validate_fixture(date_format("epoch"),
                     {"date": correct_epoch_format},
                     correct_epoch_format)


def test_file_format(validate_fixture):

    # Test that 6MB file raises ValidationError
    with pytest.raises(ValidationError):
        validate_fixture(file_format(),
                         {},
                         type("obj", (object,), {"content_length": 6 * 1024 * 1024}))

    # Test that 3MB file passes
    validate_fixture(file_format(),
                     {},
                     type("obj", (object,), {"content_length": 3 * 1024 * 1024}))


def test_image_url(validate_fixture):

    no_image_url = ""
    broken_image_url = "asd"
    non_image_url = "https://www.google.com/"
    correct_image_url = "https://massifpress.com/_next/image?url=%2Fimages%2Flancer%2Flancer-carousel.webp&w=1920&q=75"

    validate_fixture(image_url(),
                     {},
                     no_image_url)

    with pytest.raises(ValidationError):
        validate_fixture(image_url(),
                         {},
                         broken_image_url)

    with pytest.raises(ValidationError):
        validate_fixture(image_url(),
                         {},
                         non_image_url)

    validate_fixture(image_url(),
                     {},
                     correct_image_url)
