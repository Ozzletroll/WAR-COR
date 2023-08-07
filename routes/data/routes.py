from flask import render_template, redirect, request, url_for, flash, jsonify, make_response
from sqlalchemy import select
from flask_login import login_required, current_user

import auth
import forms
import models
import utils.organisers as organisers
import utils.messengers as messengers

from routes.data import bp
from app import db



#   =======================================
#            User Data Management
#   =======================================


# Backup campaign data
@bp.route("/campaigns/<campaign_name>/backup")
def campaign_backup(campaign_name):

    target_campaign_id = request.args["campaign_id"]

    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id, title=campaign_name)).scalar()

    # Export campaign data as json file.

    return redirect(url_for("campaign.campaigns"))


# Import campaign backup
@bp.route("/campaigns/<campaign_name>/import")
def import_campaign(campaign_name):

    target_campaign_id = request.args["campaign_id"]

    # Export campaign data as json file.
    return redirect(url_for("campaign.show_timeline", id=target_campaign_id))


# Export campaign timeline as pdf
@bp.route("/campaigns/<campaign_name>/export")
def export_campaign(campaign_name):

    target_campaign_id = request.args["campaign_id"]

    # Export campaign data as json file.
    return redirect(url_for("campaign.show_timeline", id=target_campaign_id))
