from flask import url_for


class EventActions(object):

    def __init__(self, client):
        self._client = client

    def create(self, campaign_object, data):

        url = url_for("event.add_event",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id)

        return self._client.post(url, data=data, follow_redirects=True)

    def edit(self, campaign_object, event_object, data):

        url = url_for("event.edit_event",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id,
                      event_name=event_object.title,
                      event_id=event_object.id)

        return self._client.post(url, data=data, follow_redirects=True)

    def create_comment(self, campaign_object, event_object, data):

        url = url_for("event.view_event",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id,
                      event_name=event_object.title,
                      event_id=event_object.id)

        return self._client.post(url, data=data, follow_redirects=True)
