from flask import render_template, redirect, request, url_for, session, flash, make_response
from flask_login import login_required, current_user
from datetime import datetime

from app.forms import forms
from app import db, models
from app.utils import authenticators, formatters, messengers, validators

from app.routes.event import bp


#   =======================================
#                  Event
#   =======================================


# View event
@bp.route("/campaigns/<campaign_name>-<campaign_id>/event/<event_name>-<event_id>", methods=["GET", "POST"])
def view_event(campaign_name, campaign_id, event_name, event_id):

    page = request.args.get("page", 1, type=int)

    event = (db.session.query(models.Event)
             .filter(models.Event.id == event_id)
             .first_or_404(description="No matching event found"))
    
    paginated_comments = event.return_paginated_comments(page)

    campaign = event.parent_campaign

    authenticators.check_campaign_visibility(campaign)
    comment_form_visible = authenticators.check_comment_form_visibility(campaign)

    form = forms.CommentForm()
    delete_form = forms.SubmitForm()

    # Format html field data for sidebar buttons
    sidebar_data = formatters.format_html_field_shortcuts(event.dynamic_fields)

    # Set scroll_to target for back button
    session["timeline_scroll_target"] = f"event-{event.id}"

    # Check if new comment submitted
    if form.validate_on_submit():

        authenticators.check_campaign_comment_status(campaign)

        comment = models.Comment()
        comment.update(form=request.form,
                       parent_event=event,
                       author=current_user)
        messengers.send_comment_notification(sender=current_user,
                                             recipients=campaign.members,
                                             campaign=campaign,
                                             event=event)

        # Set redirect page number to last page
        last_page = event.return_paginated_comments(page).pages

        # Set scroll to target to newly created comment
        session["comment_scroll_target"] = f"comment-{comment.id}"

        parameters = {
            "campaign_name": campaign.url_title,
            "campaign_id": campaign.id,
            "event_name": event.url_title,
            "event_id": event.id
        }

        # Only provide page parameter if there are multiple pages
        if last_page != 1:
            parameters["page"] = last_page

        return redirect(url_for("event.view_event", **parameters))

    return render_template("pages/event_page.html",
                           event=event,
                           campaign=campaign,
                           form=form,
                           delete_form=delete_form,
                           comments=paginated_comments,
                           comment_form_visible=comment_form_visible,
                           sidebar_data=sidebar_data)


# Add new event
@bp.route("/campaigns/<campaign_name>-<campaign_id>/event/new-event", methods=["GET", "POST"])
@login_required
def add_event(campaign_name, campaign_id):
    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign)

    form = forms.CreateEventForm()

    if "date" in request.args and request.method == "GET":
        args = validators.validate_event_url_parameters(request.args)
        # Get the date argument and increment by specified amount
        datestring = request.args["date"]
        date_values = formatters.increment_date(datestring, args)
        # Create placeholder event to prepopulate form
        event = models.Event()
        event.create_blank(date_values)
        form = forms.CreateEventForm(obj=event)
        form.format_date_fields(event)

        # Set scroll_to target for back button
        if "elem_id" in request.args:
            session["timeline_scroll_target"] = request.args["elem_id"]

    # If loading from template, update form with template's dynamic fields
    if "template_id" in request.args and request.method == "GET":
        template_id = request.args["template_id"]

        template = (db.session.query(models.Template)
                    .filter(models.Template.id == template_id)
                    .first_or_404(description="No matching template found"))
        
        authenticators.check_template_is_valid(template, campaign)
        form.load_template(template)

    if form.validate_on_submit():

        event = models.Event()
        event.update(form=form.data,
                     parent_campaign=campaign,
                     new=True)
        
        campaign.get_following_events()
        campaign.check_epochs()
        
        messengers.send_event_notification(current_user,
                                           recipients=campaign.members,
                                           campaign=campaign,
                                           event=event)

        # Set scroll_to target for back button
        session["timeline_scroll_target"] = f"event-{event.id}"

        return redirect(url_for("campaign.edit_timeline",
                                campaign_name=campaign.url_title,
                                campaign_id=campaign.id))

    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            if field_name == "body":
                field_name = "description"
            flash(field_name + ": " + error_message)

    # Flag "new" to hide searchbar and edit page toggle
    return render_template("pages/new_event.html",
                           form=form,
                           campaign=campaign,
                           new=True)


