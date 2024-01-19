import copy
from sqlalchemy import and_, or_

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
        self.has_events = False
        self.has_following_month = False
        self.epoch_offset = False
        self.hide_marker = False


class Day:

    def __init__(self):
        self.name = ""
        self.events = []
        self.has_following_day = False
        self.has_epoch = False
        self.has_epoch_end = False
        self.has_events = False
        self.epochs = []
        self.end_epochs = []
        self.epoch_has_events = False
        self.followed_by_epoch = False
        self.hide_marker = False
        self.no_following_events = True


def campaign_sort(campaign, epoch=None):
    """ Function that structures campaign event data for timeline rendering. Returns
        a list of year objects. If epoch parameter is given, returns only data
        from between that epochs start and end date values.

        Parameters:
            --------------------------------------
                campaign: Campaign model object
                    Campaign object to return timeline data from

                epoch(optional): Epoch model object
                    Epoch to use for start and end date values
            --------------------------------------

        Returns:
            year_list (list): A list of Year objects, for iteration in timeline template
  
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

                    # Sort days
                    combined_dict[year][month] = {key: value for key, value in sorted(combined_dict[year][month].items())}
            else:
                combined_dict[year] = dict2[year]

            # Sort months
            combined_dict[year] = {key: value for key, value in sorted(combined_dict[year].items())}

        # Sort years
        combined_dict = {key: value for key, value in sorted(combined_dict.items())}

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
                if epoch.has_events:
                    day_object.epoch_has_events = True


    # --- START --- #

    # Return whole campaign
    if epoch is None:
        events = (db.session.query(models.Event)
                .filter_by(campaign_id=campaign.id)
                .order_by(models.Event.year,
                        models.Event.month,
                        models.Event.day,
                        models.Event.hour,
                        models.Event.minute,
                        models.Event.second,)
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
        
    # Otherwise, get only events and epochs that fall between the given start and end values,
    # excluding the current epoch
    else:
        all_events = (db.session.query(models.Event)
                .filter_by(campaign_id=campaign.id)
                .order_by(models.Event.year,
                          models.Event.month,
                          models.Event.day,
                          models.Event.hour,
                          models.Event.minute,
                          models.Event.second,)
                          .all())
        
        events = [event for event in all_events if event in epoch.events]
        
        all_epochs_by_start_date = (db.session.query(models.Epoch)
                                    .filter_by(campaign_id=campaign.id)
                                    .order_by(models.Epoch.start_year,
                                              models.Epoch.start_month,
                                              models.Epoch.start_day)
                                              .all())
        
        epochs_by_start_date = [sub_epoch for sub_epoch in all_epochs_by_start_date 
                                if sub_epoch in epoch.sub_epochs]
        
        all_epochs_by_end_date = (db.session.query(models.Epoch)
                                  .filter_by(campaign_id=campaign.id)
                                  .order_by(models.Epoch.end_year,
                                            models.Epoch.end_month,
                                            models.Epoch.end_day)
                                            .all())
        
        epochs_by_end_date = [sub_epoch for sub_epoch in all_epochs_by_end_date 
                              if sub_epoch in epoch.sub_epochs]  

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
                    if isinstance(event, models.Event):
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
                
                # Flag day object as having epoch end element after it for
                # template rendering
                if day_object.has_epoch_end:
                    day_object.followed_by_epoch = True

                # Check if day markers can be hidden due to only having an epoch and no events
                if day_object.has_epoch or day_object.has_epoch_end:
                    if len(day_object.events) == 0:
                        day_object.hide_marker = True

                if len(day_object.events) > 0:
                    day_object.has_events = True

                # Append the day object to the month object
                month_object.days.append(day_object)

            # Flag day objects if the next day has epoch elements before them
            # for template rendering purposes
            for index, day_object in enumerate(month_object.days):
                if day_object.has_epoch and index != 0:
                    month_object.days[index - 1].followed_by_epoch = True

                if index == 0 and day_object.has_epoch:
                    month_object.epoch_offset = True

                if day_object.has_events:
                    month_object.has_events = True

                # Check all days after the current one to see if they hold any events
                if index != len(month_object.days) - 1:
                    for day in month_object.days[index + 1:]:
                        if len(day.events) != 0:
                            day_object.no_following_events = False
                            break

            # Append the month object to the year object
            year_object.months.append(month_object)   

        # Append the year object to the formatted list
        year_list.append(year_object)

    return year_list
