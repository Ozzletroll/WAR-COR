from flask import render_template, redirect, request, url_for, flash, jsonify, make_response, session, abort
from sqlalchemy import select
from flask_login import login_required, current_user

import auth
import forms
import models
import utils.messengers as messengers

from app import db
from routes.membership import bp


#   =======================================
#                 MEMBERSHIP
#   =======================================


# View and add campaign users
@bp.route("/campaigns/<campaign_name>-<campaign_id>/edit-members", methods=["GET", "POST"])
@login_required
def edit_campaign_users(campaign_name, campaign_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id, title=campaign_name)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    form = forms.AddUserForm()

    # Set back button scroll target
    session["campaign_scroll_target"] = f"campaign-{campaign.id}"

    return render_template("campaign_members.html", 
                           campaign=campaign, 
                           form=form)


# Function called when adding a new user
@bp.route("/campaigns/<campaign_name>-<campaign_id>/add-user", methods=["GET"])
@login_required
def add_user(campaign_name, campaign_id):

    user_to_add = request.args["username"]

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    # Check if username exists
    user = db.session.execute(select(models.User).filter_by(username=user_to_add)).scalar()
    if user:
        # Check if user isn't already a member
        if campaign not in user.campaigns:

            messengers.send_invite_message(sender=current_user,
                                           recipient=user,
                                           campaign=campaign)

            flash(f"{user.username} invited to campaign.")
        else:
            flash(f"{user.username} is already a member of this campaign.")
    else:
        flash("User not in database, please check username.")

    return redirect(url_for("membership.edit_campaign_users",
                            campaign_name=campaign_name,
                            campaign_id=campaign.id))


# Remove campaign users
@bp.route("/campaigns/<campaign_name>-<campaign_id>/remove-user/<username>", methods=["GET"])
@login_required
def remove_campaign_users(campaign_name, campaign_id, username):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id, title=campaign_name)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    user_to_remove = username

    # Check if username exists
    user = db.session.execute(
        select(models.User)
        .filter_by(username=user_to_remove)).scalar()

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
    return redirect(url_for("membership.edit_campaign_users", 
                            campaign_name=campaign_name, 
                            campaign_id=campaign.id))


# Join campaign page
@bp.route("/campaigns/join-campaign", methods=["GET", "POST"])
@login_required
def join_campaign():

    form = forms.CampaignSearchForm()

    # Check if page has any results to render
    if "results" not in request.args:
        results = None
    else:
        results = request.args["results"]

    if form.validate_on_submit():
        search = request.form["search"].lower()

        # Ignore search if less than 3 characters
        if len(search) < 3:
            flash("Search queries must be three or more characters")
            return redirect(url_for("membership.join_campaign"))

        else:
            search_format = "%{}%".format(search)
            campaigns = db.session.execute(
                select(models.Campaign)
                .filter(models.Campaign.title.like(search_format))).scalars()

            results = [campaign for campaign in campaigns if campaign not in current_user.campaigns]
                                        
            if len(results) == 0:
                flash("No campaigns matching query found")
                return redirect(url_for("membership.join_campaign"))

            return render_template("join_campaign.html",
                                   form=form,
                                   results=results)

    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(field_name + ": " + error_message)

    return render_template("join_campaign.html",
                           form=form,
                           results=results)


# Function called when applying to join campaign 
@bp.route("/campaigns/join_campaign/<campaign_name>-<campaign_id>", methods=["GET"])
@login_required
def request_membership(campaign_name, campaign_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id, title=campaign_name)).scalar()
    
    # Retrieve the users with editing permissions for the campaign
    campaign_admins = db.session.execute(
        db.select(models.User)
        .join(models.user_edit_permissions)
        .where(models.user_edit_permissions.c.campaign_id == campaign.id)).scalars()

    messengers.send_membership_request(current_user, campaign_admins, campaign)
    flash(f"Membership request to campaign '{campaign_name}' sent")

    return redirect(url_for("membership.join_campaign"))


# Function called by user searching for new members on edit members page
@bp.route("/campaigns/<campaign_name>-<campaign_id>/user-search", methods=["POST"])
@login_required
def user_search(campaign_name, campaign_id):

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id, title=campaign_name)).scalar()

    # Query database for users with similar usernames
    search = request.form["username"]
    if len(search) == 0:
        response = make_response(jsonify({"message": "Please enter a search query"}), 400)
        return response
    
    search_format = "%{}%".format(search)
    users = db.session.execute(select(models.User)
                               .filter(models.User.username.like(search_format))).scalars()

    # Format results as dict
    results = {user.username: [user.id, url_for('membership.add_user',
                                                 campaign_name=campaign.title,
                                                 campaign_id=campaign.id,
                                                 username=user.username)]
            for user in users if user not in campaign.members}
    
    # Check if query returned no results
    if len(results) == 0:
        response = make_response(jsonify({"message": "No users found"}), 204)
    # Otherwise, send good response
    else:
        response = make_response(results, 200)
        
    return response


