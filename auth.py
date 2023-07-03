from flask import redirect, url_for, abort
from flask_login import current_user


def permission_required(campaign):
    """Function for checking if user has campaign editing permissions"""
    if campaign in current_user.permissions:
        return True
    else:
        abort(403) 

