from flask import jsonify



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

    campaign_data = {"title": campaign.title,
                     "description": campaign.description,
                     "last_edited": campaign.last_edited,
                     "date_suffix": campaign.date_suffix,
                     "events": events_data,
                     }

    data = jsonify(campaign_data)

    return data
