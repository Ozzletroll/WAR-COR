from itertools import groupby


def campaign_sort(campaign):
    """Function that structures campaign event data for timeline rendering"""
    
    # Sort events into date order
    def custom_sort(event):

        year = event.date.split("-")[0]
        month = event.date.split("-")[1]
        day = event.date.split("-")[2].split()[0]
        hours = event.date.split("-")[2].split()[1].split(":")[0]
        minutes = event.date.split("-")[2].split()[1].split(":")[1]
        seconds = event.date.split("-")[2].split()[1].split(":")[2]
        
        return int(year), int(month), int(day), int(hours), int(minutes), int(seconds)

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
            if len(grouped_events[year][month]) >= 3:
                marker = True
            for day in grouped_events[year][month]:
                if len(grouped_events[year][month][day]) >= 3:
                    marker = True
        
        if marker:
            year_markers.append(True)
        else:
            year_markers.append(False)

    return year_markers
