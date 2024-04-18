from flask import render_template, redirect, request, url_for, session, flash, make_response
from flask_login import login_required, current_user
from datetime import datetime

from app.forms import forms
from app import db, models, limiter
from app.utils import authenticators
import app.utils.formatters as formatters
import app.utils.messengers as messengers

from app.routes.event import bp


#   =======================================
#                  Event
#   =======================================


# View event
@bp.route("/campaigns/<campaign_name>-<campaign_id>/event/<event_name>-<event_id>", methods=["GET", "POST"])
@limiter.limit("60/minute")
def view_event(campaign_name, campaign_id, event_name, event_id):
    event = (db.session.query(models.Event)
             .filter(models.Event.id == event_id)
             .first_or_404(description="No matching event found"))

    campaign = event.parent_campaign

    authenticators.check_campaign_visibility(campaign)
    comment_form_visible = authenticators.check_comment_form_visibility(campaign)

    belligerents = event.separate_belligerents()

    form = forms.CommentForm()
    delete_form = forms.SubmitForm()

    # Set scroll_to target for back button
    session["timeline_scroll_target"] = f"event-{event.id}"

    # Check if new comment submitted
    if form.validate_on_submit():
        # Check user is allowed to comment
        authenticators.check_campaign_comment_status(campaign)

        # Create new comment
        comment = models.Comment()
        comment.update(form=request.form,
                       parent_event=event,
                       author=current_user)

        # Create new comment notification
        messengers.send_comment_notification(sender=current_user,
                                             recipients=campaign.members,
                                             campaign=campaign,
                                             event=event)

        # Set scroll to target to newly created comment
        session["comment_scroll_target"] = f"comment-{comment.id}"

        return redirect(url_for('event.view_event',
                                campaign_name=campaign.url_title,
                                campaign_id=campaign.id,
                                event_name=event.url_title,
                                event_id=event.id))

    return render_template("pages/event_page.html",
                           event=event,
                           campaign=campaign,
                           belligerents=belligerents,
                           form=form,
                           delete_form=delete_form,
                           comment_form_visible=comment_form_visible)


# Add new event
@bp.route("/campaigns/<campaign_name>-<campaign_id>/event/new-event", methods=["GET", "POST"])
@login_required
@limiter.limit("60/minute")
def add_event(campaign_name, campaign_id):
    campaign = (db.session.query(models.Campaign)
                .filter(models.Campaign.id == campaign_id)
                .first_or_404(description="No matching campaign found"))

    authenticators.permission_required(campaign)

    # Check if date argument given
    if "date" in request.args:
        # Get date arguments
        datestring = request.args["date"]
        args = request.args
        # Increase the date by one unit and format the datestring
        datestring = formatters.increment_datestring(datestring, args)
        # Create placeholder event
        event = models.Event()
        event.create_blank(datestring)
        # Prepopulate form
        form = forms.CreateEventForm(obj=event)

        # Set scroll_to target for back button
        if "elem_id" in request.args:
            session["timeline_scroll_target"] = request.args["elem_id"]

    # Otherwise, create default empty form
    else:
        form = forms.CreateEventForm()

    # Check if user has submitted a new event
    if form.validate_on_submit():
        # Create new event object using form data
        event = models.Event()
        event.update(form=form.data,
                     parent_campaign=campaign,
                     new=True)
        # Update "following_event" relationships for all events
        campaign.get_following_events()
        # Check all epochs for events
        campaign.check_epochs()
        # Create notification message
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
@limiter.limit("60/minute")
def edit_event(campaign_name, campaign_id, event_name, event_id):
    event = (db.session.query(models.Event)
             .filter(models.Event.id == event_id)
             .first_or_404(description="No matching event found"))

    campaign = event.parent_campaign

    # Check if the user has permissions to edit the target campaign.
    authenticators.permission_required(campaign)

    # Set scroll_to target for back button
    session["timeline_scroll_target"] = f"event-{event.id}"

    form = forms.CreateEventForm(obj=event)
    delete_form = forms.SubmitForm()

    if form.validate_on_submit():
        # Update event object using form data
        event.update(form=form.data,
                     parent_campaign=campaign)

        # Update "following_event" relationships for all events
        campaign.get_following_events()

        # Update all epochs
        campaign.check_epochs()

        return redirect(url_for("campaign.edit_timeline",
                                campaign_name=campaign.url_title,
                                campaign_id=campaign.id))

    # Change form label to 'update'
    form.submit.label.text = "Update Event"

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
@limiter.limit("60/minute")
def delete_event(campaign_name, campaign_id, event_name, event_id):
    event = (db.session.query(models.Event)
             .filter(models.Event.id == event_id)
             .first_or_404(description="No matching event found"))

    campaign = event.parent_campaign

    # Check if the user has permissions to edit the target campaign.
    authenticators.permission_required(campaign)

    campaign.last_edited = datetime.now()

    db.session.delete(event)
    db.session.commit()

    # Update "following_event" relationships for all events
    campaign.get_following_events()

    # Update campaigns epochs
    campaign.check_epochs()

    return redirect(url_for("campaign.edit_timeline",
                            campaign_name=campaign.url_title,
                            campaign_id=campaign.id))


# Delete comment
@bp.route("/campaigns/<campaign_name>-<campaign_id>/event/<event_name>-<event_id>/comment-<comment_id>/delete",
          methods=["POST"])
@login_required
@limiter.limit("60/minute")
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
