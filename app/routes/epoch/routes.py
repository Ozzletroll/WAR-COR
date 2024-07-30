from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_required

from app import db, models
from app.forms import forms
from app.utils import authenticators, formatters, validators

from app.routes.epoch import bp


#   =======================================
#                  EPOCH
#   =======================================

# View epoch page
@bp.route("/campaigns/<campaign_name>-<campaign_id>/epoch/<epoch_title>-<epoch_id>", methods=["GET"])
def view_epoch(campaign_name, campaign_id, epoch_title, epoch_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))
    
    authenticators.check_campaign_visibility(campaign)

    epoch = (db.session.query(models.Epoch)
             .filter(models.Epoch.id == epoch_id)
             .first_or_404(description="No matching epoch found"))
    
    # Set scroll_to target for back button
    session["timeline_scroll_target"] = f"epoch-{epoch.id}"

    # Format html field data for sidebar buttons
    sidebar_data = formatters.format_html_field_shortcuts(epoch.dynamic_fields)

    # Format nested event timeline data
    timeline_data = campaign.return_timeline_data(epoch=epoch)

    return render_template("pages/epoch_page.html",
                           campaign=campaign,
                           epoch=epoch,
                           timeline_data=timeline_data,
                           sidebar_data=sidebar_data)


# Add new epoch
@bp.route("/campaigns/<campaign_name>-<campaign_id>/epoch/new-epoch", methods=["GET", "POST"])
@login_required
def new_epoch(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))
    
    authenticators.permission_required(campaign)

    form = forms.CreateEpochForm()
    
    if "date" in request.args and request.method == "GET":
        # Get the date argument
        datestring = request.args["date"]
        args = validators.validate_epoch_url_parameters(request.args)
        date_values = formatters.split_date(datestring)
        # Create placeholder event to prepopulate form
        epoch = models.Epoch()
        epoch.create_blank(date_values)
        form = forms.CreateEpochForm(obj=epoch)
        form.format_date_fields(epoch)

        # Set scroll_to target for back button
        target_date = args["date"].replace("/", "-")
        session["timeline_scroll_target"] = f"new-epoch-{target_date}"

    # If loading from template, update for with template's dynamic fields
    if "template_id" in request.args and request.method == "GET":
        template_id = request.args["template_id"]

        template = (db.session.query(models.Template)
                    .filter(models.Template.id == template_id)
                    .first_or_404(description="No matching template found"))
        
        authenticators.check_template_is_valid(template, campaign)
        form.load_template(template)

    if form.validate_on_submit():

        epoch = models.Epoch()
        epoch.update(form=form.data,
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

    return render_template("pages/new_epoch.html",
                           campaign=campaign,
                           campaign_name=campaign.url_title,
                           form=form,
                           new=True)


# Edit epoch
@bp.route("/campaigns/<campaign_name>-<campaign_id>/epoch/<epoch_title>-<epoch_id>/edit", methods=["GET", "POST"])
@login_required
def edit_epoch(campaign_name, campaign_id, epoch_title, epoch_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))
    
    authenticators.permission_required(campaign)

    epoch = (db.session.query(models.Epoch)
             .filter(models.Epoch.id == epoch_id)
             .first_or_404(description="No matching epoch found"))

    # Set back button scroll target
    session["timeline_scroll_target"] = f"epoch-{epoch.id}"

    form = forms.CreateEpochForm(obj=epoch)
    form.submit.label.text = "Update Epoch"
    delete_form = forms.SubmitForm()

    if request.method == "GET":
        form.format_date_fields(epoch)

    # If loading from template, update for with template's dynamic fields
    if "template_id" in request.args and request.method == "GET":
        template_id = request.args["template_id"]

        template = (db.session.query(models.Template)
                    .filter(models.Template.id == template_id)
                    .first_or_404(description="No matching template found"))
        
        authenticators.check_template_is_valid(template, campaign)
        form.load_template(template)

    if form.validate_on_submit():

        epoch.update(form=form.data,
                     parent_campaign=campaign)

        return redirect(url_for("campaign.edit_timeline", 
                                campaign_name=campaign.url_title,
                                campaign_id=campaign.id))
    
    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(field_name + ": " + error_message)

    return render_template("pages/new_epoch.html",
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

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign)

    epoch = (db.session.query(models.Epoch)
                .filter(models.Epoch.id == epoch_id)
                .first_or_404(description="No matching epoch found"))

    campaign.clear_cache()
    db.session.delete(epoch)
    db.session.commit()
    
    # Update all epochs
    campaign.check_epochs()

    return redirect(url_for("campaign.edit_timeline",
                            campaign_name=campaign.url_title,
                            campaign_id=campaign.id))
