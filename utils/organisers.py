from itertools import groupby
import copy
from app import db



# Classes used for timeline data organisation
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
        self.has_epoch = False
        self.has_epoch_end = False
        self.epochs = []
        self.end_epochs = []
        self.epoch_has_events = False



class Day:

    def __init__(self):
        self.name = ""
        self.events = []
        self.header = False



def split_date(datestring):
    """Function that splits a datestring into individual values,
    returns a list of integers"""

    year = datestring.split("/")[0]
    month = datestring.split("/")[1]
    day = datestring.split("/")[2].split()[0]
    hours = datestring.split("/")[2].split()[1].split(":")[0]
    minutes = datestring.split("/")[2].split()[1].split(":")[1]
    seconds = datestring.split("/")[2].split()[1].split(":")[2]

    return [int(year), int(month), int(day), int(hours), int(minutes), int(seconds)]



def campaign_sort(campaign):
    """ Function that structures campaign event data for timeline rendering. Returns
        a list of year objects.
    
        Sorting is achieved by first creating nested dictionaries to represent the
        timeline structure, which will be used for iteration purposes in order to create
        Year, Month, and Day objects. 
        
        The first dictionary structure is created by combining two dictionaries of the 
        campaigns epochs organised by start date and end date.

            Example: {year: {month: [<Epoch 1>, <Epoch 2>]}

        Next, a similar dictionary is created from the campaigns events, with an 
        additional layer of nested dictionaries representing days. The event objects
        themselves are nested inside the day entries.

            Example: {year: {month: {day: [<Event 3>, <Event 4>]}}
        
        These two nested dictionaries are then combined into one. The "events" dictionary
        is used as the primary structure, and new entries are created for any year/month
        that only contains epochs.

            Example: 
        
            If there were two events that occured in 5015/01/01, and one epoch that began
            in 5014/05/01 and ended in 5016/01/01, the dict would be:

            final_group = {5014: {05: [<Epoch 1>]}},
                        5015: {01: {01: [<Event 1>, <Event 2>]},
                        5016: {01: [<Epoch 2>]}}

        Finally, this dict is used to create a convenient structure of nested
        objects, allowing easier rendering in the Jinja template:                     

            Month objects are assigned as a property of Year objects under Year.months. 
            Day objects are assigned as properties of Month objects under Month.days.
            Epochs are assigned under Month.epochs.
            Event objects are assigned under Day.events.

        Other properties are also assigned here to assist in template rendering.
        
    """
    
    def custom_sort(event):
        """Sort key function for sorting event objects """
        return (event.year, event.month, event.day, event.hour, event.minute, event.second)


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

                try:
                    for day_index, day in enumerate(month.days):

                        # Give the day the header property if it is the first day of the month,
                        # and that day has only one event, which has the header property.
                        if day_index == 0 and len(day.events) == 1 and day.events[0].header:
                            day.header = True
                except KeyError:
                    continue

                # Give the month the header property, if the year has only one month,
                # and that month's first day has the header property.
                try:
                    if len(year.months) == 1 and month.days[0].header:
                        month.header = True
                except IndexError:
                    month.header = False


    def group_epochs(epochs, sort_key, year_key, month_key):
        """Function to sort epochs into matching data structure to the timeline events.
        Takes a list of a campaigns epochs, as well as a sort key."""
        sorted_epochs = sorted(epochs, key=sort_key)
        epoch_groups = groupby(sorted_epochs, key=year_key)
        grouped_epochs = {year: list(group) for year, group in epoch_groups}

        for year in grouped_epochs:
            groups = groupby(grouped_epochs[year], key=month_key)
            grouped_months = {month: list(group) for month, group in groups}
            grouped_epochs[year] = grouped_months

        return grouped_epochs


    # Sort and group epochs by start date and end date
    epochs_by_start_date = group_epochs(campaign.epochs, 
                                        sort_key=lambda epoch: (epoch.start_year, epoch.start_month),
                                        year_key=lambda epoch: epoch.start_year,
                                        month_key=lambda epoch: epoch.start_month)
    epochs_by_end_date = group_epochs(campaign.epochs,
                                      sort_key=lambda epoch: (epoch.end_year, epoch.end_month),
                                      year_key=lambda epoch: epoch.end_year,
                                      month_key=lambda epoch: epoch.end_month)
    
    # Merge two dictionaries for year/month population
    combined_epochs = {}

    for year in epochs_by_start_date:
        if year not in combined_epochs:
            combined_epochs[year] = epochs_by_start_date[year]
    for year in epochs_by_end_date:
            if year not in combined_epochs:
                combined_epochs[year] = epochs_by_end_date[year]

    # Sort years again
    combined_epochs = {key: value for key, value in sorted(combined_epochs.items())}

    # Current epoch structure:
    # grouped_epochs = {year: {month: [<Epoch 1>, <Epoch 2>]}

    # Sort events into date order
    sorted_events = sorted(campaign.events, key=custom_sort)
    # Structure events into dictionary, grouped by year
    groups = groupby(sorted_events, key=lambda event: event.year)
    grouped_events = {year: list(group) for year, group in groups}

    # Group each years events into months
    for year in grouped_events:
        groups = groupby(grouped_events[year], key=lambda event: event.month)
        grouped_months = {month: list(group) for month, group in groups}
        grouped_events[year] = grouped_months

    # Group each months events into days
    for year in grouped_events:
        for month in grouped_events[year]:
            groups = groupby(grouped_events[year][month], key=lambda event: event.day)
            grouped_days = {day: list(group) for day, group in groups}
            grouped_events[year][month] = grouped_days

    # Current event structure:
    # grouped_events = {year: {month: {day: [<Event 1>, <Event 2>]}}}

    # Combine both dictionaries to determine timeline structure
    final_group = copy.deepcopy(grouped_events)

    for year, month in combined_epochs.items():
        if year in final_group:
            for month in combined_epochs[year]:
                if month not in final_group[year]:
                    final_group[year][month] = combined_epochs[year][month]  
        else:
            final_group[year] = combined_epochs[year]

    # Sort final grouping into year order
    final_group = {key: value for key, value in sorted(final_group.items())}
    # Sort final grouping months
    for year in final_group:
        for month in final_group[year]:
            final_group[year] = {key: value for key, value in sorted(final_group[year].items())}

    # Turn each level of the heirarchy into an object, with the level below as a list held in a property
    year_list = []

    for year in final_group:

        year_object = Year()
        year_object.name = str(year)
        try:
            year_object.marker = check_year_marker(grouped_events[year])
        # Catch exception if year only has epoch and nothing else
        except KeyError:
            year_object.marker = False

        for month in final_group[year]:

            month_object = Month()
            month_object.name = str(month).zfill(2)

            for day in final_group[year][month]:

                day_object = Day()
                day_object.name = str(day).zfill(2)

                try:
                    for event in grouped_events[year][month][day]:
                        # Append the event to the day object
                        day_object.events.append(event)
                # Catch exception if month has no days (IE, only has epochs)
                except KeyError:
                    continue

                # Append the day object to the month object
                month_object.days.append(day_object)

            # Check if any epoch starts occur in month
            if year in epochs_by_start_date:
                if month in epochs_by_start_date[year]:
                    month_object.has_epoch = True
                    month_object.epochs = epochs_by_start_date[year][month]
                    for epoch in month_object.epochs:
                        if len(epoch.events) > 0:
                            month_object.epoch_has_events = True

            # Check if any epoch ends occur in month
            if year in epochs_by_end_date:
                if month in epochs_by_end_date[year]:
                    month_object.has_epoch_end = True
                    month_object.end_epochs = epochs_by_end_date[year][month]
                    for epoch in month_object.end_epochs:
                        if len(epoch.events) > 0:
                            month_object.epoch_has_events = True

            # Append the month object to the year object
            year_object.months.append(month_object)   

        # Append the year object to the formatted list
        year_list.append(year_object)

        # Finally, take the list of year objects and check them for header status
        check_headers(year_list)

    return year_list


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

        return incremented_values


    values = split_date(datestring)
    year_format = len(datestring.split("/")[0])

    if "new_hour" in args:
        incremented_values = increment(values, 2)
        # Format date as string for form field
        datestring = str(incremented_values[0]).zfill(year_format) + "/" + str(incremented_values[1]).zfill(2) + "/" + str(incremented_values[2]).zfill(2) + " " + str(incremented_values[3]).zfill(2) + ":00:00"

    # Move to the next day and format the string
    if "new_day" in args:
        incremented_values = increment(values, 3)
        # Format date as string for form field
        datestring = str(incremented_values[0]).zfill(year_format) + "/" + str(incremented_values[1]).zfill(2) + "/" + str(incremented_values[2]).zfill(2) + " 00:00:00"

    # Move to the next month and format the string
    if "new_month" in args:
        incremented_values = increment(values, 4)
        # Format date as string for form field
        datestring = str(incremented_values[0]).zfill(year_format) + "/" + str(incremented_values[1]).zfill(2) + "/" + "01 00:00:00"

    return datestring
