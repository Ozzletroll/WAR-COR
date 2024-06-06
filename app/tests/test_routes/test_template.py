from flask import url_for
import json

from app import db, models


def test_setup(client, auth, campaign):
    auth.register()
    campaign.create(title="Test Template Campaign",
                    description="A campaign for testing purposes")


def test_get_templates(client, auth):
    campaign_object = (db.session.query(models.Campaign)
                       .filter(models.Campaign.title == "Test Template Campaign")
                       .first())

    url = url_for("template.get_templates",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id)
    auth.login()
    response = client.get(url, follow_redirects=True)
    assert response.status_code == 200
    assert b'NO TEMPLATES' in response.data


def test_create_template(client, auth):
    campaign_object = (db.session.query(models.Campaign)
                       .filter(models.Campaign.title == "Test Template Campaign")
                       .first())

    url = url_for("template.create_template",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id)

    data = {
        "template_name": "Test Template",
        "format": [
            {"title": "Field Title 1",
             "value": "Field text 1",
             "field_type": "basic",
             "is_full_width": False},

            {"title": "Field Title 1",
             "value": "Field text 2",
             "field_type": "html",
             "is_full_width": False}
        ],
    }
    json_data = json.dumps(data)

    auth.login()
    response = client.post(url, data=json_data, content_type="application/json")
    assert response.status_code == 200
    assert b'New template created' in response.data

    template_object = (db.session.query(models.Template)
                       .filter(models.Template.name == "Test Template")
                       .first())
    assert template_object
    assert template_object.name == "Test Template"
    assert template_object.parent_campaign == campaign_object
    assert template_object.field_format == data["format"]


def test_import_template(client, auth, campaign):
    template_object = (db.session.query(models.Template)
                       .filter(models.Template.name == "Test Template")
                       .first())

    share_code = template_object.share_code

    auth.login()
    campaign.create(title="Second Test Campaign",
                    description="A campaign to test template importing")

    new_campaign_object = (db.session.query(models.Campaign)
                           .filter(models.Campaign.title == "Second Test Campaign")
                           .first())

    url = url_for("template.import_template",
                  campaign_name=new_campaign_object.title,
                  campaign_id=new_campaign_object.id)
    data = {
        "share_code": share_code
    }
    response_1 = client.post(url,
                             data=json.dumps(data),
                             content_type="application/json")
    assert response_1.status_code == 200
    assert b'Template imported' in response_1.data

    duplicated_template = (db.session.query(models.Template)
                           .filter(models.Template.origin_id == template_object.id)
                           .first())
    assert duplicated_template in new_campaign_object.templates

    # Check reimporting same template fails
    response_2 = client.post(url,
                             data=json.dumps(data),
                             content_type="application/json")
    assert response_2.status_code == 200
    assert b'Template already imported' in response_2.data
    assert len(new_campaign_object.templates) == 1


def test_delete_template(client, auth):
    campaign_object = (db.session.query(models.Campaign)
                       .filter(models.Campaign.title == "Second Test Campaign")
                       .first())
    template = (db.session.query(models.Template)
                .filter(models.Template.campaign_id == campaign_object.id)
                .first())
    auth.login()

    url = url_for("template.delete_template",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id)
    data = {
        "template_id": template.id,
    }
    response = client.delete(url,
                             data=json.dumps(data),
                             content_type="application/json")
    assert response.status_code == 200
    assert template not in campaign_object.templates


def test_load_template(client, auth):
    campaign_object = (db.session.query(models.Campaign)
                       .filter(models.Campaign.title == "Test Template Campaign")
                       .first())
    template = (db.session.query(models.Template)
                .filter(models.Template.campaign_id == campaign_object.id)
                .first())
    auth.login()

    url = url_for("template.load_template",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id)
    data = {
        "template_id": template.id,
    }
    headers = {
        "Content-Type": "application/json",
        "Referer": url_for("event.add_event",
                           campaign_name=campaign_object.title,
                           campaign_id=campaign_object.id),
    }
    response_1 = client.post(url,
                             data=json.dumps(data),
                             headers=headers,
                             follow_redirects=True)
    assert response_1.status_code == 200
    assert f"template_id={template.id}" in response_1.request.url

    # Test loading of nonexistent template
    data = {
        "template_id": 4,
    }
    response_2 = client.post(url,
                             data=json.dumps(data),
                             headers=headers,
                             follow_redirects=True)
    assert response_2.status_code == 404