# Edit existing event
@bp.route("/campaigns/<campaign_name>-<campaign_id>/event/<event_name>-<event_id>/edit", methods=["GET", "POST"])
@login_required
def edit_event(campaign_name, campaign_id, event_name, event_id):
    event = (db.session.query(models.Event)
             .filter(models.Event.id == event_id)
             .first_or_404(description="No matching event found"))

    campaign = event.parent_campaign

    authenticators.permission_required(campaign)

    # Set scroll_to target for back button
    session["timeline_scroll_target"] = f"event-{event.id}"

    form = forms.CreateEventForm(obj=event)
    form.submit.label.text = "Update Event"
    delete_form = forms.SubmitForm()

    if request.method == "GET":
        form.format_date_fields(event)

    # If loading from template, update for with template's dynamic fields
    if "template_id" in request.args and request.method == "GET":
        template_id = request.args["template_id"]

        template = (db.session.query(models.Template)
                    .filter(models.Template.id == template_id)
                    .first_or_404(description="No matching template found"))
        
        authenticators.check_template_is_valid(template, campaign)
        form.load_template(template)

    if form.validate_on_submit():

        event.update(form=form.data,
                     parent_campaign=campaign)
        campaign.get_following_events()
        campaign.check_epochs()

        return redirect(url_for("campaign.edit_timeline",
                                campaign_name=campaign.url_title,
                                campaign_id=campaign.id))

    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(field_name + ": " + error_message)

    return render_template("pages/new_event.html",
                           campaign=campaign,
                           campaign_name=campaign.url_title,
                           event_name=event.url_title,
                           form=form,
                           delete_form=delete_form,
                           event=event,
                           edit=True)


# Delete existing event
@bp.route("/campaigns/<campaign_name>-<campaign_id>/event/<event_name>-<event_id>/delete", methods=["POST"])
@login_required
def delete_event(campaign_name, campaign_id, event_name, event_id):
    event = (db.session.query(models.Event)
             .filter(models.Event.id == event_id)
             .first_or_404(description="No matching event found"))

    campaign = event.parent_campaign

    authenticators.permission_required(campaign)

    campaign.last_edited = datetime.now()
    campaign.clear_cache()

    db.session.delete(event)
    db.session.commit()

    campaign.get_following_events()
    campaign.check_epochs()

    return redirect(url_for("campaign.edit_timeline",
                            campaign_name=campaign.url_title,
                            campaign_id=campaign.id))


# Delete comment
@bp.route("/campaigns/<campaign_name>-<campaign_id>/event/<event_name>-<event_id>/comment-<comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(campaign_name, campaign_id, event_name, event_id, comment_id):
    target_comment_id = comment_id

    event = (db.session.query(models.Event)
             .filter(models.Event.id == event_id)
             .first_or_404(description="No matching event found"))

    campaign = event.parent_campaign

    comment = (db.session.query(models.Comment)
               .filter(models.Comment.id == target_comment_id)
               .first_or_404(description="No matching comment found"))

    # Check if it is the comment author who is deleting the comment
    if comment.author == current_user:
        authenticators.check_membership(campaign)
    else:
        # Check if the user has permissions to edit the target campaign.
        authenticators.permission_required(campaign)

    # Check if comment -> event -> campaign relationship is valid
    if comment in event.comments and event in campaign.events:
        # Delete the comment
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('event.view_event',
                            campaign_name=campaign.url_title,
                            campaign_id=campaign.id,
                            event_name=event.url_title,
                            event_id=event.id))
