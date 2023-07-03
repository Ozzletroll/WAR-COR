from flask import redirect, url_for, abort
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
        