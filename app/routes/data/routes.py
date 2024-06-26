from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_required

import json

from app.forms import forms
from app.utils import authenticators
from app import models
import app.utils.serialisers as serialisers

from app.routes.data import bp
from app import db, limiter


#   =======================================
#            User Data Management
#   =======================================


# Data backup main page
@bp.route("/campaigns/<campaign_name>-<campaign_id>/data", methods=["GET", "POST"])
@login_required
def backup_page(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))
    
    # Check if the user has permissions to edit the target campaign.
    authenticators.permission_required(campaign)

    # Set back button scroll target
    session["campaign_scroll_target"] = f"campaign-{campaign.id}"

    # Set url for back button
    if request.referrer and request.referrer != request.url:
        session["previous_url"] = request.referrer

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
                epoch.sub_epochs.clear()
                db.session.delete(epoch)
            for event in campaign.events:
                db.session.delete(event)
            db.session.commit()

            # Overwrite campaign data
            campaign, errors = serialisers.campaign_import(data, campaign)

            # Convert json events into event objects
            for item in data["events"]:
                event, errors = serialisers.events_import(item, campaign)

            # Convert json epochs into epoch objects
            for item in data["epochs"]:
                epoch, errors = serialisers.epochs_import(item, campaign)

            db.session.commit()

            # Update campaign event and epoch relationships
            campaign.get_following_events()
            campaign.check_epochs()
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

    return render_template("pages/backup.html", campaign=campaign, form=form)


# Backup campaign data
@bp.route("/campaigns/<campaign_name>-<campaign_id>/data/export")
@login_required
@limiter.limit("2/second;5/minute")
def campaign_backup(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))
    
    # Check if the user has permissions to edit the target campaign.
    authenticators.permission_required(campaign)

    # Export campaign data as json file.
    json = serialisers.data_export(campaign)

    return json
