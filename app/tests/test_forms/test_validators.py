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
