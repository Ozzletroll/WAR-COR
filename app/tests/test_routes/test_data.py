from sqlalchemy import select
from flask import url_for
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

