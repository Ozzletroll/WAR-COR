from sqlalchemy import select
import pytest
from app import db, models
from app.utils.authenticators import *


def test_permission_required(client, auth, campaign):

    auth.register(username="User_1", password="12345678")
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


def test_check_campaign_visibility(client, auth):

    test_campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()
    test_campaign.private = True

    auth.login(username="User_1", password="12345678")
    assert check_campaign_visibility(test_campaign)
    auth.logout()

    auth.login(username="User_2", password="12345678")
    with pytest.raises(Exception) as error:
        check_campaign_visibility(test_campaign)
    assert "403" in str(error)
    auth.logout()

    with pytest.raises(Exception) as error:
        check_campaign_visibility(test_campaign)
    assert "403" in str(error)


def test_check_campaign_comment_status(client, auth):

    test_campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    auth.register(username="member", email="member@email.com")
    auth.logout()

    member_user = db.session.execute(
        select(models.User)
        .filter_by(username="member")).scalar()

    test_campaign.members.append(member_user)

    # Test unauthenticated member cannot post comments when they are disabled
    test_campaign.comments = "disabled"

    with pytest.raises(Exception) as exception:
        check_campaign_comment_status(test_campaign)

    error = exception.value
    assert error.code == 403
    assert error.description == "Comments are disabled for this campaign"

    # Test unauthenticated user can post when comments set to open
    test_campaign.comments = "open"
    check_campaign_comment_status(test_campaign)

    # Test authenticated member cannot post comments when set to disabled
    test_campaign.comments = "disabled"
    auth.login(username="member", password="12345678")
    with pytest.raises(Exception) as exception:
        check_campaign_comment_status(test_campaign)
    error = exception.value
    assert error.code == 403
    assert error.description == "Comments are disabled for this campaign"

    # Test authenticated non-member cannot post comments when set to private
    test_campaign.members.remove(member_user)
    test_campaign.comments = "private"
    with pytest.raises(Exception) as exception:
        check_campaign_comment_status(test_campaign)
    error = exception.value
    assert error.code == 403
    assert error.description == "Comments are set to 'Members Only' for this campaign"

    # Test authenticated member can post comments when set to private
    test_campaign.members.append(member_user)
    auth.login(username="member")
    test_campaign.comments = "private"
    assert check_campaign_comment_status(test_campaign)
