from flask import abort

from app.utils.formatters import increment_date, split_date



def validate_event_url_parameters(url_parameters):

    allowed_parameters = ["date", "new_month", "new_day", "new_hour", "template_id", "elem_id"]

    for parameter in url_parameters:
        if parameter not in allowed_parameters:
            abort(400, description=f"Invalid parameter: {parameter}")

        if parameter == "date":
            # Check for presence of increment parameter
            if not any(arg in url_parameters for arg in ["new_month", "new_day", "new_hour"]):
                abort(400, description=f"Missing URL parameters")

            # Check given date parameter is correct
            try:
                increment_date(url_parameters[parameter], url_parameters)
            except TypeError:
                abort(400, description=f"Invalid parameter: {parameter}")
            except ValueError:
                abort(400, description=f"Invalid parameter: {parameter}")

        elif parameter in ["new_month", "new_day", "new_hour"]:
            if url_parameters[parameter] not in ["True", "False"]:
                abort(400, description=f"Invalid parameter: {parameter}")

    return url_parameters
    

def validate_epoch_url_parameters(url_parameters):
    
    allowed_parameters = ["date", "template_id", "elem_id"]

    for parameter in url_parameters:
        if parameter not in allowed_parameters:
            abort(400, description=f"Invalid parameter: {parameter}")

        if parameter == "date":
            # Check given date parameter is correct
            try:
                date = split_date(url_parameters[parameter])
                if len(date) != 3:
                    abort(400, description=f"Invalid parameter: {parameter}")
            except ValueError:
                abort(400, description=f"Invalid parameter: {parameter}")

        elif parameter in ["new_month", "new_day", "new_hour"]:
            if url_parameters[parameter] not in ["True", "False"]:
                abort(400, description=f"Invalid parameter: {parameter}")

    return url_parameters
