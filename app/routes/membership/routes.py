from flask import render_template, redirect, request, url_for, flash, jsonify, make_response, session, abort
from sqlalchemy import select, func, not_
from flask_login import login_required, current_user
import json

from app.utils import authenticators, formatters, messengers
import app.utils.search as search_tools
from app.forms import forms
from app import db, models

from app.routes.membership import bp


#   =======================================
#                 MEMBERSHIP
#   =======================================

# View and add campaign users
@bp.route("/campaigns/<campaign_name>-<campaign_id>/edit-members", methods=["GET", "POST"])
@login_required
def edit_campaign_users(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign)

    search_form = forms.SearchUserForm()
    add_form = forms.AddUserForm()
    remove_form = forms.AddUserForm()

    # Set url for back button
    if request.referrer and "/edit-members" not in request.referrer:
        session["previous_url"] = request.referrer

    # Set back button scroll target
    session["campaign_scroll_target"] = f"campaign-{campaign.id}"

    return render_template("pages/campaign_members.html", 
                           campaign=campaign, 
                           search_form=search_form,
                           add_form=add_form,
                           remove_form=remove_form)


# Function called by user searching for new members on edit members page
@bp.route("/campaigns/<campaign_name>-<campaign_id>/user-search", methods=["POST"])
@login_required
def user_search(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))
    
    authenticators.permission_required(campaign)

    page = request.form.get("page", 1, type=int)
    search = request.form["username"]
    
    if len(search) == 0:
        response = make_response(jsonify({"message": "Please enter a search query"}), 400)
        return response

    search_format = "%{}%".format(search)
    users = (db.session.execute(select(models.User)
             .filter(models.User.username.like(search_format)))
             .scalars())

    results = formatters.format_user_search_results(users, campaign, search)

    if len(results) == 0:
        response = make_response(jsonify({"message": "No users found"}), 204)
    else:
        paginator = search_tools.Paginator(results, page, per_page=1)
        target_url = url_for("membership.add_user",
                    campaign_name=campaign.url_title,
                    campaign_id=campaign.id)
        new_page_url = url_for("membership.user_search", 
                               campaign_name=campaign.url_title, 
                               campaign_id=campaign.id)
        json = paginator.serialise(target_url, new_page_url)
        response = make_response(json, 200)
        
    return response


# Function called when inviting a new user via new user page
@bp.route("/campaigns/<campaign_name>-<campaign_id>/add-user", methods=["POST"])
@login_required
def add_user(campaign_name, campaign_id):
    """ Function called via hidden form submission from add members page.
    The form is populated dynamically by javascript when the user clicks
    the 'invite' button beside a username search result entry. """

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign)

    username = request.form["username"]
    user_id = request.form["user_id"]

    # Check if username exists
    user = (db.session.execute(select(models.User)
            .filter_by(username=username, id=user_id))
            .scalar())
    
    if user:
        # Check if user isn't already a member
        if campaign not in user.campaigns:

            messengers.send_invite_message(sender=current_user,
                                           recipient=user,
                                           campaign=campaign)

            flash(f"{user.username} invited to campaign")
        else:
            flash(f"{user.username} is already a member of this campaign")
    else:
        flash("User not in database, please check username")

    return redirect(url_for("membership.edit_campaign_users",
                            campaign_name=campaign_name,
                            campaign_id=campaign.id))


# Remove campaign users
@bp.route("/campaigns/<campaign_name>-<campaign_id>/remove-user", methods=["POST"])
@login_required
def remove_user(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))
    
    authenticators.permission_required(campaign)

    username = request.form["username"]
    user_id = request.form["user_id"]

    user = (db.session.execute(select(models.User)
            .filter_by(username=username, id=user_id))
            .scalar())

    if user:
        campaign.remove_user(user)
        if user.id == current_user.id:
            flash(f"Left campaign '{campaign.title}'")
        else:
            flash(f"Removed {user.username} from campaign")

    # Query campaign again in case the remove_user method deleted it
    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first())

    if campaign:
        if current_user in campaign.members:
            return redirect(url_for("membership.edit_campaign_users", 
                                    campaign_name=campaign_name, 
                                    campaign_id=campaign.id))
        else:
            return redirect(url_for("campaign.campaigns"))
    else:
        return redirect(url_for("campaign.campaigns"))


@bp.route("/campaigns/<campaign_name>-<campaign_id>/leave", methods=["POST"])
@login_required
def leave_campaign(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))
    
    username = request.form["username"]
    user_id = request.form["user_id"]

    user = (db.session.execute(select(models.User)
            .filter_by(username=username, id=user_id))
            .scalar())

    authenticators.user_verification(user)

    campaign.remove_user(user)
    flash(f"Left campaign '{campaign.title}'")

    return redirect(url_for("user.user_page", 
                            username=current_user.username))


