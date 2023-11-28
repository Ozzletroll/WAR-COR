from flask import jsonify, make_response, flash
from datetime import datetime
import json

from app import models
from app.utils.sanitisers import sanitise_input


def data_export(campaign):
    """Serialise campaign object as json file for export"""
    
    events_data = []
    for event in campaign.events:
        event_dict = {"type": event.type,
                      "title": event.title,
                      "date": event.date,
                      "location": event.location,
                      "belligerents": event.belligerents,
                      "body": event.body,
                      "result": event.result,
                      "header": event.header}
        
        events_data.append(event_dict)

    epoch_data = []
    for epoch in campaign.epochs:
        epoch_dict = {"title": epoch.title,
                      "start_date": epoch.start_date,
                      "end_date": epoch.end_date,
                      "description": epoch.description}
        
        epoch_data.append(epoch_dict)

    campaign_data = {"title": campaign.title,
                     "description": campaign.description,
                     "last_edited": campaign.last_edited,
                     "date_suffix": campaign.date_suffix,
                     "negative_date_suffix": campaign.negative_date_suffix}
    
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
        errors_dict["Filetype:"] = "Invalid file format. Data backups must be a JSON file."
        flash("Invalid file format. Data backups must be a JSON file.")
        return False

    test_campaign = models.Campaign()

    # Test campaign overview data
    test_campaign, errors = campaign_import(data, test_campaign)
    if len(errors) > 0:
        errors_dict["Campaign Data"] = errors

    # Test event data
    for index, item in enumerate(data["events"]):
        event, errors = events_import(item)
        if len(errors) > 0:
            if event.title is not None:
                errors_dict[f"Event - {event.title}"] = errors
            else:
                errors_dict[f"Event - {index}"] = errors

    # Test backup epoch data
    for index, item in enumerate(data["epochs"]):
        epoch, errors = epochs_import(item)
        if len(errors) > 0:
            if epoch.title is not None:
                errors_dict[f"Epoch - {event.title}"] = errors
            else:
                errors_dict[f"Epoch - {index}"] = errors

    if len(errors_dict) == 0:
        file_valid = True
    else:
        file_valid = False
        for error, text in errors_dict.items():
            flash(f"{error}: {', '.join(text)}")

    return file_valid


def campaign_import(json, campaign):
    """Updates campaign object with json campaign data."""

    errors = []

    json = json["campaign_data"]

    try:
        campaign.title = json["title"]
        campaign.set_url_title()
    except KeyError:
        errors.append("Unable to locate campaign title.")
    try:
        campaign.description = sanitise_input(json["description"])
    except KeyError:
        errors.append("Unable to locate campaign description.")
    try:
        campaign.date_suffix = json["date_suffix"]
    except KeyError:
        errors.append("Unable to locate date suffix.")
    try:
        campaign.negative_date_suffix = json["negative_date_suffix"]
    except KeyError:
        errors.append("Unable to locate negative date suffix.")
    try:
        campaign.last_edited = datetime.now()
    except KeyError:
        errors.append("Unable to locate campaign last edited date.")

    return campaign, errors


def events_import(event):
    """Creates a new event object from json events list item."""

    new_event = models.Event()

    errors = []

    try:
        new_event.title = event["title"]
        new_event.set_url_title()
    except KeyError:
        errors.append("Unable to locate event title")
    try:
        new_event.date = event["date"]
    except KeyError:
        errors.append("Unable to locate event date")
    try:
        new_event.split_date(new_event.date)
    except ValueError:
        errors.append("Incorrect date format")
    except AttributeError:
        errors.append("Incorrect date format")
    try:
        new_event.type = event["type"]
    except KeyError:
        errors.append("Unable to locate event type")
    try:
        new_event.belligerents = event["belligerents"]
    except KeyError:
        errors.append("Unable to locate event belligerents")
    try:
        new_event.body = sanitise_input(event["body"])
    except KeyError:
        errors.append("Unable to locate event body")
    try:
        new_event.header = event["header"]
    except KeyError:
        errors.append("Unable to locate event header")
    try:
        new_event.location = event["location"]
    except KeyError:
        errors.append("Unable to locate event location")
    try:
        new_event.result = event["result"]
    except KeyError:
        errors.append("Unable to locate event result")

    return new_event, errors


def epochs_import(epoch):
    """Creates new epoch from jsons epochs list item."""    

    new_epoch = models.Epoch()
    errors = []
        
    try:
        new_epoch.title = epoch["title"]
    except KeyError:
        errors.append("Unable to locate epoch title")
    try:
        new_epoch.start_date = epoch["start_date"]
    except KeyError:
        errors.append("Unable to locate epoch start date")
    try:
        new_epoch.start_year = new_epoch.split_date(new_epoch.start_date)[0]
    except ValueError:
        errors.append("Incorrect date format")
    except AttributeError:
        errors.append("Incorrect date format")
    try:
        new_epoch.start_month = new_epoch.split_date(new_epoch.start_date)[1]
    except ValueError:
        errors.append("Incorrect date format")
    except AttributeError:
        errors.append("Incorrect date format")
    try:
        new_epoch.end_date = epoch["end_date"]
    except KeyError:
        errors.append("Unable to locate epoch end date")
    try:
        new_epoch.end_year = new_epoch.split_date(new_epoch.end_date)[0]
    except ValueError:
        errors.append("Incorrect date format")
    except AttributeError:
        errors.append("Incorrect date format")
    try:
        new_epoch.end_month = new_epoch.split_date(new_epoch.end_date)[1]
    except ValueError:
        errors.append("Incorrect date format")
    try:
        new_epoch.description = sanitise_input(epoch["description"])
    except KeyError:
        errors.append("Unable to locate epoch description")
    
    return new_epoch, errors
