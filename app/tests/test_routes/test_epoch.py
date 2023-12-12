from sqlalchemy import select
from flask import url_for
from app import db
from app import models

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

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    db.session.commit()


def test_new_epoch(client, auth, epoch):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    data = {
        "start_date": "5016/01/01",
        "end_date": "5016/01/03",
        "title": "Test Epoch",
        "description": "Epoch description",
    }

    # Test that unauthenticated user cannot access route
    response_1 = epoch.create(campaign_object, data)
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>' in response_1.data

    # Test that campaign admin can create epoch
    auth.login(username="Admin", password=TEST_PASSWORD)
    response_2 = epoch.create(campaign_object, data)
    assert response_2.status_code == 200

    epoch_object = db.session.execute(
        select(models.Epoch)
        .filter_by(title="Test Epoch")).scalar()
    assert epoch_object is not None
    assert epoch_object in campaign_object.epochs


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
        "description": "Epoch description edited",
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
