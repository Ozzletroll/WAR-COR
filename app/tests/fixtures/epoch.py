from flask import url_for


class EpochActions(object):

    def __init__(self, client):
        self._client = client

    def create(self, campaign_object, data):

        url = url_for("epoch.new_epoch",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id)

        return self._client.post(url, data=data, follow_redirects=True)

    def edit(self, campaign_object, epoch_object, data):

        url = url_for("epoch.edit_epoch",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id,
                      epoch_id=epoch_object.id,
                      epoch_title=epoch_object.title)

        return self._client.post(url, data=data, follow_redirects=True)

    def delete(self, campaign_object, epoch_object):

        url = url_for("epoch.delete_epoch",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id,
                      epoch_id=epoch_object.id,
                      epoch_title=epoch_object.title)

        return self._client.post(url, follow_redirects=True)
