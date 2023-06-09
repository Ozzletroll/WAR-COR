from flask import render_template, redirect, request, url_for, flash, jsonify, make_response
from sqlalchemy import select
from flask_login import login_required, current_user
from itertools import groupby
from datetime import datetime
import werkzeug

import auth
import forms
import models

from app import db
from routes.campaign import bp


#   =======================================
#                  Campaign
#   =======================================


# View all users campaigns
@bp.route("/campaigns")
@login_required
def campaigns():

    campaigns = current_user.campaigns
    campaigns.sort(key=lambda campaign: campaign.last_edited, reverse=True)

    return render_template("campaigns.html", campaigns=campaigns)


# View campaign overview
@bp.route("/campaigns/<campaign_name>/timeline/<campaign_id>")
def show_timeline(campaign_name, campaign_id):
    campaign = db.session.execute(select(models.Campaign).filter_by(id=campaign_id, title=campaign_name)).scalar()

    # Sort events into date order
    def custom_sort(event):

        year = event.date.split("-")[0]
        month = event.date.split("-")[1]
        day = event.date.split("-")[2].split()[0]
        hours = event.date.split("-")[2].split()[1].split(":")[0]
        minutes = event.date.split("-")[2].split()[1].split(":")[1]
        seconds = event.date.split("-")[2].split()[1].split(":")[2]
        
        return int(year), int(month), int(day), int(hours), int(minutes), int(seconds)

    sorted_events = sorted(campaign.events, key=custom_sort)

    # Structure events into dictionary, grouped by year
    groups = groupby(sorted_events, key=lambda event: (event.date.split("-")[0]))

    grouped_events = {year: list(group) for year, group in groups}

    # Group each years events into months
    for year in grouped_events:
        groups = groupby(grouped_events[year], key=lambda event: (event.date.split("-")[1]))
        grouped_months = {month: list(group) for month, group in groups}
        grouped_events[year] = grouped_months

    # Final example structure:
    # grouped_events: {5016: {06: [<Event 1>, <Event 2>], 
    #                         07: [<Event 3>, <Event 4>]},
    #                  5017: {01: [<Event 6>, <Event 7>]}}

    return render_template("timeline.html", campaign=campaign, timeline_data=grouped_events)


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
        new_campaign.last_edited = datetime.now()

        # Add new campaign to database
        db.session.add(new_campaign)
        # Add current user as campaign member, callsign will be set to None
        user.campaigns.append(new_campaign)
        # Give current user campaign editing permissions
        user.permissions.append(new_campaign)

        db.session.commit()

        campaign = db.session.execute(select(models.Campaign).filter_by(id=new_campaign.id)).scalar()
        return redirect(url_for("campaign.show_timeline", campaign_name=campaign.title, campaign_id=campaign.id))

    return render_template("new_campaign.html", form=form)


