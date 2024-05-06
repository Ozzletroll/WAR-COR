from app.utils.paginators import Paginator


def test_paginator():
    test_data = ["First", "Second", "Third"]
    paginator = Paginator(data=test_data,
                          page=1,
                          per_page=1)

    assert paginator.total_pages == 3
    assert paginator.current_page == 1
    assert paginator.page.page_number == 1
    assert paginator.page.items == ["First"]

    paginator_1 = Paginator(data=test_data,
                            page=3,
                            per_page=1)

    assert paginator_1.page.items == ["Third"]

    # Test page numbers for template rendering
    test_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    paginator_2 = Paginator(data=test_data,
                            page=1,
                            per_page=1)
    assert paginator_2.page_numbers == [1, 2, 3, 4, None, 14, 15]

    paginator_3 = Paginator(data=test_data,
                            page=6,
                            per_page=1)

    assert paginator_3.page_numbers == [1, 2, None, 4, 5, 6, 7, 8, 9, None, 14, 15]

