from sqlalchemy import select
from flask import url_for
from werkzeug.datastructures import MultiDict
from bs4 import BeautifulSoup

from app import db, models
from app.forms.forms import CreateEventForm

TEST_PASSWORD = "123456768"


def test_setup(client, auth, campaign):
    # Create test users
    auth.register(email="testemail1@email.com",
                  username="Admin",
                  password=TEST_PASSWORD)
    auth.logout()
    auth.register(email="testemail2@email.com",
                  username="User 1",
                  password=TEST_PASSWORD)
    auth.logout()
    auth.register(email="testemail3@email.com",
                  username="User 2",
                  password=TEST_PASSWORD)
    auth.logout()

    # Create test campaign and add user_1 as member
    auth.login(username="Admin", password=TEST_PASSWORD)
    campaign.create(title="Test Campaign",
                    description="A campaign for testing purposes")

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    campaign_object.members.append(user_1)
    db.session.commit()


def test_add_event(client, auth, campaign, event):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    # Test epoch form data
    # None values are used to represent False boolean checkbox values
    event_form = MultiDict({
        "title": "Test Event",
        "type": "Test",
        "year": 5016,
        "month": 1,
        "day": 1,
        "hour": 9,
        "minute": 0,
        "second": 0,
        "hide_time": "",
        "dynamic_fields-0-title": "Field 1 Title",
        "dynamic_fields-0-value": "Value 1",
        "dynamic_fields-0-is_full_width": "",
        "dynamic_fields-0-field_type": "basic",
        "dynamic_fields-1-title": "Field 2 Title",
        "dynamic_fields-1-value": "Value 2",
        "dynamic_fields-1-is_full_width": "",
        "dynamic_fields-1-field_type": "basic",
    })

    url = url_for("event.add_event",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id)

    # Test that page is not reachable when unauthenticated
    response_1 = client.get(url, follow_redirects=True)
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>' in response_1.data

    # Test that post request fails if logged in as non admin user
    auth.login(username=user_1.username, password=TEST_PASSWORD)
    response_2 = event.create(campaign_object=campaign_object, data=event_form)
    assert response_2.status_code == 403
    auth.logout()

    # Test that event can be created when logged in as campaign admin
    auth.login(username="Admin", password=TEST_PASSWORD)
    response_3 = event.create(campaign_object=campaign_object, data=event_form)
    assert response_3.status_code == 200

    event_object = db.session.execute(
        select(models.Event)
        .filter_by(title="Test Event")).scalar()

    assert event_object in campaign_object.events
    for attribute, value in CreateEventForm(event_form).data.items():
        try:
            getattr(event_object, attribute)
        except AttributeError:
            continue

        assert getattr(event_object, attribute) == value


