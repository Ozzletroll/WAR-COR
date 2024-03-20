from sqlalchemy import select
import pytest
from app import db, models
from app.utils.authenticators import *


def test_permission_required(client, auth, campaign):

    auth.register(username="User_1", password="12345678")
    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User_1")).scalar()
    campaign.create(title="Test Campaign")
    test_campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()
    user_1.permissions.append(test_campaign)
    assert permission_required(test_campaign)
    auth.logout()

    auth.register(username="User_2",
                  password="12345678",
                  email="differenttestemail@email.com")

    with pytest.raises(Exception) as error:
        permission_required(test_campaign)
    assert "403" in str(error)
    auth.logout()