# Join campaign page
@bp.route("/campaigns/join-campaign", methods=["GET", "POST"])
@login_required
def join_campaign():

    form = forms.SearchForm()
    request_form = forms.SubmitForm()

    page = request.args.get("page", 1, type=int)
    per_page = 6

    if request.method == "GET":
        
         # Check if page has any results to render
        if "search" not in request.args:
            results = None
            search = None
        else:
            search = request.args["search"]
            form.search.data = search
            search_format = "%{}%".format(search)

            campaigns_query = (select(models.Campaign)
                               .filter(
                                   func.lower(models.Campaign.title).like(search_format),
                                   models.Campaign.accepting_applications))

            results = db.paginate(campaigns_query, page=page, per_page=per_page, error_out=False)

        # Flash form errors
        for field_name, errors in form.errors.items():
            for error_message in errors:
                flash(field_name + ": " + error_message)

        return render_template("pages/join_campaign.html",
                               form=form,
                               request_form=request_form,
                               search=search,
                               results=results)


    elif request.method == "POST":

        if form.validate_on_submit():
            search = request.form["search"].lower()

            # Ignore search if less than 3 characters
            if len(search) < 3:
                flash("Search queries must be three or more characters")
                return redirect(url_for("membership.join_campaign"))

            else:
                search_format = "%{}%".format(search)

                campaigns_query = (select(models.Campaign)
                                   .filter(
                                       func.lower(models.Campaign.title).like(search_format),
                                       models.Campaign.accepting_applications))

                results = db.paginate(campaigns_query, page=page, per_page=per_page, error_out=False)

                if len(results.items) == 0:
                    flash("No campaigns matching query found")
                    return redirect(url_for("membership.join_campaign"))
                
        for field_name, errors in form.errors.items():
            for error_message in errors:
                flash(field_name + ": " + error_message)

        return render_template("pages/join_campaign.html",
                               form=form,
                               request_form=request_form,
                               search=search,
                               results=results)


# Function called when applying to join campaign 
@bp.route("/campaigns/join_campaign/<campaign_name>-<campaign_id>", methods=["POST"])
@login_required
def request_membership(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))
    
    # Retrieve the users with editing permissions for the campaign
    campaign_admins = campaign.admins

    if campaign.accepting_applications:
        messengers.send_membership_request(current_user, campaign_admins, campaign)
        flash(f"Membership request to campaign '{campaign.title}' sent")
    else:
        flash(f"Campaign '{campaign.title}' is not currently accepting membership applications")

    return redirect(url_for("membership.join_campaign"))


# Function called when user accepts a campaign invitation
@bp.route("/campaigns/accept-invite", methods=["POST"])
@login_required
def accept_invite():
    """ Function called via fetch request from navbar template when user accepts a campaign invitation. """

    message_id = request.form["message_id"]
    campaign_id = request.form["campaign_id"]

    message = (db.session.query(models.Message)
               .filter(models.Message.id == message_id)
               .first_or_404(description="No matching message found"))
    
    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

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

            # Create recipients list, omitting the accepting user themselves
            recipients = [user for user in campaign.members if user.id != message.target_user.id]

            # Send new campaign member notification
            messengers.send_new_member_notification(current_user,
                                                    recipients,
                                                    campaign,
                                                    current_user.username)
            
            # Set scroll target
            session["campaign_scroll_target"] = f"campaign-{campaign.id}"

    # If message is not valid for current user trying to access it
    # redirect to error page
    else:
        abort(403)

    return redirect(url_for("campaign.campaigns"))


# Function called when user declines a campaign invitation
@bp.route("/campaigns/decline-invite", methods=["POST"])
@login_required
def decline_invite():

    message_id = request.form["message_id"]

    message = (db.session.query(models.Message)
               .filter(models.Message.id == message_id)
               .first_or_404(description="No matching message found"))

    # Check if target message is actually for the current user
    if message.target_user == current_user:
        db.session.delete(message)
        db.session.commit()
    else:
        abort(403)

    response = make_response(jsonify({"Message": "Invite declined"}), 200)
    return response


# Function called when admin accepts new membership request
@bp.route("/campaigns/confirm-join-request", methods=["POST"])
@login_required
def confirm_request():

    campaign_id = request.form["campaign_id"]
    message_id = request.form["message_id"]

    message = (db.session.query(models.Message)
               .filter(models.Message.id == message_id)
               .first_or_404(description="No matching message found"))
    
    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign)

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
        
    return redirect(request.referrer)


# Function called when admin declines new membership request
@bp.route("/campaigns/deny-join-request", methods=["POST"])
@login_required
def deny_request():

    campaign_id = request.form["campaign_id"]
    message_id = request.form["message_id"]

    message = (db.session.query(models.Message)
               .filter(models.Message.id == message_id)
               .first_or_404(description="No matching message found"))
    
    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign)

    # Delete message
    db.session.delete(message)
    db.session.commit()

    response = make_response(jsonify({"Message": "Request declined"}), 200)
    return response


# Function called when granting a user campaign editing permissions
@bp.route("/campaigns/<campaign_name>-<campaign_id>/grant-permission", methods=["POST"])
@login_required
def add_permission(campaign_name, campaign_id):

    user_to_add = request.form["username"]
    user_id = request.form["user_id"]

    user = (db.session.query(models.User)
            .filter(models.User.id == user_id)
            .filter(models.User.username == user_to_add)
            .first_or_404(description="No matching user found"))
    
    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign)

    # Give user editing permissions
    if user in campaign.members and campaign not in user.permissions:
        user.permissions.append(campaign)
        db.session.commit()
        flash(f"Granted {user.username} campaign editing permissions")
        
    return redirect(url_for("membership.edit_campaign_users", 
                            campaign_name=campaign.url_title,
                            campaign_id=campaign.id))


# Function called via fetch request to update campaign membership settings
@bp.route("/campaigns/<campaign_name>-<campaign_id>/update-membership-settings", methods=["POST"])
@login_required
def update_membership_settings(campaign_name, campaign_id):

    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign)

    visibility = request.form["visibility"]
    membership = request.form["membership"]
    comment = request.form["comment"]

    if visibility == "private":
        campaign.private = True
    else:
        campaign.private = False

    if membership == "open":
        campaign.accepting_applications = True
    else:
        campaign.accepting_applications = False

    if comment == "private":
        campaign.comments = "private"
    elif comment == "open":
        campaign.comments = "open"
    else:
        campaign.comments = "disabled"

    db.session.commit()

    response = make_response(jsonify({"message": "Settings updated"}), 200)
    return response
