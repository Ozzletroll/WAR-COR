from sqlalchemy import select
from flask import url_for
from werkzeug.datastructures import MultiDict

from app import db
from app import models


def test_advanced_search(client, auth, campaign, event):

    auth.register()
    campaign.create(title="Backup Test Campaign",
                    description="A campaign to test backup functionality")

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Backup Test Campaign")).scalar()

    # Use MultiDict to mimic dynamic form
    # None values are used to represent False boolean checkbox values
    event_form = MultiDict({
        "title": "Test Event",
        "type": "Test",
        "year": 5016,
        "month": 1,
        "day": 1,
        "hour": 9,
        "minute": 0,
        "second": 0,
        "hide_time": "",
        "dynamic_fields-0-title": "Field 1 Title",
        "dynamic_fields-0-value": "Lorem ipsum",
        "dynamic_fields-0-is_full_width": "",
        "dynamic_fields-0-field_type": "basic",
        "dynamic_fields-1-title": "Field 2 Title",
        "dynamic_fields-1-value": "Different value",
        "dynamic_fields-1-is_full_width": "",
        "dynamic_fields-1-field_type": "basic",
    })

    event.create(campaign_object, event_form)

    url = url_for("search.advanced_search",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id)

    # Test page is accessible
    response_1 = client.get(url, follow_redirects=True)
    assert response_1.status_code == 200

    # Test search returns event
    search_data = {
        "search": "Lorem ips"
    }

    response_2 = client.post(url, data=search_data, follow_redirects=True)
    assert response_2.status_code == 200
    assert b'Test Event' in response_2.data and b'Matching fields: Field 1 Title' in response_2.data
