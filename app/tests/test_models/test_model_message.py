from datetime import datetime
from app import db, models


def test_dismiss(client, auth):

    user = models.User()
    user_form = {
        "email": "email@testemail.com",
        "username": "New Username",
        "password": "Password"
    }
    user.update(user_form, new=True)
    db.session.add(user)
    db.session.commit()

    message = models.Message()
    message.invite = False
    message.notification = True
    message.request = False
    message.body = "Test Message"
    message.date = datetime.now()
    user.messages.append(message)

    db.session.add(message)
    db.session.commit()

    message.dismiss(user)

    message = (db.session.query(models.Message)
               .filter(models.Message.id == message.id)
               .first())

    assert message is None

