from flask import render_template, redirect, request, url_for, session, flash
from sqlalchemy import select
from flask_login import login_required, current_user
from datetime import datetime

import forms
import models
import auth
import utils.organisers as organisers
import utils.messengers as messengers

from app import db
from routes.event import bp

#   =======================================
#                  Event
#   =======================================


# View event
@bp.route("/campaigns/<campaign_name>/events/<event_name>", methods=["GET", "POST"])
def view_event(campaign_name, event_name):
    target_event_id = request.args["event_id"]
    event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()
    campaign = event.parent_campaign

    # Format belligerents data
    belligerents = organisers.separate_belligerents(event.belligerents) 

    form = forms.CommentForm()

    # Set scroll_to target for back button
    scroll_target = f"event-{event.id}"

    # Check if new comment submitted
    if form.validate_on_submit():
        
        # Check user is a member of the campaign
        auth.check_membership(campaign)

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

        return redirect(url_for('event.view_event', 
                                campaign_name=campaign.title, 
                                event_name=event.title, 
                                event_id=event.id,
                                scroll_target=scroll_target))

    return render_template("event_page.html", 
                           event=event, 
                           campaign=campaign, 
                           belligerents=belligerents,
                           form=form,
                           scroll_target=scroll_target)


# Add new event
@bp.route("/campaigns/<campaign_name>/events/new_event", methods=["GET", "POST"])
@login_required
def add_event(campaign_name):

    target_campaign_id = request.args["campaign_id"]

    campaign = db.session.execute(
        select(models.Campaign)
        .filter_by(title=campaign_name, 
                   id=target_campaign_id)).scalar()

    auth.permission_required(campaign)

    # Check if date argument given
    if "date" in request.args:
        # Get date arguments
        datestring = request.args["date"]
        args = request.args
        # Increase the date by one unit and format the datestring
        datestring = organisers.format_event_datestring(datestring, args)
        # Create placeholder event
        event = models.Event()
        event.create_blank(datestring)
        # Prepopulate form
        form = forms.CreateEventForm(obj=event)

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

        scroll_target = f"event-{event.id}"

        return redirect(url_for("campaign.edit_timeline",
                                campaign_name=campaign.title,
                                campaign_id=campaign.id,
                                scroll_target=scroll_target))

    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(field_name + ": " + error_message)

    return render_template("new_event.html", 
                           form=form, 
                           campaign=campaign)



# Edit existing event
@bp.route("/campaigns/<campaign_name>/events/<event_name>/edit", methods=["GET", "POST"])
@login_required
def edit_event(campaign_name, event_name):
    target_campaign_id = request.args["campaign_id"]
    target_event_id = request.args["event_id"]

    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()
    event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()

    # Create scroll target for back button
    scroll_target = f"event-{event.id}"

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    form = forms.CreateEventForm(obj=event)

    if form.validate_on_submit():
        # Update event object using form data
        event.update(form=form.data, 
                     parent_campaign=campaign)

        # Update "following_event" relationships for all events
        campaign.get_following_events()

        # Update all epochs
        campaign.check_epochs()

        return redirect(url_for("campaign.edit_timeline", 
                                campaign_name=campaign.title, 
                                campaign_id=campaign.id, 
                                scroll_target=scroll_target))

    # Change form label to 'update'
    form.submit.label.text = 'Update Event'

    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(field_name + ": " + error_message)

    return render_template("new_event.html",
                            campaign=campaign,
                            campaign_name=campaign.title,
                            event_name=event.title,
                            form=form,
                            scroll_target=scroll_target,
                            event=event,
                            edit=True)


# Delete existing event
@bp.route("/campaigns/<campaign_name>/events/<event_name>/delete", methods=["GET"])
@login_required
def delete_event(campaign_name, event_name):
    target_campaign_id = request.args["campaign_id"]
    target_event_id = request.args["event_id"]

    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()
    event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()

    # Check if the user has permissions to edit the target campaign.
    auth.permission_required(campaign)

    campaign.last_edited = datetime.now()

    db.session.delete(event)
    db.session.commit()

    # Update "following_event" relationships for all events
    campaign.get_following_events()

    # Update campaigns epochs
    campaign.check_epochs()

    return redirect(url_for("campaign.edit_timeline", 
                                campaign_name=campaign.title, 
                                campaign_id=campaign.id))


