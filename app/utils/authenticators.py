from flask import abort
from flask_login import current_user


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
                return
        else:
            abort(403, description=description)
