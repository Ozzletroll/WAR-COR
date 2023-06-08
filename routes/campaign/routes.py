from flask import render_template, redirect, request, url_for, flash, session
from sqlalchemy import select
from flask_login import login_required, current_user

import forms
import models

from app import db
from routes.campaign import bp

#   =======================================
#                  Campaign
#   =======================================


# View all users campaigns
@bp.route("/campaigns")
def campaigns():
    return render_template("campaigns.html")


# View campaign overview
@bp.route("/campaigns/<campaign_name>")
def show_timeline(campaign_name):

    target_id = session.get("campaign_id", None)
    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_id)).scalar()

    return render_template("timeline.html", campaign=campaign)


# Create new campaign
@bp.route("/campaigns/create_campaign", methods=["GET", "POST"])
@login_required
def create_campaign():

    form = forms.CreateCampaignForm()

    if form.validate_on_submit():
        user = current_user

        new_campaign = models.Campaign()

        new_campaign.title = request.form["title"]
        new_campaign.description = request.form["description"]

        # Add new campaign to database
        db.session.add(new_campaign)
        # Add current user as campaign member, callsign will be set to None
        user.campaigns.append(new_campaign)
        # Give current user campaign editing permissions
        user.permissions.append(new_campaign)

        db.session.commit()

        campaign = db.session.execute(select(models.Campaign).filter_by(id=new_campaign.id)).scalar()
        session["campaign_id"] = campaign.id
        return redirect(url_for("campaign.show_timeline", campaign_name=campaign.title))

    return render_template("new_campaign.html", form=form)


# Edit campaign data
@bp.route("/campaigns/<campaign_name>/edit", methods=["GET", "POST"])
def edit_campaign(campaign_name):

    target_campaign_id = session.get("campaign_id", None)

    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()

    # Check if the user has permissions to edit the target campaign.
    if campaign in current_user.permissions:

        form = forms.CreateCampaignForm(obj=campaign)

        if form.validate_on_submit():

            campaign.title = request.form["title"]
            campaign.description = request.form["description"]

            db.session.add(campaign)
            db.session.commit()

            session["campaign_id"] = campaign.id
            return redirect(url_for("campaign.show_timeline", campaign_name=campaign.title))

        return render_template("edit_campaign.html", form=form)

    # Redirect to homepage if user is trying to access a campaign they don't have permissions for.
    return redirect(url_for("home.home"))


# Edit campaign users
@bp.route("/campaigns/<campaign_name>/add_users", methods=["GET", "POST"])
@login_required
def add_campaign_users(campaign_name):

    target_campaign_id = session.get("campaign_id", None)

    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()

    # Check if the user has permissions to edit the target campaign.
    if campaign in current_user.permissions:

        form = forms.AddUserForm()

        if form.validate_on_submit():

            user_to_add = request.form["username"]

            # Check if username exists
            user = db.session.execute(select(models.User).filter_by(username=user_to_add)).scalar()
            if user:
                # Get campaign and add user as member
                user.campaigns.append(campaign)
                db.session.commit()
            else:
                print("User not in database, please check username.")
                flash("User not in database, please check username.")
            return redirect(url_for("campaign.edit_campaign", campaign_name=campaign_name))

        return render_template("edit_campaign.html", form=form)

    # Redirect to homepage if user is trying to access a campaign they don't have permissions for.
    return redirect(url_for("home.home"))


# Remove campaign users
@bp.route("/campaigns/<campaign_name>/remove_users/<username>", methods=["GET"])
@login_required
def remove_campaign_users(campaign_name, username):

    target_campaign_id = session.get("campaign_id", None)
    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()

    # Check if the user has permissions to edit the target campaign.
    if campaign in current_user.permissions:

        user_to_remove = username

        # Check if username exists
        user = db.session.execute(select(models.User).filter_by(username=user_to_remove)).scalar()
        if user:
            # Check is user is actually a member of the campaign
            if user in campaign.members:
                user.campaigns.remove(campaign)
                flash(f"Removed user {user} from campaign.")
                print(f"Removed user {user} from campaign.")
            # Remove editing permissions if they exist
            if campaign in user.permissions:
                user.permissions.remove(campaign)
                flash(f"Removed user {user}'s campaign permissions.")
                print(f"Removed user {user}'s campaign permissions.")
            db.session.commit()
        else:
            print("User not in database, please check username.")
            flash("User not in database, please check username.")
        return redirect(url_for("campaign.edit_campaign", campaign_name=campaign_name))

    # Redirect to homepage if user is trying to access a campaign they don't have permissions for.
    return redirect(url_for("home.home"))