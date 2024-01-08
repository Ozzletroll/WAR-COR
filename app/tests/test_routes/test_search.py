from sqlalchemy import select
from flask import url_for

from app import db
from app import models


def test_advanced_search(client, auth, campaign, event):

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

    event.create(campaign_object, event_data_1)

    url = url_for("search.advanced_search",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id)

    # Test page is accessible
    response_1 = client.get(url, follow_redirects=True)
    assert response_1.status_code == 200

    # Test search returns event
    search_data = {
        "search": "Test Location"
    }

    response_2 = client.post(url, data=search_data, follow_redirects=True)
    assert response_2.status_code == 200
    assert b'Test Event' in response_2.data
