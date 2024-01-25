def split_date(datestring, epoch_date=False):
    """Function that splits a datestring into individual values,
    returns a list of integers"""

    year = datestring.split("/")[0]
    month = datestring.split("/")[1]
    day = datestring.split("/")[2].split()[0]

    if not epoch_date:
        hours = datestring.split("/")[2].split()[1].split(":")[0]
        minutes = datestring.split("/")[2].split()[1].split(":")[1]
        seconds = datestring.split("/")[2].split()[1].split(":")[2]
        return [int(year), int(month), int(day), int(hours), int(minutes), int(seconds)]

    else:
        return [int(year), int(month), int(day)]



def increment_datestring(datestring, args):
    """Function that takes a datestring, and the dictionary from request.args, 
    and returns the next day/week/month/year date as a string,
    ready for form pre population."""

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

    if "new_epoch" in args:
        values = split_date(datestring, epoch_date=True)
    else:
        values = split_date(datestring)
    year_format = len(datestring.split("/")[0])

    if "new_hour" in args:
        incremented_values = increment(values, 2)
        # Format date as string for form field
        datestring = (str(incremented_values[0]).zfill(year_format) 
                      + "/" + str(incremented_values[1]).zfill(2) 
                      + "/" + str(incremented_values[2]).zfill(2) 
                      + " " + str(incremented_values[3]).zfill(2) 
                      + ":00:00")

    # Move to the next day and format the string
    if "new_day" in args:
        incremented_values = increment(values, 3)
        # Format date as string for form field
        if "new_epoch" in args:
            datestring = (str(incremented_values[0]).zfill(year_format) 
                        + "/" + str(incremented_values[1]).zfill(2) 
                        + "/" + str(incremented_values[2]).zfill(2))
        else:
            datestring = (str(incremented_values[0]).zfill(year_format) 
                        + "/" + str(incremented_values[1]).zfill(2) 
                        + "/" + str(incremented_values[2]).zfill(2) 
                        + " 00:00:00")

    # Move to the next month and format the string
    if "new_month" in args:
        incremented_values = increment(values, 4)
        # Format date as string for form field
        datestring = (str(incremented_values[0]).zfill(year_format) 
                      + "/" + str(incremented_values[1]).zfill(2) 
                      + "/" + "01 00:00:00")

    return datestring
