from flask import url_for


class AuthActions(object):
    """ Class to facilitate common user auth functions during testing """

    def __init__(self, client):
        self._client = client

    def login(self, username="test_username", password="12345678"):
        return self._client.post("/login", follow_redirects=True, data={
            "username": username,
            "password": password,
        })

    def register(self, email='test@testemail.com', username='test_username', password='12345678'):
        return self._client.post("/register", follow_redirects=True, data={
            "email": email,
            "username": username,
            "password": password,
            "confirm_password": password,
        })

    def logout(self):
        return self._client.get("/logout", follow_redirects=True)

    def delete(self, username, given_username, given_password):
        url = url_for("user.delete_user", username=username)
        return self._client.post(url, follow_redirects=True, data={
            "username": given_username,
            "password": given_password,
        })

    def accept_invite(self, campaign_name, campaign_id, message_id):
        url = url_for("membership.accept_invite",
                      campaign_name=campaign_name,
                      campaign_id=campaign_id,
                      message_id=message_id)
        return self._client.get(url, follow_redirects=True)
