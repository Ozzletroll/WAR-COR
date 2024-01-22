from flask import render_template, redirect, url_for, flash, session
from sqlalchemy import select
from flask_login import login_required

import json

from app.forms import forms
from app.utils import authenticators
from app import models
import app.utils.serialisers as serialisers

from app.routes.data import bp
from app import db


#   =======================================
#            User Data Management
#   =======================================


# Data backup main page
@bp.route("/campaigns/<campaign_name>-<campaign_id>/data", methods=["GET", "POST"])
@login_required
def backup_page(campaign_name, campaign_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id)).scalar()

    # Check if the user has permissions to edit the target campaign.
    authenticators.permission_required(campaign)

    # Set back button scroll target
    session["campaign_scroll_target"] = f"campaign-{campaign.id}"

    form = forms.UploadJsonForm()

    if form.validate_on_submit():

        # Test json file
        file = form.file.data

        # If json is ok, populate campaign with json data
        if serialisers.test_json(file):

            # Reset the file pointer to the beginning
            file.seek(0) 
            data = json.load(file)   

            # Delete all existing current campaign data
            for epoch in campaign.epochs:
                db.session.delete(epoch)
            for event in campaign.events:
                db.session.delete(event)
            db.session.commit()

            # Overwrite campaign data
            campaign, errors = serialisers.campaign_import(data, campaign)

            # Convert json events into event objects
            for item in data["events"]:
                event, errors = serialisers.events_import(item)
                event.parent_campaign = campaign
                db.session.add(event)

            db.session.commit()

            # Convert json epochs into epoch objects
            for item in data["epochs"]:
                epoch, errors = serialisers.epochs_import(item)
                db.session.add(epoch)
                epoch.parent_campaign = campaign
                epoch.populate_self()

            db.session.commit()

            # Update campaign event and epoch relationships
            campaign.get_following_events()
            campaign.check_epochs()

            # Commit to db
            db.session.commit()
            flash(f"Campaign: {campaign.title} successfully restored from backup")

            return redirect(url_for("campaign.campaigns"))

        else:

            return redirect(url_for("data.backup_page", 
                                    campaign_name=campaign.url_title,
                                    campaign_id=campaign.id))

    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(error_message)

    return render_template("backup.html", campaign=campaign, form=form)


# Backup campaign data
@bp.route("/campaigns/<campaign_name>-<campaign_id>/data/export")
@login_required
def campaign_backup(campaign_name, campaign_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id)).scalar()

    # Check if the user has permissions to edit the target campaign.
    authenticators.permission_required(campaign)

    # Export campaign data as json file.
    json = serialisers.data_export(campaign)

    return json