# Edit campaign data
@bp.route("/campaigns/<campaign_name>/<campaign_id>/edit", methods=["GET", "POST"])
@login_required
def edit_campaign(campaign_name, campaign_id):
    campaign = db.session.execute(select(models.Campaign).filter_by(id=campaign_id, title=campaign_name)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    form = forms.CreateCampaignForm(obj=campaign)
    form.submit.label.text = "Update Campaign Data"

    if form.validate_on_submit():
        campaign.title = request.form["title"]
        campaign.description = request.form["description"]
        campaign.last_edited = datetime.now()

        db.session.add(campaign)
        db.session.commit()

        return redirect(url_for("campaign.campaigns"))

    return render_template("edit_campaign.html", form=form, campaign=campaign)


# Delete campaign
@bp.route("/campaigns/<campaign_name>/<campaign_id>/delete", methods=["GET", "POST"])
@login_required
def delete_campaign(campaign_name, campaign_id):

    campaign = db.session.execute(select(models.Campaign).filter_by(title=campaign_name, id=campaign_id)).scalar()
    auth.permission_required(campaign)

    # Create login form to check credentials
    form = forms.LoginForm()

    if form.validate_on_submit():

        search_username = request.form["username"]
        password = request.form["password"]

        user = current_user
        search_user = db.session.execute(select(models.User).filter_by(username=search_username)).scalar()

        if search_user:
            if werkzeug.security.check_password_hash(pwhash=user.password, password=password):
                
                # Delete campaign from database
                db.session.delete(campaign)
                # Commit changes
                db.session.commit()
                return redirect(url_for("campaign.campaigns"))
            else:
                flash("Authentication failed. Incorrect password.")
                return redirect(url_for("campaign.delete_campaign", campaign_name=campaign_name, campaign_id=campaign_id))
        else:
            flash("Authentication failed. Incorrect username.")
            return redirect(url_for("campaign.delete_campaign", campaign_name=campaign_name, campaign_id=campaign_id))

    else:
        # Change LoginForm submit button text
        form.submit.label.text = "Delete Campaign"

        return render_template("delete_campaign.html", form=form, campaign=campaign)


# View and add campaign users
@bp.route("/campaigns/<campaign_name>/edit_members", methods=["GET", "POST"])
@login_required
def edit_campaign_users(campaign_name):
    target_campaign_id = request.args["campaign_id"]

    campaign = db.session.execute(
        select(models.Campaign).filter_by(id=target_campaign_id, title=campaign_name)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    form = forms.AddUserForm()

    return render_template("campaign_members.html", campaign=campaign, form=form)


# Remove campaign users
@bp.route("/campaigns/<campaign_name>/remove_users/<username>", methods=["GET"])
@login_required
def remove_campaign_users(campaign_name, username):
    target_campaign_id = request.args["campaign_id"]
    campaign = db.session.execute(
        select(models.Campaign).filter_by(id=target_campaign_id, title=campaign_name)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    user_to_remove = username

    # Check if username exists
    user = db.session.execute(select(models.User).filter_by(username=user_to_remove)).scalar()

    if user:
        # Check is user is actually a member of the campaign
        if user in campaign.members:
            user.campaigns.remove(campaign)
            flash(f"Removed {user.username} from campaign.")
        # Remove editing permissions if they exist
        if campaign in user.permissions:
            user.permissions.remove(campaign)
            flash(f"Removed {user.username}'s campaign permissions.")
        # Check if campaign is left with no users, and delete if so
        if len(campaign.members) == 0:
            db.session.delete(campaign)
            db.session.commit()
            return redirect(url_for("campaign.campaigns"))

        db.session.commit()
    else:
        flash("User not in database, please check username.")
    return redirect(url_for("campaign.edit_campaign_users", campaign_name=campaign_name, campaign_id=campaign.id))


# Function called by user searching for new members on edit members page
@bp.route("/campaigns/<campaign_name>/user_search", methods=["POST"])
@login_required
def user_search(campaign_name):
    target_campaign_id = request.args["campaign_id"]
    campaign = db.session.execute(
        select(models.Campaign).filter_by(id=target_campaign_id, title=campaign_name)).scalar()

    # Query database for users with similar usernames
    search = request.form["username"]
    search_format = "%{}%".format(search)
    users = db.session.execute(select(models.User)
                               .filter(models.User.username.like(search_format))).scalars()

    # Format results as dict
    results = {user.username: [user.id, url_for('campaign.add_user',
                                            campaign_name=campaign.title,
                                            campaign_id=campaign.id,
                                            username=user.username)]
            for user in users if user not in campaign.members}
    
    # Check if query returned no results
    if len(results) == 0:
        response = make_response(jsonify({"message": "No users found"}), 404)
    # Otherwise, send good response
    else:
        response = make_response(results, 200)
        
    return response


# Function called when adding a new user
@bp.route("/campaigns/<campaign_name>/add_user", methods=["GET"])
@login_required
def add_user(campaign_name):
    user_to_add = request.args["username"]
    target_campaign_id = request.args["campaign_id"]

    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    # Check if username exists
    user = db.session.execute(select(models.User).filter_by(username=user_to_add)).scalar()
    if user:
        # Check if user isn't already a member
        if campaign not in user.campaigns:
            # Add user as campaign member
            user.campaigns.append(campaign)
            db.session.commit()
            flash(f"{user.username} added to campaign.")
        else:
            flash(f"{user.username} is already a member of this campaign.")
    else:
        flash("User not in database, please check username.")

    return redirect(url_for("campaign.edit_campaign_users", campaign_name=campaign_name, campaign_id=campaign.id))


# Function called when granting a user campaign editing permissions
@bp.route("/campaigns/<campaign_name>/grant_permission", methods=["GET"])
@login_required
def add_permission(campaign_name):

    user_to_add = request.args["username"]
    user_id = request.args["user_id"]
    target_campaign_id = request.args["campaign_id"]

    user = db.session.execute(select(models.User).filter_by(username=user_to_add, id=user_id)).scalar()
    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id, title=campaign_name)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    # Give user editing permissions
    if campaign not in user.permissions:
        user.permissions.append(campaign)
        db.session.commit()

    flash(f"Granted {user.username} campaign editing permissions.")
    return redirect(url_for("campaign.edit_campaign_users", campaign_name=campaign_name, campaign_id=campaign.id))
