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
        "date": "5016/01/01 09:00:00",
        "location": "Test Location",
        "belligerents": "Belligerent 1, Belligerent 2",
        "body": "Test Body Text",
        "result": "Test Result",
        "header": False,
        "hide_time": False,
    }
    event_data_2 = {
        "type": "Test",
        "title": "Test Event 2",
        "date": "5016/01/02 09:00:00",
        "location": "Test Location",
        "belligerents": "Belligerent 1, Belligerent 2",
        "body": "Test Body Text",
        "result": "Test Result",
        "header": False,
        "hide_time": False,
    }
    epoch_data = {
        "start_date": "5016/01/01",
        "end_date": "5016/01/02",
        "title": "Test Epoch",
        "description": "Epoch description",
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

    # Convert JSON to BytesIO object, and then into a file-like object
    json_bytes = BytesIO(json.dumps(response_1.json).encode())
    file = FileStorage(stream=json_bytes, filename='data.json')
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

    for index, epoch in enumerate(campaign_object_1.epochs):
        assert epoch.start_date == campaign_object_2.epochs[index].start_date
        assert epoch.end_date == campaign_object_2.epochs[index].end_date