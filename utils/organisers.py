from itertools import groupby



class Year:

    def __init__(self):
        self.name = ""
        self.months = []
        self.marker = False



class Month:

    def __init__(self):
        self.name = ""
        self.days = []
        self.header = False



class Day:

    def __init__(self):
        self.name = ""
        self.events = []
        self.header = False



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
    """Function that structures campaign event data for timeline rendering. Returns
    a list of year objects."""
    
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


    # Current structure:
    # grouped_events = {year: {month: {day: [<Event 1>, <Event 2>]}}}

    # Turn each level of the heirarchy into an object, with the level below as a list held in a property
    year_list = []

    for year in grouped_events:

        year_object = Year()
        year_object.name = year
        year_object.marker = check_year_marker(grouped_events[year])

        for month in grouped_events[year]:

            month_object = Month()
            month_object.name = month

            for day in grouped_events[year][month]:

                day_object = Day()
                day_object.name = day

                for event in grouped_events[year][month][day]:

                    # Append the event to the day object
                    day_object.events.append(event)

                # Append the day object to the month object
                month_object.days.append(day_object)

            # Append the month object to the year object
            year_object.months.append(month_object)

        # Append the year object to the formatted list
        year_list.append(year_object)

        # Finally, take the list of year objects and check them for header status
        check_headers(year_list)

    return year_list



def check_year_marker(year):
    """Check if a given year is long enough to warrant a year marker """

    year_markers = []
    marker = False

    if len(year) >= 3:
        marker = True
        
    for month in year:
        if len(year[month]) >= 5:
            marker = True
        for day in year[month]:
            if len(year[month][day]) >= 5:
                marker = True
    
    if marker:
        return True
    else:
        return False



def check_headers(year_list):
    """Takes the list of year objects and checks each month and day within them,
    flagging the header properties."""

    for year_index, year in enumerate(year_list):

        for month_index, month in enumerate(year.months):

            for day_index, day in enumerate(month.days):

                # Give the day the header property, if the month has only one day,
                # and that day has only one event with the header property.
                if len(month.days) == 1 and len(day.events) == 1 and day.events[0].header:
                    day.header = True

            # Give the month the header property, if the year has only one month,
            # and that month's first day has the header property.
            if len(year.months) == 1 and month.days[0].header:
                month.header = True



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
    year_format = len(datestring.split("-")[0])

    if "new_hour" in args:
        incremented_values = increment(values, 2)

        # Format date as string for form field
        datestring = str(incremented_values[0]).zfill(year_format) + "-" + str(incremented_values[1]).zfill(2) + "-" + str(incremented_values[2]).zfill(2) + " " + str(incremented_values[3]).zfill(2) + ":00:00"

    # Move to the next day and format the string
    if "new_day" in args:
        incremented_values = increment(values, 3)

        # Format date as string for form field
        datestring = str(incremented_values[0]).zfill(year_format) + "-" + str(incremented_values[1]).zfill(2) + "-" + str(incremented_values[2]).zfill(2) + " 00:00:00"

    # Move to the next month and format the string
    if "new_month" in args:
        incremented_values = increment(values, 4)

        # Format date as string for form field
        datestring = str(incremented_values[0]).zfill(year_format) + "-" + str(incremented_values[1]).zfill(2) + "-" + "01 00:00:00"

    return datestring
