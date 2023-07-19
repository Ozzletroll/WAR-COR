from itertools import groupby


def split_date(datestring):
    """Function that splits a datestring into individual values,
    returns a list of integers"""

    year = datestring.split("-")[0]
    month = datestring.split("-")[1]
    day = datestring.split("-")[2].split()[0]
    hours = datestring.split("-")[2].split()[1].split(":")[0]
    minutes = datestring.split("-")[2].split()[1].split(":")[1]
    seconds = datestring.split("-")[2].split()[1].split(":")[2]
    
    return [int(year), int(month), int(day), int(hours), int(minutes), int(seconds)]



def campaign_sort(campaign):
    """Function that structures campaign event data for timeline rendering"""
    
    def custom_sort(event):
        """Function that splits a datestring into individual integers"""

        year = event.date.split("-")[0]
        month = event.date.split("-")[1]
        day = event.date.split("-")[2].split()[0]
        hours = event.date.split("-")[2].split()[1].split(":")[0]
        minutes = event.date.split("-")[2].split()[1].split(":")[1]
        seconds = event.date.split("-")[2].split()[1].split(":")[2]
        
        return int(year), int(month), int(day), int(hours), int(minutes), int(seconds)


    # Sort events into date order
    sorted_events = sorted(campaign.events, key=custom_sort)

    # Structure events into dictionary, grouped by year
    groups = groupby(sorted_events, key=lambda event: (event.date.split("-")[0]))

    grouped_events = {year: list(group) for year, group in groups}

    # Group each years events into months
    for year in grouped_events:
        groups = groupby(grouped_events[year], key=lambda event: (event.date.split("-")[1]))
        grouped_months = {month: list(group) for month, group in groups}
        grouped_events[year] = grouped_months

    # Group each months events into days
    for year in grouped_events:
        for month in grouped_events[year]:
            groups = groupby(grouped_events[year][month], key=lambda event: (event.date.split("-")[2].split()[0]))
            grouped_days = {day: list(group) for day, group in groups}
            grouped_events[year][month] = grouped_days

    # Final example structure:
    # grouped_events = {year: {month: {day: [<Event 1>, <Event 2>]}}}

    return grouped_events



def get_year_markers(grouped_events):
    """Parses timeline data, determining if jinja should render extra year markers.
    Returns a list of booleans, to be iterate through alongside the 'years'. """

    year_markers = []

    for year in grouped_events:
        marker = False
        if len(grouped_events[year]) >= 3:
            marker = True
        for month in grouped_events[year]:
            if len(grouped_events[year][month]) >= 5:
                marker = True
            for day in grouped_events[year][month]:
                if len(grouped_events[year][month][day]) >= 5:
                    marker = True
        
        if marker:
            year_markers.append(True)
        else:
            year_markers.append(False)

    return year_markers



def format_event_datestring(datestring, args):
    """Function that takes a datestring, and the dictionary from request.args, 
    and returns the next day/week/month/year date as a string,
    ready for form prepopulation."""

    def increment(values, column):
        """Function iterates through the datestring tuple, incrementing 
        at the value of the given index. Rollover at 100. """

        incremented_values = []

        # Working from the smallest unit, increment by one from the given index
        for index, value in enumerate(reversed(values)):
            if index == column:
                value += 1
                # If any column except the year value exceeds 99, increment the next value and reset to 1
                if value >= 100 and index != 5:
                    value = 1
                    column += 1
            incremented_values.append(value)

        incremented_values.reverse()

        print(incremented_values)
        return incremented_values


    values = split_date(datestring)

    if "new_hour" in args:
        incremented_values = increment(values, 2)

        # Format date as string for form field
        datestring = str(incremented_values[0]).zfill(2) + "-" + str(incremented_values[1]).zfill(2) + "-" + str(incremented_values[2]).zfill(2) + " " + str(incremented_values[3]).zfill(2) + ":00:00"

    # Move to the next day and format the string
    if "new_day" in args:
        incremented_values = increment(values, 3)

        # Format date as string for form field
        datestring = str(incremented_values[0]).zfill(2) + "-" + str(incremented_values[1]).zfill(2) + "-" + str(incremented_values[2]).zfill(2) + " 00:00:00"

    # Move to the next month and format the string
    if "new_month" in args:
        incremented_values = increment(values, 4)

        # Format date as string for form field
        datestring = str(incremented_values[0]).zfill(2) + "-" + str(incremented_values[1]).zfill(2) + "-" + "01 00:00:00"

    return datestring
