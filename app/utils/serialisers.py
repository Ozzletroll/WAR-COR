from flask import jsonify, make_response, flash
import json

from app import db, models



def data_export(campaign):
    """Serialise campaign object as json file for export"""

    events_data = []
    for event in campaign.events:
        event_dict = {"type": event.type,
                      "title": event.title,
                      "date": event.date,
                      "hide_time": event.hide_time,
                      "dynamic_fields": event.dynamic_fields, }

        events_data.append(event_dict)

    epoch_data = []
    for epoch in campaign.epochs:
        epoch_dict = {"title": epoch.title,
                      "start_date": epoch.start_date,
                      "end_date": epoch.end_date,
                      "overview": epoch.overview,
                      "dynamic_fields": epoch.dynamic_fields}

        epoch_data.append(epoch_dict)

    campaign_data = {"title": campaign.title,
                     "description": campaign.description,
                     "image_url": campaign.image_url,
                     "date_suffix": campaign.date_suffix,
                     "negative_date_suffix": campaign.negative_date_suffix,
                     "system": campaign.system}

    final_output = {"campaign_data": campaign_data,
                    "events": events_data,
                    "epochs": epoch_data}

    response = make_response(jsonify(final_output))

    # Set headers for downloading
    filename = "WAR_COR_Backup " + campaign.title
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "application/json"

    return response


def test_json(file):
    """ Function to test a json backup file prior to importing """

    errors_dict = {}

    # Test if file is actually a json file
    try:
        data = json.load(file)
    except json.JSONDecodeError:
        flash("Invalid file format. Data backups must be a WAR/COR JSON file.")
        return False

    test_campaign = models.Campaign()

    # Test campaign overview data
    test_campaign, errors = campaign_import(data, test_campaign)
    if len(errors) > 0:
        errors_dict["Campaign Data"] = errors

    # Test event data
    for index, item in enumerate(data["events"]):
        try:
            event, errors = events_import(item, test_campaign)
        except ValueError:
            errors.append("Invalid event data")
            db.session.rollback()
        if len(errors) > 0:
            if event.title is not None:
                errors_dict[f"Event - {event.title}"] = errors
            else:
                errors_dict[f"Event - {index}"] = errors

    # Test backup epoch data
    for index, item in enumerate(data["epochs"]):
        try:
            epoch, errors = epochs_import(item, test_campaign)
        except ValueError:
            errors.append("Invalid epoch data")
            db.session.rollback()
        if len(errors) > 0:
            if epoch.title is not None:
                errors_dict[f"Epoch - {epoch.title}"] = errors
            else:
                errors_dict[f"Epoch - {index}"] = errors

    if len(errors_dict) == 0:
        file_valid = True
    else:
        file_valid = False
        for error, text in errors_dict.items():
            flash(f"{error}: {', '.join(text)}")

    # Teardown
    db.session.delete(test_campaign)
    db.session.commit()

    return file_valid


def campaign_import(json_data, campaign):
    """Updates campaign object with json campaign data."""

    errors = []

    json_data = json_data["campaign_data"]
    expected_values = {
        "title": "required",
        "description": "required",
        "image_url": "optional",
        "date_suffix": "optional",
        "negative_date_suffix": "optional",
        "system": "optional",
    }
    for field_name, requirement in expected_values.items():
        try:
            json_data[field_name]
        except KeyError:
            if requirement == "required":
                errors.append(f"Unable to locate {field_name}")

    if len(errors) == 0:
        form = {field_name: value for field_name, value in json_data.items()}
        try:
            campaign.update(form)
        except AttributeError:
            db.session.rollback()

    return campaign, errors


def events_import(event, campaign):
    """Creates a new event object from json events list item."""

    new_event = models.Event()

    errors = []

    expected_values = {
        "title": "required",
        "type": "required",
        "date": "required",
        "hide_time": "optional",
        "dynamic_fields": "optional",
    }
    for field_name, requirement in expected_values.items():
        try:
            event[field_name]
        except KeyError:
            if requirement == "required":
                errors.append(f"Unable to locate {field_name}")
        
    if len(errors) == 0:
        form = {field_name: value for field_name, value in event.items()}
        try:
            new_event.update(form, parent_campaign=campaign, new=True)
        except AttributeError:
            errors.append(f"Incorrect data format")
            db.session.rollback()
        except KeyError:
            db.session.rollback()

    return new_event, errors


def epochs_import(epoch, campaign):
    """Creates new epoch from json epochs list item."""

    new_epoch = models.Epoch()
    errors = []

    expected_values = {
        "title": "required",
        "start_date": "required",
        "end_date": "required",
        "overview": "optional",
        "dynamic_fields": "optional",
    }
    for field_name, requirement in expected_values.items():
        try:
            epoch[field_name]
        except KeyError:
            if requirement == "required":
                errors.append(f"Unable to locate {field_name}")

    if len(errors) == 0:
        form = {field_name: value for field_name, value in epoch.items()}
        try:
            new_epoch.update(form, parent_campaign=campaign, new=True)
        except AttributeError:
            errors.append(f"Incorrect data format")
            db.session.rollback()
        except KeyError:
            db.session.rollback()

    return new_epoch, errors