def test_add_event_prepopulate(client, auth, campaign, event):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    # Test if date string is incremented by 1 hour and form is prepopulated with new value
    url = url_for("event.add_event",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id,
                  date="5016/01/01 00:00:00",
                  new_hour=True)

    auth.login(username="Admin", password=TEST_PASSWORD)
    response = client.get(url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    input_elements = soup.find_all(class_="form-date-input")
    values = [input_element.get("value") for input_element in input_elements]
    assert values == ["5016", "01", "01", "01", "00", "00"]


def test_edit_event(client, auth, campaign, event):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    user_2 = db.session.execute(
        select(models.User)
        .filter_by(username="User 2")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    event_object = db.session.execute(
        select(models.Event)
        .filter_by(title="Test Event")).scalar()

    # None values are used to represent False boolean checkbox values
    event_form = MultiDict({
        "title": "Test Event",
        "type": "Test",
        "year": 1111,
        "month": 1,
        "day": 1,
        "hour": 11,
        "minute": 0,
        "second": 0,
        "hide_time": "",
        "dynamic_fields-0-title": "Field 1 Title",
        "dynamic_fields-0-value": "Value 1",
        "dynamic_fields-0-is_full_width": "",
        "dynamic_fields-0-field_type": "basic",
        "dynamic_fields-1-title": "Field 2 Title",
        "dynamic_fields-1-value": "Value 2",
        "dynamic_fields-1-is_full_width": "",
        "dynamic_fields-1-field_type": "basic",
    })

    get_url = url_for("event.edit_event",
                      campaign_name=campaign_object.title,
                      campaign_id=campaign_object.id,
                      event_name=event_object.title,
                      event_id=event_object.id)

    # Test page is not reachable when logged in as non-member user
    auth.login(username=user_2.username, password=TEST_PASSWORD)
    response_1 = client.get(get_url)
    assert response_1.status_code == 403
    response_2 = event.edit(campaign_object, event_object, data=event_form)
    assert response_2.status_code == 403
    auth.logout()

    # Test page cannot be accessed by member without admin permissions
    auth.login(username=user_1.username, password=TEST_PASSWORD)
    response_3 = client.get(get_url)
    assert response_3.status_code == 403
    response_4 = event.edit(campaign_object, event_object, data=event_form)
    assert response_4.status_code == 403
    auth.logout()

    # Test page cannot be accessed by member without admin permissions
    auth.login(username=user_1.username, password=TEST_PASSWORD)
    response_5 = client.get(get_url)
    assert response_5.status_code == 403
    response_6 = event.edit(campaign_object, event_object, data=event_form)
    assert response_6.status_code == 403
    auth.logout()

    # Test admin can view editing page and update event data
    auth.login(username="Admin", password=TEST_PASSWORD)
    response_7 = client.get(get_url)
    assert response_7.status_code == 200
    response_8 = event.edit(campaign_object, event_object, data=event_form)
    assert response_8.status_code == 200
    assert event_object.date == "1111/01/01 11:00:00"
    auth.logout()


def test_view_event(client, auth, campaign):

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    event_object = db.session.execute(
        select(models.Event)
        .filter_by(title="Test Event")).scalar()

    url = url_for("event.view_event",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id,
                  event_name=event_object.title,
                  event_id=event_object.id)

    # Test if event route is reachable
    response = client.get(url)
    assert response.status_code == 200


def test_leave_comment(client, auth, campaign, event):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    user_2 = db.session.execute(
        select(models.User)
        .filter_by(username="User 2")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    event_object = db.session.execute(
        select(models.Event)
        .filter_by(title="Test Event")).scalar()

    data = {
        "body": "Comment text"
    }

    # Test non-member cannot leave comment
    auth.login(username=user_2.username, password=TEST_PASSWORD)
    response_1 = event.create_comment(campaign_object=campaign_object,
                                      event_object=event_object,
                                      data=data)
    assert response_1.status_code == 403
    auth.logout()

    # Test member can leave comment
    auth.login(username=user_1.username, password=TEST_PASSWORD)
    response_2 = event.create_comment(campaign_object=campaign_object,
                                      event_object=event_object,
                                      data=data)
    assert response_2.status_code == 200
    assert event_object.comments[0].body == "<p>Comment text</p>"


def test_delete_comment(client, auth, campaign, event):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    user_2 = db.session.execute(
        select(models.User)
        .filter_by(username="User 2")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    event_object = db.session.execute(
        select(models.Event)
        .filter_by(title="Test Event")).scalar()

    comment_object = db.session.query(models.Comment) \
        .filter(models.Comment.author_id == 2,
                models.Comment.body == "<p>Comment text</p>",
                models.Comment.event_id == event_object.id).scalar()

    url = url_for("event.delete_comment",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id,
                  event_name=event_object.title,
                  event_id=event_object.id,
                  comment_id=comment_object.id)

    # Test that non-admin, non-author user cannot delete comment
    auth.login(username=user_2.username, password=TEST_PASSWORD)
    response_1 = client.post(url, follow_redirects=True)
    assert response_1.status_code == 403
    auth.logout()

    # Test that comment author can delete the comment
    auth.login(username=user_1.username, password=TEST_PASSWORD)
    response_1 = client.post(url, follow_redirects=True)
    assert response_1.status_code == 200
    assert len(event_object.comments) == 0

    # Test that campaign admin can delete the comment
    event.create_comment(campaign_object, event_object, data={"body": "Comment text"})
    assert len(event_object.comments) == 1
    auth.logout()
    auth.login(username="Admin", password=TEST_PASSWORD)

    second_comment_object = db.session.query(models.Comment) \
        .filter(models.Comment.body == "<p>Comment text</p>",
                models.Comment.event_id == event_object.id).scalar()

    url = url_for("event.delete_comment",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id,
                  event_name=event_object.title,
                  event_id=event_object.id,
                  comment_id=second_comment_object.id)

    response_2 = client.post(url, follow_redirects=True)
    assert response_2.status_code == 200
    assert len(event_object.comments) == 0


def test_delete_event(client, auth, campaign, event):

    user_1 = db.session.execute(
        select(models.User)
        .filter_by(username="User 1")).scalar()

    user_2 = db.session.execute(
        select(models.User)
        .filter_by(username="User 2")).scalar()

    campaign_object = db.session.execute(
        select(models.Campaign)
        .filter_by(title="Test Campaign")).scalar()

    event_object = db.session.execute(
        select(models.Event)
        .filter_by(title="Test Event")).scalar()

    url = url_for("event.delete_event",
                  campaign_name=campaign_object.title,
                  campaign_id=campaign_object.id,
                  event_name=event_object.title,
                  event_id=event_object.id)

    # Test route is not reachable when not logged in
    response_1 = client.post(url, follow_redirects=True)
    assert response_1.status_code == 200
    assert b'<li>Please log in to access this page</li>' in response_1.data

    # Test event cannot be deleted by non-member user
    auth.login(username=user_2.username, password=TEST_PASSWORD)
    response_2 = client.post(url, follow_redirects=True)
    assert response_2.status_code == 403
    event_object = db.session.execute(
        select(models.Event)
        .filter_by(title="Test Event")).scalar()
    assert event_object is not None

    # Test event cannot be deleted by non-admin member
    auth.login(username=user_1.username, password=TEST_PASSWORD)
    response_3 = client.post(url, follow_redirects=True)
    assert response_3.status_code == 403
    event_object = db.session.execute(
        select(models.Event)
        .filter_by(title="Test Event")).scalar()
    assert event_object is not None
    auth.logout()

    # Test event can be deleted by admin
    auth.login(username="Admin", password=TEST_PASSWORD)
    response_4 = client.post(url, follow_redirects=True)
    assert response_4.status_code == 200
    event_object = db.session.execute(
        select(models.Event)
        .filter_by(title="Test Event")).scalar()
    assert event_object is None
