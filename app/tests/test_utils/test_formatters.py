from app.utils import formatters


def test_split_date():

    test_string_1 = "5016/01/01 10:00:00"
    output_1 = formatters.split_date(test_string_1)
    assert output_1 == [5016, 1, 1, 10, 0, 0]

    test_string_2 = "150432/99/99 25:10:00"
    output_2 = formatters.split_date(test_string_2)
    assert output_2 == [150432, 99, 99, 25, 10, 0]

    test_string_3 = "5016/01/01"
    output_3 = formatters.split_date(test_string_3, epoch_date=True)
    assert output_3 == [5016, 1, 1]
