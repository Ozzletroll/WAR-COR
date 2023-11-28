from flask import render_template, redirect, request, url_for, flash, session
from sqlalchemy import select
from flask_login import login_required

from app.forms import forms
from app import models
from app.utils import authenticators

from app import db
from app.routes.epoch import bp


#   =======================================
#                  EPOCH
#   =======================================

# Add new epoch
@bp.route("/campaigns/<campaign_name>-<campaign_id>/epoch/new_epoch", methods=["GET", "POST"])
@login_required
def new_epoch(campaign_name, campaign_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(title=campaign_name, id=campaign_id)).scalar()

    authenticators.permission_required(campaign)

    # Check if date argument given
    if "date" in request.args:
        # Create placeholder event to prepopulate form
        epoch = models.Epoch()

        epoch.start_date = request.args["date"]
        epoch.end_date = request.args["date"]
        form = forms.CreateEpochForm(obj=epoch)

    # Otherwise, create default empty form
    else:
        form = forms.CreateEpochForm()

    if form.validate_on_submit():

        # Create new epoch and populate with form data
        epoch = models.Epoch()
        epoch.update(form=request.form,
                     parent_campaign=campaign,
                     new=True)

        # Set back button scroll target
        session["timeline_scroll_target"] = f"epoch-{epoch.id}"

        return redirect(url_for("campaign.edit_timeline", 
                                campaign_name=campaign.url_title,
                                campaign_id=campaign.id))
    
    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(field_name + ": " + error_message)

    return render_template("new_epoch.html",
                           campaign=campaign,
                           campaign_name=campaign.url_title,
                           form=form)



# Edit epoch
@bp.route("/campaigns/<campaign_name>-<campaign_id>/epoch/<epoch_title>-<epoch_id>/edit", methods=["GET", "POST"])
@login_required
def edit_epoch(campaign_name, campaign_id, epoch_title, epoch_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(title=campaign_name, id=campaign_id)).scalar()

    authenticators.permission_required(campaign)

    epoch = db.session.execute(
        select(models.Epoch)
        .filter_by(title=epoch_title, id=epoch_id)).scalar()

    # Set back button scroll target
    session["timeline_scroll_target"] = f"epoch-{epoch.id}"

    form = forms.CreateEpochForm(obj=epoch)

    if form.validate_on_submit():

        epoch.update(form=request.form,
                     parent_campaign=campaign)

        return redirect(url_for("campaign.edit_timeline", 
                                campaign_name=campaign.url_title,
                                campaign_id=campaign.id))
    
    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(field_name + ": " + error_message)

    # Change form label to 'update'
    form.submit.label.text = "Update Epoch"

    return render_template("new_epoch.html",
                           campaign=campaign,
                           campaign_name=campaign.url_title,
                           form=form,
                           epoch=epoch,
                           edit_page=True)



# Delete epoch
@bp.route("/campaigns/<campaign_name>-<campaign_id>/epoch/<epoch_title>-<epoch_id>/delete", methods=["GET", "POST"])
@login_required
def delete_epoch(campaign_name, campaign_id, epoch_title, epoch_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(title=campaign_name, id=campaign_id)).scalar()

    authenticators.permission_required(campaign)

    epoch = db.session.execute(
        select(models.Epoch)
        .filter_by(title=epoch_title, id=epoch_id)).scalar()

    db.session.delete(epoch)
    db.session.commit()
    
    # Update all epochs
    campaign.check_epochs()

    return redirect(url_for("campaign.edit_timeline",
                            campaign_name=campaign.url_title,
                            campaign_id=campaign.id))
