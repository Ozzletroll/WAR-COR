from itertools import groupby
import copy
from collections import defaultdict

from app import db, models



# Classes used for timeline data organisation
class Year:

    def __init__(self):
        self.name = ""
        self.months = []


class Month:

    def __init__(self):
        self.name = ""
        self.days = []
        self.has_following_month = False


class Day:

    def __init__(self):
        self.name = ""
        self.events = []
        self.has_following_day = False
        self.has_epoch = False
        self.has_epoch_end = False
        self.epochs = []
        self.end_epochs = []
        self.epoch_has_events = False


def campaign_sort(campaign):
    """ Function that structures campaign event data for timeline rendering. Returns
        a list of year objects.
    
        Sorting is achieved by first creating nested dictionaries to represent the
        timeline structure, which will be used for iteration purposes in order to create
        Year, Month, and Day objects. 
        
        The first dictionary structure is created by combining two dictionaries of the 
        campaigns epochs organised by start date and end date.

            Example: {year: {month: [<Epoch 1>, <Epoch 2>]}}

        Next, a similar dictionary is created from the campaigns events, with an 
        additional layer of nested dictionaries representing days. The event objects
        themselves are nested inside the day entries.

            Example: {year: {month: {day: [<Event 3>, <Event 4>]}}}
        
        These two nested dictionaries are then combined into one. The "events" dictionary
        is used as the primary structure, and new entries are created for any year/month
        that only contains epochs.

            Example: 
        
            If there were two events that occurred in 5015/01/01, and one epoch that began
            in 5014/05/01 and ended in 5016/01/01, the dict would be:

            final_group = {5014: {05: [<Epoch 1>]}},
                           5015: {01: {01: [<Event 1>, <Event 2>]},
                           5016: {01: [<Epoch 2>]}}

        Finally, this dict is used to create a structure of nested
        objects, allowing easier rendering in the Jinja template:                     

            Month objects are assigned as a property of Year objects under Year.months. 
            Day objects are assigned as properties of Month objects under Month.days.
            Epochs are assigned under Month.epochs.
            Event objects are assigned under Day.events.

        Other properties are also assigned here to assist in template rendering.
        
    """

    def create_dict(object_list, year_attr, month_attr, day_attr):

        dict = {}
        for item_object in object_list:
            
            year = getattr(item_object, year_attr)
            month = getattr(item_object, month_attr)
            day = getattr(item_object, day_attr)

            if year not in dict:
                dict[year] = {}

            if month not in dict[year]:
                dict[year][month] = {}

            if day not in dict[year][month]:
                dict[year][month][day] = []

            dict[year][month][day].append(item_object)

        return dict
    

    def merge_dicts(dict1, dict2):

        combined_dict = copy.deepcopy(dict1)

        for year in dict2:
            if year in combined_dict:
                for month in dict2[year]:
                    if month in combined_dict[year]:
                        for day in dict2[year][month]:
                            if day in combined_dict[year][month]:
                                pass
                            else:
                                combined_dict[year][month][day] = dict2[year][month][day]
                    else:
                        combined_dict[year][month] = dict2[year][month]
            else:
                combined_dict[year] = dict2[year]

        return combined_dict


    def has_following(index, level, current_item):
        """ Function to determine if month/day within timeline has a consecutive following month/day.
            Used within the template to determine placement of +New Event buttons.
            
            Parameters:
            -------------------------------------------------
                index : int
                    Index of current loop

                level: dict
                    The current level of the nested dict
                    being iterated through.

                    When checking a month, use:
                    level=final_group[year]

                    When checking a day, use:
                    level=final_group[year][month]

                item: dict
                    The current item of the level iterable

            -------------------------------------------------

            """

        if index != len(level) - 1:
            next = list(level.keys())[index + 1]

            if int(next) == int(current_item) + 1:
                return True

        else:
            return False


    def check_for_epoch(dictionary, year, month, day, day_object, has_epoch_attr, epochs_attr):
        try:
            epochs = dictionary[year][month][day]
        except KeyError:
            pass
        else:
            setattr(day_object, has_epoch_attr, True)
            for epoch in epochs:
                epochs_attr.append(epoch)


    # --- START ---

    events = (db.session.query(models.Event)
            .filter_by(campaign_id=campaign.id)
            .order_by(models.Event.year, 
                    models.Event.month, 
                    models.Event.day)
                    .all())
    
    epochs_by_start_date = (db.session.query(models.Epoch)
                            .filter_by(campaign_id=campaign.id)
                            .order_by(models.Epoch.start_year,
                                      models.Epoch.start_month,
                                      models.Epoch.start_day)
                                      .all())
    
    epochs_by_end_date = (db.session.query(models.Epoch)
                          .filter_by(campaign_id=campaign.id)
                          .order_by(models.Epoch.end_year,
                                    models.Epoch.end_month,
                                    models.Epoch.end_day)
                                    .all())

    year_dict = create_dict(object_list=events,
                            year_attr="year",
                            month_attr="month",
                            day_attr="day")
    
    epoch_start_dict = create_dict(object_list=epochs_by_start_date,
                                   year_attr="start_year",
                                   month_attr="start_month",
                                   day_attr="start_day")
    
    epoch_end_dict = create_dict(object_list=epochs_by_end_date,
                                 year_attr="end_year",
                                 month_attr="end_month",
                                 day_attr="end_day")

    combined_epochs_dict = merge_dicts(epoch_start_dict, epoch_end_dict)

    final_group = merge_dicts(year_dict, combined_epochs_dict)

    # Turn each level of the hierarchy into an object, with the level below as a list held in a property
    year_list = []

    for year in final_group:

        year_object = Year()
        year_object.name = str(year)

        for month_index, month in enumerate(final_group[year]):

            month_object = Month()
            month_object.name = str(month).zfill(2)

            # Determine if the following month is the next consecutive month
            if has_following(index=month_index, level=final_group[year], current_item=month):
                month_object.has_following_month = True

            for day_index, day in enumerate(final_group[year][month]):

                day_object = Day()
                day_object.name = str(day).zfill(2)

                # Determine if the following day is the next consecutive day
                if has_following(index=day_index, level=final_group[year][month], current_item=day):
                    day_object.has_following_day = True

                # Append all the days event to the day object
                for event in final_group[year][month][day]:
                    day_object.events.append(event)

                # Check if day has any epoch starts
                check_for_epoch(epoch_start_dict, 
                                year, month, day,
                                day_object, 
                                "has_epoch", 
                                day_object.epochs)
                
                # Check if day has any epoch ends
                check_for_epoch(epoch_end_dict, 
                                year, month, day,
                                day_object, 
                                "has_epoch_end", 
                                day_object.end_epochs)

                # Append the day object to the month object
                month_object.days.append(day_object)

            # Append the month object to the year object
            year_object.months.append(month_object)   

        # Append the year object to the formatted list
        year_list.append(year_object)

    return year_list
