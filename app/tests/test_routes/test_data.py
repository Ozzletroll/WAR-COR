from sqlalchemy import select
from flask import url_for
import json
from io import BytesIO
from werkzeug.datastructures import FileStorage

from app import db
from app import models


def test_backup_page(client, auth, campaign, epoch, event):

    auth.register()
    campaign.create(title="Backup Test Campaign",
                    description="A campaign to test backup functionality")

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Backup Test Campaign")).scalar()

    event_data_1 = {
        "type": "Test",
        "title": "Test Event",
        "year": 5016,
        "month": 1,
        "day": 1,
        "hour": 9,
        "minute": 0,
        "second": 0,
        "dynamic_fields": [],
        "hide_time": False,
    }
    event_data_2 = {
        "type": "Test",
        "title": "Test Event 2",
        "year": 5016,
        "month": 1,
        "day": 2,
        "hour": 9,
        "minute": 0,
        "second": 0,
        "dynamic_fields": [],
        "hide_time": False,
    }
    epoch_data = {
        "start_year": 5016,
        "start_month": 1,
        "start_day": 1,
        "end_year": 5016,
        "end_month": 1,
        "end_day": 2,
        "title": "Test Epoch",
        "overview": "Epoch overview",
        "dynamic_fields": [],
    }

    # Create basic campaign data
    event.create(campaign_object, data=event_data_1)
    event.create(campaign_object, data=event_data_2)
    epoch.create(campaign_object, data=epoch_data)

    url = url_for("data.backup_page",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id)

    # Test page is accessible
    response_1 = client.get(url, follow_redirects=True)
    assert response_1.status_code == 200


def test_backup_campaign(client, auth, campaign):

    auth.login()

    campaign_object_1 = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Backup Test Campaign")).scalar()

    # Test data is serialised as json correctly
    backup_url = url_for("data.campaign_backup",
                         campaign_name=campaign_object_1.title,
                         campaign_id=campaign_object_1.id)
    response_1 = client.get(backup_url, follow_redirects=True)
    assert response_1.status_code == 200
    assert response_1.headers["Content-Disposition"] == "attachment; filename=WAR_COR_Backup Backup Test Campaign"

    # Create new campaign and restore data from backup file
    campaign.create(title="Campaign To Restore To",
                    description="A campaign to test backup restoration")

    campaign_object_2 = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Campaign To Restore To")).scalar()

    # Restore data from campaign 1 to campaign 2
    restoration_url = url_for("data.backup_page",
                              campaign_name=campaign_object_2.title,
                              campaign_id=campaign_object_2.id)

    # # Convert JSON to BytesIO object, and then into a file-like object
    json_bytes = BytesIO(json.dumps(response_1.json, ensure_ascii=False).encode("utf8"))
    file = FileStorage(stream=json_bytes, filename="data.json")
    form_data = {
        "file": file
    }

    response_2 = client.post(restoration_url, data=form_data, follow_redirects=True)
    assert response_2.status_code == 200

    # Check that both campaigns have a matching structure
    assert campaign_object_1.title == campaign_object_2.title
    for index, event in enumerate(campaign_object_1.events):
        assert event.title == campaign_object_2.events[index].title
        assert event.date == campaign_object_2.events[index].date

    epoch_attributes = ["start_date", "end_date", "title", "overview"]
    event_attributes = ["title", "date", "hide_time"]

    for index, epoch in enumerate(campaign_object_1.epochs):
        # Check epoch attributes
        for attr in epoch_attributes:
            assert getattr(campaign_object_1.epochs[index], attr) == getattr(campaign_object_2.epochs[index], attr)
        # Check contained event attributes
        for event_index, event in enumerate(epoch.events):
            for attr in event_attributes:
                assert getattr(campaign_object_1.epochs[index].events[event_index], attr) \
                       == getattr(campaign_object_2.epochs[index].events[event_index], attr)