# Function called when user accepts a campaign invitation
@bp.route("/campaigns/accept-invite", methods=["POST"])
@login_required
def accept_invite():
    """ Function called via fetch request from navbar template when user accepts a campaign invitation. """

    message_id = request.form["message_id"]
    campaign_id = request.form["campaign_id"]

    message = db.session.execute(
        select(models.Message)
        .filter_by(id=message_id)).scalar()
    
    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id)).scalar()

    # Check if the campaign invitation is valid and for the current user
    if message in campaign.pending_invites and message.target_user == current_user:

        if current_user not in campaign.members:
            # Add user to campaign
            message.target_user.campaigns.append(campaign)
            # Remove message from user.messages list
            message.target_user.messages.remove(message)
            # Delete message
            db.session.delete(message)
            db.session.commit()
            flash(f"Accepted invitation to campaign: {campaign.title}")

            # Create recipients list, omitting the accepting user themselves
            recipients = [user for user in campaign.members if user.id != message.target_user.id]

            # Send new campaign member notification
            messengers.send_new_member_notification(current_user, 
                                                    recipients,
                                                    campaign,
                                                    current_user.username)
            
            # Set scroll target
            session["campaign_scroll_target"] = f"campaign-{campaign.id}"

        else:
            flash(f"Already a member of campaign: {campaign.title}")

    # If message is not valid for current user trying to access it
    # redirect to error page
    else:
        abort(403)

    return redirect(url_for("campaign.campaigns"))


# Function called when user declines a campaign invitation
@bp.route("/campaigns/decline-invite", methods=["GET"])
@login_required
def decline_invite():

    message_id = request.args["message_id"]

    message = db.session.execute(
        select(models.Message)
        .filter_by(id=message_id)).scalar()

    # Check if target message is actually for the current user
    if message.target_user == current_user:

        campaign_name_flash = message.target_campaign.title

        db.session.delete(message)
        db.session.commit()

        flash(f"Declined invitation to campaign: {campaign_name_flash}")

    return redirect(url_for("campaign.campaigns"))


# Function called when admin accepts new membership request
@bp.route("/campaigns/<campaign_name>-<campaign_id>/confirm-join-request", methods=["GET"])
@login_required
def confirm_request(campaign_name, campaign_id):

    message_id = request.args["message_id"]

    message = db.session.execute(
        select(models.Message)
        .filter_by(id=message_id)).scalar()
    
    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id)).scalar()

    # Assert current user has campaign editing permissions
    auth.permission_required(campaign)

    # Check message is valid and user not already in campaign
    if message.request and message.target_user not in campaign.members:
        
        # Add user to campaign
        message.target_user.campaigns.append(campaign)
        
        # Delete message
        db.session.delete(message)
        db.session.commit()

        # Send new member notification to campaign members
        messengers.send_new_member_notification(current_user, 
                                                campaign.members, 
                                                campaign, 
                                                message.target_user.username)
        
        flash(f"Added {message.target_user.username} to campaign: {campaign.title}")

    return redirect(url_for("campaign.campaigns"))


# Function called when admin declines new membership request
@bp.route("/campaigns/<campaign_name>-<campaign_id>/deny-join-request", methods=["GET"])
@login_required
def deny_request(campaign_name, campaign_id):

    message_id = request.args["message_id"]

    message = db.session.execute(
        select(models.Message)
        .filter_by(id=message_id)).scalar()
    
    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id)).scalar()

    # Assert current user has campaign editing permissions
    auth.permission_required(campaign)

    flash(f"Declined {message.target_user.username}'s request to join to campaign: {campaign.title}")

    # Delete message
    db.session.delete(message)
    db.session.commit()

    return redirect(url_for("campaign.campaigns"))


# Function called when granting a user campaign editing permissions
@bp.route("/campaigns/<campaign_name>-<campaign_id>/grant-permission", methods=["GET"])
@login_required
def add_permission(campaign_name, campaign_id):

    user_to_add = request.args["username"]
    user_id = request.args["user_id"]

    user = db.session.execute(
        select(models.User)
        .filter_by(username=user_to_add, id=user_id)).scalar()
    
    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(id=campaign_id, title=campaign_name)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    # Give user editing permissions
    if campaign not in user.permissions:
        user.permissions.append(campaign)
        db.session.commit()

    flash(f"Granted {user.username} campaign editing permissions.")
    return redirect(url_for("membership.edit_campaign_users", 
                            campaign_name=campaign_name, 
                            campaign_id=campaign.id))
