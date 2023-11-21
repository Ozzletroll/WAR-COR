from flask import render_template, redirect, request, url_for, flash, session
from sqlalchemy import select
from flask_login import login_required, current_user
import werkzeug

from warcor.forms import forms
from warcor import models
from warcor.utils import authenticators
import warcor.utils.organisers as organisers

from warcor import db
from warcor.routes.campaign import bp


#   =======================================
#                  Campaign
#   =======================================


# View all campaigns
@bp.route("/campaigns")
@login_required
def campaigns():

    campaigns = current_user.campaigns
    campaigns.sort(key=lambda campaign: campaign.last_edited, reverse=True)

    return render_template("campaigns.html", 
                           campaigns=campaigns)


# View campaign overview
@bp.route("/campaigns/<campaign_name>-<campaign_id>")
def show_timeline(campaign_name, campaign_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id, title=campaign_name)).scalar()

    # Sort event data for template rendering
    grouped_events = organisers.campaign_sort(campaign)

    # Set back button scroll target
    session["campaign_scroll_target"] = f"campaign-{campaign.id}"

    return render_template("timeline.html", 
                           campaign=campaign, 
                           timeline_data=grouped_events)


# View campaign editing page
@bp.route("/campaigns/<campaign_name>-<campaign_id>/edit")
@login_required
def edit_timeline(campaign_name, campaign_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id, title=campaign_name)).scalar()
    
    # Check if the user has permissions to edit the target campaign.
    authenticators.permission_required(campaign)

    # Sort event data for template rendering
    grouped_events = organisers.campaign_sort(campaign)

    # Set back button scroll target
    session["campaign_scroll_target"] = f"campaign-{campaign.id}"

    return render_template("timeline.html", 
                           campaign=campaign, 
                           timeline_data=grouped_events,
                           edit=True)


# Create new campaign
@bp.route("/campaigns/create_campaign", methods=["GET", "POST"])
@login_required
def create_campaign():
    form = forms.CreateCampaignForm()

    if form.validate_on_submit():

        # Create and populate campaign object
        new_campaign = models.Campaign()
        new_campaign.update(form=request.form, 
                            new=True)
        
        # Add current user as campaign members
        current_user.campaigns.append(new_campaign)

        # Give current user campaign editing permissions
        current_user.permissions.append(new_campaign)

        db.session.commit()

        # Get campaign for redirect
        campaign = db.session.execute(
            select(models.Campaign)
            .filter_by(id=new_campaign.id)).scalar()

        return redirect(url_for("campaign.edit_timeline", 
                                campaign_name=campaign.title, 
                                campaign_id=campaign.id))

    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(field_name + ": " + error_message)

    return render_template("new_campaign.html", 
                           form=form)


# Edit campaign data
@bp.route("/campaigns/<campaign_name>-<campaign_id>/data/edit", methods=["GET", "POST"])
@login_required
def edit_campaign(campaign_name, campaign_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id, title=campaign_name)).scalar()

    # Check if the user has permissions to edit the target campaign.
    authenticators.permission_required(campaign)

    form = forms.CreateCampaignForm(obj=campaign)
    form.submit.label.text = "Update Campaign Data"

    # Update campaign if form submitted
    if form.validate_on_submit():
        campaign.update(form=request.form)
        return redirect(url_for("campaign.campaigns"))

    # Set back button scroll target
    session["campaign_scroll_target"] = f"campaign-{campaign.id}"

    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(field_name + ": " + error_message)

    return render_template("new_campaign.html", 
                           form=form, 
                           campaign=campaign,
                           edit=True)


# Delete campaign
@bp.route("/campaigns/<campaign_name>-<campaign_id>/delete", methods=["GET", "POST"])
@login_required
def delete_campaign(campaign_name, campaign_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(title=campaign_name, id=campaign_id)).scalar()
    
    authenticators.permission_required(campaign)

    # Create login form to check credentials
    form = forms.LoginForm()

    if form.validate_on_submit():

        search_username = request.form["username"]
        password = request.form["password"]

        user = current_user
        search_user = db.session.execute(
            select(models.User)
            .filter_by(username=search_username)).scalar()

        if search_user:
            if search_user.id == current_user.id:
                if werkzeug.security.check_password_hash(pwhash=user.password, password=password):
                    
                    # Delete campaign from database
                    db.session.delete(campaign)
                    # Commit changes
                    db.session.commit()
                    return redirect(url_for("campaign.campaigns"))

        flash("Authentication failed. Please check username/password.")
        return redirect(url_for("campaign.delete_campaign", 
                                campaign_name=campaign_name, 
                                campaign_id=campaign_id))

    else:
        # Change LoginForm submit button text
        form.submit.label.text = "Delete Campaign"

        return render_template("delete_campaign.html", 
                               form=form, 
                               campaign=campaign)
