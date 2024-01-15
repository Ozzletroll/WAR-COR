from flask import render_template, redirect, request, url_for, flash, session
from sqlalchemy import select
from flask_login import login_required

from app import db, models
from app.forms import forms
from app.utils import authenticators

from app.routes.epoch import bp


#   =======================================
#                  EPOCH
#   =======================================

# View epoch page
@bp.route("/campaigns/<campaign_name>-<campaign_id>/epoch/<epoch_title>-<epoch_id>", methods=["GET"])
def view_epoch(campaign_name, campaign_id, epoch_title, epoch_id):

    campaign = db.session.execute(
            select(models.Campaign)
            .filter_by(id=campaign_id)).scalar()
    
    authenticators.check_campaign_visibility(campaign)

    epoch = db.session.execute(
        select(models.Epoch)
        .filter_by(id=epoch_id)).scalar()
    
    # Set scroll_to target for back button
    session["timeline_scroll_target"] = f"epoch-{epoch.id}"

    timeline_data = campaign.return_timeline_data(epoch=epoch)

    # Find all the contained child epochs
    sub_epochs = [epoch for year in timeline_data 
                  for month in year.months 
                  for day in month.days 
                  if day.has_epoch 
                  for epoch in day.epochs]
    
    # Determine back button functionality if dealing with nested epochs
    url_titles = [epoch.url_title for epoch in sub_epochs] 
    url_titles_found = [title for title in url_titles if title in request.referrer]
    if len(url_titles_found) == 0:
        can_use_referrer = True
    else:
        can_use_referrer = False

    return render_template("epoch_page.html",
                           campaign=campaign,
                           epoch=epoch,
                           timeline_data=timeline_data,
                           can_use_referrer=can_use_referrer)


# Add new epoch
@bp.route("/campaigns/<campaign_name>-<campaign_id>/epoch/new_epoch", methods=["GET", "POST"])
@login_required
def new_epoch(campaign_name, campaign_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id)).scalar()

    authenticators.permission_required(campaign)

    # Check if date argument given
    if "date" in request.args:
        # Create placeholder event to prepopulate form
        epoch = models.Epoch()

        epoch.start_date = request.args["date"] + "/01"
        epoch.end_date = request.args["date"] + "/02"
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
                           form=form,
                           new=True)


# Edit epoch
@bp.route("/campaigns/<campaign_name>-<campaign_id>/epoch/<epoch_title>-<epoch_id>/edit", methods=["GET", "POST"])
@login_required
def edit_epoch(campaign_name, campaign_id, epoch_title, epoch_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id)).scalar()

    authenticators.permission_required(campaign)

    epoch = db.session.execute(
        select(models.Epoch)
        .filter_by(id=epoch_id)).scalar()

    # Set back button scroll target
    session["timeline_scroll_target"] = f"epoch-{epoch.id}"

    form = forms.CreateEpochForm(obj=epoch)
    delete_form = forms.SubmitForm()

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
                           delete_form=delete_form,
                           epoch=epoch,
                           edit_page=True)


# Delete epoch
@bp.route("/campaigns/<campaign_name>-<campaign_id>/epoch/<epoch_title>-<epoch_id>/delete", methods=["POST"])
@login_required
def delete_epoch(campaign_name, campaign_id, epoch_title, epoch_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id)).scalar()

    authenticators.permission_required(campaign)

    epoch = db.session.execute(
        select(models.Epoch)
        .filter_by(id=epoch_id)).scalar()

    db.session.delete(epoch)
    db.session.commit()
    
    # Update all epochs
    campaign.check_epochs()

    return redirect(url_for("campaign.edit_timeline",
                            campaign_name=campaign.url_title,
                            campaign_id=campaign.id))
