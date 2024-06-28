import editdistance
import re
from bs4 import BeautifulSoup


def split_date(datestring):
    """Function that splits a datestring into individual values,
    returns a list of integers"""

    split_date = re.split("/|:| ", datestring)
    return list(map(int, split_date))


def increment_date(datestring, args):
    """Function that takes a date string, and the dictionary from request.args, 
    and returns the next day/week/month/year date as a string,
    ready for form pre population."""

    def increment(values, column):
        """Function iterates through the datestring tuple, incrementing 
        at the value of the given index. Rollover values are specified in 
        the "rollover" list. """

        # Year, month, day, hour, minute, second rollover values
        rollover = list(reversed([float("inf"), 100, 100, 100, 59, 59][-len(values):]))
        incremented_values = []

        # Working from the smallest unit, increment by one from the given index
        for index, value in enumerate(reversed(values)):
            if index == column:
                value += 1
                if value >= rollover[index] and index != len(values) - 1:
                    # Reset to zero on hour rollover
                    if column <= 2:
                        value = 0
                    # All other values reset to 1
                    else:
                        value = 1
                    column += 1
            incremented_values.append(value)

        incremented_values.reverse()

        return incremented_values

    # Map arguments to column index values
    date_mapping = {
        "new_hour": 2,
        "new_day": 3,
        "new_month": 4
    }
    increment_column = [value for key, value in date_mapping.items() if key in args][0]

    values = split_date(datestring)
    incremented_values = increment(values, increment_column)

    # Format incremented values as dict
    date_parts = ["year", "month", "day", "hour", "minute", "second"]
    output = dict(zip(date_parts, incremented_values + [None]*(6-len(incremented_values))))

    return output


def format_user_search_results(users, campaign, query):
    """ Function to format add user query results """

    results = [{"id": user.id,
                "username": user.username,
                "relevance": editdistance.eval(user.username, query)}
               for user in users if user not in campaign.members]

    sorted_results = sorted(results, key=lambda x: x["relevance"])

    return sorted_results


def format_html_field_shortcuts(dynamic_fields):
    """ Function to format an event or epoch model's html field
        data for sidebar button rendering.
    """

    def extract_header_text(html):
        soup = BeautifulSoup(html, "html.parser")
        header_tags = soup.find_all(re.compile(r"^h"))
        header_texts = [tag.get_text(strip=True) for tag in header_tags]
        return header_texts

    output = []

    for index_1, field in enumerate(dynamic_fields):

        if field["field_type"] != "html":
            continue

        header_texts = extract_header_text(field["value"])

        groups = {
            "field_index": index_1,
            "subheadings": [],
        }
        for index_2, header in enumerate(header_texts):
            subheading = {
                "title": header,
                "element_id": f"field-{index_1 + 1}-header-{index_2 + 1}"
            }
            groups["subheadings"].append(subheading)

        output.append(groups)

    return output
