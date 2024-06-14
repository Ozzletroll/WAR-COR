from sqlalchemy import select
from flask import url_for
from werkzeug.datastructures import MultiDict
from bs4 import BeautifulSoup

from app import db, models
from app.forms.forms import CreateEpochForm

TEST_PASSWORD = "123456768"


def test_setup(client, auth, campaign):
    # Create test users
    auth.register(email="testemail1@email.com",
                  username="Admin",
                  password=TEST_PASSWORD)
    auth.logout()

    # Create test campaign
    auth.login(username="Admin", password=TEST_PASSWORD)
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")

    db.session.commit()


def test_new_epoch(client, auth, epoch):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    # Test epoch form data
    # None values are used to represent False boolean checkbox values
    epoch_form = MultiDict({
        "title": "Test Epoch",
        "start_year": 5016,
        "start_month": 1,
        "start_day": 1,
        "end_year": 5016,
        "end_month": 1,
        "end_day": 3,
        "overview": "Epoch Overview",
        "dynamic_fields-0-title": "Field 1 Title",
        "dynamic_fields-0-value": "Value 1",
        "dynamic_fields-0-is_full_width": "",
        "dynamic_fields-0-field_type": "basic",
        "dynamic_fields-1-title": "Field 2 Title",
        "dynamic_fields-1-value": "Value 2",
        "dynamic_fields-1-is_full_width": "",
        "dynamic_fields-1-field_type": "basic",
    })

    # Test that unauthenticated user cannot access route
    response_1 = epoch.create(campaign_object, epoch_form)
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>' in response_1.data

    # Test that campaign admin can create epoch
    auth.login(username="Admin", password=TEST_PASSWORD)
    response_2 = epoch.create(campaign_object, epoch_form)
    assert response_2.status_code == 200

    # Test that epoch data matches expected values
    epoch_object = db.session.execute(
        select(models.Epoch)
        .filter_by(title="Test Epoch")).scalar()
    assert epoch_object is not None
    assert epoch_object in campaign_object.epochs

    for attribute, value in CreateEpochForm(epoch_form).data.items():
        try:
            getattr(epoch_object, attribute)
        except AttributeError:
            continue

        if attribute == "overview":
            assert getattr(epoch_object, attribute) == "<p>" + value + "</p>"
        else:
            assert getattr(epoch_object, attribute) == value

    # Test that passing date url parameter pre-populates form correctly
    url = url_for("epoch.new_epoch",
                  campaign_name=campaign_object.url_title,
                  campaign_id=campaign_object.id,
                  date="5016/01/01")
    response_3 = client.get(url)
    assert response_3.status_code == 200
    soup = BeautifulSoup(response_3.data, "html.parser")
    input_elements = soup.find_all(class_="form-date-input")
    values = [input_element.get("value") for input_element in input_elements]
    assert values == ["5016", "01", "01", "5016", "01", "01"]


def test_view_epoch(client, auth, epoch):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    epoch_object = db.session.execute(
        select(models.Epoch)
        .filter_by(title="Test Epoch")).scalar()

    url = url_for("epoch.view_epoch",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id,
                  epoch_title=epoch_object.title,
                  epoch_id=epoch_object.id)

    response = client.get(url)
    assert response.status_code == 200
    assert b'Test Epoch' in response.data


def test_edit_epoch(client, auth, epoch):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    epoch_object = db.session.execute(
        select(models.Epoch)
        .filter_by(title="Test Epoch")).scalar()

    data = {
        "start_date": "5017/01/01",
        "end_date": "5017/01/03",
        "title": "Test Epoch Edited",
        "overview": "Overview Text",
    }

    # Test that epoch can be edited
    auth.login(username="Admin", password=TEST_PASSWORD)
    response_1 = epoch.edit(campaign_object,
                            epoch_object,
                            data=data)
    assert response_1.status_code == 200

    epoch_object_edited = db.session.execute(
        select(models.Epoch)
        .filter_by(title="Test Epoch Edited")).scalar()

    assert epoch_object_edited is not None
    assert epoch_object_edited.title == "Test Epoch Edited"


def test_delete_epoch(client, auth, epoch):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    epoch_object_edited = db.session.execute(
        select(models.Epoch)
        .filter_by(title="Test Epoch Edited")).scalar()

    # Test epoch can be deleted
    auth.login(username="Admin", password=TEST_PASSWORD)
    response_1 = epoch.delete(campaign_object,
                              epoch_object_edited)
    assert response_1.status_code == 200

    epoch_object_edited = db.session.execute(
        select(models.Epoch)
        .filter_by(title="Test Epoch Edited")).scalar()

    assert epoch_object_edited is None
    assert len(campaign_object.epochs) == 0
