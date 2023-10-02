from flask import jsonify, make_response
from datetime import datetime

import models


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
                      "header": event.header,
                      }
        
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
                     "events": events_data,
                     "epochs": epoch_data}

    response = make_response(jsonify(campaign_data))

        # Set headers for downloading
    filename = "WAR_COR_Backup " + campaign.title
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "application/json"

    return response



def campaign_import(json, campaign):
    """Updates campaign object with json campaign data."""

    campaign.title = json["title"]
    campaign.description = json["description"]
    campaign.date_suffix = json["date_suffix"]
    campaign.last_edited = datetime.now()

    return campaign



def events_import(event):
    """Creates a new event object from json events list item."""

    new_event = models.Event()

    new_event.title = event["title"]
    new_event.date = event["date"]
    new_event.type = event["type"]
    new_event.belligerents = event["belligerents"]
    new_event.body = event["body"]
    new_event.header = event["header"]
    new_event.location = event["location"]
    new_event.result = event["result"]

    return new_event


def epochs_import(epoch):
    """Creates new epoch from jsons epochs list item."""

    new_epoch = models.Epoch()

    new_epoch.title = epoch["title"]
    new_epoch.start_date = epoch["start_date"]
    new_epoch.end_date = epoch["end_date"]
    new_epoch.description = epoch["description"]

    return new_epoch
