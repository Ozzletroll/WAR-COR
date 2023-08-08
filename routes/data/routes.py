from flask import render_template, redirect, request, url_for, flash
from sqlalchemy import select
from flask_login import login_required

import json

import forms
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
@bp.route("/campaigns/<campaign_name>/data", methods=["GET", "POST"])
@login_required
def backup_page(campaign_name):

    target_campaign_id = request.args["campaign_id"]
    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id, title=campaign_name)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    form = forms.UploadJsonForm()

    if form.validate_on_submit():

        try:
            # Get file and read json data
            file = form.file.data
            data = json.load(file)

        except json.JSONDecodeError:
            flash("Invalid JSON format")
            return redirect(url_for("data.backup_page", campaign_name=campaign.title, campaign_id=campaign.id))

        else:

            try:
                # Convert json data to campaign object
                campaign = serialisers.campaign_import(data, campaign)

            except KeyError:
                flash("KeyError: Please check JSON file formatting")
                return redirect(url_for("data.backup_page", campaign_name=campaign.title, campaign_id=campaign.id))


            else:
                # Delete all existing current campaign events
                for event in campaign.events:
                    db.session.delete(event)

                db.session.commit()
            
            try:
                # Convert json events into event objects
                for item in data["events"]:
                    event = serialisers.events_import(item)

                    event.parent_campaign = campaign
                    db.session.add(event)

            except KeyError:
                flash("KeyError: Please check JSON file formatting")
                return redirect(url_for("data.backup_page", campaign_name=campaign.title, campaign_id=campaign.id))

            else:
                db.session.commit()
                flash(f"Campaign {campaign.title} succesfully restored from backup")

        return redirect(url_for("campaign.campaigns"))

    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(error_message)

    return render_template("backup.html", campaign=campaign, form=form)


# Backup campaign data
@bp.route("/campaigns/<campaign_name>/data/export")
@login_required
def campaign_backup(campaign_name):

    target_campaign_id = request.args["campaign_id"]
    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id, title=campaign_name)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    # Export campaign data as json file.
    json = serialisers.data_export(campaign)

    return json
