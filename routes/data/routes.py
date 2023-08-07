from flask import render_template, redirect, request, url_for, flash, jsonify, make_response
from sqlalchemy import select
from flask_login import login_required

import auth
import models
import utils.organisers as organisers
import utils.messengers as messengers
import utils.serialisers as serialisers

from routes.data import bp
from app import db



#   =======================================
#            User Data Management
#   =======================================


# Data backup main page
@bp.route("/campaigns/<campaign_name>/data")
@login_required
def backup_page(campaign_name):

    target_campaign_id = request.args["campaign_id"]
    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id, title=campaign_name)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    return render_template("backup.html", campaign=campaign)


# Backup campaign data
@bp.route("/campaigns/<campaign_name>/data/export")
@login_required
def campaign_backup(campaign_name):


    target_campaign_id = request.args["campaign_id"]
    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id, title=campaign_name)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    # Export campaign data as json file.
    serialisers.data_export(campaign)

    return redirect(url_for("campaign.campaigns"))


# Import campaign backup
@bp.route("/campaigns/<campaign_name>/data/import")
@login_required
def import_campaign(campaign_name):

    target_campaign_id = request.args["campaign_id"]

    # Export campaign data as json file.
    return redirect(url_for("campaign.show_timeline", id=target_campaign_id))
