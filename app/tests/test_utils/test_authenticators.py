from sqlalchemy import select
import pytest
from unittest.mock import Mock, patch
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
    auth.logout()


def test_check_comment_form_visibility(client, auth):
    test_campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    member_user = db.session.execute(
        select(models.User)
        .filter_by(username="member")).scalar()

    test_campaign.members.append(member_user)

    auth.login(username="member", password="12345678")
    test_campaign.comments = "private"
    assert check_comment_form_visibility(test_campaign)

    auth.logout()
    test_campaign.comments = "private"
    assert not check_comment_form_visibility(test_campaign)

    test_campaign.comments = "disabled"
    assert not check_comment_form_visibility(test_campaign)

    auth.login(username="member", password="12345678")
    test_campaign.comments = "disabled"
    assert not check_comment_form_visibility(test_campaign)

    test_campaign.comments = "open"
    assert check_comment_form_visibility(test_campaign)
    auth.logout()
    assert check_comment_form_visibility(test_campaign)


def test_login_required_api(client):
    # Mock function to be decorated
    mock_function = Mock()

    # Decorate the function
    decorated_function = login_required_api(mock_function)

    with patch("app.utils.authenticators.current_user") as mock_user:
        # Test when user is authenticated
        mock_user.is_authenticated = True
        result = decorated_function()
        mock_function.assert_called_once()
        assert result == mock_function.return_value

        # Reset the mock function
        mock_function.reset_mock()

        # Test when user is not authenticated
        mock_user.is_authenticated = False
        result = decorated_function()
        assert result[0].get_json() == jsonify(error="Login required").get_json() and result[1] == 401
        mock_function.assert_not_called()


def test_check_template_is_valid():
    # Mock template and campaign
    template = Mock()
    campaign = Mock()

    with patch("flask_login.utils._get_user") as mock_user:
        # Test when template.parent_campaign == campaign and campaign in current_user.permissions
        template.parent_campaign = campaign
        mock_user.return_value.permissions = [campaign]
        assert check_template_is_valid(template, campaign)

        # Test when template.parent_campaign != campaign
        template.parent_campaign = Mock()
        with pytest.raises(Exception) as error:
            check_template_is_valid(template, campaign)
        assert str(error.value.code) == "403"

        # Test when campaign not in current_user.permissions
        template.parent_campaign = campaign
        mock_user.return_value.permissions = []
        with pytest.raises(Exception) as error:
            check_template_is_valid(template, campaign)
        assert str(error.value.code) == "403"
