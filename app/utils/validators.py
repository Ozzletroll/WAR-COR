from flask import abort
from urllib.parse import urlparse, urljoin
from flask import request

from app.utils.formatters import increment_date, split_date



def validate_redirect_url(target_url):
    
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target_url))

    if test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc:
        return True
    else:
        abort(400, description=f"Invalid redirect url")


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
