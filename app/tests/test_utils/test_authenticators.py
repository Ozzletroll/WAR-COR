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
    assert permission_required(test_campaign)
    auth.logout()

    auth.register(username="User_2",
                  password="12345678",
                  email="differenttestemail@email.com")

    with pytest.raises(Exception) as error:
        permission_required(test_campaign)
    assert "403" in str(error)
    auth.logout()


def test_user_verification(client, auth):

    auth.login(username="User_1", password="12345678")
    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User_1")).scalar()
    assert user_verification(user_1)

    user_2 = db.session.execute(
        select(models.User)
        .filter_by(username="User_2")).scalar()
    with pytest.raises(Exception) as error:
        user_verification(user_2)
    assert "403" in str(error)
    auth.logout()


def test_check_membership(client, auth):

    auth.login(username="User_1", password="12345678")
    test_campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()
    assert check_membership(test_campaign)
    auth.logout()

    auth.login(username="User_2", password="12345678")
    with pytest.raises(Exception) as error:
        check_membership(test_campaign)
    assert "403" in str(error)
