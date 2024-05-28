from flask import abort, jsonify
from flask_login import current_user
from functools import wraps


def permission_required(campaign):
    """Function for checking if user has campaign editing permissions"""
    if campaign in current_user.permissions:
        return True
    else:
        abort(403) 


def user_verification(user):
    """Function for checking if current user is the user they are trying to edit"""
    try: 
        if user.id == current_user.id:
            return True
        else:
            abort(403) 
    except AttributeError:
        abort(403) 
        

def check_membership(campaign):
    """Function for checking if the current user is actually a member of a given campaign"""
    if campaign in current_user.campaigns:
        return True
    else:
        abort(403)
        

def check_campaign_visibility(campaign):
    """Function to require login if campaign is private"""
    if campaign.private:
        description = "This campaign is flagged as 'Members Only'. To obtain access, please contact the campaign administrator."
        if current_user.is_authenticated:
            if current_user not in campaign.members:
                abort(403, description=description)
            else:
                return True
        else:
            abort(403, description=description)


def check_campaign_comment_status(campaign):
    """ Function to check if campaign comments are enabled """
    if campaign.comments == "private":
        description = "Comments are set to 'Members Only' for this campaign"
        if current_user in campaign.members:
            return True
    elif campaign.comments == "open":
        return True
    else:
        description = "Comments are disabled for this campaign"

    abort(403, description=description)


def check_comment_form_visibility(campaign):

    if campaign.comments == "private":
        if current_user in campaign.members:
            return True
    elif campaign.comments == "open":
        return True
        
    return False


def login_required_api(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return function(*args, **kwargs)
        else:
            return jsonify(error="Login required"), 401
    return decorated_function