# Delete comment
@bp.route("/campaigns/<campaign_name>/events/<event_name>/comments/<comment_id>/delete")
@login_required
def delete_comment(campaign_name, event_name, comment_id):
    
    target_campaign_id = request.args["campaign_id"]
    target_event_id = request.args["event_id"]
    target_comment_id = comment_id

    campaign = db.session.execute(select(models.Campaign).filter_by(id=target_campaign_id)).scalar()
    event = db.session.execute(select(models.Event).filter_by(id=target_event_id)).scalar()
    comment = db.session.execute(select(models.Comment).filter_by(id=target_comment_id)).scalar()

    # Check if it is the comment author who is deleting the comment
    if comment.author == current_user:
        auth.check_membership(campaign)
    else:
        # Check if the user has permissions to edit the target campaign.
        auth.permission_required(campaign)

    # Delete the comment
    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('event.view_event', 
                            campaign_name=campaign.title, 
                            event_name=event.title, 
                            event_id=event.id))



# Add new epoch
@bp.route("/campaigns/<campaign_name>/epochs/new_epoch", methods=["GET", "POST"])
@login_required
def new_epoch(campaign_name):

    target_campaign_id = request.args["campaign_id"]
    campaign = db.session.execute(select(models.Campaign)
                                  .filter_by(title=campaign_name, 
                                             id=target_campaign_id)).scalar()

    auth.permission_required(campaign)

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

        scroll_target = f"epoch-{epoch.id}"

        return redirect(url_for("campaign.edit_timeline", 
                                campaign_name=campaign.title, 
                                campaign_id=campaign.id, 
                                scroll_target=scroll_target))
    
    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(field_name + ": " + error_message)

    return render_template("new_epoch.html",
                           campaign=campaign,
                           campaign_name=campaign.title,
                           form=form)



# Edit epoch
@bp.route("/campaigns/<campaign_name>/epochs/<epoch_title>/edit", methods=["GET", "POST"])
@login_required
def edit_epoch(campaign_name, epoch_title):

    target_campaign_id = request.args["campaign_id"]
    epoch_id = request.args["epoch_id"]

    campaign = db.session.execute(select(models.Campaign)
                                  .filter_by(title=campaign_name, 
                                             id=target_campaign_id)).scalar()

    auth.permission_required(campaign)

    epoch = db.session.execute(select(models.Epoch)
                               .filter_by(title=epoch_title, 
                                          id=epoch_id)).scalar()

    form = forms.CreateEpochForm(obj=epoch)

    if form.validate_on_submit():

        epoch.update(form=request.form,
                     parent_campaign=campaign)

        scroll_target = f"epoch-{epoch.id}"

        return redirect(url_for("campaign.edit_timeline", 
                                campaign_name=campaign.title, 
                                campaign_id=campaign.id, 
                                scroll_target=scroll_target))
    
    # Flash form errors
    for field_name, errors in form.errors.items():
        for error_message in errors:
            flash(field_name + ": " + error_message)

    # Change form label to 'update'
    form.submit.label.text = "Update Epoch"

    return render_template("new_epoch.html",
                           campaign=campaign,
                           campaign_name=campaign.title,
                           form=form,
                           epoch=epoch,
                           edit_page=True)



# Delete epoch
@bp.route("/campaigns/<campaign_name>/epochs/<epoch_title>/delete", methods=["GET", "POST"])
@login_required
def delete_epoch(campaign_name, epoch_title):

    target_campaign_id = request.args["campaign_id"]
    epoch_id = request.args["epoch_id"]

    campaign = db.session.execute(select(models.Campaign)
                                  .filter_by(title=campaign_name, 
                                             id=target_campaign_id)).scalar()

    auth.permission_required(campaign)

    epoch = db.session.execute(select(models.Epoch)
                               .filter_by(title=epoch_title, 
                                          id=epoch_id)).scalar()

    db.session.delete(epoch)
    db.session.commit()
    
    # Update all epochs
    campaign.check_epochs()

    return redirect(url_for("campaign.edit_timeline", 
                                campaign_name=campaign.title, 
                                campaign_id=campaign.id))
