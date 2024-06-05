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

    db.session.commit()


def test_new_epoch(client, auth, epoch):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    data = {
        "start_date": "5016/01/01",
        "end_date": "5016/01/03",
        "title": "Test Epoch",
        "overview": "Epoch Overview",
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
