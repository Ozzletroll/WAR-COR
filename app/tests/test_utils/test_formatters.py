from app import models
from app.utils import formatters


def test_split_date():

    test_string_1 = "5016/01/01 10:00:00"
    output_1 = formatters.split_date(test_string_1)
    assert output_1 == [5016, 1, 1, 10, 0, 0]

    test_string_2 = "150432/99/99 25:10:00"
    output_2 = formatters.split_date(test_string_2)
    assert output_2 == [150432, 99, 99, 25, 10, 0]

    test_string_3 = "5016/01/01"
    output_3 = formatters.split_date(test_string_3)
    assert output_3 == [5016, 1, 1]


def test_increment_date():

    test_string_1 = "5016/01/01 10:00:00"
    output_1 = formatters.increment_date(test_string_1, args={"new_month": True})
    assert output_1 == {
        "year": 5016,
        "month": 2,
        "day": 1,
        "hour": 10,
        "minute": 0,
        "second": 0,
    }

    test_string_2 = "5016/99/01 10:00:00"
    output_2 = formatters.increment_date(test_string_2, args={"new_month": True})
    assert output_2 == {
        "year": 5017,
        "month": 1,
        "day": 1,
        "hour": 10,
        "minute": 0,
        "second": 0,
    }

    test_string_3 = "5016/01/01 10:00:00"
    output_3 = formatters.increment_date(test_string_3, args={"new_day": True})
    assert output_3 == {
        "year": 5016,
        "month": 1,
        "day": 2,
        "hour": 10,
        "minute": 0,
        "second": 0,
    }

    test_string_4 = "5016/01/99 10:00:00"
    output_4 = formatters.increment_date(test_string_4, args={"new_day": True})
    assert output_4 == {
        "year": 5016,
        "month": 2,
        "day": 1,
        "hour": 10,
        "minute": 0,
        "second": 0,
    }

    test_string_5 = "5016/01/01 10:00:00"
    output_5 = formatters.increment_date(test_string_5, args={"new_hour": True})
    assert output_5 == {
        "year": 5016,
        "month": 1,
        "day": 1,
        "hour": 11,
        "minute": 0,
        "second": 0,
    }

    test_string_6 = "5016/01/01 99:00:00"
    output_6 = formatters.increment_date(test_string_6, args={"new_hour": True})
    assert output_6 == {
        "year": 5016,
        "month": 1,
        "day": 2,
        "hour": 0,
        "minute": 0,
        "second": 0,
    }

    test_string_7 = "5016/99/99 99:00:00"
    output_7 = formatters.increment_date(test_string_7, args={"new_hour": True})
    assert output_7 == {
        "year": 5017,
        "month": 1,
        "day": 1,
        "hour": 0,
        "minute": 0,
        "second": 0,
    }


def test_format_user_search_results(client):

    user_1 = models.User()
    user_1.username = "TestUser"
    user_1.id = 1

    user_2 = models.User()
    user_2.username = "TestUser123"
    user_2.id = 2

    campaign = models.Campaign()
    campaign.title = "Test Campaign"
    campaign.set_url_title()
    campaign.id = 1

    users = [user_1, user_2]

    query = "TestUser"

    results = formatters.format_user_search_results(users, campaign, query)

    assert results[0]["relevance"] <= results[1]["relevance"]

    # Assert that "TestUser" comes before "TestUser123" in the list
    assert results[0]["username"] == "TestUser"
    assert results[1]["username"] == "TestUser123"
