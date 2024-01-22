from flask import url_for


class CampaignActions(object):
    """ Class to facilitate common campaign actions """

    def __init__(self, client):
        self._client = client

    def create(self, title="Test Campaign", description="Test Description"):
        url = url_for("campaign.create_campaign")
        return self._client.post(url, follow_redirects=True, data={
            "title": title,
            "description": description,
            "date_suffix": "",
            "negative_date_suffix": "",
        })

    def edit(self, campaign_name, campaign_id, new_title="Edited Title", new_description="Edited Description"):
        url = url_for("campaign.edit_campaign",
                      campaign_name=campaign_name,
                      campaign_id=campaign_id)
        return self._client.post(url, follow_redirects=True, data={
            "title": new_title,
            "description": new_description,
        })

    def view(self, campaign_name, campaign_id):
        url = url_for("campaign.show_timeline", campaign_name=campaign_name, campaign_id=campaign_id)
        return self._client.get(url, follow_redirects=True)

    def delete(self, campaign_name, campaign_id, username="test_username", password="12345678"):
        url = url_for("campaign.delete_campaign",
                      campaign_name=campaign_name,
                      campaign_id=campaign_id)
        return self._client.post(url, follow_redirects=True, data={
            "username": username,
            "password": password
        })

    def add_user(self, campaign_name, campaign_id, username, user_id):
        url = url_for("membership.add_user",
                      campaign_name=campaign_name,
                      campaign_id=campaign_id)
        data = {
            "username": username,
            "user_id": user_id,
        }
        return self._client.post(url, data=data, follow_redirects=True)

    def remove_user(self, campaign_name, campaign_id, username, user_id):
        url = url_for("membership.remove_user",
                      campaign_name=campaign_name,
                      campaign_id=campaign_id)
        data = {
            "username": username,
            "user_id": user_id,
        }
        return self._client.post(url, data=data, follow_redirects=True)
